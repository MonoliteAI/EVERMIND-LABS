"""Body A: NeuroMechFly v2 through FlyGym 2.x, legs actuated with position actuators.

No brain here. This module only builds the body and drives it. The brain-body interface (phase 3)
will drive the same actuators.
"""
import numpy as np
from flygym import Simulation
from flygym.anatomy import ActuatedDOFPreset, AxisOrder, JointPreset, Skeleton
from flygym.compose import FlatGroundWorld
from flygym.compose.fly import NeuroMechFly
from flygym.compose.fly.base_fly import ActuatorType
from flygym.compose.pose import KinematicPosePreset
from flygym.utils.math import Rotation3D

FLY = "nmf"


def build(spawn_z_mm: float = 0.7, kp: float = 50.0, adhesion_gain: float = 1.0, camera: bool = False):
    fly = NeuroMechFly(name=FLY)
    skeleton = Skeleton(axis_order=AxisOrder.PITCH_ROLL_YAW, joint_preset=JointPreset.ALL_BIOLOGICAL)
    fly.add_joints(skeleton, neutral_pose=KinematicPosePreset.NEUTRAL, stiffness=10.0, damping=0.5)
    dofs = ActuatedDOFPreset.LEGS_ACTIVE_ONLY.filter(fly.get_jointdofs_order())
    fly.add_actuators(dofs, ActuatorType.POSITION, neutral_input=KinematicPosePreset.NEUTRAL, kp=kp)
    fly.add_leg_adhesion(gain=adhesion_gain)
    if camera:
        fly.add_tracking_camera(name="trackcam", mode="track", pos_offset=(-0.5, -6.0, 4.0))
    world = FlatGroundWorld()
    world.add_fly(fly, spawn_position=(0, 0, spawn_z_mm), spawn_rotation=Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    return fly, sim


def neutral_targets(fly):
    """Neutral joint angles (rad) in the order the position actuators expect."""
    lookup = fly.get_pose_lookup(KinematicPosePreset.NEUTRAL)
    names = [d.name for d in fly.get_actuated_jointdofs_order(ActuatorType.POSITION)]
    return names, np.array([lookup[n] for n in names], dtype=float)


def thorax_xyz(sim):
    return np.array(sim.get_body_positions(FLY)[0])
