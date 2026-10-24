---
kind: handoff
goal: G-003
seq: 20
from: game-director
to: studio
stage: Close
outcome: goal-met
---
# 20: game-director → studio — Review: G-003 intent is met on the evidence observed; scope cut and proposed Goals

## Task

Close G-003 as `goal-met`, with the limits below stated plainly. Record the proposed Goals and Owner items. No Owner cost escalation is needed.

## Context

Owner request: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. The success condition in `goal.md` is that a player with only the text view and `repo/manual.md` can tell at any moment whether dash is available and, if not, when it will be again. Diagnose (02) found missing information, not rules. Design (D-028, D-029), Build (14), QA re-verification (17) and one independent Playtest (18) followed. The budget (17) is used. I reviewed against the success condition, not against the plan.

## Findings

**Verdict: `goal-met`**, limited to the conditions actually observed. Where the rest was not observed, the verdict does not claim it.

Why it is met:
- Every observed picture ends with `dash: ready`, `dash: active` or `dash: N s`. QA found the values equal to the build's behavior at 60 and 30 FPS, and the Playtester read them without guessing.
- A too-early press prints `dash not ready — N s left`, with a reason suffix where it applies. The Playtester knew exactly how long to wait.
- `dash ready` is printed at the exact moment (0.85 s at 60 FPS, 0.90 s at 30 FPS, as D-029 allows). The Playtester could rely on it instead of polling.
- Rule-driven refusals print the same line on the legacy route and the public driver. Unit tests: 180 OK.
- The manual explains the field, the messages and the 0.1 s rounding.

**Answers to the open questions**

1. *Does the hit-stun countdown break the condition?* No. After a hit the field shows a correct countdown to the time dash works again (`0.3 s` → `ready`). The success condition asks about availability and when. The reason is a separate readability gap. The Playtester rated it moderate, and the manual explains it. It becomes a proposed Goal (D-030).
2. *`(nothing happens)`.* Not part of this Goal. The Playtester's script had no dash rule, so these lines are not dash refusals, which now print the new text. They are most likely rule actions (face or move) ignored during hit-stun, but I cannot show that from the packet. It is another readability issue and possibly a defect, and goes to a proposed Goal for diagnosis (and QA if it proves a defect).
3. *Public-driver cadence.* Accepted as documented in `public-driver.md` and recorded in D-030. It affects when periodic pictures appear, not any dash value, and `dash ready` is on time. The conflicting spec wording is to be corrected when `design/dash-availability.md` is next edited.
4. *Unverified items.* See below.

**Passed (evidence)**: P1–P7, P10 (as observed), P13 (dash action on both routes, `dash toward` on both routes), Q1/Q2 (30 and 60 FPS), the reduced Q12 (note line exact, field present), event identity between views on two scripts, P12 on scripted rooms 3 and 5, partial Q9. Playtest: readable field, accurate numbers, usable refusal text and `dash ready` in room 1 at 60 and 30 FPS.

**Not observed (not counted as pass) — `skipped`**:
- Q5 (room-entry reset in a run), Q7 (bot consistency), P12 via public replay scripts, P8/P9/P11 (hit with no dash, hit-stun press, wind-up case), the attack-refusal half of P13 on both routes, Q3/Q4/Q6/Q10/Q11 (unit tests exist, not read by QA), and the Q9 gaps (some rooms/screens).
- Why skipping is acceptable for the request: the field reports the build's state and every refusal shows its time, and no observed case showed ready while a press was refused or the reverse. A failure in these areas would show as wrong numbers in a particular situation. That risk remains and is accepted, not removed. The budget is also used, and the items do not change the Owner-facing answer.

**Unverifiable with available means**: the baseline-dependent parts of Q8 and Q12, and the claim that timing is unchanged (the before build does not exist; only the frame-quantized values 51 frames at 60 FPS and 27 at 30 FPS were checked). Not a pass. Not claimed.

**Limits of the human evidence**: one Playtester, scripted non-adaptive play in room 1 only, no live or gamepad play, no dodge-by-dash on purpose, no other enemies or boss, no edge timing between 0.85 and 0.9 s. Whether the one-decimal rounding and the 0.9 s at 30 FPS feel clear in real play is not shown.

**Source id note**: ids seen across files (`b62005468da6`, `aa28af2ce710`, `3951a3656940`) are unreconciled; QA saw only `3951a3656940`. The verdict refers to the build QA and Play ran. This is not resolved here.

**Scope cut and proposed Goals** (each is a new Goal, not an extension of G-003)
1. *Hit-stun reason on screen*: show on the field (or by a message) that dash is unavailable because of hit-stun. Wording only, no rule change. Fold in the correction of the spec cadence wording when `design/dash-availability.md` is edited.
2. *Unexplained `(nothing happens)` lines*: diagnose which action they come from and whether it is a defect.
3. *Stale grub warning countdowns between pictures*: a lunge cue issue, outside dash availability.
4. *Optional verification of the skipped items* (Q5, Q7, P12 via replay scripts, P8/P9/P11, attack-rule half, Q3/Q4/Q6/Q10/Q11, Q9 gaps), together with a live and adaptive playtest of dodging with the dash in other rooms. Only worthwhile if the Owner wants stronger assurance; it needs generated replay scripts or a repo-side runner.

**Decisions to revisit**: none reached. D-028 (field breaks results or rules): not found. D-029 (human finds 0.9 s at 30 FPS confusing; refusal pictures called clutter): not reported. D-030 is new.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-028: dash indicator on the legacy route too (including room 5).
- D-029: 30 FPS tolerance, driver pictures after dash messages, rule-driven refusals print, no-baseline evidence for Q8 and Q12.
- D-027: G-002 stopped; its verification is not reopened.
- D-030 (new, this step): the scope calls above and the cadence acceptance.

## Constraints

- Dash rules, timing and inputs did not change and must not change under this Goal.
- The budget is used. Nothing here is a planned Design, Build or QA stage.
- Unverified and unverifiable items must be reported as such to the Owner, not as pass.

## Open questions

- For the Owner, in the closing message: do they want proposed Goals 1 and 2 opened, and is the optional verification (4) wanted? These are priorities, not blockers for closing G-003.

## Expected output

The Studio Closes G-003 with outcome `goal-met`, updates `goal.md` Route and Outcome, lists proposed Goals 1–4 and the Owner items, and informs the Owner. The Owner message (ja) should say plainly: ダッシュの可否と再使用までの時間は、確認できた範囲（第1部屋、60/30 FPS、スクリプトによるプレイ）で画面から読み取れた。被弾後の表示理由や「(nothing happens)」の説明は別Goal候補。実機プレイや一部のQA項目は未確認で、変更前ビルドがないため「タイミング不変」は確認できない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md
- Project: goals/G-003-dash-availability-clarity/goal.md, design/dash-availability.md, repo/public-driver.md
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md, decisions/D-030-g003-review-scope-cut.md
- Previous handoff: goals/G-003-dash-availability-clarity/19-studio-to-game-director.md
