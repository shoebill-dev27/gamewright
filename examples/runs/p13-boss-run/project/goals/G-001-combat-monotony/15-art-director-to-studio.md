---
kind: handoff
goal: G-001
seq: 15
from: art-director
to: studio
stage: Verify
outcome: done
---
# 15: art-director → studio: Visual review of build 0.5 combat cues

## Task

Report on the readability and consistency of the build 0.5 threat cues, with player-observable requirements for the graphical build.

## Context

G-001 (combat monotony). Handoff 12 asked for a review of the grub wind-up and spitter aim cues against the art direction and pillar 3 (readable threats).

## Findings

**Basis and limits.** I reviewed the cue descriptions in handoff 12, `design/combat.md` and `repo/manual.md`. I did not run `play.py`. The build is text-only, so color, brightness and look are not verifiable yet. This is a design-level verdict for the cue forms, and graphical acceptance is still open.

**Verdict by question**

1. **Are the cue forms readable and consistent with the art direction?** Yes, with conditions.
   - Saturated orange-red against a dark cave fits the art direction. The forms (flash, lane, aim line, glow ramp) are appropriate and reuse simple assets.
   - The same hue is used for the grub cue, the aim line and the shot, so shape and motion must carry the differences (see problems 3 and 4).
2. **What the graphical implementation must satisfy.** See `design/combat-cues-visual-spec.md`, criteria V1–V12.

**Problems found, with where they occur**

1. **The grub lane must show its true width.** The combat design calls it a "thin line" but also says the danger is 0.6 tiles either side (1.2 wide). A hairline would make the sidestep requirement unreadable. Requirement: draw the lane at 1.2 tiles wide. This is a visual fix, with no rule change.
2. **The spitter glow starts at 0% brightness.** The text cue shows `brightness 0%` at the start, so the glow carries no information on the first frame. Requirement: a glow floor of at least 30%, and the aim line at full brightness from the first frame. The ramp then conveys time left.
3. **Grub lane vs spitter aim line vs shot.** All three are orange-red and the text view draws the lane and aim line with the same `~`. In the text view the `cue:` line resolves this, but a graphical build needs different shapes: a wide short band for the grub, a thin long line for the spitter, and a round moving core for the shot. The line must disappear when the shot fires.
4. **Threat color vs lantern.** The lantern is also warm. The threat cues must be self-lit, more saturated and redder than the lantern, and not dimmed by distance from the lantern. Spitters in the far corners of the room must still show their cue (rooms 3–5).
5. **Short Runner cue (0.35 s).** About 10 frames at 30 FPS, with no room for a fade-in. The cue must appear at full contrast on the first frame. Variants must differ by silhouette and cadence, not by hue.
6. **No "safe" state is specified.** The recovery and stagger windows are where the player is meant to swipe. The grub should clearly return to a neutral untinted look so the player knows it is safe.
7. **Flash rate.** Keep pulses at or below 3 Hz. Do not strobe, including for the Runner.

**Does any of this need a rule or timing change?** No. All seven points are visual. I do not ask the game-designer to change timings. The 0.35 s minimum wind-up remains workable if V3 is met. If playtesting shows Runner cues are still missed in graphics, the escalation is a wind-up change within the allowed 0.35–0.7 s range, which is the game-designer's call.

**Also noted.** The open question in `design/combat.md` about whether the `r` / `G` text marks suit the graphical build is answered: the graphical build should use silhouette and size instead (spec table). The text marks stay for the text view.

## Decisions already made

- D-001: one attack button plus dash (not affected).
- Art direction in project.md: warm lantern vs cold blue-black, with threats in saturated orange/red (applied above).

## Constraints

- No gameplay rules or parameters were changed. No new decision file was needed.
- The graphical cue appearance is not testable until a graphical build exists.

## Open questions

1. Route the spec's V1–V12 to whichever step implements the graphical cues. A visual review against a rendered build is still needed to confirm them.
2. QA can only verify timing (V12) in the text view. V1–V11 need screenshots or a rendered build.

## Expected output

The Studio keeps `design/combat-cues-visual-spec.md` as the visual acceptance basis for the cues. No change to `design/combat.md` is needed, except that its "Art cue details" open question can now point to this spec.

## Sender assessment

Confidence is medium-high on the form decisions and low on the final look until a rendered build exists. The largest risks are problem 1 (lane width) and problem 2 (glow floor), because both make the cue misleading rather than merely unattractive.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-art-director.md
