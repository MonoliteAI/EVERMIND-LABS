# Log

Newest first. Every agent that works appends here: what was done, what was found, what is blocked.
Founder decisions are marked **Decision**.

## 2026-11-14 (Week 1, day 5, first pass)

Same caveat as above: written and run by one AI session, not yet independently rerun.

- **Installed.** FlyGym 2.1.1 (Apache-2.0) and MuJoCo 3.16.0 in the same environment; versions pinned in
  `environment/requirements.txt`. FlyGym 2 is a different major version from the 1.x that the
  NeuroMechFly v2 paper describes: the API was rewritten (`compose`, `Simulation`). The simplified body
  meshes ship inside the package, so no download from outside was needed. Offscreen video works with
  `MUJOCO_GL=egl`.
- **Body A built** (`bodies/body_a.py`): NeuroMechFly, all biological joints, 42 leg joints driven by
  position actuators (kp 50), adhesion on the six leg tips, flat ground. It stands: after settling the
  thorax sits at about 1.10 mm and stays there.
- **Scripted tripod gait, no brain** (`bodies/tripod_gait.py`, `experiments/02_walk_body_a.py`):
  open-loop sinusoids on coxa, femur and tibia joints, adhesion on in stance and off in swing.
  Parameters were found by a coarse search over stroke and lift directions (8 combinations, 2 s each)
  and then 24 combinations of frequency and amplitude (4 s each). Raw results in `results/day5/`. This
  is tuned by us on this one metric (forward speed with low sideways drift); it is not a biological
  gait model.
- **Result, 6 s, one run:** forward speed 3.0 mm/s, sideways drift 0.02 mm/s, thorax height
  1.00 +- 0.06 mm. Stance fraction per leg 0.37 to 0.60. One tripod is on the ground and the other is
  not for 94% of the time after the first second. A standing-still control moves 0.0 mm/s.
  Video: `results/day5/body_a_tripod_walk.mp4` (slow motion, 4x). Plot: `body_a_walk.png`.
- **Not checked.** (1) Only one run and one set of parameters; repeatability across repeated runs was
  not tested. (2) 3 mm/s is slow; real flies walk several times faster (approximate, from memory,
  not sourced here). (3) Thorax speed oscillates between about 2 and 12 mm/s within each step, so the
  gait is jerky. (4) The standing fly creeps forward by about 0.16 mm/s when adhesion is on during the
  stand-still test. (5) The geometry and joint sign conventions were found by trial, not read from the
  documentation, which could not be opened.
- **Plan impact.** Body A exists and moves, so phase 2 (closing the loop) can start: the open question
  is how descending-neuron activity (P9 forward walking, DNa01/02 turning, MN9 proboscis) maps to these
  42 joint targets. That mapping is the interface, and it is what experiment 03 has to define.

## 2026-11-14 (Week 1, days 1 to 3, first pass)

Done in one AI working session, drafted and run by the same session. This is NOT the independent
rerun: the sceptical reviewer still has to repeat it from scratch in a fresh session.

- **Environment.** Python 3.13.18, Brian2 2.11.0, numpy 2.5.4, pandas 3.1.1 on Linux, 2 cores, 7 GB RAM.
  Exact versions in `environment/requirements.txt`. The upstream repository targets Python 3.10 and
  Brian2 2.8.0; we ran on newer versions and it worked without changes.
- **Brain model.** `eonsystemspbc/fly-brain` at commit `a3db62f`. Model code `model.py` (MIT, Shiu and
  Spiller) and connectome files v783 used unchanged: 138,639 neurons, 15,091,983 connection rows.
  Checksums in `environment/brain_model.sha256`, verified before and after the runs.
- **Experiment 01, sugar to proboscis** (`experiments/01_sugar_proboscis.py`, 1 s simulated, 4 trials,
  seeds 1000, 1001, 2000, 2001; raw numbers in `results/`):

  | Condition | MN9 left (Hz) | MN9 right (Hz) | Active neurons |
  | --- | --- | --- | --- |
  | No input | 0 | 0 | 0 |
  | 23 sugar GRNs at 200 Hz | 88.3 (83 to 91) | 64.3 (62 to 66) | about 411 |
  | Sugar + 42 bitter GRNs at 200 Hz | 0.5 (0 to 1) | 0.3 (0 to 1) | about 323 |

- **Reading.** Matches the published qualitative results: sugar GRN activation drives the proboscis
  motor neuron MN9, and bitter co-activation suppresses it. Seed 1000 run twice gave identical
  numbers, so runs are repeatable.
- **Not yet checked.** (1) No comparison with the paper's actual firing rates: the article page could
  not be opened from this environment, so the match is qualitative only. (2) 4 trials, where the
  upstream example uses 30. (3) MN9 left fires more than right; the paper reports the contralateral
  MN9 firing more under one-sided activation, which would fit if these 23 GRNs are right-hemisphere,
  but their side was not verified. (4) One trial takes 6 s to 130 s depending on compile caching.
- **Found.** The upstream repository contains the brain model and benchmark code only. No body
  coupling code (no MuJoCo or FlyGym) is in it at this commit: the brain-to-body link for body A
  has to be built by us or taken from another open project.
- **Found.** Licences: upstream repository is GPL-2.0 at top level, the model folder is MIT. This
  bears on the founder's choice of licence; we import the code, we do not copy it into this repository.
- **Blocked.** Two runs in parallel were killed (memory): one run at a time on 7 GB.

### Next

- Sceptical reviewer: rerun experiment 01 from zero in a fresh session, then try to break it
  (GRN side, 30 trials, compare with the paper's figures).
- Day 5: install FlyGym, body A walking with its own controller.

## 2026-11-13 (Day 0)

- **Decision.** Name: Evermind Labs. Trademark position still to be checked with a consultant before
  any spending on brand.
- **Decision.** No legal entity for now: a private project with a website, documentation and code.
- **Decision.** Repository public from day 1.
- **Decision.** Body C (hexapod robot model or wheeled vehicle) is chosen at day 60.
- **Decision.** The founder acts as scientific reviewer until an external neuroscientist is found.
  Nothing is described as peer-reviewed until then.
- **Decision.** Models: research-lead and sceptical-reviewer on fable; simulation-engineer and
  ethics-safety on opus; chief-of-staff, data-infra-engineer, communication and grants-partnerships
  on sonnet; admin-finance on haiku.
- Day 0 plan, whitepaper v0.1 and manifesto drafted with AI assistance, approved by the founder.

### Open

- Licence for the code.
- Monthly spending cap.
- Where the code runs (local machine or cloud).
- External neuroscientist reviewer.
