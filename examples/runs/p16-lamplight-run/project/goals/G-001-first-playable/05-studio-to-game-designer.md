---
kind: handoff
goal: G-001
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — settle the first-screen display of Night 3

## Task

Decide whether the first screen of Night 3 shows `~` on (3,4)-(3,6) (the starting aim is RIGHT), and amend `design/first-playable.md` so that §8, §2, AC-1 and AC-3 no longer contradict each other.

## Context

Goal G-001: first playable of Lamplight Keeper. The engineer built the game from your spec (`repo/`). One contradiction came up during Build:
- Night 3 starts with aim RIGHT. §8 draws its first screen with no `~` (`3 ...T...`).
- AC-3 and §2 say that under RIGHT the tiles (3,4)-(3,6) show `~`.
- AC-1 says the first screen shows the board "exactly as in §8".

It changes no ship movement (lit status is judged after the first command), only what the first Night 3 screen looks like.

## Findings

Engineer's options (see handoff 04):
- (a) Draw `~` under the starting aim. This matches AC-3 and every later screen. The §8 drawing is then layout only. The engineer proposes this and has provisionally built it.
- (b) Draw the first screen with no `~` until a command has been given. This matches the §8 drawing literally, but the lit state would disagree with the aim shown in the header, so say how the first-screen lit state should be shown.

Studio note: the question is yours (player-facing behavior). Pick the option that best serves pillar 2 (readable ahead); (a) looks consistent with it, but the choice is yours.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.

## Constraints

- Change only what resolves this contradiction; no new mechanics, no changes to the other nights' behavior.
- Do not change the code. The engineer applies your answer in the next Build step.
- Stay within the vision and D-001. If the answer would need a direction choice, say so and hand back.
- Do not take up the two Review questions (mid-night arrivals, wrecks always losing the night): they remain for `game-director`.

## Open questions

- Option (a) or (b) for the first screen of Night 3? State the final wording of AC-1 / §8 so QA can check it.

## Expected output

Amend `design/first-playable.md` in place and write a handoff to `studio` with the decision stated in one sentence and the exact amended sections. The Studio then routes to `gameplay-engineer` to apply it, fix the failing tests and rebuild.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/first-playable.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/04-gameplay-engineer-to-studio.md
