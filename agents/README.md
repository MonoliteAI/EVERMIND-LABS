# Agent roster

The definitions live in `agents/definitions/`. Each file names the model that runs the agent. To use them in Claude Code, copy them to `.claude/agents/` (Windows: `copy agents\definitions\*.md .claude\agents\`; macOS/Linux: `cp agents/definitions/*.md .claude/agents/`).

| Agent | File | Model | Why this model |
| --- | --- | --- | --- |
| Chief of staff | `chief-of-staff.md` | sonnet | Recurring planning and summaries: reliability over depth |
| Research lead | `research-lead.md` | fable | Hypotheses and experiment design: the hardest reasoning in the lab |
| Simulation engineer | `simulation-engineer.md` | opus | Long, complex code across Brian2, FlyGym and MuJoCo |
| Data and infrastructure | `data-infra-engineer.md` | sonnet | Environment, tests, datasets: well-defined technical work |
| Sceptical reviewer | `sceptical-reviewer.md` | fable | Finding the error is harder than writing the work |
| Communication | `communication.md` | sonnet | Clear writing at volume, always checked against the claims rules |
| Grants and partnerships | `grants-partnerships.md` | sonnet | Searching calls and drafting applications |
| Administration and finance | `admin-finance.md` | haiku | Deadlines, tables, reminders: simple and frequent |
| Ethics and safety | `ethics-safety.md` | opus | Judgement on claims and risks, low volume |

Rule of thumb: use the largest model only where a mistake costs the most. Review the assignments at
each month-end retrospective.

## Weekly rhythm

- **Monday**: chief of staff proposes three goals; the founder approves or changes them.
- **Daily**: every agent that worked appends to `LOG.md`.
- **Friday**: sceptical reviewer reruns the week's results; demo of what works.
- **Month end**: retrospective, budget check, timeline update.

## Hand-offs

research-lead designs -> simulation-engineer builds -> data-infra-engineer makes it reproducible ->
sceptical-reviewer reruns from scratch -> ethics-safety checks anything meant for the public ->
the founder decides.
