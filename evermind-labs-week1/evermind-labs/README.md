# Evermind Labs

**One mind, many bodies.** We take a published emulation of the fruit-fly brain, freeze it, and connect
it to different bodies to see which behaviours survive.

## Status

Day 0. Nothing here is a result yet. This repository is public from the first commit so that every
step, including the failures, can be checked.

## What this is not

- Not a claim that minds can be transferred. Nothing here concerns human minds.
- Not a claim that an emulated fly brain is conscious, or is "the same" fly.
- Not peer-reviewed. Scientific review is currently done by the founder; an external neuroscientist
  reviewer is still to be found.

## The experiment

1. **Reproduce** the public whole-brain model (Shiu et al., Nature 2024) unchanged.
2. **Body A**: close the loop with NeuroMechFly v2 (FlyGym, MuJoCo).
3. **Interface**: isolate the layer that translates between neurons and body, so it can be replaced.
4. **Bodies B and C**: the same brain in a fly with altered proportions, then in a body that is not a fly.

We measure which behaviours survive, how much brain activity changes, and how much of the interface
must be rewritten for each body. A negative result is published like a positive one.

## Built on the work of others

- FlyWire connectome: https://codex.flywire.ai
- Shiu et al., 2024: https://doi.org/10.1038/s41586-024-07763-9
- NeuroMechFly v2: https://doi.org/10.1038/s41592-024-02497-y , https://neuromechfly.org/
- Eon Systems embodied fly and brain code: https://eon.systems/updates/embodied-brain-emulation ,
  https://github.com/eonsystemspbc/fly-brain

Evermind Labs is not affiliated with any of these groups.

## How the lab works

One person decides; nine AI agents prepare the work. See `CLAUDE.md` for the rules and
`agents/README.md` for the roster. AI-drafted text and code are marked as such in the history.

## Licence

To be chosen by the founder before the first code commit.
