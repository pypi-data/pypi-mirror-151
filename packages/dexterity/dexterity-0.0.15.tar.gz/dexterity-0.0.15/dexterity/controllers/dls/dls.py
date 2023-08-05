import dataclasses
from typing import List, Optional, Sequence

import numpy as np

from dexterity import hints
from dexterity.controllers import mapper
from dexterity.utils import mujoco_utils


@dataclasses.dataclass(frozen=True)
class DampedLeastSquaresParameters(mapper.Parameters):

    regularization_weight: float
    """Damping factor used to regularize the pseudoinverse."""

    def _validate_parameters(self) -> None:
        super()._validate_parameters()

        if self.regularization_weight < 0:
            raise ValueError(
                "`regularization_weight` must be non-negative, but was "
                f"{self.regularization_weight}."
            )


@dataclasses.dataclass(frozen=True)
class DampedLeastSquaresMapper(mapper.CartesianVelocitytoJointVelocityMapper):
    """A `CartesianVelocitytoJointVelocityMapper` that uses damped least-squares to
    solve for the joint velocities.

    Specifically, it maps the desired Cartesian velocity V to desired joint velocities
    v using the relationship:

    `J^T v = [J^T @ J + λI] @ V`

    where @ denotes the matrix product, J is the end-effector Jacobian, λ is a damping
    factor and I is the identity matrix.
    """

    params: DampedLeastSquaresParameters

    def compute_joint_velocities(
        self,
        data: hints.MjData,
        target_velocities: Sequence[np.ndarray],
        nullspace_bias: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        del nullspace_bias

        # Compute and concatenate the Jacobian matrices for each end-effector.
        jacobians: List[np.ndarray] = []
        for obj_type, obj_name in zip(
            self.params.object_types, self.params.object_names
        ):
            jacobian = mujoco_utils.compute_object_6d_jacobian(
                model=self.params.model,
                data=data,
                object_type=obj_type,
                object_id=self.params.model.name2id(obj_name, obj_type),
            )
            jacobians.append(jacobian[:3])  # Ignore rotation component.
        jacobian = np.concatenate(jacobians, axis=0)

        # Concatenate twists for each end-effector.
        twist = np.concatenate(target_velocities, axis=0)

        # Solve!
        if self.params.regularization_weight > 0:
            hess_approx = jacobian.T @ jacobian
            hess_approx += (
                np.eye(hess_approx.shape[0]) * self.params.regularization_weight
            )
            return np.linalg.solve(hess_approx, jacobian.T @ twist)
        # Note: In the undamped case, the problem reduces to standard least-squares,
        # i.e., we are solving the following linear system of equations: `V = J @ v`.
        return np.linalg.lstsq(jacobian, twist, rcond=None)[0]
