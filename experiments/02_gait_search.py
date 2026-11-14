"""Coarse search over stroke and lift signs for the scripted tripod gait of body A."""
import itertools, json, sys, time
sys.path.insert(0, "bodies")
import numpy as np
from tripod_gait import GaitParams, run

out = sys.argv[1]
res = []
for cs, rs, ls in itertools.product([1, -1], [1, -1], [1, -1]):
    p = GaitParams(coxa_sign=cs, right_sign=rs, lift_sign=ls)
    t0 = time.time()
    r = run(p, duration_s=2.0)
    th = np.array(r["final_thorax"]); hd = np.array(r["head_dir_xy"])
    r["forward_mm"] = float(th[0] * hd[0] + th[1] * hd[1])   # thorax starts near origin, so final position is the displacement
    r["wall_s"] = round(time.time() - t0, 1)
    print(cs, rs, ls, "fwd_mm=%.2f z=%.2f finite=%s wall=%ss" % (r["forward_mm"], r["z"], r["finite"], r["wall_s"]), flush=True)
    r.pop("traj"); res.append(r)
    json.dump(res, open(out, "w"), indent=1)
