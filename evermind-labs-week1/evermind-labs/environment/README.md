# Environment

Tested on Linux, Python 3.13, 2 cores, 7 GB RAM. A C++ compiler (g++) is required by Brian2.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r environment/requirements.txt

# the frozen brain model (about 370 MB), kept outside this repository
git clone https://github.com/eonsystemspbc/fly-brain ../fly-brain
git -C ../fly-brain checkout a3db62f9436074e485c0278290c2164ed6150808
(cd ../fly-brain && sha256sum -c "$OLDPWD/environment/brain_model.sha256")

# experiment 01: sugar -> proboscis, 2 trials, seeds 1000 and 1001 (a few minutes)
python experiments/01_sugar_proboscis.py ../fly-brain 2 outputs/run.json 1000
```

Run one simulation at a time on a 7 GB machine. `requirements.in` lists what later phases will
need (FlyGym, MuJoCo); those are not installed or pinned yet.

FlyGym 2.x and MuJoCo are installed and pinned (day 5). For offscreen video set `MUJOCO_GL=egl`.

```bash
MUJOCO_GL=egl python experiments/02_walk_body_a.py outputs/day5 6   # body A, scripted tripod gait
```
