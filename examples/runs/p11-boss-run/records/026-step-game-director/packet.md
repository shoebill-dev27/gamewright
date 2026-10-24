# Studio operation packet

operation: Step
goal: G-002
role: game-director
incoming_handoff: goals/G-002-final-boss/21-studio-to-game-director.md
next_seq: 22
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-002-final-boss/22-game-director-to-<recipient>.md
- decisions/D-021-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-002-final-boss/21-studio-to-game-director.md
---
kind: handoff
goal: G-002
seq: 21
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 21: studio → game-director — 供給・費用承認のOwner判断を具体化する

## Task

20の限定調査とbriefを基に、現行仕様を継続するための供給・費用承認について、一つのOwner Escalationを日本語で準備する。必要物、回答すべき権限者、未確定費用、選択後の経路を明記し、未確認を承認・供給不能へ読み替えない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。D-015で連続ラン・単体ボス・先頭retryを承認し、D-016〜D-019で方向・仕様・基準適用を確定した。D-020による限定Plan補完は20で終了したが、Build開始の五条件は揃っていない。

回帰正本の読込みは解決した。一方、供給責任者、利用権、独立検証枠、予算承認根拠はパケットから生成できず、実行経路の確認も取得不能として返された。Studioは同じ不足だけの三度目のPlanを開かず、権限を持つ相手への具体的な判断準備へ進める。

## Findings

- 20の§1〜2：実行ツールの取得経路が利用できず、shell・Pythonは未着手。指定sha `27fe16268ac8`との一致、基線、版表記差の原因は未確認。このexecutorの制約はプロジェクト資源の不存在を示さない。
- 20の§3：回帰正本と実テストの保持・終了・置換対応を補完。D-020条件2はPlan上充足したが、実行合格ではない。
- 20の§4〜7：最小desktopホスト方式を提示したが、OS・表示環境、依存権限、keyboard／gamepad、独立QA・Art・Play枠の供給は未確認。pygame／SDL系は候補であり確定依存ではない。
- 暫定計画18〜33.5人日はBuild、独立検証、Designer判断、修正・再検証枠、Reviewを含む。金銭費用、日程、既消化工数との精算、環境対応増分は未確定。承認済み総額ではない。
- 20の§8は既存資源指定、不足分の調達を伴う継続、供給・承認まで停止の案を提示している。Studioはゲーム内容の選択や推奨を決定していない。

## Decisions already made

- D-015：連続ラン、第5部屋単体ボス、先頭retryのOwner承認。無制限の費用承認ではない。
- D-016／D-017：体験方向と詳細契約。headlessだけへの縮小やV2任意化は未承認。
- D-019：回帰適用、対応bot比較、Designer実測後判断を維持。
- D-020：最小実機ホストは既存要件の実現作業。五条件解決までBuild保留。費用承認根拠の取得不能などを再検討条件とする。

## Constraints

Owner requestとInterpretationを維持する。Goalの再解釈、範囲縮小、費用・権限・調達の承認はOwnerへ戻す。技術方式はTechnical Director、詳細仕様はDesignerの権限に残す。

実装、依存導入、購入、外部費用の確約、外部への連絡は行わない。人物名、予算上限、単価、供給可能性を創作しない。回答者が特定できない場合は、Ownerに供給責任者・予算権限者の指定を求める形にする。

予算不明を超過とも承認内とも扱わない。暫定人日幅を金銭総額・納期の確約にしない。秘密情報や個人情報を求めず、必要な権限・資源の非秘密の条件のみ扱う。

Build保留、逐次作業、独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

1. 読取・実行可能なcheckout、shell／Python、対象desktop・入力機器・依存利用権限、独立検証枠について、誰が供給と条件を回答するか。
2. 既存承認との照合資料を誰が提供できるか。取得不能なら、Ownerに今求める供給・承認条件は何か。
3. 既存資源を指定して継続、不足分の条件付き調査・調達準備、停止のうち、現時点で提示できる2〜3案と推奨は何か。未見積もりの購入を包括承認する案にはしない。

## Expected output

`studio/templates/escalation.md`に従う日本語のEscalationをOwner宛てに作成する。判断対象を「必要な供給・費用条件を整えて現行仕様を継続するか」にまとめ、Roleで生成できない必要物、権限者、既知の暫定幅、未確定部分、2〜3案、Game Directorの推奨と再検討条件、各案の後続ルートを示す。

供給情報の提出や責任者指定への同意と、未確定の購入・実装費用の承認を区別する。どの継続案でもD-020の五条件を満たす前にBuildを許可しない。範囲変更案を含める場合はOwnerのResume後にDesign／Planへ戻す。

Studioは提出されたEscalationを次のRouteでOwnerへ開き、依存Stepを停止してGoalをblocked-on-ownerにする。現Stepは判断準備であり、Owner承認を取得済みにしない。同じ資料のままPlanへ返さない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: studio/orchestration.md
- Project: studio/templates/escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: goals/G-002-final-boss/18-game-director-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Previous handoff: goals/G-002-final-boss/20-technical-director-to-studio.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
>>>END

<<<FILE studio/orchestration.md
# Studio Orchestration

The Studio receives an Owner Goal and moves it forward until the Goal is met or the next decision
belongs to the Owner (spec §13).

The Studio decides **process**: which Role works next, with which Skills, on which context, in what
order. It never decides game content, specs, technical approach or verification verdicts — those
belong to Roles (see Decision authority). Choosing only the stages a Goal needs is the Studio's
core job; adding stages is not.

## Operations

Every executor performs these operations the same way. In Phase 1 a human starts each operation;
the Studio stops after Intake and after every Route, and states the next action (spec §18).
`execution.md` defines how a runtime runs each operation in a fresh, isolated executor that sees
only its packet; the procedures below are the same either way.

`goal.md` holds the Goal's current state; its history is the **Goal log**, `log.md` in the
Goal's directory. After every Intake, Route and Resume, whoever runs the operation appends one
entry (an isolated runtime does it itself): the operation and date, the Goal's status and open
steps, and the *Route changes* text just written. Entries are never edited or removed, and no Role
or Studio operation rewrites the log. Every operation keeps *Owner request* exactly as quoted at
Intake. Only Resume, after an Owner decision, may change *Interpretation*; a Route that would need
to reinterpret the Goal escalates instead.

### Intake — a new Goal

Load: `studio/README.md`, this file, `studio/workflows/development-loop.md`, `<project>/project.md`,
and the titles of `<project>/decisions/`. Open a design document or Decision only if the Goal
touches it.

1. **Understand the Goal.** Quote the Owner's words verbatim. Restate the Goal as an observable
   success condition, qualitatively; numeric thresholds belong to Design (acceptance criteria) and
   the final verdict to Review. Note what is out of scope.
2. **Check the Project Context.** Vision, current state, constraints, and Decisions the Goal touches.
3. **Check for an immediate escalation.** If acting on the Goal requires reinterpreting it, or it
   conflicts with the vision or a Decision, escalate before routing (see Escalation).
4. **List the unknowns.** Ask each stage's entry question in `development-loop.md`. Every question
   that cannot be answered from the Project Context is an unknown.
5. **Select stages, Roles and Skills.** One stage per unknown, plus Verify after any Build. The Role
   is whoever holds authority over that question; the Skills come from the stage table. Mark each
   stage `planned` (needed whatever earlier steps find), `tentative` (needed only if an earlier
   step's result calls for it — say which result), or `skipped` (the Project Context already
   answers its question — say how).
6. **Order and parallelize.** Default is sequential. Parallel only for independent steps (see
   Parallel work).
7. **Write** `goals/G-NNN-<slug>/goal.md` (templates/goal.md; next free number in the project,
   short kebab-case slug, ISO dates) and the first Handoff `01-studio-to-<role>.md`; mark that
   first step `open` in the route table. Apply Route
   steps 4–5 to that Handoff: read the recipient's Role contract ("Works from", "Independence")
   before writing it.
8. **Return to the Owner** and stop: the route, why each stage is there, which stages were skipped
   or left tentative and why, and the next action.

### Step — run the next step

Load exactly the incoming Handoff, the files in its **Load** list, and the template of the artifact
you write (`studio/templates/`). Nothing else. `file#section` means that section only; scanning the
file's headings to find it is fine.

1. Act as the receiving Role: respect its contract (Decides / Must not), follow the listed Skills.
2. Produce the Expected output.
3. Write the outgoing Handoff (templates/handoff.md), filling Task through Open questions from your
   own work. Your output (report, diagnosis, plan, verdict) goes in Findings, or in the project
   files Findings names (e.g., a design document). Set `outcome`, and set `to` to the next Role
   per the route — or per your Role contract's "Hands back / escalates when" if your result calls
   for it. If the incoming Handoff's Expected output names another recipient (e.g., `studio`),
   use that.
4. Do not route around your contract: if the work needs a decision you do not hold, hand back.

### Route — after every step

Load: `goal.md`, the last few entries of the Goal log, the latest Handoff, this file,
`studio/workflows/development-loop.md`; for steps 4–5 also the recipient's Role contract and the
files you put in its Load list.

1. Mark the step done in the route table, linking its Handoff.
2. **Compare the outcome with the plan.** If it fits, the next planned step follows. If not, apply
   the return rules in `development-loop.md`, revise the remaining route, and say why under
   *Route changes* in one to three lines (600 characters at most), replacing the previous text
   (the Goal log keeps the history; the Handoffs carry the details). Keep *Unknowns* current the
   same way: update a stage's line, do not narrate earlier passes. Confirm (`planned`) or drop
   (`skipped`) any `tentative` stage whose condition this result settles. The route is a plan,
   not a contract.
3. **Check escalation triggers** (below). If one fires, write an Escalation instead of a Handoff.
4. **Check the recipient's inputs.** Compare the outgoing Handoff with the recipient Role's
   "Works from" section; remove what the recipient must not receive and add what is missing,
   editing the Handoff in place (it keeps `from`: the sender). Leave `## Sender assessment`
   untouched: it stays on record, and Roles whose policy strips it never receive it.
   When the recipient has an Independence section that forbids what the sender knows (e.g., a
   Playtester after Build or Verify), the Studio composes a fresh Handoff for the recipient from
   permitted information only. To make that possible, the Handoff that routes work to the sender
   says in its Expected output: address the result to `studio`.
5. **Select context.** Fill the Handoff's Load list: the recipient's Role contract, its Skills, the
   Project Context sections and Decisions this step needs, and the previous Handoff. You choose
   files by name (the project file list); you do not need to read a file to list it — the recipient
   reads it. Never route a step to `studio` itself: the open step is always a Role's or the Owner's.
   When opening parallel steps, write one Handoff per step in the same Route (consecutive `seq`).
   If you truly cannot route without reading an artifact's content, an isolated runtime lets you
   request specific files once (`execution.md`, context request).
6. **Mark the next step `open`** in the route table, with the Handoff that starts it, and update
   Next action in `goal.md`. If the Goal is met, Close.

### Resume — after an Owner decision

1. Record the Owner's choice as a Decision with `decided_by: owner` (templates/decision.md),
   including the Owner's own words and any conditions they added.
2. Set the Escalation to `status: resolved` with `decision: D-NNN`; set the Goal back to `active`.
3. Re-plan the remaining route from the Escalation's "If chosen" consequences for the chosen option.
   If the Owner chose something no option described, re-run Intake steps 4–6 on the remaining work.
4. Write the next Handoff with `from: studio`, citing the Decision under *Decisions already made*.

### Close

Fill the Goal record's **Outcome** for the Owner: results, Decisions made, next issues (proposed
new Goals), and items needing the Owner. Set `status: done` (or `abandoned`, with the reason).
Then bring `project.md`'s `## Current state` up to date with what exists now (build, content,
known problems, how to run it; 1,500 characters at most), so the next Goal starts from the facts.
Nothing else in `project.md` changes: the rest belongs to the Owner.

Owner-facing text — the Outcome, Escalation briefs, and the Studio's replies to the Owner — uses
the project's `owner_language`. Other artifacts use whatever language the project's executors
share.

## Escalation

The Studio does not finalize every judgment on its own (spec §5, §19).

### Escalate to the Owner when

- the game's core concept, a vision pillar, or an Owner-made Decision would change;
- several major directions are viable and the evidence does not settle which;
- scope, cost or risk would change significantly beyond what the Goal implies;
- the Owner's taste or values are the main criterion for the choice;
- the change is irreversible (destructive data or asset changes, releases, public commitments);
- the Goal itself has to be reinterpreted to make progress;
- the work is blocked on information or material that no Role can produce (e.g., reproduction
  details only the Owner has, a build or repository that does not exist). The brief says exactly
  what is needed and why no Role can produce it; options include providing it, narrowing the Goal,
  or stopping.

### Do not escalate

Choices inside a Role's authority that stay within the vision, the constraints and existing
Decisions. The responsible Role decides and, if significant, records a Decision. Escalating these
pushes work back onto the Owner that the Studio exists to absorb.

### How to escalate

1. The Role with authority nearest the question prepares the brief with `prepare-owner-escalation`
   (usually `game-director`; `technical-director` for technical risk or irreversibility).
2. The brief is an Escalation file (templates/escalation.md): options, consequences, a Studio
   recommendation, reasoning, and what happens next under each option.
3. The Studio sets the Goal to `blocked-on-owner`, pauses every step that depends on the answer
   (independent steps may continue), and returns the brief to the Owner.
4. One question at a time: while an Escalation is open, do not open another. Later questions wait
   for the answer, or go into the next Escalation once it is resolved.

## Decision authority

Final decisions belong to the responsible Role — never to a vote across executors or opinions
(spec §14).

| Question | Decides |
|---|---|
| Direction, priorities, which approach to pursue within the vision, scope within a Goal, whether an experience Goal is met | `game-director` |
| Rules, systems, tuning, player-facing behavior within the approved direction | `game-designer` |
| Technical approach, architecture, sequencing, parallelization | `technical-director` |
| Implementation details within the spec and plan; root cause of a defect | `gameplay-engineer` |
| Visual direction and consistency within the vision | `art-director` |
| Pass/fail against acceptance criteria; reproducibility and severity | `qa` |
| Accuracy of experience observations (no decision authority over the game) | `playtester` |
| Routing and process | `studio` |
| Anything matching an escalation trigger | `owner` |

Record a Decision when it constrains work beyond the current step, when a real alternative was
rejected, or when the Owner made it. Smaller choices are noted in the Handoff. A Decision is never
edited once written, not even for a typo or a stray line: a change is a new Decision that
`supersedes:` it, so do not route an edit of one to a Role.

## Parallel work, workspaces and sub-executors

- **Parallel steps** only when neither consumes the other's output (e.g., QA verification and an
  Art Director visual review of the same build). Each gets its own Handoff (consecutive `seq`).
  Steps open at the same time are parallel; label their rows as you like (e.g., 2a, 2b). The Route
  operation waits for all of them before moving on.
- **Isolated code workspaces** (e.g., separate working trees) only when independent code changes
  run in parallel, as decided in a Technical Director plan. Never to separate Roles (spec §15).
- **Sub-executors** may do specialist research or independent review for a Role. They report to
  that Role; the Role decides.
- **Independence.** Run `qa` and `playtester` steps in a fresh executor context without the
  implementation history, whenever the executor makes that possible.

## Loop limits

No unbounded loops (Phase 1 has no autonomous loop at all, but routes can cycle):

- The same acceptance criterion fails verification twice → route to `technical-director` to
  re-plan, not to a third fix attempt.
- A Goal re-enters Diagnose twice without measurable progress → `game-director` reviews; this may
  become an escalation about scope or the Goal itself.
- A step hands back `question` twice for the same missing input, with nothing new supplied in
  between → do not route it to a Role again; escalate to the Owner for that input.
>>>END

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE goals/G-002-final-boss/goal.md
---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-20
---
# G-002: 最後に手応えのあるボス戦

## Owner request

> 最後に手応えのあるボス戦がほしい

## Interpretation

既存の第1〜4部屋を連続して進み、第5部屋を置き換えた単体ボスへ到達する。プレイヤーが位置取り、攻撃とダッシュのタイミング、敵の挙動への対応を通じて手応えを感じられる最終戦とし、最終勝利・死亡・ランの最初からの再挑戦まで成立する。短いランと、被害を受ける前に脅威を読み取れる体験を維持する。

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。具体的なボスの仕組み、難度、数値基準、継承・終端の詳細は担当Roleが定める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。承認範囲を超える規模・費用・リスクや既存Decisionとの衝突が判明した場合は、実装前にOwnerへ戻す。

## Unknowns

- Observe：既存の不具合報告ではないため skipped。実行による現状確認は未実施。
- Diagnose：done。静的調査では連続ラン・部屋間継承・最終勝利・専用リトライがない。指定shaとの一致、実行時の終端挙動、戦闘時間は未確認。調査の制限は04に記録。
- Decide：done。D-015でOwnerが連続ランと第5部屋の単体ボスを承認。D-016で読み取り・位置取り・回避後の反撃を中心とする方向と設計境界を確定。既存Decisionは存続し、旧第5部屋依存の基準への適用関係はDesignで整理する。
- Design：done。D-017とfinal-boss-and-continuous-run.mdで詳細契約、30/60 FPSの受け入れ基準、旧基準対応表を確定。未実装・未検証。
- Decide（既存Decisionとの整合）：done。D-018で旧集計を新構成の評価から分離する方向を確定。D-006自体の適用変更は未完了。
- Design補足：done。D-019と仕様§8・§10で旧集計の適用終了、保持する回帰、ボスdash検証、対応botのFPS比較条件、実測後のDesigner再判断を確定。過去G-001の判断・結果は保持する。
- Plan：16・20で計画と回帰対応を補完。回帰正本の読込み・試験対応はPlan上充足したが、実行合格ではない。指定sha・実行基線、実機供給・独立検証枠、費用承認は未確認。計画合計18〜33.5人日は暫定で、金銭費用・日程は未算定。D-020の五条件未充足につきBuild保留。
- Decide（実装開始条件）：done。D-020で最小実機ホストを既存要件の実現作業としてPlan対象に含める。費用・リスクの承認は未確定で、超過・供給不能も未確定。Buildは五条件の解決まで保留する。
- Plan補完：done。20で回帰対応、最小ホスト方式、未算入工数と必要供給物を整理。executorのツール取得経路が利用できず実行未着手。資源不存在・供給不能・承認超過は確定していない。
- Decide（供給・承認）：open。供給責任者・予算権限者と既存承認根拠が不明で、Roleが生成できない情報が残る。Game Directorが20のbriefから、必要物・回答者・継続条件を明記した一つのOwner Escalationを準備する。同じ不足だけでPlanを再発行しない。
- Design（実測後）：planned。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、Review前に追加数値ゲート・調整の要否を判断する。不要でも理由を記録する。明白な対処不能・到達不能はPlay前に戻す。
- Build：仕様と計画の確定後にゲーム変更が必要。
- Verify：Build後の独立QAが必要。30/60 FPS、連続到達・勝敗・再挑戦、共有戦闘ルールの回帰、実機入力経路を含む。Art Directorの限定表現確認をplannedに確定。player viewの二攻撃、予兆と実弾、回復、HP、終端・retryの識別を対象とする。
- Play：最終戦と到達体験の手応え、連続ランの所要時間を独立したプレイヤー観察で評価する。実装内容や期待結果は渡さない。
- Review：体験Goalの達成判断が必要。
- Next：結果と残課題をOwnerへ返す。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md → 結果: 02-game-designer-to-studio.md |
| 2 | Diagnose | technical-director | technical-plan | done | 03-studio-to-technical-director.md → 結果: 04-technical-director-to-studio.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done | 05-studio-to-game-director.md → 結果: 06-game-director-to-owner.md |
| 3a | Decide | owner | — | done | 06-game-director-to-owner.md → D-015 |
| 3b | Decide | game-director | make-decision, prepare-owner-escalation | done | 07-studio-to-game-director.md → 結果: 08-game-director-to-studio.md |
| 4 | Design | game-designer | write-design-spec | done | 09-studio-to-game-designer.md → 結果: 10-game-designer-to-studio.md |
| 4a | Decide | game-director | make-decision, prepare-owner-escalation | done | 11-studio-to-game-director.md → 結果: 12-game-director-to-studio.md |
| 4b | Design | game-designer | make-decision, write-design-spec | done | 13-studio-to-game-designer.md → 結果: 14-game-designer-to-studio.md |
| 5 | Plan | technical-director | technical-plan | done | 15-studio-to-technical-director.md → 結果: 16-technical-director-to-studio.md（question・開始条件未充足） |
| 5a | Decide | game-director | make-decision, prepare-owner-escalation | done | 17-studio-to-game-director.md → 結果: 18-game-director-to-studio.md |
| 5b | Plan | technical-director | technical-plan | done | 19-studio-to-technical-director.md → 結果: 20-technical-director-to-studio.md |
| 5c | Decide | game-director | make-decision, prepare-owner-escalation | open | 21-studio-to-game-director.md |
| 5d | Plan | technical-director | technical-plan | tentative | 新しい供給・承認資料の取得後、残条件を確認 |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。21でGame Directorが供給・費用承認に関するOwner Escalationを準備する。現時点のopenは準備Stepであり、Ownerへの質問はまだ開いていない。新しい供給・承認資料が得られた場合のみPlanの残条件確認を開き、必要なOwner判断とD-020の五条件が解決するまでBuildを保留する。独立QA、Art Directorの限定Verify、独立Play、Designerの実測後判断、Reviewの順序を維持する。初回基線やQAで明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

20のPlan補完を完了し、回帰対応の充足と実行・供給・承認の不足を分離した。Roleで生成できない供給情報と承認根拠の不足が具体化したため、21でGame DirectorへOwner Escalation準備を戻す。同じPlan質問を繰り返さず、Build保留と後続の独立検証順序を維持する。

## Next action

Game Directorが `21-studio-to-game-director.md` を実行し、供給・費用承認の一つのOwner Escalationを日本語で準備する。Buildは開始しない。

## Outcome

未完了・進行中。D-015〜D-020を維持し、回帰正本と試験対応の計画補完を完了した。実行基線、実機・独立検証の供給、費用承認は未解決。計画合計は暫定18〜33.5人日で、機器等の金銭費用・日程は未算定、承認済みではない。次はGame Directorによる供給・承認のOwner Escalation準備。実装、独立検証、Play、Designer実測後判断、Reviewは未実施。指定sha一致、実行成功、実機供給、難度、所要時間の新しい証拠はない。資源不存在や承認超過とは断定しない。Goalはactive、Buildは保留し、project.mdのCurrent stateは変更しない。
>>>END

<<<FILE design/final-boss-and-continuous-run.md
# G-002 最終ボスと連続ラン仕様

Status: Designと基準適用整理を確定。未実装・未検証。詳細契約はD-017、D-018に基づく旧基準の適用変更はD-019に記録する。

本書は新しい連続ラン、第5部屋、ラン境界・終端についての追加仕様。第1〜4部屋の構成、部屋内の既存敵・プレイヤー戦闘規則は既存仕様が正本である。G-002新構成への基準適用はD-019と本書§8が正本。過去G-001の判断・結果と既存Decision本文は変更しない。

## 1. 体験意図

道中で覚えた固定照準と回避を使い、ボスの次の攻撃を見て、避けた後にも攻撃できる場所を選ぶ。遠くへ逃げる安全と、近くに残って反撃する利益を区別し、通常敵との混戦とは異なる一対一の山場を作る。

## 2. ランと入場

通常ランは第1部屋から始まり、1→2→3→4→5の順に進む。第5部屋はボス1体のみ。通常敵、増援、第6部屋、ボス用チェックポイントはない。

各戦闘フレームの勝敗解決後、生存して全敵撃破なら第1〜4部屋は部屋クリアとなる。クリア表示を1.0秒間出してから次部屋へ自動遷移する。この間に戦闘は進まず、操作も受け付けない。次部屋の開始表示を出した後、次の戦闘フレームから動く。第5部屋の全敵撃破は部屋遷移を起こさず最終勝利となる。

通常ランの初期状態は第1部屋、3/3 hearts、位置(8,4)、右向き、停止。敵は各部屋の正規初期配置から始まる。

### 境界での継承

| 状態 | 第1〜4部屋クリア後の処理 |
|---|---|
| hearts | 生存者に1 heart回復、上限3。0から回復しない |
| 回復の時点 | 次部屋入場時に1回だけ。クリア表示中の再適用なし |
| 位置・向き | (8,4)、右向きへ戻す |
| 移動・ダッシュ | 停止。ダッシュ中なら終了させる |
| 攻撃回復、ダッシュ待ち時間 | 0へ戻す |
| hit-stun、被弾保護 | 0へ戻す |
| 予約攻撃 | 破棄 |
| 敵、予兆、弾、攻撃の接触消費状態 | 旧部屋分を破棄し、次部屋を新規開始 |
| 保持入力 | 破棄。実機入力では離して再入力するまで再発火させない |
| 反応ルールの定義・順序 | 同じラン内で継承 |
| 反応ルールの最終実行時刻、直前の盤面・メッセージ記憶 | 入場時に初期化。新部屋の表示から判断する |
| 未来の時刻指定入力 | ラン時刻に従い保持。境界中に期限が来た戦闘入力は破棄し、後からまとめて実行しない |

3 heartsでクリアすれば3、2なら3、1なら2で次へ進む。第4部屋も同じ扱いなのでボスには2または3 heartsで入る。消耗を完全には消さず、最低2回の被弾余地を確保する。部屋内回復、回復アイテム、任意回復は追加しない。

「3 hearts per room」は独立部屋試験の開始条件として保持する。通常ランの継承は本書の新契約であり、既存部屋内ルールの変更ではない。

## 3. ボス「洞窟の番人」

盤面印は`B`。初期位置(12,4)、HP12。プレイヤーへの接触そのものではダメージを与えず、攻撃の有効期間だけ危害がある。全フェーズで既存の正面スワイプが届けば1ダメージを受ける。装甲、無敵フェーズ、HPによる加速・形態変化はない。

攻撃は「突進」「短射」の2種類。順序は突進→短射→突進…で固定し、HPや距離で飛ばさない。初回入場時は突進を準備する。

各攻撃の前は接近状態となり、速度1.0 tile/sでプレイヤーへ歩く。距離2.0 tiles以下になったフレームで停止し、その攻撃の予兆を始める。予兆以降、回復終了まで追尾・再照準しない。回復終了後に次の攻撃の接近へ移る。距離0での照準は右(+x)に固定する。

### 攻撃定義

| 項目 | 突進 | 短射 |
|---|---|---|
| 予兆 | 0.7秒 | 0.8秒 |
| 照準 | 予兆開始時のプレイヤー位置への単位方向に固定 | 同左 |
| 予兆中の移動 | なし | なし |
| 発動 | 8.0 tiles/sで0.3秒、最大2.4 tiles移動 | 固定方向へ弾1個を発射 |
| 危険範囲 | 移動中のボス中心から半径0.6 tile | 弾中心から半径0.4 tile |
| 弾 | なし | 3.0 tiles/s、寿命1.0秒、最大移動3.0 tiles |
| ダメージ | 1 heart、1突進につき最大1回 | 1 heart、1弾につき最大1回 |
| 有効期間後 | 1.2秒の回復 | 発射から1.0秒の有効期間後、1.4秒の回復 |
| 回復中 | 停止、無害、スワイプ可能 | 同左。回復開始時には当該弾が存在しない |

短射は弾が早く消費されても発射から1.0秒待って回復へ入る。命中・吸収によって次の予兆が早まらない。寿命到達フレームは弾を失効させ、その弾の接触を新たに判定しない。

突進は部屋端でクランプするが、壁到達や接触によって有効期間・回復開始を早めない。通常命中、保護中接触とも突進の一撃を消費し、移動自体は継続する。

短射の弾は部屋端、寿命、最初の接触で消える。短射の有効期間にボス本体からの接触ダメージはない。ボスの弾は同時に最大1個であり、スピッターのcap／cue gap調停には参加しない。

### 中断と反撃

非致死スワイプはどのフェーズも中断・遅延・延長しない。HPは通常どおり減る。予兆中には`the boss takes the swipe; the warning continues`を出す。致死スワイプなら直ちに予兆と攻撃主体を失効させ、フレーム末の勝敗解決へ進む。

回復中は接触しても無害で、プレイヤーの攻撃回復0.35秒は変更しない。回復開始から届く位置にいれば、突進回復では時刻0、0.35、0.70、1.05秒の4回、短射回復では少なくとも同じ4回の攻撃開始が可能。これは理論上の機会数で、実測の撃破時間ではない。

突進には横移動またはダッシュ、短射には射線からの横移動、ダッシュ吸収、射程外への退避が使える。後退だけで避けた場合は回復中に距離を戻す必要がある。横へ避けて近くに残れば反撃しやすい。2種類とも予兆中の連打で止められない。

### 共有戦闘との関係

攻撃1ダメージ、射程1.5 tiles、回復0.35秒、ダッシュ4 tiles／0.25秒・待ち時間0.6秒、ダッシュ中の予約攻撃、被弾stun0.3秒・被弾後0.8秒までの保護は保持する。

D-005の結果規則をボスにも明示適用する。保護中の弾接触は弾消費、保護中の突進接触はその突進の一撃消費。保護終了後に持ち越しダメージを起こさない。

接触は移動後のフレームごとの距離判定、`distance <= reach`とする。本仕様は、既存と同じ速度・接触半径の突進と弾に限り、D-002／D-003と同じ帯を明示採択する。

- 弾：横ずれ0.39以下は命中、0.40超は非命中。
- 突進：横ずれ0.57以下は命中、0.60超は非命中。
- その間は上端を含み、30/60 FPSで命中差を許容する。
- 許容は命中／消費の有無だけ。照準、フェーズ、表示、時間の違いを免責しない。
- 新形状・別速度への包括的な拡張ではない。帯外差または突進帯0.03 tile超の所見はDesignerへ戻す。

## 4. フレーム内勝敗と終端

同一戦闘フレームでは、受理済みのプレイヤー行動と、まだ有効な危害による結果を解決した後、次の優先順位で終端を一度だけ決定する。

1. heartsが0なら死亡。
2. 生存して第5部屋のボスHPが0なら最終勝利。
3. 生存して第1〜4部屋の全敵HPが0なら部屋クリア。
4. それ以外は戦闘継続。

同一フレームに致死スワイプと既発射弾による致死被弾が成立した場合は死亡。スワイプで攻撃主体を倒したなら、その主体から新しい突進接触や発射は生じない。既発射弾はフレーム末の結果確定までは独立した危害として扱う。

部屋クリア・最終勝利・死亡の確定時に、残弾と予兆を全消去する。以後の表示時間中にダメージ、移動、予約攻撃、回復待ち時間、敵行動を進めない。死亡したまま次部屋へ進まず、勝利後の残弾死もない。確定後の勝敗変更と重複イベントは禁止する。

### 再挑戦

最終勝利・死亡の画面で`retry`を受け付ける。戦闘中と部屋クリア表示中のretryは無効。retryは終端メニュー操作であり、新しい戦闘入力ではない。

再挑戦は第1部屋、3 hearts、通常ラン初期状態へ戻る。ボスHP・順序、敵、弾、タイマー、予約・保持入力、勝敗、両ゲーム時刻、反応記憶を初期化する。FPSと反応ルール定義は同じセッション設定として保持する。旧試行の未来の時刻入力は破棄し、再挑戦の入力列を新試行用として明示して渡す。旧時刻入力を自動再生しない。

同一プロセス内のretryと、通常ランを新規起動した場合の初期戦闘状態は一致する。独立第5部屋試験の再実行は診断経路に留まり、通常ランのチェックポイントとして表示しない。

## 5. 時刻、入力、ポーズ、実行上限

- 部屋時刻は入場時0。戦闘中だけ進む。
- ラン時刻は第1部屋開始時0。戦闘と1.0秒の部屋間表示中に進む。ポーズ・死亡・勝利画面中は停止する。
- 各イベントは試行番号、部屋番号、ラン時刻、部屋時刻を区別して観測できること。
- 通常ランの時刻指定戦闘入力はラン時刻基準。独立部屋試験は部屋時刻基準。モードを冒頭に表示し、同じ入力列の基準を途中で変えない。
- 同じ時刻の入力は記載順。時刻入力を処理してから反応ルールを上から評価する。反応は既存のルールごとの0.15秒制限を保持する。
- 入場時刻と一致する時刻入力は、入場初期化と開始表示の後に受理する。クリア確定フレームでまだ受理していない戦闘入力を次部屋へ持ち越さない。
- ポーズは戦闘・部屋間表示を凍結する。時刻、フェーズ、弾、ダッシュ、保護、入力待ち時間、反応評価も進めない。
- ポーズ突入時に保持移動を解除する。予約済み攻撃は凍結して保持し、再開後のダッシュ終了時に通常どおり実行する。ポーズ中の戦闘入力は破棄する。
- 再開はゲーム時刻に依存しない制御操作で可能とする。スクリプト経路にも有限時間で再開を検証する手段が必要。具体構文はPlanで定め、停止したゲーム時刻にresumeを予約するだけの方式にはしない。
- 検証実行のlimit到達は`time limit — run unfinished`。勝利・死亡・部屋クリアと異なる終了理由とし、limitそのものを敗北にしない。
- limitと戦闘結果が同じ最終フレームなら、そのフレームの死亡／勝利／クリアを先に解決し、実行停止理由も別に記録する。

現行のpause、retry、連続モード、実機入力層、長時間player／trace経路は存在すると仮定しない。上記は新設要求である。Desktopキーボード／ゲームパッドの同等操作を要求として保持し、実装・検証経路と費用をPlanへ渡す。

## 6. player viewの情報契約

数値座標を内部確認専用にせず、テキストだけで危険を識別できること。

常設表示：

- `run — room n/5 — hearts h/3`と両ゲーム時刻。
- ボス部屋では`boss B — HP n/12 — <approach|warning|active|recovery>`。
- 次攻撃名は、その攻撃の接近開始時から`next: charge`または`next: short shot`として表示する。
- 既存のプレイヤー、敵、弾の印は保持し、ボスだけ`B`を追加する。

予兆開始時に即時描画し、全予兆中に`cue: B <charge|short shot> — locked <direction> — <seconds> left`を出す。

- 突進：固定した2.4-tile経路を`~`で示し、`danger: charge lane, radius 0.6 tile, rounded ends`を併記する。
- 短射：固定した3.0-tile射程を`~`で示し、`danger: one shot, contact radius 0.4 tile, range 3.0 tiles`を併記する。
- 文字セルの線は正確な連続座標の境界そのものではないことをmanualで説明する。方向と射程・接触幅の数値を省略しない。
- 発動で予兆線を外し、短射の実弾を`*`で描く。敵印と重なって隠れる弾も、活動中の弾数を表示して存在が消えたように見せない。

メッセージ：

| 契機 | 文字列 |
|---|---|
| 突進予兆 | `the boss prepares a charge` |
| 短射予兆 | `the boss aims a short shot` |
| 発動 | `the boss charges` / `the boss fires a short shot` |
| 回復開始 | `the boss is recovering — safe to approach and swipe` |
| 回復中 | `recovery: <seconds> left` |
| 回復終了 | `the boss resumes pursuit` |
| 突進被弾 | `YOU ARE HIT by the boss's charge`＋既存hearts suffix |
| 短射被弾 | 既存`YOU ARE HIT by a shot from the <direction>`＋suffix |
| 部屋クリア | `room n cleared — next room n+1` |
| 入場回復 | `recovered 1 heart`または`hearts already full` |
| 最終勝利 | `run won — boss defeated — retry: start from room 1` |
| 死亡 | `you went down — run lost — retry: start from room 1` |
| 再挑戦 | `new attempt — room 1/5` |

半秒ごとの定期表示に加え、予兆、発動、回復開始・終了、HP変化、被弾、部屋クリア、入場、勝敗、retry、pause／resumeで即時描画する。同時刻の複数変化は順序を保って1画面へまとめてよいが、メッセージを欠落させない。

既存敵の`rears back`、`takes aim`、`YOU ARE HIT by`のprefixとstep94の文言・方向規則を保持する。ボス予兆は既存敵の文字列に偽装しない。ボス対応の反応ルール／botsは、プレイヤーに見えるボス印・状態・攻撃名を根拠に追加する。

Art Directorによる限定Verifyを推奨する。対象はテキストの2攻撃の区別、予兆と実弾の区別、回復と次攻撃、重なり、勝敗・retryの識別。成果はplayer viewの具体的な読みにくさと文言・表示配置の修正案。グラフィカル素材制作や戦闘ルール決定は依頼しない。

## 7. 独立QAの受け入れ基準

以下を30 FPSと60 FPSで別々に判定する。時間許容は各実行の1フレーム以内、位置は仕様上の値とそのフレームの移動量を照合する。接触帯以外の結果差を、時間許容だけで免責しない。

player表示と同一ビルドの状態観測を対照する。試験用状態設定は独立した境界再現に使ってよいが、通常ランの連続到達の証拠にはしない。

| ID | 条件と合格条件 | 必要な観測 |
|---|---|---|
| R1 | 新規通常ランで1→2→3→4→5へ生存到達。各正規敵を実際に倒し、第5部屋はB1体だけ | 入場・撃破・クリア列、状態とplayer表示 |
| R2 | 第1〜4部屋の構成・配置・既存パラメータが元仕様と一致 | 部屋データと回帰試験 |
| R3 | 境界直前hearts1/2/3から次入場2/3/3。0なら死亡し遷移しない | 境界前後のhearts、回復イベント |
| R4 | ダッシュ、保護、予約攻撃、弾、保持移動、反応記憶を残した境界で、§2の各リセットが成立 | 境界前後全状態、次部屋最初の行動 |
| R5 | 部屋クリアから1.0秒後に次入場。表示中の戦闘入力は持ち越されず、入場同時刻入力は新部屋へ1回だけ適用 | 両時刻、入力処理列 |
| B1 | Bは(12,4)、HP12、攻撃順が突進→短射で反復。HP6以下でも変わらない | 初期状態、少なくとも各3回の予兆 |
| B2 | 予兆の途中にプレイヤーが移動しても照準不変。距離0では右。発動まで突進0.7秒／短射0.8秒 | cueと方向、発動時刻 |
| B3 | 開けた位置で突進2.4 tiles／0.3秒。壁ではクランプし、回復開始時刻は変化しない | 毎フレーム位置・フェーズ |
| B4 | 短射は1弾、速度3.0、寿命1.0秒。未接触・通常命中・吸収の各場合で回復開始は発射1.0秒後 | 発射、弾消滅理由、回復開始 |
| B5 | 開けた位置で、予兆開始から0.4秒以内に射線と直交して1 tile移動を完了すると各攻撃を無傷で避ける | 操作列、固定方向、hearts |
| B6 | 各攻撃へのダッシュ接触で無傷。ダッシュ終了後も同じ攻撃からダメージなし | 接触時の保護、消費、以後のhurt |
| B7 | 被弾保護が攻撃途中で切れる設定でも、既に接触した突進／弾から追加ダメージなし。次攻撃は通常命中 | 消費状態と各hurt |
| B8 | 非致死スワイプは全フェーズでHPだけ1減り、時刻・照準・状態不変。予兆中は継続文言。致死なら新発動なし | スワイプ前後状態と表示 |
| B9 | 回復中に接触しても無傷。開始から射程内・正面なら少なくとも4回の攻撃が成立。回復時間1.2／1.4秒 | 攻撃・HP・フェーズ時刻 |
| B10 | 接触帯の内側・外側・上端を各攻撃で確認。帯外は両FPSで同じ結果、帯内だけ許容差 | 実軌道の横ずれと接触距離 |
| T1 | 最後の敵撃破後に残弾を残す。クリア確定後は弾消去、追撃死なし、操作拒否 | 終端前後とその後2秒の状態 |
| T2 | ボス致死スワイプと既発射弾の致死接触を同フレームで成立させると死亡のみ。生存なら勝利のみ | 同フレーム結果、終端イベント数 |
| T3 | 勝利／死亡後に2秒分stepと戦闘入力を与えても戦闘状態・ゲーム時刻不変 | 終端状態比較 |
| T4 | 勝利と死亡の各々からretryし、初期状態が新規通常ランと一致。旧未来入力・予約攻撃・メッセージは再発しない | 試行番号、初期状態、入力列 |
| C1 | 部屋時刻は毎入場0、ラン時刻は連続。境界1秒はランだけ進む | 両時刻の列 |
| C2 | 予兆・ダッシュ・保護・部屋間表示の各途中でpause。外部経過2秒を挟んでも各残時間不変、再開後に通常継続 | pause前後とresume後状態 |
| C3 | 戦闘中のlimit到達はunfinishedで勝敗なし。勝利／死亡同フレームではその結果が記録される | 終了理由と勝敗の別字段 |
| V1 | §6の各表示がplayer viewだけで読め、変化フレームに出る。短射の予兆と実弾、回復終了を取り違える文字列なし | player出力と状態の照合 |
| V2 | キーボード／ゲームパッドで移動・攻撃・ダッシュ・pause・終端retryが同じ状態遷移を生む | 実機経路の同等操作記録 |

V2をheadless scriptのみで合格にしない。実機入力経路が未実装なら未検証／依存として明記する。

共有回帰はcombat.md基準1〜11、17〜21、step68のvariant文字列・runner kill解釈、step72 R3-1〜R3-10、step94 W1〜W8を対象にする。第5部屋固有部分と既存の既知ギャップは§8に従う。既存テストのgreenだけで新しい連続ランを合格にしない。

## 8. 旧基準とDecisionの対応

D-019で以下を確定する。「保持」は該当する独立部屋／共有挙動で保持する意味であり、通常ランのhearts合計へ置き換えない。「適用終了」はG-002新構成に限る。旧Decision本文と過去G-001の判断・結果は保存する。

| 出典・対象 | 扱い | 置換先・理由 |
|---|---|---|
| combat.md Rooms、12、test_rooms_match_the_spec | 第1〜4部屋保持、第5部屋置換 | 旧5番ブルート位置のassertをB(12,4)、HP12、1体の確認へ置換。R2／B1。単体ボスへの構成変更による |
| step72 R3-1の「rooms 1,2,4,5 unchanged」 | 第5部屋だけ適用終了 | 新5番はB1。他のR3-1〜R3-10と第1〜4部屋は保持 |
| combat.md1〜10、19〜21、D-001／D-004／D-005 | 保持 | 既存敵・プレイヤーの共有回帰。ボスの明示適用は§3、B5〜B9 |
| combat.md11／18、step46、CueGapTest | 第4部屋と共有試験保持、旧5番依存を置換 | 4番の初射・実部屋gap・強制同時射撃・cap遅延等を保持。5番の旧spitter試験はB2／B4へ。ボスはspitter gap調停に参加しない |
| D-002／D-003、combat.md17／16e | 保持＋ボスへ明示適用 | §3／B10。帯内の命中差だけを許容し、時刻・表示・フェーズは免責しない |
| D-006、step44の13a／13b | 新構成への適用終了 | walker独立3〜5合計3〜7 hearts、2/3 clear、構造上限7を新ボス・連続ランへ移さない。独立3・4の部屋別報告、ボス対処試験、独立Playへ接続 |
| step44の13c | 新構成への適用終了 | dodgerのwalker比1/2以下・3/3 clearを終了。母集団変更のため。新しい比率・clear数は未設定 |
| step44の13d | 新構成への適用終了 | camperのclear数がwalker未満という旧比較を終了。独立3・4の両者成績は引き続き報告 |
| step44の13e／13f、Reporting rule、Revisit、What QA re-verifies | 旧集計部分の適用終了 | 旧FPS別集計、旧逸脱報告・再計測手順、過去実測値を新構成のゲートにしない。両FPS別の新報告と下記再判断へ。過去記録は保持 |
| combat.md14、step44の14保持注記 | 保持 | 独立1〜2、各FPS別にwalker合計1以上、dodger合計1以下・両方clear。walkerのclear義務なし。brute対応方針も保持 |
| combat.md15、step44の15保持注記 | 独立3・4保持、5番置換 | 3・4は各FPSでdodger dash1回以上。0ならDesigner報告、使用を強制する変更はしない。5番は両攻撃の実接触を伴うB6で有効性を確認。B5と独立Playも保持 |
| combat.md16a／16b | 適用対象を更新 | 保持した共有基準と14／15を両FPSで確認。終了した13の旧集計を16b経由で復活させない。新仕様§7も両FPSで確認 |
| combat.md16c、BotsTest.test_dodger_agrees_at_30_and_60_fps | 独立1〜4保持、5番置換 | 新5番はボス対応dodgerで同じclear結果・hearts lost差1以下を採択。下記条件を必須とし、難度評価の代用にしない |
| combat.md16d／16e | 保持 | walker成績の一致は要求しない。bot時刻感度と規則違反を区別し、共有ルールの差は免責しない |
| BotsTest.test_walker_meets_criteria_13_and_14_at_each_rate | 一部保持・置換 | 旧13のwalker下限・clear数・dodger比率と3/3・camper比較を新構成から外す。14の1〜2 assert、15の3・4確認を保持。独立3・4報告と新5番比較・対処試験を追加する |
| その他BotsTest | 保持＋対応確認 | bot終了、ログ有無の結果一致、ログ観測、walker比較距離、brute wind-upへswipeしない試験を保持。新ボス対応とログの観測範囲を確認 |
| D-007、step46、SpitterTestのroom3 | 保持 | 一般上限は最大5。静止12秒最大3の試験だけでcap遅延の一般境界を合格にしない。player印＋直近spitによる観測法も保持 |
| step59→step68／D-011 | 保持 | step68が正本。runner通常HPはcancelではなくkill。variant文字列も保持 |
| step94、D-013／D-014 | 保持、一部経路置換 | 既存文字列・方向・prefixとW1〜W8を保持。W2の旧5番実spitter経路は4番とpracticeへ、新5番はボス短射の表示確認へ |
| D-013／D-014のG-001既知ギャップ・合格判断 | 保持 | 過去判断を変更せず、新機能への検証免除に拡張しない |
| 旧終端記述、manual、04の静的所見 | 新契約へ接続 | §4、T1〜T4。現行実装が満たすとの証拠ではない |

旧第5部屋fixtureの維持は必須ではない。使用するなら旧構成と明示した共有回帰に限り、新5番・連続ランの難度や合格を示すものにしない。テストの削除だけで完了とせず、上表の保持部分と置換先を追跡可能にする。具体的な試験構造はPlanに残す。

### ボスのFPS比較条件

同一ビルド、同一方針のボス対応dodger、同一初期位置・向き・戦闘状態、同一ゲーム時間limitで独立5番を30/60 FPS比較する。3 hearts開始と、連続ランで可能な2 hearts開始を別々に比較し、各対で同じclear結果・hearts lost差1以下を要求する。

対応botはplayer viewのB、攻撃名、固定方向・危険範囲、予兆、回復、実弾に基づき、反応間隔0.15秒で回避と反撃を選ぶ。未表示の将来状態を利用せず、非致死swipeで予兆を止める方針を使わない。両FPSで同一方針を使い、対応根拠と実際の判断ログをQAが確認する。独立1〜4の方針を変更する場合は影響を明示して回帰する。対応前の旧bot成績は比較の合格根拠にしない。

clear／death／unfinishedを区別する。一方のみunfinishedなら比較未完了として原因とlimitを再評価する。両方死亡またはunfinishedで数値が一致しても、攻略可能性の証拠にはしない。秒数差の追加閾値は設けず、各フェーズ時間はB1〜B10で検証する。

数値差は判断時刻・位置・照準・接触距離・消費・被弾のログで診断する。帯内接触差はB10の許容対象だが、比較閾値超過を自動免除しない。Designerへ戻して比較条件または基準の再判断を記録する。帯外の同条件差、時間・表示・フェーズの規則違反はQAの不合格対象とする。walker／camperには新たなFPS成績一致条件を置かない。

### 新評価への接続と実測後の判断

難度評価を未実施のまま基準整理だけで合格にしない。

- 独立3・4：各bot・各FPSで開始hearts、clear／death／unfinished、終了時heartsと損失、秒数、被弾源、攻撃・dash回数、limit、方針・ビルド識別を報告する。失敗や差があれば判断ログを添える。新しい合計数値ゲートは現時点で設けない。
- 独立5番：上記の3／2 hearts別FPS比較と、B1〜B10・V1で二攻撃の読み取り、横移動、dash、消費、反撃機会を確認する。独立Playで最終戦の体験を観察する。bot成績だけで手応えを合格にしない。
- 通常ラン：R1〜R5で正規敵を倒した連続到達、T1〜T4で終端とretry、C1〜C3で時刻・pause・limit、V2で実機入力を確認する。状態設定した境界試験は連続到達の代用にしない。
- 時間・到達体験：§9に従い同一試行のラン時刻、pauseを分けた実経過、部屋別時間、遷移、ボス入場hearts、被弾・反撃・再挑戦回数を記録する。完走と死亡・未完了を分け、試行数を明記する。独立部屋時間の合算は禁止する。

Planは、対応botと観測経路の整備後に両FPSの基線を測り、独立QA・独立Play後、Review前にDesignerへ返す経路を含める。初回基線で明白な対処不能や到達不能が見つかればPlay前にも返す。

Designerが実測後に判断する項目は、独立3・4のbot間比較に数値ゲートが必要か、新5番のhearts別clear・被害・反撃機会に追加ゲートが必要か、連続到達と回復・retry負担に調整が必要かである。報告された試行条件・件数と独立Playを根拠に、新Decisionと仕様更新、または追加不要の理由を記録する。今ここで成功率や秒数の閾値を推定しない。

Studioは未判断項目をReview前に再ルーティングし、適用整理完了と難度・体験の検証済みを区別する。15〜20分と整合しない場合は差と原因を報告し、HPや待機だけで合わせない。承認範囲内で解消できないVision不整合、承認超過の費用・リスク、Owner Decision変更はGame Directorへ戻す。独立QA、限定Art Verify、独立Play、Reviewは省略しない。Playtester資料に本節の期待結果や§9のReview用体験信号を転記しない。

### 仕様とテストの相違

- SpitterTestのroom3試験は、その静止プレイヤーの12秒実行で最大3をassertしている。D-007はcap遅延条件で最大5を許容する。特定入力で3以下という試験と一般上限5は必ずしも矛盾しないが、この試験だけではD-007の一般境界を検証できない。条件付きの確認として保持し、cap遅延の別試験を必要とする。
- BotsTestのコメントは旧上限6を説明し、上限assertを持たない。過去構成の正本はstep44／D-006の3〜7である。新構成での下限・clear数・関連比較の適用終了と置換先はD-019および上表で確定した。テスト実装の改訂は未実施。
- combat.mdの旧13の6という記載よりstep44が優先する。step72内の旧限界への言及も現行合否値ではない。
- D-007の11.7秒表記よりstep46のstep54補足が印刷画面による算定時刻を具体化する。旧Decision本文は編集しない。
- 04が指摘する残弾・終端のコード差は未実行。新契約を実装済みや現行不具合確認済みと扱わない。

## 9. 体験評価と時間

本Stepではplay／botsを実行していない。戦闘時間、連続到達率、実行成功、指定sha一致を示す数値はない。

HP12は既存スワイプ12回であり、理論上の4回反撃を3回成立させれば倒せる値として選ぶ。実際の反撃回数は接近と向き直しで減る。秒数の目標に合わせた値ではない。初期調整の判断は「2種類を学び、複数回の反撃へ戻れるか」で行い、秒数だけを理由に増やさない。

ボス単体の秒数ゲートは設けない。連続ラン15〜20分のVisionは保持し、実測が外れたら差を報告する。範囲内の調整で整合しない場合はGame Director経由でOwnerへ戻す。

計測は同一試行で第1部屋開始から勝敗確定までのラン時刻と、pauseを分けた実経過、各部屋時間、遷移時間、ボス初入場hearts、被弾・反撃回数、再挑戦回数を記録する。終端後表示時間は戦闘時間へ加えない。独立部屋bots時間の合算を連続ラン実測として扱わない。

Review用の体験信号。PlaytesterへのHandoffには転記しない。

- 予兆から、突進と短射のどちらかを説明できる。
- 回避後に攻撃する場所を選び、単に遠ざかり続ける以外の行動が見られる。
- 被弾理由を固定射線・突進・タイミングに結び付けられる。
- ボスを通常部屋とは異なる山場と述べ、同じ回答を長時間繰り返す戦闘と述べない。
- 道中の消耗と入場回復を理解し、ボスで試す余地があったと説明する。
- 死亡後に最初から戻ることと、再挑戦方法を迷わず認識できる。

これらが成立しない場合は読みやすさ→反撃位置と時間→継承・回復の順でDesignerへ戻す。攻撃追加や新フェーズは自動採択しない。

## 10. Planへ渡す依存

1. 指定sha `27fe16268ac8`との一致、実行対象、project.mdの0.4と他資料の0.6の差を同定する。
2. D-019と§8の確定した基準対応を試験計画へ反映する。旧集計の新構成への適用は終了した。独立3・4の両FPS別報告、ボス対応dodgerの条件確認・比較、実測後のDesigner再判断を計画へ含める。適用整理を難度検証済みと扱わない。
3. 単体敵の攻撃切替、進行、終端優先順位、入力・時刻・retryを実現・観測する方式と費用を評価する。
4. 現行60秒上限を超える連続player／traceと同一試行の計測経路を用意する。必要長は実行結果とVisionの双方から評価する。
5. pause／resume、終端retry、モードと時刻基準、再試行用入力列の具体的な公開構文を確定しmanualへ反映する。
6. ボス対応botsを試験道具として明示する。対応前の成績を難度判断へ使わない。
7. Desktop実機入力の現状・対応範囲・独立検証経路を提示する。headlessビルドで実機対応済みと扱わない。
8. player表示、重なり、イベント発火の実現性とArt Directorの限定Verifyを計画する。
9. 通常到達の長時間証拠と、同時勝敗等の制御された境界試験を両方可能にする。
10. 承認された案Aを超える費用・リスクがあればBuild前に具体的影響をStudioへ返す。

実装順序、コード構造、人日見積もりは本仕様では決めない。独立QA、独立Play、Reviewを省略しない。
>>>END

<<<FILE goals/G-002-final-boss/18-game-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 18
from: game-director
to: studio
stage: Plan
outcome: done
---
# 18: game-director → studio — 最小ホストの位置付けとPlan補完・Build保留条件

## Task

D-020に従い、Technical Directorへ限定したPlan補完をルーティングする。実行基線、回帰正本、実機環境の供給、費用承認の根拠を揃え、解決できないOwner権限の問題は具体化してGame Directorへ戻す。

## Context

OwnerはD-015で連続ラン、第5部屋の単体ボス、ラン先頭からの再挑戦を承認した。16の技術計画は提出済みだが、実行基線・実機環境・費用が未確認で、Buildは開始していない。

本Stepは承認範囲の解釈と次の調査条件を決めた。技術方式、詳細仕様、実装、検証の代行はしていない。

## Findings

### 承認範囲の判断

D-020を採択した。desktopのkeyboard／gamepadは既存要件であり、その操作・表示に必要な最小ホストをPlanで検討することは、Goalの追加ではない。ホスト新設の必要性と、費用・リスクの承認は別に判断する。

16のBuild準備〜統合11.5〜20人日にはホスト2〜4人日が含まれる。独立QA 2〜3、限定Art 0.5〜1、独立Play 1〜2を加えると提示済み部分は15〜26人日である。これは確約でも総費用でもない。Designer判断、修正・再検証、機器・ライセンス等の金銭費用は未算入または未確認で、予算上限もない。

現時点で承認超過・環境供給不能が確定したとは判断しない。OwnerへのEscalationはまだ作らず、無条件のBuild許可も出さない。

### 次のPlan補完で取得する最小の証拠

| 項目 | Technical Directorが確認する事項 | Roleで解決できない場合の返却内容 |
|---|---|---|
| 実行対象 | gitルート、対象commit、指定sha `27fe16268ac8`との関係、作業差分の有無、0.4／0.6表記の由来 | 必要なcheckout・資料・権限と、取得できない理由 |
| 実行基線 | Python版・既存依存、既存tests、player／trace、各botの30/60 FPS結果。実行条件・終了理由・失敗を記録 | 利用可能な実行経路と不足。静的所見を実行済みにしない |
| 回帰正本 | combat.md、step44、step46、step68、step72、step94、関連Decisionと実テストを読み、保持／終了／置換先を照合 | 未提供の正本を特定。未読を不存在としない |
| 実機環境 | 利用可能なdesktop OS・表示環境、keyboard／gamepadの種類、既存依存、導入権限、独立検証担当・利用条件 | 必要なOS・機器・権限・検証枠、既存資源で代替できない理由 |
| ホスト計画 | 共通Sessionへの接続、実機入力・表示・記録、保持入力解除、30/60 FPSと実時間pause確認の実現方式 | 最小方式でも残る制約・リスクと代替案 |
| 費用・承認 | 環境確認後の見積もり、前提・除外・不確実性、独立検証・Designer判断・修正枠、金銭費用の有無、既存承認との対応 | Ownerに承認を求める具体的な幅・必要物・未確定部分 |

既存資源の調査と、新たな供給の確約を分ける。OS、機器、予算上限、導入権限をRoleが推定・創作して埋めない。既存の権限内で確認できればOwnerへ質問する必要はない。購入、追加予算、権限付与、Roleでは確保できない検証環境などが必要なら、供給権限を持つ相手を特定する。

### 返却条件とBuild保留解除

Plan補完は、各依存について「確認済みの証拠」「残る不足」「解決する担当・経路」を示して返す。実行不能なら、不能の証拠と必要な供給物を返すことで調査結果とするが、開始条件の充足にはしない。

BuildはD-020の五条件がすべて解決した後にStudioが開く。特に、予算資料がないまま見積もりを承認内と認定しない。既存承認だけで費用・リスクを判断できなければ、環境確認済みの最小案と見積もりを添えてGame Directorへ戻す。

Owner権限の問題が具体化した場合は、次のEscalationを作れる形で返す。

- 一つの判断対象：必要な供給・費用を伴う現行仕様の継続を認めるか。
- 必要な機器・OS・依存権限・独立検証枠、費用幅と未確定部分。
- 供給して継続、必要なら追加調査、範囲変更、停止のうち現実的な2〜3案と各ルート。
- 推奨と、その推奨を変える証拠。

範囲変更はOwner判断後にDesigner／Technical Directorへ戻す。V2を任意化したり、headlessのみで満たした扱いにしたりしない。

### 証拠の限界

本Stepは提供パケットのみを使用し、play／botsを実行していない。指定sha一致、実行成功、実機供給、難度、時間の新しい証拠はない。

make-decisionとprepare-owner-escalationが参照するstudio/orchestration.mdはパケットに含まれていない。D-015と17に明記された承認超過・Owner権限の境界で判断した。Studioは次のLoadへ同文書を追加し、他の適用トリガーがあればBuild前に解決する。

## Decisions already made

- D-015：連続ラン、第5部屋単体ボス、先頭retryをOwnerが承認。承認超過は実装前に戻す。
- D-016：読み取り、位置取り、回避後の反撃を優先し、既存部屋・共有規則と再利用方針を維持。
- D-017：ボス・ラン・入力・表示・終端の詳細契約。実機入力と長時間検証はPlan依存。
- D-019：旧集計の適用整理、保持回帰、ボス対応bot比較、Review前のDesigner実測後判断。
- D-020：最小ホストを既存要件の実現作業としてPlanで検討する。費用承認は未確定。限定調査へ返し、開始条件の充足までBuildを保留。

## Constraints

- Owner request、Interpretation、D-015〜D-019、詳細仕様を変更しない。
- 技術方式はTechnical Directorが選ぶ。本判断はSDL系その他のライブラリを指定しない。
- 次Stepでゲーム・ホストの実装、新規依存導入、購入、外部費用の確約を行わない。
- 秘密情報、環境変数の値、個人情報を調査記録へ含めない。
- 過去Decision、G-001の結果、project.mdのCurrent stateを変更しない。
- Plan補完→Build→独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。明白な対処不能・到達不能はPlay前でもDesignerへ戻す。
- 追加難度ゲートの未設定はD-019による実測後判断であり、それ自体をBuild阻害へ追加しない。

## Open questions

1. 実行対象・指定sha・Python基線・版表記の差を、どの証拠で確定できるか。
2. 利用可能なOS・機器・導入権限・独立実機検証枠でV2と実時間pause確認を実施できるか。追加供給が必要なら何か。
3. 環境確認後の見積もりと残る不確実性は何か。費用・リスクを既存承認内と判断する根拠はあるか、Ownerの具体的承認が必要か。

## Expected output

StudioはD-020を記録し、Technical DirectorへPlan補完をルーティングする。次のLoadには16の既存Loadに加え、D-020、studio/orchestration.md、未読の回帰正本step46・step68・step72・step94およびD-011〜D-014を、プロジェクト一覧の正確なパスで追加する。

Technical Directorの返却には、実行証拠、回帰対応、実機方式と供給条件、更新見積もり、承認根拠、各未解決依存とBuild開始可否を必要とする。取得不能の場合も必要物と解決経路を明記する。

Owner権限の問題が具体化したらGame Directorへ戻し、日本語の具体的なEscalationを準備する。それまではBuildを開かず、調査の完了と実装開始条件の充足を区別する。

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: studio/orchestration.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Project: goals/G-002-final-boss/16-technical-director-to-studio.md
- Previous handoff: goals/G-002-final-boss/17-studio-to-game-director.md
>>>END

<<<FILE decisions/D-015-owner-approves-continuous-run-and-final-boss.md
---
kind: decision
id: D-015
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-015: Owner approves Option A — continuous run and final boss

## Decision

Owner response, verbatim:

> 案Aで進めてください（Studio の推奨どおり、連続ランと第5部屋の単体ボス、ランの最初から再挑戦）。

Proceed with Option A in `goals/G-002-final-boss/06-game-director-to-owner.md`: connect rooms 1–4 to a standalone boss replacing room 5, include final victory and death, and allow retry from the beginning of the run. Do not add a boss checkpoint or combat inputs.

Preserve rooms 1–4 and shared attack, dash and enemy rules. The old room-5 composition and room-specific criteria dependent on it are replacement targets; this approval does not amend existing Decisions. Any conflict with those Decisions must be identified and resolved through the proper authority.

Do not expand the work into wholesale changes to existing rooms or enemy-HP inflation solely to meet the 15–20 minute vision target. If technical planning reveals scope beyond the approved option, return to the Owner before implementation.

This approves scope, not detailed combat design, tuning, state inheritance, terminal-state rules or technical architecture. The Game Director records the direction within this authorization; Design and Plan follow.

## Rationale

Option A preserves the requested experience of reaching a challenging boss at the end of a run. The Owner explicitly accepted the additional progression, ending and retry work described in the escalation.

## Alternatives considered

Option B would deliver a selectable standalone boss room without continuous progression. It limits immediate work but changes this Goal's success condition and cannot evaluate reaching the final encounter through a run. The Owner chose Option A.

## Revisit when

Planning reveals materially greater scope, cost or risk than Option A describes; implementation would require changing an existing Owner Decision or vision pillar; or the Owner changes the approved scope.
>>>END

<<<FILE decisions/D-016-final-boss-experience-direction.md
---
kind: decision
id: D-016
status: accepted
decided_by: game-director
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-016: 連続ランの最後に、読み取りと反撃の判断を問う単体ボスを置く

## Decision

D-015の承認範囲内で、G-002の体験方向と優先順位を次のとおり定める。

1. 第1〜4部屋を連続して進み、第5部屋の単体ボスに到達する。ボスを倒した最終勝利、死亡、ラン先頭からの再挑戦までを一つの体験として成立させる。選択式のボス戦だけでは本Goalの達成としない。
2. 最終戦の手応えは、脅威を読んで位置を選び、攻撃・ダッシュのタイミングを判断し、回避後に攻撃へ戻る過程から生む。既習の対処を活用しつつ、通常戦とは異なる山場として認識できることを重視する。
3. 優先順位は、危害と対処の読みやすさ、判断に応じた攻撃機会、連続ランからの難度接続と再挑戦の納得感、所要時間の調整の順とする。読みやすさは難度との交換条件にしない。
4. ボス到達時の消耗と回復は、前半の行動が意味を持ち、最終戦で対処を学び直せる余地を両立するようDesignで定める。HP継承や全回復などの具体的な方式は本Decisionでは選ばない。
5. 15〜20分のVisionは維持するが、未計測の現状からボスの秒数や時間割合を確定しない。時間合わせだけのHP増加、待機の水増し、既存部屋の全面改修は行わない。実測との差は後続の評価に残す。
6. 小規模チームとして既存システムの再利用を優先する。第6部屋、通常敵との同居、ボス専用チェックポイント、追加の戦闘入力は含めない。新たな成長・報酬システムや複数ボスへの拡張も今回の方向に含めない。

第1〜4部屋の構成と共有戦闘ルールは維持する。攻撃構成、数値、状態継承、回復、同時勝敗、残弾、終端後操作、時刻・入力契約はGame Designerが仕様化し、技術方式と費用・依存はTechnical Directorが評価する。

旧第5部屋の敵構成・配置と、それを前提とする部屋固有の受け入れ基準は置換対象である。ただし、本Decisionは既存Decisionを改訂しない。Designは旧基準の置換と既存Decisionとの衝突を分けて記録し、必要な変更を適切な権限へ戻す。

## Rationale

Ownerが承認したのは、通常戦を経て最終戦へ到達する連続ランである。単体ボスなら、複数敵の予兆競合を増やさず、位置取りと回避後の反撃を中心に山場を設計できる。

初回Designは、HPを増やすだけでは既存の回答を長く繰り返す懸念を示した。手応えの根拠を判断とその結果に置き、攻撃機会と被弾理由をプレイヤーが読み取れる方向を採る。

根拠は提供資料と静的調査であり、実行結果や体験評価ではない。指定shaとの一致、build表記の差、連続ランの所要時間は未確認である。

## Alternatives considered

- 選択式ボス戦だけに限定：D-015が選んだ到達体験を満たさない。
- 第6部屋への追加：戦闘量と調整範囲が増え、承認された第5部屋置換から外れる。
- 旧第5部屋の混成戦への同居：単体ボスの承認範囲から外れ、予兆と回避経路の競合も増える。
- HPや待機時間を増やして長さを確保：判断の深さを保証せず、時間目標だけを満たす調整になる。

## Revisit when

- Designで、既存Decisionとの具体的な衝突が判明した場合。
- Planで、D-015を超える規模・費用・リスク、Owner DecisionまたはVisionの変更が必要と判明した場合。実装前にOwnerへ戻す。
- 独立QAで読みやすさや共有戦闘ルールを維持できないことが判明した場合。
- 独立Playで、判断の違いが結果につながらない、最終戦が単調、到達時の状態が学習を妨げる、または再挑戦の負担が山場を損なうと観察された場合。
- 連続ランの実測が15〜20分のVisionと整合せず、承認範囲内の調整では解消できない場合。Visionを暗黙に緩和せずOwnerへ戻す。
>>>END

<<<FILE decisions/D-017-final-boss-and-run-contract.md
---
kind: decision
id: D-017
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-017: 二攻撃のボスと、1 heart回復を伴う連続ランの契約

## Decision

D-015／D-016の範囲内で、詳細を`design/final-boss-and-continuous-run.md`として採択する。未実装・未検証である。

- 第5部屋はHP12のボス1体。固定照準の突進と短射を交互に使い、非致死攻撃では中断しない。回避後に明示的な無害の回復時間を置く。
- 生存して第1〜4部屋をクリアすると1.0秒の表示後に次部屋へ進み、1 heart回復、上限3。位置・戦闘タイマー・旧部屋の危害・保持入力・予約攻撃はリセットする。
- 同フレームの最終結果は死亡を優先する。確定後の残弾ダメージと操作による戦闘進行はない。
- 勝利／死亡後のretryは第1部屋へ戻る。ボス用チェックポイントはない。
- 部屋時刻とラン時刻を分離し、pauseでは両方を停止する。実行limitは未完了であり勝敗ではない。
- ボスの同速度・同半径の突進／弾に、既存の接触判定・保護中接触消費と接触帯を明示適用する。他の新形状への包括的な許可ではない。
- player viewに攻撃名、固定方向、危険範囲、回復、HP、進行、勝敗、retryを表示する。

既存Decisionを改訂しない。特にD-006の旧3〜5部屋集計は本Decisionで廃止せず、対応と改訂提案を仕様§8に記録する。Studioによる判断経路の解決が必要である。

## Rationale

2種類の既習に近い危害なら、入力を増やさず、横へ避けて近くに残る利益と退避の安全を比較できる。短射の寿命を区切り、その後に回復することで反撃機会に残弾が混ざらない。

1 heart回復は道中の消耗を残しつつ、生存到達したボス戦を2または3 heartsで始められる。全回復や無回復より、道中の意味と学習余地を両立する初期案とする。

HP12は攻撃機会の回数から選んだ調整値であり、15〜20分に合わせる水増しではない。時間目標との一致は実測後に評価する。

## Alternatives considered

- HPの多い突進だけのボス：同じ回答の反復になりやすい。
- 多数の弾や通常敵との同居：読み取りの競合と検証範囲が増え、同居は承認外。
- 毎部屋全回復：道中の消耗を最終戦へ残さない。
- 回復なし：残り1 heartで到達すると学習余地が狭い。
- 最終撃破直後の残弾を継続：勝利表示後の死亡と部屋境界の不透明さを生む。
- D-006を暗黙に新ボスへ移植：旧独立部屋の成績と連続ランの評価を混同する。

## Revisit when

独立QAで契約の不整合、帯外のFPS差、表示の不足が判明した場合。独立Playで反撃へ戻れない、二攻撃が同じ判断になる、消耗や再挑戦負担が学習を妨げる場合。

Planで承認範囲を超える費用・リスク、実機入力や長時間検証の不足が判明した場合はStudioへ返す。15〜20分のVisionと実測が整合しない場合も、HPや待機だけで合わせずGame Directorへ戻す。
>>>END

<<<FILE decisions/D-018-legacy-balance-gate-transition-direction.md
---
kind: decision
id: D-018
status: accepted
decided_by: game-director
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-018: 旧第5部屋依存の難度集計を、新構成の評価から分離する方向を採る

## Decision

D-015／D-016の範囲内で、Designerの推奨する適用変更の方向を採択する。

1. D-006の旧独立3〜5部屋集計は過去構成の記録として保存し、新しい第5部屋および連続ランの合否ゲートから外す方向で進める。実際の適用変更はGame Designerが新しいDecisionに対象・範囲・維持事項を記録して確定する。本DecisionはD-006を改訂しない。
2. 独立3・4のwalker／dodger／camper成績は、30/60 FPSそれぞれで部屋別に報告する。旧集計から新たな合計下限・上限・クリア数を算出しない。追加の数値ゲートの必要性は実測後にDesignerが判断する。
3. 新ボスは仕様の攻撃・対処・表示の検証と独立Playで評価する。連続ランは実際の連続到達、継承、終端、再挑戦と同一試行の時間計測で評価する。旧fixtureや独立部屋成績の合算を、その代用にしない。
4. combat.md15のdash使用数、16cのFPS比較、関連BotsTestの置換はDesignerが詳細を確定する。botの使用回数だけで対処を強制せず、実際に対処が有効であることと体験上の判断を重視する。
5. 旧第5部屋fixtureの維持を必須成果にはしない。共有挙動の回帰に必要な場合の限定利用は妨げないが、新構成への適用を明示し、旧構成の合格を新構成の合格と呼ばない。

D-006の適用変更が確定するまでは既存基準が存続する。関連テストの削除だけで整合済みとは扱わない。DesignerのDecisionと仕様補足を完了してからPlanへ進む。

## Rationale

D-006は旧第5部屋を含む独立3部屋と各3 hearts開始を前提とする。新ボスと部屋間回復を含む連続ランでは、その集計の母集団と開始条件が変わる。旧数値の継承は難度の証拠にならず、D-006自身も部屋変更時の再計測を求めている。

旧記録を保存し、保持する回帰と新しい評価を明示的に接続する方が、過去の判断を失わずにD-015の第5部屋置換を実現できる。これはDesigner権限の評価基準の適用整理であり、Ownerが承認した体験・範囲やVisionの変更を要しない。

判断根拠は提供された仕様とDecisionである。実装、play、bots、QA、所要時間の実測は行っていない。

## Alternatives considered

- **旧集計を新ボスや連続ランへ継承する：** 敵構成と開始条件が異なり、数値の意味を維持できないため採らない。
- **旧第5部屋fixtureを必須で維持する：** 過去構成の再現には使えるが、新構成の難度評価にはならず保守が増えるため、標準方針にはしない。
- **新たな集計値を今ここで決める：** 実測がなく、詳細基準はDesignerの権限であるため採らない。
- **Ownerへ判断を戻す：** 現時点では承認範囲やVisionを変える必要が具体化していないため行わない。

## Revisit when

- Designerが、適用整理だけでは保持すべき共有ルールやOwner Decisionと両立できないと示した場合。
- 再計測または独立Playで、対処を学べない難度や到達・再挑戦の問題が判明した場合。
- PlanでD-015を超える規模・費用・リスクが具体化した場合。実装前にOwnerへの判断経路へ戻す。
- 連続ランの実測が15〜20分と整合せず、承認範囲内の調整では解消できない場合。Visionを暗黙に緩和しない。
>>>END

<<<FILE decisions/D-019-g002-balance-criteria-applicability.md
---
kind: decision
id: D-019
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-019: G-002新構成における旧集計の適用終了と代替評価

## Decision

D-018の方向に基づき、D-006、正本step44、combat.mdの関連基準の適用を次のとおり変更する。本DecisionはG-002の新第5部屋と連続ランに限定した適用変更であり、D-006本文、過去G-001の判断・結果、旧構成に対する基準は変更しない。

1. 新構成には、step44基準13a〜dのwalker独立3〜5合計3〜7 hearts・2/3 clear、dodgerのwalker比1/2以下・3/3 clear、camperのwalker未満clearを適用しない。13eの旧集計に関するFPS別判定と、13fの過去実測値も新構成の合否根拠にしない。旧集計の逸脱に関する再判断条件は新構成へ移植しない。
2. 第1〜4部屋の構成、共有戦闘ルール、独立部屋の3 hearts開始を保持する。combat.md14の独立1〜2比較は30/60 FPSそれぞれで保持する。独立3・4はwalker／dodger／camperの部屋別・FPS別成績を報告し、新たな合計下限・上限・clear数・bot間比率を旧値から算出しない。
3. combat.md15は独立3・4で保持する。各FPSでdodgerのdash1回以上を確認し、0回ならDesignerへ報告する既存規則も保持する。使用を強制するためcapやgapを変更しない。新5番は使用回数条件を終了し、仕様B6の実接触による無傷・攻撃消費・終了後の追加被害なしを、突進と短射それぞれ、両FPSで検証する。B5の横移動も保持し、dash必須戦にはしない。
4. combat.md16cと対応BotsTestの独立1〜4のdodger比較は保持する。新5番にも「同じclear結果、hearts lost差1以下」を採択する。ただし下記の対応条件を満たすボス対応dodgerによる独立試験に限る。これはFPS比較であり、ボスの難度や到達可能性の合格基準ではない。
5. 新5番比較は、同一ビルド・同一bot方針・同一初期状態・同一ゲーム時間limitを使う。独立標準開始は3 heartsとし、連続ランで生じる2 hearts開始も別対として試験する。開始heartsを混ぜて比較しない。両FPSで終了理由をclear／death／unfinishedとして区別し、一方のみunfinishedの場合は比較を未完了として再調査する。両方unfinishedでも攻略の証拠にはならない。
6. ボス対応dodgerはplayer viewで読めるB、攻撃名、予兆の固定方向・範囲、回復、実弾を根拠に行動する。未表示の将来状態を使わず、非致死スワイプによる中断を前提にせず、回避後の反撃へ戻る。反応間隔0.15秒と方針を両FPSで共通にする。対応確認前の数値は診断資料に留め、比較をpassにしない。独立1〜4の既存方針は保持し、変更が必要なら影響と回帰を明示する。
7. FPS比較の不一致はログと制御入力で原因を分ける。帯内接触だけによる命中差にはD-017の許容を適用するが、bot比較の閾値を自動的に緩和しない。閾値超過はDesignerへ戻す。帯外の同条件差、フェーズ・表示・時間の不一致はQAが規則違反として扱う。walker／camperに新たな成績一致条件は設けず、bot時刻感度を共有規則の違反の免責にしない。
8. 旧第5部屋fixtureは必須にしない。残す場合は共有回帰専用と明示する。新評価は仕様B1〜B10・V1、通常ランR1〜R5・T1〜T4・C1〜C3・V2、独立Play、同一試行の連続ラン時間計測へ接続する。

追加の難度数値ゲートの要否は、対応botの両FPS成績とログ、独立QA、独立Play、連続到達・終端・時間の実測後にDesignerが判断する。StudioはReview前にその再判断を必ずルーティングする。追加不要の場合も理由を記録し、未判断のままGoal達成へ進めない。詳細は仕様§8による。

## Rationale

旧基準は旧第5部屋を含む独立3部屋と各3 hearts開始に依存する。単体ボスと回復付き連続ランでは、集計の母集団と開始条件が変わり、旧数値から難度を推定できない。

dashの価値は実接触に対する有効性と独立Playで評価できる。使用回数を強制すると、有効な横移動を不当に罰する。

ボス対応dodgerの数値比較はFPSによる大きな挙動差を検出する補助ゲートとして採る。両FPSで死亡する同一結果も通り得るため、攻略可能性や体験の代用にはしない。

## Alternatives considered

- 旧集計を新5番または連続ランへ継承する：開始条件と敵構成が異なるため不採択。
- 独立3・4へ比例配分した新数値を置く：実測上の根拠がないため不採択。
- 新5番でもdash1回以上を強制する：対処の有効性と使用頻度を混同するため不採択。
- ボスのFPS比較を設けない：共有規則試験だけでは対応botの戦闘全体の差を見落とすため不採択。
- 旧fixtureを必須維持する：新構成の難度証拠にならず、必須成果にはしない。

## Revisit when

対応botのFPS比較が閾値を超える、対処が有効でも反撃へ戻れない、道中で到達が妨げられる、回復やretryが学習を妨げる場合。

追加数値ゲートの判断に必要な実測が揃った場合。15〜20分との不整合を承認範囲内で解消できない場合、または承認を超える費用・リスクが判明した場合は、StudioからGame Directorへ戻す。

本Decisionは適用整理の完了を示す。実行成功、指定sha一致、難度、体験、所要時間の検証済みを示さない。
>>>END

<<<FILE decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
---
kind: decision
id: D-020
status: accepted
decided_by: game-director
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-020: 実機ホストの必要性を認め、費用・供給条件を限定調査で確定する

## Decision

D-015／D-016とproject.mdのdesktop・keyboard／gamepad要件に照らし、承認された連続ランを実機で操作・表示するための最小ホストは、Goalを追加するものではなく、既存要件を実現するための作業としてPlanの検討対象に含める。

ただし、この判断はホスト新設の費用・リスクがD-015の承認内であるとの認定ではない。具体的ライブラリ、OS、機器、依存、構造はTechnical Directorが評価する。グラフィカル素材制作、対応プラットフォーム拡張、ゲーム内容の追加を承認しない。

次はTechnical DirectorのPlan補完へ返す。許可するのは既存資料・実行環境・利用可能資源の確認と計画の補完であり、ゲームやホストの実装、依存の新規導入、機器購入、外部費用の確約は含めない。実行権限や資料が足りなければ、その不足を具体的に返す。

Buildは保留する。解除には以下をすべて必要とする。

1. 対象commit、指定shaとの関係、Python・依存、実行基線、版表記の差を記録し、未解決事項の影響を整理する。
2. 保持・置換する回帰正本を読み、D-019と仕様の試験対応を補完する。
3. 実機ホストの対象環境、実現方式、依存導入権限、keyboard／gamepad機器、独立実機検証の供給元と利用条件を確認する。V2の合格はBuild後の独立QAで判断する。
4. 実機ホスト、統合、独立QA・Art・Play、Designer判断、修正・再検証を含む費用・リスクを、確定部分と未確定部分に分ける。
5. 費用・リスクを承認内と判断できる根拠を示す。既存承認との照合で判断できなければ、必要なOwner承認を具体化して実装前に戻す。

現時点では、承認超過またはOwnerしか供給できない環境の必要性は確定していないため、OwnerへのEscalationは作らない。予算不明を承認内とも超過とも扱わない。

## Rationale

実機入力は既存のプロジェクト要件であり、D-017のV2にも残っている。headlessだけへ縮小する判断はできない。一方、必要な手段であることだけでは、その追加費用や調達リスクまで承認済みとはいえない。

16の11.5〜20人日は実行基線未確認の暫定値である。別枠の独立QA・Art・Playを加えた提示済み部分は15〜26人日だが、Designer判断、修正・再検証、機器・ライセンス等の金銭費用は含まれていない。総額や承認上限との関係を確定する証拠にはならない。

限定調査によってRoleで取得できる証拠を先に揃えれば、Ownerに必要な判断を一つの具体的な問いとして提示できる。

## Alternatives considered

- 直ちにBuildを許可する：実行基線、実機検証の供給、費用承認の根拠が不足している。
- ホスト新設という理由だけで直ちにOwnerへ戻す：既存要件の実現手段であり、新設だけでは承認超過を示さない。必要物・調達条件も未特定である。
- headlessだけで完了する：desktop実機要件とV2を満たさず、仕様を暗黙に緩和する。
- 予算上限がないため見積もりを承認内とする：D-015の範囲承認を費用の無制限承認へ拡張するため採らない。

## Revisit when

最小ホストでも新たな調達・権限・外部費用が必要と判明した場合、既存資源で独立実機検証を供給できない場合、費用承認の根拠を取得できない場合、またはD-015を超える範囲・費用・リスクが具体化した場合。

限定調査が資料・実行権限の不足で進められない場合も、同じ未確認事項を繰り返さず、必要な供給物と回答者を示してStudioへ返す。
>>>END

<<<FILE goals/G-002-final-boss/20-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 20
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 20: technical-director → studio — 回帰対応を補完し、実行・供給・費用承認の不足を返す

## Task

Studioは本報告を受け、Game Directorへ「必要な供給・費用を伴う現行仕様の継続」の判断準備をルーティングする。実行可能なcheckout、desktop実機環境、独立検証枠、費用承認の根拠が揃うまでBuildを保留する。

## Context

D-015〜D-019で連続ラン・単体ボス・先頭retryと詳細契約・基準適用は確定している。D-020は最小実機ホストをPlan対象に含める一方、実装・依存導入・購入を許可せず、五条件の解決までBuildを保留した。

本Stepでは提供された回帰正本と実テスト本文を照合した。実行環境への確認経路を試したが利用できず、実ファイル・git・Python・機器の確認には至っていない。調査報告の提出とBuild開始条件の充足は別である。

## Findings

### 1. 取得できた証拠と取得不能の範囲

環境確認に使えるshell・ファイル読取等のツールを探すため、`functions.exec`から利用可能ツールのメタデータ取得を試した。応答は`code-mode host is disabled`であり、ツール列挙自体が実行されなかった。shellコマンド、ファイル読取、Python実行は開始できていない。これは本executorの経路の制約であり、プロジェクト全体の資源不存在や供給不能を示さない。

実行環境の権限設定はread-only、ネットワーク制限、権限昇格不可である。read-only自体がPython実行不能を意味するとは判断しない。今回の直接の障害は利用できる実行ツールを取得できなかったことである。ゲーム変更、依存導入、購入、外部連絡は行っていない。

| 調査項目 | 確認済み | 残る不足・影響 |
|---|---|---|
| 実行対象 | パケットの対象表記は`repo/`、指定shaは`27fe16268ac8` | gitルート、HEAD、指定shaとの一致・祖先関係、差分の有無は未確認。実行結果を特定commitへ帰属できない |
| Python・依存 | 提供ソースのimportは標準ライブラリとローカルモジュール | Python版、インストール済み依存、追加の依存定義は未確認。新ホスト用ライブラリの導入済み証拠はない |
| tests | `repo/tests/test_game.py`の全文を静的照合 | 実行未着手。成功件数・失敗件数・実行時間は取得していない |
| player／trace | README・manual・play.pyから既存実行方法と60秒上限を確認 | 両viewとも未実行。終了後の挙動を不具合として再現確認していない |
| bots | 全bot、30/60 FPS、独立部屋・3 hearts・既定limit60の経路を確認 | 全bot×全室×両FPSは未実行。clear／death／unfinished、秒数、損失等の新測定値はない |
| 版表記 | project.mdは0.4、README・manual・game.py・player bannerは0.6 | combat.mdは0.4以降の変更経緯を記す。ただし対象checkoutの履歴を確認できず、表記差の原因・修正漏れは確定できない |
| desktop・機器 | 既存要件とV2を確認 | OS、表示サーバー、keyboard、gamepad、ドライバー、利用条件は未確認 |
| 独立検証 | QA→Art→Play→Designer→Reviewの必要性を確認 | 担当供給元、機器利用枠、費用、独立性を保つ実施条件は未確保 |

過去DecisionのQA成功記録や旧bot値は履歴として保持するが、今回の実行基線には転記しない。環境コンテキストにある作業ディレクトリもgitルートの確認済み証拠にはしない。

### 2. 実行基線を取得する具体的な経路

Studioはまず実行基盤の管理者またはrepository管理担当へ、次を供給する経路を確認する。人物名・供給権限者はパケットにないため特定できない。Studioが担当を割り当て、Role内で確保できなければGame DirectorがOwnerへまとめる。

1. 読取・実行可能な`repo/`のcheckoutとshell、Python3。指定shaのobjectと、差分確認可能なgit情報を含める。
2. 対象commitと指定shaの一致／差異、作業差分の有無を記録する。差分本文・remote URL・環境変数値を一括出力しない。秘密情報を含み得るファイルは内容を開かない。
3. READMEどおり、`repo/`で`python3 -m unittest discover -s tests`を実施する。read-only環境ではbytecode生成を抑止する等、ソースを変更しない実行方法を選ぶ。
4. manualの既存構文だけで、両FPSのplayer／traceを実行する。最小例は`room empty`、`spawn grub 10 4`、`spawn spitter 1 1`、`end 5`にFPS指定を加えたものとする。CLIは既存`play.py --view player|trace SCRIPT`に従う。scriptを保存できなければ既存parserとplay関数へメモリ上で同じ文字列を渡し、その経路を明記する。
5. botsは既存`bots.py`のscriptで全bot・rooms1-5・limit60を両FPSで実行する。出力の`NOT cleared`だけでは死亡とlimitを区別できないため、既存`play_room`の戻り値の損失から終了heartsを確認し、clear／death／unfinishedを別に記録する。観測用呼出しとCLI実行を区別する。
6. 失敗、実行不能、未着手を分ける。commit、FPS、script、limit、終了理由、結果を対応付ける。必要時は既存`log on`で判断・被弾を診断する。

この順序は将来の実施手順であり、実行済み記録ではない。基線取得後に予想外の既存失敗があれば影響と見積もりを更新する。

### 3. 回帰正本と実テストの対応

今回、combat.md、step44・46・68・72・94、D-001〜D-007、D-011〜D-020、および提供test_game.pyを読んだ。16の「回帰正本未読」は解消した。基準の適用関係に新たな仕様衝突は認めないが、既存suiteは全基準を網羅していない。

| 正本・Decision | 実テスト本文との照合 | G-002での保持・終了・置換と試験先 |
|---|---|---|
| combat1〜10、19〜21、D-001／004／005 | CombatTest、GrubTest、BruteTest、SpitterTest、DashTest、InvulnerabilityTest、ShotContactTest、LungeContactTestが関連 | 共有ルールを保持。既存試験が片FPSだけの箇所や限定条件は独立QAで補完。ボスはB5〜B9へ明示適用 |
| combat12、Rooms、step72 R3-1、D-012 | `test_rooms_match_the_spec`は2・3・4番と旧5番brute位置を確認。1番の完全配置assertはない | 1〜4番を完全照合するR2へ補完。旧5番assertはB(12,4)、HP12、1体のB1へ置換 |
| combat11／18、step46、D-007 | CueGapTestに4・5番の実部屋、強制同時、取消、cap遅延。room3静止12秒は最大3をassert | 4番・共有試験を保持。新5番にspitter試験を空適用せずB2／B4へ置換。room3一般上限5とcap遅延は別試験 |
| step46の11d、step68の訂正 | 静止12秒試験はplayer印＋spitイベントの算定検証ではない | 7.5秒・12.0秒の表示と直近0.3秒のspitを記録する経路を保持。D-007の11.7秒表記は正本補足に従う |
| combat17／16e、D-002／003 | 提供suiteに帯内外・上端の軌道比較を網羅する試験はない | 共有接触回帰を補完し、新ボスはB10。帯は命中・消費だけに適用 |
| step44の13a〜f、D-006 | BotsTestに旧下限、clear数、dodger比、camper比較が残存。コメントは旧上限6 | 新構成への適用終了。関連assertを単に削除せず、独立3・4のFPS別報告と新5番比較へ接続。過去記録は保存 |
| combat14、D-019 | 同BotsTest内に1〜2番のwalker損失、dodger損失・clearを確認するassert | 両FPSで保持。旧13の撤去に巻き込まない |
| combat15、D-019 | 同BotsTestは旧3〜5番のdodger dash回数を確認 | 独立3・4を保持、0回はDesigner報告。新5番は実接触を伴うB6、横移動B5へ |
| combat16c、D-019 | dodger比較は旧1〜5番を同列処理 | 独立1〜4を保持。新5番は対応確認済みbot、同条件、開始3／2 hearts別のFPS比較へ置換 |
| その他BotsTest | 終了、ログ有無の結果一致、観測字段、walker比較距離、brute方針を確認 | 保持。新5番とSession経路でもログが結果を変えないことを追加確認 |
| step68、D-011 | VariantMessageTestとReactionTestにvariant・共通prefix・manualの確認 | V-a〜V-eを保持。runner通常HPのswipeはkill。HPを増やしたrunner試験は共有cancel機構の試験であり通常個体の証拠とは区別 |
| step72 R3-1〜R3-10、D-012 | 配置と全敵死亡によるclearは明示試験あり。他は共有試験との組合せ | teaching schedule、初回grub cue≥4秒、cap遅延、最後のspitterへの経路等を個別追跡。共有suiteのgreenだけで全R3合格にしない |
| step94 W1〜W8 | ShotSourceTest、LateSwipeTest等は方向・一部表示・順序・非表示を確認 | 全文言とprefixを保持。W2旧5番spitter経路は4番・practiceへ、新5番はボス短射V1へ。未網羅のW3・W6・W7等は補完 |
| D-013／D-014 | 過去Goalの限定検証・既知ギャップを記録 | 過去判断は維持。新機能への検証免除に拡張しない。比較用の旧ビルドがない場合、byte比較を実施済みにしない |
| 新仕様R／B／T／C／V | 連続ラン、ボス、pause、retry、実機ホストの既存実装・試験は提供されていない | 16の全ID対応を維持し、新設する。R1の正規連続到達と境界fixtureを別証拠にする |

実装担当は変更報告に「正本・基準ID→旧assert→保持／終了／置換→新試験」を付ける。QAは両FPSで個別に判定する。未実施・既知ギャップも記録し、難度・体験の判断は独立PlayとDesignerへ返す。

### 4. 最小ホストの技術方式と供給条件

技術構造は16を維持し、共通Sessionへ接続する単一のdesktopウィンドウホストを採る。ホストは入力正規化、固定刻み駆動、公開player表示、操作・時刻記録に限定する。ゲーム規則をホストへ複製しない。

入力・表示基盤の第一候補はpygame／SDL系とする。ただし対象OS・Python・既存依存の互換性が未確認であり、ライブラリの確定・導入は保留する。新規依存の追加は本Stepで行わない。無条件に後続を拘束するライブラリDecisionは作成しない。

- 表示は既存の文字盤面と§6の情報をウィンドウに描画する。新しい素材制作は含めない。
- keyboardとgamepadの移動・attack・dash・pause・終端retryを共通actionへ渡す。軸閾値、対応機器、具体mappingは供給された機器で確定しmanualへ記す。
- 押下・解放、軸状態、正規化action、受理／拒否、Session通番を対応付ける。機器識別は検証に必要な非個人的情報に限定し、serialや利用者情報は記録しない。
- 境界・retry時は現在保持中の操作を遮断し、解放・軸neutral後の再入力で解除する。pause突入では保持移動を解除し、予約攻撃はSession内で凍結する。
- focus喪失・機器切断で保持移動を解除する。自動pause等の新たなplayer-facing behaviorが必要ならDesignerへ確認し、暗黙に追加しない。
- シミュレーションは30または60 FPSの固定刻み。実機の単調増加時計をdriver時刻に使い、pause中も入力イベントとresumeを処理する。処理遅延や追いつき実行は記録し、危険表示を見せずにゲーム時刻だけを進める挙動を合格にしない。
- C2は実時間2秒を挟んだ前後のSession状態で確認する。V2は独立QAが両入力・両FPSで実機操作記録と状態遷移を照合する。

供給に必要なのは、対象desktop OSと表示環境、対応Python、依存利用・導入権限、keyboard、実gamepadとドライバー、独立QA／Art／Playの利用枠である。OS・機器の種類や利用期間は未確認であり、全OS対応を約束しない。

既存desktop資源が見つかればその環境を優先する。pygame／SDLが利用できない場合は既存の別入力・表示基盤を調べるが、機器対応・保守費用を比較してから再選択する。terminalのみ、模擬イベントのみ、headlessのみではV2を充足しない。独自OS別gamepad層の新設は複数入力経路の保守・検証を増やすため第一候補にしない。

### 5. 順序・リスク・検証への引継ぎ

実装順は16の順序を維持する。

実行基線・資源確定→Game終端と観測→ボスと弾属性→Session境界・両時刻・pause・retry→parser／player表示／長時間trace／manual→対応botsと測定→実機ホスト→統合基線と独立検証資料。

コード作業は逐次とする。Game、play、bots、ホストが種別・時刻・観測契約を共有し、独立して変更できる境界がまだない。並列コード作業や隔離workspaceは開かない。

主要リスクと対処は次のとおり。

| リスク | 対処 |
|---|---|
| 既存の「grub以外はspitter」という分岐へボスが混入 | 種別を明示し、共有回帰とB試験を分ける |
| ボス突進に既存grubの命中時短縮が混入 | 通常命中・保護吸収・壁の全active時間をB3／B7で確認 |
| 境界とretryで入力・反応記憶が再発火 | Session入場処理を共通化し、R4／R5／T4と実機解放記録を照合 |
| pause後に止まったゲーム時刻のresumeが発火しない | 16の独立driver時刻を維持し、C2で実時間確認 |
| 長時間traceがメモリを圧迫 | 逐次出力と毎フレームtraceの選択。1200秒は初期測定limitであり合格閾値ではない |
| 未知のOS・機器・依存でホスト工数が増加 | Build前に対象と権限を限定し、互換性不足なら見積もりを戻す |
| bot一致を攻略・体験合格と誤認 | clear／death／unfinished、開始hearts、方針を分け、独立PlayとDesigner判断を必須にする |

統合後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewの順とする。明白な対処不能・到達不能はPlay前にDesignerへ戻す。Playtesterへの資料はStudioが起動・操作・記録方法から新規作成し、本報告の設計意図・期待結果・実装情報を転記しない。

### 6. 更新見積もりと承認根拠

環境・実行基線が未確認のため、16の作業見積もりを実測で精密化できない。以下は未算入部分を可視化するための計画用の幅であり、調達見積書・確約・承認済み予算ではない。

| 項目 | 人日 | 根拠・条件 |
|---|---:|---|
| Build準備〜統合 | 11.5〜20 | 16を維持。ホスト2〜4を含む。未知の環境対応は確定していない |
| 独立QA | 2〜3 | 既提示枠。対象desktopと実機が利用可能であることが前提 |
| 限定Art Verify | 0.5〜1 | テキスト表示の限定確認 |
| 独立Play | 1〜2 | 実施枠と記録条件の確保が必要 |
| 提示済み部分の小計 | 15〜26 | 総費用・承認額ではない |
| Designer実測後判断 | 0.5〜1.5 | 本Stepで追加した暫定計画枠。新規大幅設計を含まない |
| 修正・再検証の予備枠 | 2〜5 | 本Stepで追加した暫定枠。障害件数の予測や無制限修正の保証ではない |
| Review・引継ぎ整理 | 0.5〜1 | 本Stepで追加した暫定計画枠 |
| 計画上の合計 | 18〜33.5 | 上記仮定下のみ。供給確認後に再見積もりが必要 |

本Stepは経過作業時間を計測していない。既に消化した工数と残工数の精算も未確認である。

人日単価、通貨、税、機器・OS・ライセンス・外部担当の料金、配送や待ち時間は不明である。金銭総額や完了日を算出できない。既存資源の無償利用も確認していない。大幅な仕様再設計、追加OS対応、素材制作、予備枠を超える反復は上の合計に含めない。

D-015は範囲承認、D-020はPlan対象の整理であり、今回の人日・金銭・供給条件の費用承認ではない。既存承認との照合に使える予算上限・単価・配員枠がパケットにないため、承認内とも超過とも認定できない。費用承認根拠を取得できないという不足は具体化した。

### 7. D-020の五条件とBuild判断

| 条件 | 状況 | 解決担当・経路 |
|---|---|---|
| 1. commit・sha・Python・依存・基線・版表記 | 未充足。静的な表記差のみ確認 | Studioが実行基盤／repository管理担当を割当て、§2の実行証拠を取得。供給できなければGame DirectorからOwnerへ |
| 2. 回帰正本の読込みと試験対応 | Plan上は充足。本Step§3で未読を解消し対応を補完 | Buildがassert移行表を成果に含め、独立QAが検証。これは実行合格ではない |
| 3. 実機環境・方式・導入権限・機器・独立検証供給 | 一部のみ。方式を提示したが供給条件は未確認 | Studioがdesktop／機器管理担当と独立検証担当を確保。権限者不明・Roleで供給不可ならGame Directorへ |
| 4. 全費用・リスクを確定／未確定で分離 | 整理は実施。供給条件と金銭費用が残り、総費用確定には未充足 | Technical Directorが資源情報で更新、Game Directorが費用判断を準備 |
| 5. 承認内の根拠または必要Owner承認 | 未充足。根拠資料がなく承認内と判断できない | Game Directorが下記briefと予算・供給条件をまとめ、必要ならOwnerへ一問として提示 |

Build開始不可。本StepでBuildは開かない。追加難度ゲート未設定は阻害理由に含めない。

### 8. Game Directorへ戻すbrief

**判断対象：必要な実行・実機供給と費用を伴う現行仕様の継続を、どの条件で認めるか。**

orchestration.mdの「Roleで生成できない情報・資材による停止」と費用承認境界を照合した。ソース本文からcommit証拠、機器の利用権、独立担当の稼働枠、予算承認を生成することはできない。一方、既存資源の不存在や承認超過そのものは未確定である。

16と本Stepは同じ依存を未解決で返す形になるが、今回は回帰正本の読込みと利用可能経路の失敗という新情報がある。単純な「新情報なしのquestion二回」とは断定しない。ただし、同じパケットのまま三度目のPlan確認へ戻す経路は作らない。Studioは供給責任者の割当て、またはGame Directorによる具体的な供給・承認判断準備へ進める。

| 案 | 必要物・費用幅・未確定部分 | 後続ルート |
|---|---|---|
| A. 既存資源を指定して現行仕様を継続 | checkoutと実行経路、対象desktop、両入力機器、依存利用権限、独立検証枠、予算責任者の承認根拠。計画18〜33.5人日、金銭額・稼働日程は未算定 | 供給確認→基線・見積もり更新→五条件確認→Build。既存資源だけで足りると確認されるまで購入不要とは断定しない |
| B. 不足分の調達・権限付与を含めて継続 | Aの不足分について供給者、価格、導入権限、QA／Play条件を取得。18〜33.5人日に環境対応の増分が生じ得る。増分・調達金額は未確定 | Game Directorが具体的見積もり・上限・条件をOwner承認へまとめる。承認前は購入・導入・Buildを行わない |
| C. 供給・費用の確約までGoalを停止 | 実装費用を新たに確約しない。再開調査の工数・時期は別途必要 | Owner判断で停止・再開条件を記録。範囲縮小を望む場合はOwnerによるInterpretation判断後にDesign／Planへ戻す |

推奨はAの必要資源と承認根拠を具体的な責任者に割り当てて確認し、既存資源で不足する項目だけBへまとめること。これは実装開始の推奨ではない。供給者や費用根拠をRole内で得られない場合、Game Directorは「供給して継続／不足分を承認して継続／停止」を一つのOwner判断へまとめる。

推奨の再検討条件は、必要資源の調達価格・権限・利用枠が得られない、未知のOS対応で暫定工数を超える、またはOwnerが費用を受け入れない場合である。headlessだけへの縮小、V2任意化、独立検証省略はこのRoleで選べない。仕様変更の要望が出た場合はOwner／Game Director判断を経てDesignerへ戻す。

## Decisions already made

- D-001：戦闘入力はattackとdash。追加入力を設けない。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵のgap・非中断・保護中接触消費とroom3境界を保持。
- D-006：旧構成の履歴として保持。新構成への適用はD-019に従う。
- D-011／D-012：variant文言とroom3構成を保持。
- D-013／D-014：過去Goalの判断・既知ギャップを保存し、新機能への検証免除にしない。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017／D-019：詳細契約、回帰適用、対応bot比較、Designer実測後判断。
- D-020：最小ホストをPlan対象に含め、五条件解決までBuild保留。
- D-021は作成しない。ライブラリの環境適合性と供給条件が未確認であり、最終選択を記録できる段階ではない。

## Constraints

ゲーム・ホスト実装、依存導入、購入、外部費用の確約は行わない。Owner request、Interpretation、仕様、過去Decision、project.mdは変更しない。

秘密情報、環境変数値、個人情報を記録しない。実行ツールの不在をプロジェクト資源の不存在へ一般化しない。未実行を成功・失敗・再現済みと扱わず、headlessや模擬入力をV2の代用にしない。

逐次実装と独立QA→限定Art Verify→独立Play→Designer判断→Reviewを維持する。QAによる計画結果の独立検証を省略しない。

## Open questions

1. Studio／実行基盤・repository管理担当：指定shaを含むcheckoutと実行経路を供給できるか。§2の基線を取得する担当と条件は何か。
2. Studio／desktop・機器管理担当：対象OS、表示環境、keyboard／gamepad、依存権限、独立検証の供給元・利用枠は何か。
3. Game Director／予算権限者：暫定18〜33.5人日と未算定の金銭費用を照合する既存承認資料はあるか。なければ、どの供給・上限・条件をOwnerへ求めるか。
4. Game Director：既存資源確認で解けない場合、briefの継続条件または停止をOwner判断へまとめる。現時点でDesignerへの新規仕様質問はない。

## Expected output

Studioは本Stepの回帰対応補完を記録し、Build保留を維持する。次はGame Directorへ本briefを渡し、供給・費用承認の責任者と取得経路、必要なら一つのOwner Escalationを具体化する。

同じ不足だけを記したPlan質問を再発行しない。新しいcheckout・実行権限・資源情報・承認資料が揃った場合に限り、残条件の確認をTechnical Directorへ戻す。五条件がすべて解決した後、StudioがBuildを開く。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: studio/orchestration.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Project: goals/G-002-final-boss/16-technical-director-to-studio.md
- Project: goals/G-002-final-boss/18-game-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-013-review-pass-3-readability-wording-then-close.md
- Decisions: decisions/D-014-review-pass-4-goal-met.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Previous handoff: goals/G-002-final-boss/19-studio-to-technical-director.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/22-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
