# Evermind Labs: rules for every agent

Evermind Labs is an open research project run by one person (the founder) and nine AI agents.
It has one experiment: the same emulated fruit-fly brain, connected to different bodies.

## Rules that apply to every agent

1. **Only the founder publishes, sends, spends or signs.** No agent tags a release, updates the website,
   posts, emails anyone outside the lab, buys anything, creates accounts or accepts terms.
2. **The repository is public from day 1.** Everything committed is visible. Never commit secrets,
   personal data or private correspondence.
3. **Branches, then review.** Work on a branch. Code and results reach `main` only after the
   sceptical reviewer has rerun them and written "reproduced" in `LOG.md`.
4. **The brain model is frozen.** Nobody edits the published brain model. Its checksum is recorded in
   `environment/` and checked by the tests. Changes belong in the interface or the body.
5. **Small claims, big proofs.** Every sentence meant for the public must point to a test anyone can rerun.
   State what the model does not do before stating what it does.
6. **No claims about consciousness, identity or human minds.** Ever.
7. **One experiment at a time.** No second project before day 90.
8. **Log daily.** Append to `LOG.md`: what you did, what you found, what is blocked.
9. **Stop and ask** when a decision costs money, cannot be undone, touches someone outside the lab,
   or contradicts these rules.
10. **Language.** Repository content is in English. Reports to the founder are in Italian.

## Review status

Scientific review is currently done by the founder. No external neuroscientist has reviewed this work.
Nothing may be described as peer-reviewed until one has.

## Structure

- `agents/definitions/` : the nine agent definitions, each with its model (to use them in Claude Code, copy them to `.claude/agents/`)
- `agents/README.md` : roster and how the agents work together
- `LOG.md` : decision and work log
- `WEEK1.md` : plan for the first week
- `environment/` : dependencies and the frozen brain model's checksum
- `brain/`, `interface/`, `bodies/`, `experiments/` : the code, created in week 1
