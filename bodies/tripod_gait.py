"""Open-loop tripod gait for body A. This is a scripted controller, not a brain and not a
biological model: it only shows that body A can be driven to walk, so that later the interface
has something to be compared against.

Each leg follows a sinusoid on three joints (coxa pitch for protraction and retraction, femur
and tibia pitch for lifting) around the neutral pose. Adhesion is on in stance, off in swing.
Legs lf, rm, lh move together, half a cycle apart from rf, lm, rh.
"""
from dataclasses import dataclass, asdict

import numpy as np
from flygym.compose.fly.base_fly import ActuatorType

import body_a as B

LEGS = ["lf", "lm", "lh", "rf", "rm", "rh"]
TRIPOD_PHASE = {"lf": 0.0, "rm": 0.0, "lh": 0.0, "rf": np.pi, "lm": np.pi, "rh": np.pi}


@dataclass
class GaitParams:
    freq_hz: float = 4.0
    coxa_amp: float = 0.4      # rad, protraction/retraction
    lift_amp: float = 0.5      # rad, femur flexion during swing
    tibia_amp: float = 0.5     # rad, tibia flexion during swing
    coxa_sign: float = 1.0     # direction of the stroke (+1 or -1) on the left legs
    right_sign: float = 1.0    # extra sign for right-leg coxa (axes may be mirrored)
    lift_sign: float = 1.0     # direction of lift (+1 or -1)
    adhesion: bool = True
    ramp_s: float = 0.3        # amplitude ramps up linearly to avoid a jerk at the start


def targets(names, q0, t, p: GaitParams):
    q = q0.copy()
    idx = {n: i for i, n in enumerate(names)}
    ramp = min(1.0, t / p.ramp_s) if p.ramp_s > 0 else 1.0
    for leg in LEGS:
        theta = 2 * np.pi * p.freq_hz * t + TRIPOD_PHASE[leg]
        side = p.right_sign if leg[0] == "r" else 1.0
        stroke = np.sin(theta)                       # >0 moving forward in swing
        swing = max(0.0, np.sin(theta))              # lift only while swinging
        q[idx[f"c_thorax-{leg}_coxa-pitch"]] += ramp * p.coxa_sign * side * p.coxa_amp * np.cos(theta)
        q[idx[f"{leg}_coxa-{leg}_trochanterfemur-pitch"]] += ramp * p.lift_sign * p.lift_amp * swing
        q[idx[f"{leg}_trochanterfemur-{leg}_tibia-pitch"]] += ramp * p.lift_sign * p.tibia_amp * swing
    return q


def adhesion_state(t, p: GaitParams):
    if not p.adhesion:
        return np.ones(6)
    return np.array([0.0 if np.sin(2 * np.pi * p.freq_hz * t + TRIPOD_PHASE[l]) > 0.05 else 1.0 for l in LEGS])


def run(p: GaitParams, duration_s=2.0, control_dt=0.001, record=False, video=None):
    fly, sim = B.build(camera=video is not None)
    if video is not None:
        sim.set_renderer(fly.cameraname_to_mjcfcamera["trackcam"], camera_res=(288, 384), playback_speed=0.25, output_fps=25)
    names, q0 = B.neutral_targets(fly)
    n_sub = max(1, int(round(control_dt / sim.timestep)))
    heading_body = [s.name for s in fly.get_bodysegs_order()].index("c_head")
    traj = []
    contacts = []
    n_ctrl = int(duration_s / control_dt)
    fell = False
    for k in range(n_ctrl):
        t = k * control_dt
        sim.set_actuator_inputs(B.FLY, ActuatorType.POSITION, targets(names, q0, t, p))
        sim.set_leg_adhesion_states(B.FLY, adhesion_state(t, p))
        for _ in range(n_sub):
            sim.step()
        pos = sim.get_body_positions(B.FLY)
        if record and k % 10 == 0:
            traj.append((sim.time, *pos[0]))
            contacts.append(np.asarray(sim.get_ground_contact_info(B.FLY)[0], dtype=float).copy())
        if video is not None:
            sim.render_as_needed()
        if not np.all(np.isfinite(pos)):
            fell = True
            break
    if video is not None:
        sim.renderer.save_video(video)
    pos = sim.get_body_positions(B.FLY)
    thorax = pos[0]
    head = pos[heading_body]
    forward = head - thorax
    forward = forward[:2] / (np.linalg.norm(forward[:2]) + 1e-9)
    # displacement over the second half, after the start-up transient
    return dict(params=asdict(p), final_thorax=thorax.tolist(), head_dir_xy=forward.tolist(),
                z=float(thorax[2]), finite=not fell, traj=traj, contacts=contacts)
