---
kind: handoff
goal: G-001
seq: 9
from: gameplay-engineer
to: game-designer
stage: Design
outcome: question
---
# 09: gameplay-engineer → game-designer — level 1 spec has a gap in the intro-cancel case; Build is held

## Task

Settle the intro-cancel gap below (Q1 and Q2) in `design/onboarding.md`, and accept or change the proposed defaults for the minor gaps (Q3–Q6). Then return the spec to the Studio so Build can resume. No change has been applied to build 0.2 and nothing goes to QA yet.

## Context

Goal G-001 (first-puzzle-stall). Handoff 08 asked for the level 1 opening spec to be implemented for build 0.2. Before coding I listed every player-observable behavior the spec produces and checked each against the spec. Most are fully defined. One case is not: what happens when a touch cancels the start-of-level intro and that touch is not on the pool. The spec also doesn't define the intro's relationship to undo history. Both change what the child sees, so they are not implementation details I may decide.

## Findings

**Blocked part (Q1, Q2).** Rule 2 says "Any touch-down during the intro cancels it at once, and the pool follows the finger from its current position." That only covers a touch on the pool. The edge case "Touch during the intro" just points back to rule 2.

**Q1. A touch-down on the crab, the home or the sand during the intro (about 1.6 s window).**

Rule 2 says any touch cancels the intro. Rules 3–5 say those touches wiggle/glow and trigger the redirect pulse. Undefined:
- (a) Where does the pool end up after the cancel?
- (b) Does the idle pulse start from there?
- (c) Does the touched object's normal response and the redirect pulse play on top of the cancel?
- Option A: the pool stays where it is mid-slide.
  - Cost: low. The cancel just stops the tween.
  - Side effects: the pool rests off its authored start position. The "home glows within 1.5 pool-widths" check may trigger at rest if the start is near the home. See Q2.
- Option B: the pool eases back to its authored start position (about 0.2 s) and the idle pulse starts there.
  - Cost: low to medium. It needs one extra short tween.
  - Side effects: the touched object's response and the redirect pulse (which also moves the pool's scale) play while the pool is moving. Say whether the redirect pulse waits for the ease-back.
- Option C: ignore non-pool touches during the intro (the intro keeps playing).
  - Cost: lowest.
  - Side effects: contradicts "any touch cancels" and "every touch gets a visible response within 0.2 s", unless the crab/home still respond.
- My proposal, not applied: Option B. The crab/home reaction plays at once, the redirect pulse is allowed to start after the ease-back, and the 0.2 s pulse window then applies from the end of the ease-back. This needs your acceptance because it changes the "within 0.2 s" criterion for this case.

**Q2. Does the intro move enter the undo history and the pool's logical position?**

Rule 1 says undo restores the previous position, and the edge case says undo does not replay the intro.
- Undefined: if the pool is left displaced (Option A), is the displaced position its first undo state or is the authored start position?
- Proposed default: the intro is a visual offset only and never pushes a history entry. The pool's logical position is always the authored start until a real drag is dropped, and undo returns to that.

**Minor gaps with proposed defaults (none applied until you accept):**

- **Q3. "Turns to face the pool" (crab, rules 3).** The permitted effects are scale, rotation, position and brightness. Default: a horizontal flip (scale x −1) of the existing sprite where the pool is on the other side, plus the ±8° wiggle. Alternative: rotation only, no flip.
- **Q4. "Within 1.5 pool-widths of the home" (rule 4).** Default: measured center-to-center, using the pool's at-rest width. Alternative: edge-to-edge.
- **Q5. Touch-down on the pool during a redirect pulse (rules 1 and 5).** Default: touch-down wins. The pulse is cancelled and the 1.10 lift applies from the current scale.
- **Q6. Header says "for build 0.3"; the Handoff 08 task says build 0.2.** Default: treat as the next build after 0.2, level 1 only.

**Open questions from Handoff 08 (answers):**

1. **Touch on crab and home:** per `sim/repo-notes.md`, "only tide pools respond to touch... Touches on creatures and homes are ignored." So the current state is no handler for those pieces. Input is not blocked. This does not change the spec.
2. **Home's current styling:** I cannot capture it from the packet. Per repo-notes, each piece names an outline style and an idle animation in the level data. When Build resumes I will set the level 1 home to the scenery outline style and no idle animation. That satisfies the spec whatever the current value is. A real capture is still needed at Verify (spec check 3).
3. **Reduced-motion setting:** I cannot confirm availability on target platforms from the packet. Nothing in `project.md` or repo-notes names the platforms' accessibility settings. This stays open and needs a platform check (iOS "Reduce Motion", Android "Remove animations"). The spec's static-brightness fallback is implementable either way. If the setting is not available on a platform, the fallback is simply unreachable there. I will read the OS flag where it exists and will not add an in-game toggle, which would be a scope change.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies. None of the options above add a timer or an irreversible step. Q2's default keeps undo intact.

## Constraints

- Level 1 only. Existing sprite sheet only. Touch only. No dependence on reading text. No timers or inactivity triggers.
- The role forbids me from interpreting the spec or applying a default before you accept it.

## Open questions

- Q1 and Q2 (blocking): decide the cancel behavior and the undo relationship. Choose one of Options A–C, or another.
- Q3–Q6 (minor): accept the proposed defaults or change them.
- Platform reduced-motion availability: needs someone with platform access. The Studio decides who. It does not block your spec edit.
- Not blocked: everything else in the spec is fully defined. Once Q1–Q2 are settled the work is local, as the spec says.

## Expected output

An updated spec section in `design/onboarding.md` answering Q1–Q6, then a Handoff to `studio` (outcome `done`) to route Build again. On re-entry I implement the whole spec and hand the change to QA. What can proceed once unblocked, none of it affected by any answer:
- pool recolor, outline and idle pulse;
- touch-down lift;
- crab tap/drag responses and demotion;
- home glow;
- the redirect pulse with its 1.5 s rate limit;
- edge cases other than the intro cancel.

I held all of it back from the Handoff on purpose. In the dry run, stating a change counts it as made, and I don't want a partial level 1 to reach QA.

Studio notes for the designer:
- If you accept Option B, state the changed timing for the cancel case in the player-observable acceptance criteria, since it alters the "within 0.2 s" criterion for that case. Keep the spec free of Option C (idle hint) as before.
- Platform reduced-motion availability is not yours to settle. Keep the static-brightness fallback in the spec; the Studio will handle the platform check outside Design.
- The Build handoff that follows must say its result is addressed to `studio`, so Verify and a fresh Playtester handoff can be composed.

## Sender assessment

Confidence is high that Q1 and Q2 are real gaps. A 7–10 child tapping the crab in the first 1.6 s is likely, since the playtest children tapped the crab first. So the case will occur in the re-playtest, and the answer decides what they see. Confidence is medium that Option B is the best for the child, because it keeps the scene identical across children. Option A is simpler and equally safe under D-001. The root-cause reasoning from the diagnosis is unchanged by this question.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
