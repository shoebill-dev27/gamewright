---
kind: handoff
goal: G-001
seq: 16
from: art-director
to: studio
stage: Design
outcome: done
---
# 16: art-director → studio — Visual review of the Option A spec: rulings and visual spec for Build

## Task

Route the visual spec in `design/combat-visuals.md` to Build alongside `design/combat.md`. Route the manual change and the one question below.

## Context

G-001: combat monotony. D-002 chose Option A. The game-designer's spec (`design/combat.md`) leaves glyphs and colors to Build and to my review. The rooms 4–5 playtest (08) found that spitters read as scenery and their shots were never reacted to. This was a spec review against `project.md#art-direction` and pillar 3. There is no build yet, so nothing could be checked against actual output. I changed no rules, timings or parameters.

## Findings

### Verdicts

| Question | Verdict | Evidence |
|---|---|---|
| Are Wind-up, Charge and Recovery distinguishable from idle and harmless states? | **Fail as specified, fixed by rulings below.** | The spec says only "glyph and color change". The view is text, so a color-only change would be invisible. A Recovery that "returns to the normal glyph" is identical to Approach in a still frame. |
| Can the player see the telegraph in time? | **Fail as specified.** | The room is drawn every 0.5 s, and the grub Wind-up lasts 0.5 s. A frame can miss it entirely. The swipe arc lasts 0.15 s and would almost never be drawn. |
| Do threat colors read against the dark? | **Pass in principle.** | Saturated orange/red against cold blue-black matches the art direction. Not verifiable until the build exists. |
| Are damaged states and the downed marker clear? | **Pass with changes.** | The spec requires a distinct glyph and color but gives none. Rulings fix them. `x` was unstyled. |

### Rulings (what to keep, what to change)

**Keep:**
- Saturated orange/red for committed threats and projectiles.
- The swipe arc, the damaged state, the remaining-HP hit lines and the explicit "(miss)" reasons.
- The `x` downed marker and the run-over text.

**Change** (full detail in `design/combat-visuals.md`):
1. **Glyph carries the state, not color alone.** Uppercase means committed to hurting (`G`, `W`, `S`, `Z`). Lowercase means harmless (`g`, `w`, `s`, `z`). A damaged enemy uses the `w/z` family.
2. **Harmless enemies are muted.** Orange/red is reserved for telegraphed enemies and `*`. The player, the swipe arc and `x` never use it. This makes the telegraph the loudest thing on the map, and it is what makes the spitter stop looking like scenery.
3. **Extra draws on telegraph events.** The room is drawn at Wind-up start, Charge start, projectile spawn, every swipe, grub Recovery start and player down. Otherwise short telegraphs fall between 0.5 s frames. Timings are untouched.
4. **Text lines name the enemy and its position.** Grub: "a grub rears back (left)". Spitter lines are named by position. A new "the grub is open" line marks the start of Recovery, the counter window. A stagger line is added for spitters.
5. **Swipe arc glyphs** `) ( ^ v` in lantern color on the tiles in reach.
6. **Run-over screen** adds the line "press attack to start again", because the spec's restart rule is otherwise undiscoverable.

### Handoff items

- **`manual.md` must be updated** (not on my write list): the glyph table, the `x` marker, the arc, the practice room, the new lines and the run-over screen (V-5). Route to whoever owns the manual, after Build fixes the final glyphs.
- **Acceptance:** V-1…V-8 in `design/combat-visuals.md` join AC-1…AC-17 for Verify. After Build, I should review the actual player view for color and legibility.
- `design/combat.md` is unchanged. Its line "chosen in Build and documented in the manual" now means: follow `design/combat-visuals.md` and document any change in `manual.md`.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: Option A, reuse existing enemy behavior.
- No new decision recorded; nothing here changes a style pillar.

## Constraints

- No rule, timing or parameter changed. No new inputs. Reuse existing systems.

## Open questions

- **For Build / Plan:** can the extra draws on events (principle 4) be added cheaply? If not, tell `game-designer`: a 0.5 s Wind-up cannot be guaranteed visible with only a 0.5 s draw cadence.
- **Optional, for game-designer:** should the player's invulnerability (hit and dash) be visible? Suggested `p` for `P`. This needs no rule change.

## Expected output

The Studio routes Build (`gameplay-engineer`) with `design/combat.md` plus `design/combat-visuals.md`, then Verify (`qa`) with AC-1…AC-17 and V-1…V-8, then a visual review of the built player view by the art-director.

## Sender assessment

Confidence high on glyph, case and event-draw rulings: they follow from the text view and the 0.5 s draw cadence. Confidence medium on colors: they cannot be judged until a build exists.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-art-director.md
