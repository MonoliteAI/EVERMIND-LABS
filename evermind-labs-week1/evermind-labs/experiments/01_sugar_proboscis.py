"""Week 1, day 3: reproduce the sugar -> proboscis result with the public brain model, unchanged.

Activates the labellar sugar gustatory receptor neurons (GRNs) at 200 Hz and reports the firing
rate of the proboscis motor neuron MN9, with two controls:
  - no input at all (the model should be silent),
  - sugar + bitter GRNs together (the published model shows bitter suppressing MN9).

The model code and data are NOT modified. They are imported from a checkout of
https://github.com/eonsystemspbc/fly-brain (code/paper-phil-drosophila/model.py, MIT licence,
Shiu and Spiller). Neuron IDs are copied from that repository's example notebook.

Usage:
    python 01_sugar_proboscis.py <path-to-fly-brain-checkout> [n_trials] [out.json] [seed_base]
"""
import json
import sys
import time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
n_trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4
out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("sugar_proboscis.json")
seed_base = int(sys.argv[4]) if len(sys.argv) > 4 else 1000

sys.path.insert(0, str(repo / "code" / "paper-phil-drosophila"))

import pandas as pd  # noqa: E402
from brian2 import Hz, ms, seed  # noqa: E402
from model import default_params, run_trial  # noqa: E402

PATH_COMP = repo / "data" / "2025_Completeness_783.csv"
PATH_CON = repo / "data" / "2025_Connectivity_783.parquet"

MN9 = {"MN9_left": 720575940660219265, "MN9_right": 720575940618238523}

SUGAR_GRNS = [
    720575940616885538, 720575940630233916, 720575940639332736, 720575940632889389,
    720575940617000768, 720575940632425919, 720575940637568838, 720575940629176663,
    720575940621502051, 720575940638202345, 720575940612670570, 720575940611875570,
    720575940621754367, 720575940633143833, 720575940613601698, 720575940630797113,
    720575940639198653, 720575940639259967, 720575940624963786, 720575940640649691,
    720575940610788069, 720575940623172843, 720575940628853239,
]
BITTER_GRNS = [
    720575940619072513, 720575940646212996, 720575940622298631, 720575940642088333,
    720575940627692048, 720575940617239197, 720575940618682526, 720575940604714528,
    720575940603266592, 720575940604027168, 720575940619197093, 720575940610259370,
    720575940627578156, 720575940629481516, 720575940618887217, 720575940614281266,
    720575940634859188, 720575940645743412, 720575940637742911, 720575940617094208,
    720575940629416318, 720575940630195909, 720575940615641798, 720575940638312262,
    720575940624310345, 720575940621778381, 720575940619659861, 720575940629146711,
    720575940625750105, 720575940610483162, 720575940610481370, 720575940602353632,
    720575940610773090, 720575940617433830, 720575940628962407, 720575940626287336,
    720575940623183083, 720575940618025199, 720575940619028208, 720575940621864060,
    720575940613061118, 720575940621008895,
]

df_comp = pd.read_csv(PATH_COMP, index_col=0)
flyid2i = {fid: i for i, fid in enumerate(df_comp.index)}

missing = [n for n in SUGAR_GRNS + BITTER_GRNS + list(MN9.values()) if n not in flyid2i]
if missing:
    sys.exit(f"IDs not found in this connectome version: {missing}")

T_RUN_S = 1.0
CONDITIONS = {
    "no_input": dict(exc=[], exc2=[], r_poi=0, r_poi2=0),
    "sugar_200Hz": dict(exc=SUGAR_GRNS, exc2=[], r_poi=200, r_poi2=0),
    "sugar_200Hz_plus_bitter_200Hz": dict(exc=SUGAR_GRNS, exc2=BITTER_GRNS, r_poi=200, r_poi2=200),
}

results = {"t_run_s": T_RUN_S, "n_trials": n_trials, "conditions": {}}
for name, c in CONDITIONS.items():
    params = dict(default_params)
    params["t_run"] = T_RUN_S * 1000 * ms
    params["r_poi"] = c["r_poi"] * Hz
    params["r_poi2"] = c["r_poi2"] * Hz
    exc = [flyid2i[n] for n in c["exc"]]
    exc2 = [flyid2i[n] for n in c["exc2"]]
    trials = []
    for k in range(n_trials):
        seed(seed_base + k)  # fixed seeds so the run can be repeated exactly
        t0 = time.time()
        spk = run_trial(exc, exc2, [], PATH_COMP, PATH_CON, params)
        rates = {lab: len(spk.get(flyid2i[fid], [])) / T_RUN_S for lab, fid in MN9.items()}
        trials.append({"seed": seed_base + k, "mn9_rate_hz": rates, "active_neurons": len(spk),
                       "total_spikes": int(sum(len(v) for v in spk.values())),
                       "wall_s": round(time.time() - t0, 1)})
        print(name, trials[-1], flush=True)
    results["conditions"][name] = trials
    out_path.write_text(json.dumps(results, indent=1))

print("written", out_path)
