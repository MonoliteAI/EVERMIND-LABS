# Week 1

Goal: the public brain model runs here and reproduces a published result, checked twice.

| Day | Task | Owner | Done means |
| --- | --- | --- | --- |
| 1 | Create the pinned environment and setup instructions | data-infra-engineer | First pass done 14 Nov (brain side only); FlyGym and MuJoCo still to pin |
| 2 | Download the public brain model and run it unchanged; record its checksum | simulation-engineer | First pass done 14 Nov |
| 3 | Reproduce one published result: sugar sensing to proboscis extension | simulation-engineer | First pass done 14 Nov, qualitative match; numbers vs paper still to compare |
| 4 | Redo day 3 from scratch in a fresh session on a clean environment | sceptical-reviewer | Verdict written in `LOG.md` |
| 5 | Install FlyGym; body A walks with its own controller, no brain. Friday demo | simulation-engineer | First pass done 14 Nov: scripted tripod gait, 3 mm/s, video in `results/day5/`; one run, not independently checked |

In parallel:

| Task | Owner | Done means |
| --- | --- | --- |
| Literature review: has anyone changed the body of an embodied brain model? | research-lead | `docs/literature.md`, every source opened and read |
| Ten neuroscientists to contact; calendar of funding calls | grants-partnerships | List ready for the founder to approve |
| Budget table and deadlines | admin-finance | `admin/budget.md` and `admin/deadlines.md` exist |
| Monday goals and Friday status | chief-of-staff | Founder approves in 15 minutes |

Founder only: choose the licence, set the monthly cap, call the trademark consultant.

If day 3 does not reproduce, week 2 continues on reproduction. Nothing new is built on a result that
does not match.
