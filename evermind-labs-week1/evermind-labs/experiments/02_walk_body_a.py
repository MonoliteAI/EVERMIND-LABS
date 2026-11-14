"""Day 5: body A walks with a scripted tripod gait, no brain. Writes metrics, a plot and a video.

    MUJOCO_GL=egl python 02_walk_body_a.py <out_dir> [duration_s]
"""
import json, sys
from pathlib import Path
sys.path.insert(0, "bodies")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tripod_gait import GaitParams, LEGS, run

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
T = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
p = GaitParams(freq_hz=8.0, coxa_amp=0.3, lift_amp=0.4, tibia_amp=0.4, coxa_sign=1.0, right_sign=1.0, lift_sign=-1.0)
r = run(p, duration_s=T, record=True, video=str(out / "body_a_tripod_walk.mp4"))
tr = np.array(r["traj"]); ct = (np.array(r["contacts"]) > 0).astype(float)   # raw sensor value counts contacts: binarize
t = tr[:, 0]; xy = tr[:, 1:3]
sel = t >= 1.0
d = xy[sel][-1] - xy[sel][0]; hd = np.array(r["head_dir_xy"])
speed = float(d @ hd) / (t[sel][-1] - t[sel][0]); lat = float(d @ np.array([-hd[1], hd[0]])) / (t[sel][-1] - t[sel][0])
duty = {l: float(ct[sel][:, i].mean()) for i, l in enumerate(LEGS)}
grpA = ct[sel][:, [0, 4, 2]].mean(axis=1) > 0.5            # lf, rm, lh
grpB = ct[sel][:, [3, 1, 5]].mean(axis=1) > 0.5            # rf, lm, rh
alt = float(np.mean(grpA != grpB))                          # fraction of time exactly one tripod is on the ground
metrics = dict(params=r["params"], duration_s=T, speed_mm_s=speed, lateral_mm_s=lat,
               z_mean_mm=float(tr[sel][:, 3].mean()), z_std_mm=float(tr[sel][:, 3].std()),
               stance_fraction_per_leg=duty, tripod_alternation_fraction=alt, finite=r["finite"])
json.dump(metrics, open(out / "body_a_walk_metrics.json", "w"), indent=1)
print(json.dumps(metrics, indent=1))
fig, ax = plt.subplots(2, 2, figsize=(10, 7))
ax[0, 0].plot(xy[:, 0], xy[:, 1]); ax[0, 0].set_aspect("equal"); ax[0, 0].set_title("thorax path (mm)")
ax[0, 1].plot(t, tr[:, 3]); ax[0, 1].set_title("thorax height (mm)"); ax[0, 1].set_xlabel("s")
for i, l in enumerate(LEGS):
    ax[1, 0].fill_between(t, i, i + 0.8 * ct[:, i], step="pre", label=l)
ax[1, 0].set_yticks([i + 0.4 for i in range(6)]); ax[1, 0].set_yticklabels(LEGS); ax[1, 0].set_title("ground contact"); ax[1, 0].set_xlabel("s")
ax[1, 1].plot(t, np.hypot(*np.gradient(xy, t, axis=0).T)); ax[1, 1].set_title("thorax speed (mm/s)"); ax[1, 1].set_xlabel("s")
fig.tight_layout(); fig.savefig(out / "body_a_walk.png", dpi=110)
