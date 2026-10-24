---
kind: handoff
goal: G-001
seq: 67
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 67: game-director → studio — Review pass 2 on build 0.6.1: goal not met yet, but the gap is narrow and inside D-001. No Owner escalation. Build the D-008 message and manual text now; Design gets a room 3 content question.

## Task

Route the Review result. Verdict: **goal-not-met**, moderate confidence. The remaining gap is design content inside D-001 and the pillars. The Owner escalation named in D-009 is **not** needed. Decision D-010 records this.

## Context

Goal G-001. Success condition: different situations call for noticeably different play (positioning, timing, attack, dash), and the player can tell why. Pass 1 (60, D-009) asked for a variant-aware playtest. It is done (63, build 0.6.1, scripted, six sessions, rooms 1–5), and QA (64) closed the 30 FPS gaps with no defect. I ran no `play` or `bots` this step.

## Findings

### Verdict

**Goal-not-met, with a much smaller gap than at pass 1.** The main suspicion in D-009 is mostly cleared: the differences the build was changed to create do show up when the player plays them separately. Two things keep me from calling the Goal met: one room is still flat for a long stretch, and the "can tell why" half is only partly met in the text view.

### Evidence that the intent is met

- **Enemies ask different things.**
  - Grub and runner: "step aside or swipe first". For the runner, the 0.35 s warning makes acting early matter more.
  - Brute: "step aside; a swipe will not stop it". The tester called it the first time a swipe cannot stop the warning.
  - Spitter: "cross or dash the aim line, or close in".
- **Rooms 4–5 hold attention.** Several asks overlap, the tester had to choose which to answer first, and attention stayed high through room 5. This is the strongest evidence for the Goal.
- **Readable threats.** Warnings always came before damage. QA 64 confirms the warnings, cue lines and messages match the design at 30 and 60 FPS, with no defect.
- **Cost of ignoring cues.** The fast run in room 2 lost to the brute because the script had no brute rule. That is the design working as intended, and it is not evidence of failure.

### Evidence that it is not met yet

- **Room 3 (spitters only).** The tester called it the most repetitive stretch: about 20 s of "aim, dash, shot lands behind me, again", with attention dropping. The single ask is the content gap. Only the tester's own choice of killing two spitters and leaving the third in a far corner made the standoff last that long, so part of it is script behaviour. It matches the cautious-play standoff in 53, and I treat it as real but not severe.
- **Room 1** offers one kind of ask. The tester rated this low impact, and it is a teaching room. I do not act on it.
- **Rooms 3 → 4 → 5** differ mostly in how many things overlap, not in what each thing asks (the tester's summary). Variety comes from overlap more than from distinct asks. That is acceptable under D-001, since depth is meant to come from positioning and enemy behaviour. It means variety outside rooms 4–5 is thin.
- **"Can tell why" is partly unmet.** The message line reads "a grub rears back" and "hit by a grub" for runner and brute, and only the `cue:` line names the enemy. The tester was confused by a brute hit that read as a grub hit. This is a clarity gap that D-008 already proposes to fix.

### D-009 escalation condition: not triggered

The condition was that the melee enemies still read as one answer, with runner, standard grub and brute not told apart, or the brute only kited.
- The brute **was** told apart from the grub and runner.
- The runner and the standard grub share an answer, but they differ in time pressure. That was designed (D-008 says so).
- The brute loop in the slow room 2 run (about 8–27 s, six or seven dodges, never punished in the recovery) was partly caused by the tester's rules. The tester said so, and their rules never hit the brute in its recovery window. This is the D-004 trigger "human dodges the brute without fighting it". It is not confirmed on scripted evidence, so Option 3 (a spitter in room 2) stays deferred.

So there is no Owner question. A new melee behaviour or enemy type, healing, or an input change is not needed on this evidence.

### Confidence and limits

- Confidence in "not met, narrow gap": moderate. Confidence that no Owner decision is needed now: fairly high.
- All play was scripted. The tester could not feel the pad, reaction rules ran on a 0.15 s grid, and three outputs were cut at about 19–27 s. The 30 FPS run was room 3 only, with no frame-rate difference seen (QA 64 covers it).
- A human check would add what scripts cannot: whether room 3 and the brute loop feel flat to a person, whether a person understands the brute's no-flinch rule without the manual, and whether the shot clutter in rooms 4–5 feels unfair (the tester expected some hits would). I recommend one short live check after Build 21, as the closing evidence, not as a new Diagnose.

## Next issues

1. **Room 3 has a single ask** (inside G-001, Design). Ask `game-designer` for room-content options inside D-001, using existing enemies only. Room 3 should offer a second kind of ask, or avoid a long standoff against one cornered spitter, without breaking criterion 11 or the room 3 cue timing that teaches the aim cue. This is design content. It is not an Owner choice.
2. **Variant names in the wind-up message and the manual late-swipe text** (clarity, "can tell why"). Build now, see below.
3. **Room 3 in-flight count vs D-007 (66, non-blocking).** I do not decide it here. The tester read room 3 volleys as readable and took no hit in the 26 s seen. QA's conflict is about which stated rule governs, and that is the Design call. If Design changes the room 3 cap or the cue rule, bundle it with issue 1 so one room 3 change is built and checked once.
4. **Brute loop and the "dodge without fighting" trigger (D-004).** Not confirmed. Watch it in the human check. Option 3 stays the first lever.
5. **Proposed new Goal at Close:** visual criteria V1–V11 need a graphical build, and V12 stays open.

I do not ask for another Diagnose. There is no new cause. The remaining questions are about content and wording, and a human check.

## Answer to question 3: build D-008 and the manual text now

Build 21 should carry the D-008 variant-named message (`a grub`, `a runner`, `a brute rears back`) and the manual late-swipe wording from 59. Reasons:
- D-009 item 5 kept the message out of the playtested build to keep the comparison fair. That playtest is done, so the reason to wait is gone.
- Clarity is half of the success condition ("the player can tell why"), and the tester hit it directly.
- The change is small, reuses the existing message system, and keeps the substring `rears back`, so reaction scripts still work. `game-designer` stays the owner of the wording and acceptance criteria (`design/combat-step59.md`).
- The message change should not wait for the room 3 Design answer. They can be built together if Design is ready in time. If not, ship the message and manual text first and Verify them, and do the room 3 change in a later build. The next playtest must state which build it used.

Treat D-008 as ready to build. Because D-008 is `proposed` and written by the Designer, the Studio should mark it accepted once Build 21 is routed (D-010 records that I do not object).

## Decisions already made

- D-001: one-button combat. Respected; nothing here needs a new input.
- D-004 to D-007: stand. D-007 is touched only by QA's non-blocking question (66), which is Design's call.
- D-008 (proposed): now cleared to build (see D-010).
- D-009: its escalation condition was checked and is not triggered. The "revisit when" items "cannot tell runner, standard grub and brute apart" and "stalls against the brute" are not reached on this evidence.
- New: **D-010** (this step).

## Constraints

- Stay inside D-001 and the pillars. A new enemy type, healing, or an input needs the Owner, and nothing here needs it.
- New issues become proposed Goals unless they serve "the player can tell why" or the room 3 variety gap named above.
- Evidence stays scripted until a human check is done. Weigh the next report that way.

## Open questions

For `studio` (routing):
1. Route Design for room 3 (issue 1), together with the existing 66 question.
2. Route Build 21 (message and manual text), then Verify (QA).
3. After Build 21, one playtest of the new build, ideally a live player or a hand-timed run, with room 3, the brute in room 2, and the brute hit message as checks. Then Review pass 3. If the melee reads as one fight in that pass, escalate per D-009; otherwise the Goal can be met or partially-met with the reasons stated.

## Expected output

The Studio routes Design (room 3), Build 21 and Verify, then a final playtest and Review pass 3. No Owner escalation is drafted: the trigger is not met.

## Sender assessment

Verdict confidence is moderate because the evidence is scripted. I weighed the playtester's own admissions that the room 2 brute loop and the fast-run deaths came from their rules. I counted the room 3 standoff as real because the same standoff was reported in 53, in a different script. I did not run the build.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
- Previous handoff: goals/G-001-combat-monotony/65-studio-to-game-director.md
