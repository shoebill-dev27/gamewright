---
kind: handoff
goal: G-001
seq: 1
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 01: studio → game-designer — specify a complete five-floor run of Ember Hollow

## Task

Write the design spec for the first complete playable version of Ember Hollow: everything the player-facing game needs so that one run, from floor 1 to a win or a loss, can be built and verified. Include player-observable acceptance criteria with numbers.

## Context

G-001. The Owner asked (ja): "このコンセプトで、最初から最後まで通して遊べる版を作ってほしい。ブラウザで遊べるようにしてほしい" ("Make a version of this concept that can be played from start to finish, playable in the browser"). The project is concept only: `repo/` holds a README, with no design documents and no Decisions. You are the first step. After you come Plan (`technical-director`), Build, Verify, Play and Review. The Plan and Build steps work from your spec and cannot ask you what you meant, so it must stand alone.

## Findings

Nothing yet; this is the first step. The vision, pillars, player profile and constraints are in `project.md` (see Load). Points to cover:

- **Ember and light:** how the glow sets how far the player sees, how it dims per turn, how braziers rekindle it, what happens when it goes out, and how the player can read the ember's state.
- **Turn actions:** move, wait, fight, use an item; what each costs and does.
- **Creatures:** the roster for five floors and how each reacts to light and acts. Each behavior must be learnable. Every threat that can hurt the player next turn is visible and readable beforehand (pillar 1).
- **Floor 5 creature:** the one that keeps the hollow dark. Its behavior, and the win condition.
- **Items:** only what the run needs, with their effects.
- **Floors:** what a floor contains (layout rules, brazier placement, creature and item placement) and that floors derive from a seed (same seed gives the same run, different seeds differ).
- **Run shape:** the 15–30 minute target, translated into floor sizes and counts that can be checked; the end of run states and what the player sees at each.
- **Player-facing information:** what the screen must show (grid, ember state, health, threats, messages), described by what the player can tell, not by layout code. Keyboard and mouse controls in the browser.
- **Acceptance criteria:** player-observable and numeric where numbers matter, checkable through text output of `node play.js {script}` and by looking at the browser page.

## Decisions already made

None. (There are no Decisions in the project.)

## Constraints

- Stay inside the vision and pillars. If completing the spec would need a change to the concept, a pillar, or the scope of the Goal, hand back to the Studio for a `game-director` decision instead of choosing it yourself.
- Specify player-facing behavior only. Do not decide technical approach, architecture or file structure. The script format is the build's to define in `repo/manual.md`; do not specify it.
- Keep content to what one complete five-floor run needs. No saving, meta-progression, sound or mobile layouts.
- The game is deterministic: the same seed and commands always give the same run. Rules must allow this (no rule that depends on real time or other outside input).
- The spec must be buildable in the project's technology (JavaScript, Node.js 20 and browser, no dependencies, no network); keep rules simple enough to implement and test as such.
- Write the spec as project design documents under `design/` (for example `design/game-spec.md`), not only in the Handoff. Use several files if that helps, and name them in Findings.

## Open questions

None for you to route beyond the escalation condition in Constraints. List any ambiguity you resolved yourself, with the choice made, in Findings of your outgoing Handoff.

## Expected output

The design spec in `design/`, with player-observable acceptance criteria. The outgoing Handoff goes to `technical-director` (stage Plan), with the spec file names under Findings. If the spec needs a direction, priority or scope choice that is not yours, set `to` to `studio` with `outcome: question` and say which choice.

## Sender assessment

Studio's routing view: the vision is already specific, so no Diagnose or Decide stage is planned. The main risk is size: five floors with a creature roster and a boss in one spec. Prefer a small, complete content set with clear behaviors over a large one. The art-director's visual review comes after Build; what the player must see should be in your acceptance criteria.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, repo/README.md
- Decisions: none
- Previous handoff: none
