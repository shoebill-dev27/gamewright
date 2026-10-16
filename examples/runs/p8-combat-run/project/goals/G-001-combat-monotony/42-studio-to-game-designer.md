---
kind: handoff
goal: G-001
seq: 42
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 42: studio → game-designer — Tuning question on criterion 13 (walker bot, 60 FPS, rooms 3–5)

## Task

Rule on criterion 13 with `write-design-spec`: build 0.6's walker bot loses more hearts in rooms 3–5 at 60 FPS than the criterion allows. Decide whether the limit, the criterion's wording or a room or enemy parameter should change, and write the result as a spec amendment with player-observable acceptance criteria.

## Context

G-001 (combat monotony). The engineer finished build 0.6 per Design 35 and 38 (D-004, D-005) and found no spec gap. All criteria it checked hold except one bot figure: the walker bot (a deliberately naive player that walks toward enemies and swipes) loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS), against criterion 13's limit of 6. Other criterion 13 limits hold: the walker clears 2 of 3 rooms at both rates, the dodger loses 0 and clears 3 of 3, the camper clears fewer rooms than the walker. Build 0.6 is going to QA for Verify in parallel (41); QA will report its own measured figures.

## Findings

Engineer's bot figures for 0.6 (hearts lost; `run_bots`, limit 60), for your reference. QA will re-measure.

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker room 3 | 0 lost, cleared | 2 lost (shots), cleared |
| Walker room 4 | 1 lost (grub), cleared | 3 lost (grub 1, shot 2), not cleared |
| Walker room 5 | 3 lost (grub 2, shot 1), not cleared | 2 lost (grub), cleared |
| Walker rooms 3–5 | 4 lost, 2 of 3 cleared | 7 lost, 2 of 3 cleared |
| Dodger rooms 1–5 | 0 lost, 5/5 cleared | 0 lost, 5/5 cleared |

- The 0.5 values in the spec were: walker rooms 3–5 4 lost and 2 cleared at 30 FPS, 6 lost and 3 cleared at 60 FPS. So the 30 FPS figure is unchanged and the 60 FPS figure moved from 6 to 7 hearts with one fewer room cleared.
- The engineer reports the walker is sensitive to its 0.15 s decision grid, and per-room totals moved in opposite directions between 0.5 and 0.6.
- The 30/60 difference comes from bot timing, not from a rule difference; criterion 16 (rates agree for the dodger) holds.
- Hearts lost by the walker in rooms 1–2 are 5 (criterion 14 wants at least 1), which is unchanged in intent.

## Decisions already made

- D-001: one-button combat; no new input.
- D-004: rooms 4–5 cue gap 0.6 s; brute not cancelled; room 2 spitter deferred.
- D-005: blocked contact consumes the shot and spends the lunge hit.
- Design 35 and 38 are the approved spec for 0.6; the engineer built it as written.

## Constraints

- Must play correctly at both 30 and 60 FPS; the pillars apply (readable threats, short runs, one-button combat).
- Prefer changes that reuse existing systems; no new enemy, healing, input or room content.
- Do not undo D-004 or D-005. If the answer needs a change that contradicts them or a scope or priority change, hand back for Decide (`game-director`).
- The purpose of criterion 13 is a gradient: the naive player is punished more than the dodger, but not walled out. Keep that purpose, state whether 7 at 60 FPS breaks it, and give the reason.

## Open questions

- Is 7 hearts for the walker at 60 FPS a breach of intent, or is the limit of 6 too tight for a grid-sensitive bot? If the limit changes, what should it be, and should it be expressed as a range across both rates?
- If a parameter should change instead, which one, and what must QA re-verify afterwards?
- Does the answer depend on QA's independent figures? If so, say which figure would change your ruling.

## Expected output

An amendment to the spec (in `design/combat.md` or a design note you name) and a handoff to `studio` (`kind: handoff`, `from: game-designer`, `to: studio`) stating the ruling, the changed criteria and, if a build change is needed, the exact change list. Record a Decision if the ruling constrains later work.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/diagnose-experience.md
- Project: design/combat.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/40-gameplay-engineer-to-studio.md
