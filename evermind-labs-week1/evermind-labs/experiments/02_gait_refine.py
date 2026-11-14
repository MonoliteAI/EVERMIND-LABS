"""Refine the scripted tripod gait of body A: frequency and amplitudes for the two best sign sets.
Metric: net displacement of the thorax between t=1 s and t=4 s, along the final heading, plus
lateral drift, height, and the standing-still baseline for comparison."""
import itertools, json, sys, time
sys.path.insert(0, "bodies")
import numpy as np
from tripod_gait import GaitParams, run

out = sys.argv[1]
T = 4.0
def measure(p):
    r = run(p, duration_s=T, record=True)
    tr = np.array(r["traj"])                       # t, x, y, z of thorax
    a = tr[np.argmin(abs(tr[:, 0] - 1.0))]; b = tr[-1]
    d = (b[1:3] - a[1:3])
    hd = np.array(r["head_dir_xy"])
    fwd = float(d @ hd); lat = float(d @ np.array([-hd[1], hd[0]]))
    zs = tr[tr[:, 0] > 1.0, 3]
    return dict(params=r["params"], speed_mm_s=fwd / (b[0] - a[0]), lateral_mm_s=lat / (b[0] - a[0]),
                z_mean=float(zs.mean()), z_std=float(zs.std()), finite=r["finite"])

res = []
base = measure(GaitParams(coxa_amp=0, lift_amp=0, tibia_amp=0, adhesion=False))
base["label"] = "standing baseline"; res.append(base)
print("baseline", round(base["speed_mm_s"], 2), flush=True)
for (cs, rs, ls), f, ca, la in itertools.product([(-1, 1, 1), (1, 1, -1)], [4.0, 6.0, 8.0], [0.3, 0.5], [0.4, 0.7]):
    p = GaitParams(freq_hz=f, coxa_amp=ca, lift_amp=la, tibia_amp=la, coxa_sign=cs, right_sign=rs, lift_sign=ls)
    t0 = time.time(); m = measure(p); m["wall_s"] = round(time.time() - t0, 1); res.append(m)
    print((cs, rs, ls), f, ca, la, "speed=%.2f lat=%.2f z=%.2f+-%.2f" % (m["speed_mm_s"], m["lateral_mm_s"], m["z_mean"], m["z_std"]), flush=True)
    json.dump(res, open(out, "w"), indent=1)
