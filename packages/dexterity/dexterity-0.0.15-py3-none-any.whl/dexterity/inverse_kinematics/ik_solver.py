# TODO(kevin): In the future, we'd like to solve for finger orientation as well.

import copy
from typing import List, NamedTuple, Optional, Sequence

import mujoco
import numpy as np
from absl import logging
from dm_control import mjcf
from dm_robotics.geometry import geometry
from dm_robotics.geometry import mujoco_physics

from dexterity import controllers
from dexterity.models.hands import dexterous_hand
from dexterity.utils.mujoco_utils import get_element_type

# Gain for the linear twist computation, should always be between 0 and 1.
# 0 corresponds to not moving and 1 corresponds to moving to the target in a single
# integration timestep.
_LINEAR_VELOCITY_GAIN = 0.95

# Integration timestep used to convert from joint velocities to joint positions.
_INTEGRATION_TIMESTEP_SEC = 1.0

# Damping factor.
_REGULARIZATION_WEIGHT = 1e-5

# If the norm of the error divided by the magnitude of the joint position update is
# greater than this value, then the solve is ended prematurely. This helps us avoid
# getting stuck in local minima.
_PROGRESS_THRESHOLD = 20.0


class _Solution(NamedTuple):
    """Return value of an IK solution."""

    qpos: np.ndarray
    linear_err: List[float]


class IKSolver:
    """Inverse kinematics solver for a dexterous hand."""

    def __init__(self, hand: dexterous_hand.DexterousHand) -> None:
        # Note: We need the root model in case the hand is attached to another entity.
        self._physics = mjcf.Physics.from_mjcf_model(hand.mjcf_model.root_model)
        self._geometry_physics = mujoco_physics.wrap(self._physics)

        # Get joint bindings.
        self._elements = hand.fingertip_sites
        self._all_joints_binding = self._physics.bind(hand.joints)
        self._joint_bindings = []
        for joint_group in hand.joint_groups:
            joint_binding = self._physics.bind(joint_group.joints)
            self._joint_bindings.append(joint_binding)

        # Make the midrange of the joints be the nullspace.
        self._nullspace_reference = np.mean(self._all_joints_binding.range, axis=1)

        self._create_mapper()

    def _create_mapper(self) -> None:
        params = controllers.dls.DampedLeastSquaresParameters(
            model=self._physics.model,
            object_types=[get_element_type(element) for element in self._elements],
            object_names=[element.full_identifier for element in self._elements],
            regularization_weight=_REGULARIZATION_WEIGHT,
        )
        self._mapper = controllers.dls.DampedLeastSquaresMapper(params)

    def solve(
        self,
        target_positions: np.ndarray,
        linear_tol: float = 1e-3,
        max_steps: int = 100,
        early_stop: bool = False,
        num_attempts: int = 30,
        stop_on_first_successful_attempt: bool = False,
    ) -> Optional[np.ndarray]:
        """Attemps to solve the inverse kinematics problem.

        Args:
            target_positions (np.ndarray): A 2D array of Cartesian fingertip positions,
                one for each finger.
            linear_tol (float, optional): The linear tolerance, in meters, that
                determines if the solution found is valid. Defaults to 1e-3.
            max_steps (int, optional): Maximum number of integration steps used for a
                single IK solve. The larger, the more likely a solution can be found at
                a the cost of increased computation time. Defaults to 100.
            early_stop (bool, optional): If True, stops an IK attempt as soon as the
                joint configuration is within the linear tolerance for all fingers. If
                False, it will always run `max_steps` iterations per attempt and return
                the last configuration. Defaults to False.
            num_attempts (int, optional): The number of different IK attempts the solver
                should do. Having more attempts increases the chances of finding a
                correct solution, at the cost of computation time. Defaults to 30.
            stop_on_first_successful_attempt (bool, optional): If True, the method will
                return the first solution that meets the tolerance criteria. If False,
                it returns the solution where the joints are closer to their respective
                operating range. Defaults to False.

        Raises:
            ValueError: If target_positions does not have a shape of (num_fingers, 3).

        Returns:
            Optional[np.ndarray]: Returns the corresponding joint configuration if a
            solution is found. If IK fails, it returns None.
        """
        target_positions = target_positions.reshape(-1, 3)
        if target_positions.shape[0] != len(self._elements):
            raise ValueError(
                "The number of target positions must be equal to the number of "
                "end-effector sites."
            )

        # Initialize solution variables.
        nullspace_jnt_qpos_min_err: float = np.inf
        success: bool = False
        sol_qpos: Optional[np.ndarray] = None

        # Each iteration of this loop attempts to solve the IK problem.
        for attempt in range(num_attempts):
            # Randomize the initial joint configuration so that IK can find different
            # solutions.
            if attempt == 0:
                self._all_joints_binding.qpos = self._nullspace_reference
            else:
                self._all_joints_binding.qpos = np.random.uniform(
                    *self._all_joints_binding.range.T
                )

            # Solve!
            qpos, linear_errors = self._solve_ik(
                target_positions, linear_tol, max_steps, early_stop
            )

            # Check that all fingers are within the desired tolerance.
            if all(err <= linear_tol for err in linear_errors):
                success = True
                nullspace_jnt_qpos_err = float(
                    np.linalg.norm(qpos - self._nullspace_reference)
                )
                if nullspace_jnt_qpos_err < nullspace_jnt_qpos_min_err:
                    nullspace_jnt_qpos_min_err = nullspace_jnt_qpos_err
                    sol_qpos = qpos

            if success and stop_on_first_successful_attempt:
                break

        if not success:
            logging.warning("Inverse kinematics failed to find a solution.")

        return sol_qpos

    def _solve_ik(
        self,
        target_positions: np.ndarray,
        linear_tol: float,
        max_steps: int,
        early_stop: bool,
    ) -> _Solution:
        cur_frames: List[geometry.PoseStamped] = []
        cur_poses: List[geometry.Pose] = []
        previous_poses: List[geometry.Pose] = []
        for element in self._elements:
            cur_frame = geometry.PoseStamped(pose=None, frame=element)
            cur_pose = cur_frame.get_world_pose(self._geometry_physics)
            cur_frames.append(cur_frame)
            cur_poses.append(cur_pose)
            previous_poses.append(copy.copy(cur_pose))

        target_poses = [geometry.Pose(position=pos) for pos in target_positions]

        # Each iteration of this loop attempts to reduce the error between the site's
        # position and the target position.
        for _ in range(max_steps):
            twists = []
            for cur_pose, target_pose in zip(cur_poses, target_poses):
                twist = _compute_twist(
                    cur_pose,
                    target_pose,
                    _LINEAR_VELOCITY_GAIN,
                    _INTEGRATION_TIMESTEP_SEC,
                )
                twists.append(twist)

            qdot_sol = self._compute_joint_velocities(twists)

            mujoco.mj_integratePos(
                self._physics.model.ptr,
                self._physics.data.qpos,
                qdot_sol,
                _INTEGRATION_TIMESTEP_SEC,
            )
            self._update_physics_data()

            linear_errors: List[float] = []
            close_enough: bool = True
            not_enough_progress: bool = False

            for i, target_position in enumerate(target_positions):
                # Get the distance between the current pose and the target pose.
                cur_pose = cur_frames[i].get_world_pose(self._geometry_physics)
                linear_err = float(np.linalg.norm(target_position - cur_pose.position))
                linear_errors.append(linear_err)

                # Stop if the pose is close enough to the target pose.
                if linear_err > linear_tol:
                    close_enough = False

                # Stop the solve if not enough progress is being made.
                previous_pose = previous_poses[i]
                linear_change = np.linalg.norm(
                    cur_pose.position - previous_pose.position
                )
                if linear_err / (linear_change + 1e-10) > _PROGRESS_THRESHOLD:
                    not_enough_progress = True

                # Update the previous pose.
                previous_poses[i] = copy.copy(cur_pose)
                cur_poses[i] = cur_pose

            # Break conditions.
            if (early_stop and close_enough) or not_enough_progress:
                break

        qpos = np.array(self._all_joints_binding.qpos)
        return _Solution(qpos=qpos, linear_err=linear_errors)

    def _compute_joint_velocities(
        self, cartesian_6d_target: Sequence[np.ndarray]
    ) -> np.ndarray:
        """Maps a Cartesian 6D target velocity to joint velocities."""
        return self._mapper.compute_joint_velocities(
            data=self._physics.data,
            target_velocities=cartesian_6d_target,
            nullspace_bias=None,
        )

    def _update_physics_data(self) -> None:
        """Updates the physics data following the integration of velocities."""
        # Clip joint positions.
        qpos = self._all_joints_binding.qpos
        qpos = np.clip(qpos, *self._all_joints_binding.range.T)
        self._all_joints_binding.qpos[:] = qpos

        # Forward kinematics to update the pose of the tracked site.
        mujoco.mj_normalizeQuat(self._physics.model.ptr, self._physics.data.qpos)
        mujoco.mj_kinematics(self._physics.model.ptr, self._physics.data.ptr)
        mujoco.mj_comPos(self._physics.model.ptr, self._physics.data.ptr)


def _compute_twist(
    init_pose: geometry.Pose,
    final_pose: geometry.Pose,
    linear_velocity_gain: float,
    control_timestep_seconds: float,
) -> np.ndarray:
    """Returns the twist to apply to the element to reach final_pose from init_pose."""
    position_error = final_pose.position - init_pose.position
    return linear_velocity_gain * position_error / control_timestep_seconds
