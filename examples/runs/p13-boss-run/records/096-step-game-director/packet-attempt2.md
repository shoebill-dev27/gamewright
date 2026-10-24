# Studio operation packet

operation: Step
goal: G-002
role: game-director
incoming_handoff: goals/G-002-final-boss/77-studio-to-game-director.md
next_seq: 78
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}
context_request: used (the requested files are in Inputs)

## You may write

- goals/G-002-final-boss/78-game-director-to-<recipient>.md
- decisions/D-025-<name>.md
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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-002-final-boss/77-studio-to-game-director.md
---
kind: handoff
goal: G-002
seq: 77
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 77: studio → game-director — 予算超過後の残作業をOwner requestへ絞る

## Task

残作業を「最後に手応えのあるボス戦がほしい」に必要なものへ絞る。継続必須・省略可能な工程とその理由、終了条件を決定し、Owner Decision・Vision・Goal解釈の変更が必要ならOwner向けのエスカレーションを作成する。

## Context

Goalは80/40 operationsで予算超過。76で同じE1が連続partial 3回（72・74・76）になった。通常はTechnical Directorへ分割・再計画を戻すが、予算規則はそのループより範囲判断を優先する。Studioは内容上の省略を決めず、このStepを開く。予算はOwnerのResume以外では変更できない。

## Findings

- 製品の連続ランとボスは実装報告済みだが、独立QAの直近判定60はfailのまま。Goal達成のReviewはない。
- 76は再生互換診断と証拠helperの本文出力を保存した。runtimeはsource e99408d647c7、160 tests OKを報告した。必要な診断行の本文は未確認で、件数成功は受け入れ判定ではない。
- 実dodgerは旧判断経路を使い、非公開active残時間を参照する。公開境界prototype成功を実経路の適合には使えない。
- 公開境界接続、接続案の被弾差の原因確定、実経路の記憶・全分岐監査、判断列整備が残る。76は接続・互換診断・監査・証拠の4単位を提案しているが、方式は未決定。
- 従来計画68はE1の後に接触診断、ボス4条件再測定、保持回帰、通常ラン入力再生成、独立Q1〜Q6を予定する。さらに後続工程条件判断、限定Art Verify、独立Play、Designer実測後判断、Reviewが残る。
- D-024の歴史的確認不能は現行suiteで解消しない。対応前botの通常ラン時間約87／104秒は診断資料であり、対応後の基線やプレイヤー所要時間ではない。
- 新しい供給質問はない。追加環境、全文保存先、変更前ビルドは存在しない。

範囲判断の選択肢は、承認済み契約を維持して任意の重複作業・出力整備を絞ること、または必要な縮小がOwnerの承認事項に及ぶなら具体的な費用・範囲の選択をOwnerへ求めること。どの作業が削減可能かは本Stepが判断する。確認不足を合格に変える選択肢はない。

## Decisions already made

- D-019：公開情報限定bot、保持回帰、開始3/2 hearts別FPS比較、Review前のDesigner実測後判断。
- D-021：Studio内テキスト検証。独立QA・限定Art Verify・独立Playを別Stepで実施し、追加金銭を使わない。
- D-023：個別Load、@need一度最大8ファイル、@run最大3回、出力最大2万字。仕様・難度・Goal判断は変更していない。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離する。

## Constraints

Owner requestとInterpretationを変更しない。Owner-made Decision、Vision、予算の変更はOwnerへエスカレーションする。技術方式や詳細仕様、QAの合否を代行しない。

未確認・切断・未実行をpass、免除、適用終了へ変更しない。残りのplanned工程は本Stepの判断まで開かない。存在しない供給を再要求しない。

## Open questions

1. 承認済み契約の範囲で、Owner requestに必要な作業へ何を絞れるか。
2. 何を残し、何をskippedにできるか。その根拠と終了条件は何か。
3. 必須作業を維持すると追加の費用判断が必要か。必要ならOwnerが選べる具体的な選択肢は何か。
4. 歴史的確認不能を保持した後続評価の条件判断を、既存のplanned工程とどう整理するか。

## Expected output

範囲内で決められる場合はDecisionとstudio宛Handoffを作成する。残す工程・省略する工程・依存関係・終了条件を列挙し、未完了の技術課題を保持する。単に従来の全工程を再掲せず、削減できる作業と削減できない理由を明示する。

Owner権限が必要なら、日本語のEscalationを作成し、studioへ返す。供給事実を再質問せず、継続費用または承認変更について一つの決定を求める。Goal達成のReview verdictは今回の成果物としない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
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

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。

D-021により、今回はrepo/のテキスト表示とスクリプト実行で実装・検証する。Desktop、keyboard、gamepadは製品対象であり、実機ホストや実gamepadの供給・検証を今回の要件としない。基線はrepo/の現状とし、指定sha確認は不要。独立QA・PlayはStudio内の別Stepが担う。購入・外部委託・追加金銭を使わず、通常Stepの範囲で進める。具体的な追加支出や承認範囲を超える変更が必要になった場合はOwnerへ戻す。

## Unknowns

- Observe：skipped。既存不具合の再現依頼ではない。
- Diagnose：done。既存基盤の不足と計画上の回帰対応を整理済み。24に変更前のtests基線（69 tests、OK）が報告されている。
- Decide：done。D-015〜D-019で範囲・体験方向・仕様契約・旧基準の適用関係を確定。
- Design：done。design/final-boss-and-continuous-run.mdとD-017・D-019が正本。24では実装変更なし。変更後の検証は未実施。
- Plan：done。16・20の計画と回帰対応を使用する。D-021と衝突する実機ホスト・実機供給・外部配員・見積もり取得の要求は適用しない。
- Decide（供給・承認）：done。22へのOwner回答をD-021に記録。Ownerは実行経路とStudio内検証を指定し、Build開始を承認。実機供給、指定sha照合、人日見積もりは不要。
- Plan補完：skipped。新しいOwner条件を後続Stepへ直接渡せるため、同じ供給質問で再発行しない。具体的な技術上の不成立が判明した場合に限り戻す。
- Build：done。56でSplit Cを納品。runtimeの保存ソース04fa2b1c168aは全suite152件OK。pause/retry込み通常ランの同一試行計測、dodger独立1〜4の回帰固定、ボス判断ログを提出済み。報告された通常ラン勝利時間は30 FPS 86.967 s／60 FPS 103.533 s。履歴値との報告精度での一致と、変更前の厳密な同一性の未証明を区別する。Build証拠であり独立検証・体験判定ではない。
- Verify：未完了。60はfail。製品戦闘の再現済み不具合や同一基準の修正後再失敗2回とは扱わない。同じ不足のまま第三のQA依頼は出さず、D-023に合わせた基準整理・再計画・試験道具対応・再測定後に独立QAを再開する。全文保存先は存在しないため、検証対象を明示した出力と直列分割で必要な証拠を構成し、未確認を合格にしない。
- Plan（検証供給・試験道具）：done。62で公開情報だけのボス判断境界、接触診断、完全証拠保存、4条件再測定、独立1〜4回帰、変更前基線調査を計画。実行・修正・基線探索は未実施。仕様・難度・秒数ゲートは変更しない。
- Decide（検証供給）：done。D-023で案Aと供給上限を確定。Loadは個別ファイル本文、@needは一度8ファイルまで、@runはStepごとに3回まで、出力は最大2万字で全文保存先なし。変更前ビルドは存在しない。D-021のまま進める。
- Design（変更前一致）：done。65とD-024で、歴史的一致の確認不能、独立1〜4 dodgerの40の記録精度での比較、現行仕様照合・現行内対照を分離した。確認不能はpass・免除にせず最終Reviewへ残す。
- Plan（供給条件への適合）：done。68が62の実行計画を置換する。E0棚卸し→E1公開情報bot→E2接触診断→E3ボス4条件→E4保持回帰→E5公開再生→独立Q1〜Q6を直列実行する。各Step最大3回・各出力2万字以内、欠落は未確認。存在しない保存機構や変更前ビルドを前提にしない。
- Build（試験道具・再測定）：未完了・保留。76は同じE1の連続partial 3回目（72・74・76）。再生互換診断とhelper本文出力を保存し、runtimeはsource e99408d647c7の160 tests OKを確認した。実dodgerの公開境界接続、被弾差の原因確定、記憶・全分岐・判断出力は未完了。必要な診断本文は未確認。13ファイルのQA配布台帳と追加IDを76から継承する。E2以降は未着手。
- Decide（予算超過時の範囲）：open。80/40 operationsで予算超過。同じ作業のpartial 3回によるTechnical Director再計画より、予算規則のGame Director範囲判断を優先する。Owner requestに必要な残作業へ絞り、不要工程を明示する。Owner Decision・Vision・Goal解釈の変更が必要ならOwnerへエスカレーションする。
- Decide（後続工程条件）：planned。歴史的確認不能を残して限定Art Verify以降へ進む条件をGame Directorに判断してもらう。Engineer・QAは先行可能。現行検証の完了を全基準passやGoal達成に読み替えない。
- Play：planned。独立したプレイヤー観察で最終戦・到達体験・通常ランの所要時間を評価する。実装内容と期待結果は渡さない。
- Design（実測後）：planned。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、追加数値ゲート・調整の要否を判断する。不要でも理由を記録。明白な対処不能・到達不能はPlay前に戻す。
- Review：planned。Game Directorが体験Goalの達成を判断する。
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
| 5 | Plan | technical-director | technical-plan | done | 15-studio-to-technical-director.md → 結果: 16-technical-director-to-studio.md |
| 5a | Decide | game-director | make-decision, prepare-owner-escalation | done | 17-studio-to-game-director.md → 結果: 18-game-director-to-studio.md |
| 5b | Plan | technical-director | technical-plan | done | 19-studio-to-technical-director.md → 結果: 20-technical-director-to-studio.md |
| 5c | Decide | game-director | make-decision, prepare-owner-escalation | done | 21-studio-to-game-director.md → 結果: 22-game-director-to-owner.md |
| 5c-owner | Decide | owner | — | done | 22-game-director-to-owner.md → D-021 |
| 5d | Plan | technical-director | technical-plan | skipped | D-021で供給・承認条件を解決。再照会不要 |
| 6 | Build | gameplay-engineer | implement-change | done | 23-studio-to-gameplay-engineer.md → 結果: 24-gameplay-engineer-to-studio.md |
| 6a | Build | gameplay-engineer | implement-change | done | 25-studio-to-gameplay-engineer.md → 結果: 26-gameplay-engineer-to-studio.md |
| 6b | Build | gameplay-engineer | implement-change | done | 27-studio-to-gameplay-engineer.md → 結果: 28-gameplay-engineer-to-studio.md |
| 6c | Build | gameplay-engineer | implement-change | done | 29-studio-to-gameplay-engineer.md → 結果: 30-gameplay-engineer-to-studio.md |
| 6d | Build | gameplay-engineer | implement-change | done | 31-studio-to-gameplay-engineer.md → 結果: 32-gameplay-engineer-to-studio.md |
| 6e | Build | gameplay-engineer | implement-change | done | 33-studio-to-gameplay-engineer.md → 結果: 34-gameplay-engineer-to-studio.md |
| 6f | Build | gameplay-engineer | implement-change | done | 35-studio-to-gameplay-engineer.md → 結果: 36-gameplay-engineer-to-studio.md |
| 6g | Build | gameplay-engineer | implement-change | done | 37-studio-to-gameplay-engineer.md → 結果: 38-gameplay-engineer-to-studio.md |
| 6h | Build | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md → 結果: 40-gameplay-engineer-to-studio.md |
| 6i | Build | gameplay-engineer | implement-change | done | 41-studio-to-gameplay-engineer.md → 結果: 42-gameplay-engineer-to-studio.md（未着手） |
| 6j | Build | gameplay-engineer | implement-change | done | 43-studio-to-gameplay-engineer.md → 結果: 44-gameplay-engineer-to-studio.md |
| 6k | Build | gameplay-engineer | implement-change | done | 45-studio-to-gameplay-engineer.md → 結果: 46-gameplay-engineer-to-studio.md（部分成果、V1は質問） |
| 6k-d | Design | game-designer | write-design-spec | done | 47-studio-to-game-designer.md → 結果: 48-game-designer-to-studio.md（D-022） |
| 6k-b | Build | gameplay-engineer | implement-change | done | 49-studio-to-gameplay-engineer.md → 結果: 50-gameplay-engineer-to-studio.md（partial、入力不足） |
| 6k-c | Build | gameplay-engineer | implement-change | done | 51-studio-to-gameplay-engineer.md → 結果: 52-gameplay-engineer-to-studio.md（partial、140件OK） |
| 6k-d2 | Build | gameplay-engineer | implement-change | done | 53-studio-to-gameplay-engineer.md → 結果: 54-gameplay-engineer-to-studio.md |
| 6l | Build | gameplay-engineer | implement-change | done | 55-studio-to-gameplay-engineer.md → 結果: 56-gameplay-engineer-to-studio.md |
| 7 | Verify | qa | verify-change | done | 57-studio-to-qa.md → 結果: 58-qa-to-studio.md（証拠不足） |
| 7a | Verify | qa | verify-change | done | 59-studio-to-qa.md → 結果: 60-qa-to-studio.md（供給不足・bot所見） |
| 7b | Plan | technical-director | technical-plan, prepare-owner-escalation | done | 61-studio-to-technical-director.md → 結果: 62-technical-director-to-studio.md |
| 7b-owner | Decide | owner | — | done | 63-studio-to-owner.md → D-023 |
| 7b-design | Design | game-designer | make-decision, write-design-spec | done | 64-studio-to-game-designer.md → 結果: 65-game-designer-to-studio.md（D-024） |
| 7b-plan | Plan | technical-director | technical-plan | done | 66-studio-to-technical-director.md → 結果: 68-technical-director-to-studio.md |
| 7b-e0 | Build | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md → 結果: 70-gameplay-engineer-to-studio.md（partial、棚卸し受領） |
| 7b-e1 | Build | gameplay-engineer | implement-change | done | 71-studio-to-gameplay-engineer.md → 結果: 72-gameplay-engineer-to-studio.md（partial、prototype未接続） |
| 7b-e1a | Build | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md → 結果: 74-gameplay-engineer-to-studio.md（E1 partial 2回目） |
| 7b-e1b | Build | gameplay-engineer | implement-change | done | 75-studio-to-gameplay-engineer.md → 結果: 76-gameplay-engineer-to-studio.md（E1 partial 3回目） |
| 7b-scope | Decide | game-director | make-decision, prepare-owner-escalation | open | 77-studio-to-game-director.md |
| 7b-build | Build | gameplay-engineer | implement-change | planned | 68のE2→E3群→E4群→E5群を直列分割。70の残作業を継承 |
| 7c | Verify | qa | verify-change | planned | E0の全試験台帳を使い68のQ1〜Q6を直列分割 |
| 7d | Decide | game-director | make-decision, prepare-owner-escalation | planned | 歴史的確認不能を保持した後続評価工程の条件判断 |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。まず77で予算超過時の範囲判断を行う。残りのplanned行は既存計画として保持し、このRouteでは開かない。77の判断後に不要工程をskippedへ更新する。従来計画は68のE0→E1→E2→E3群→E4群→E5群→独立Q1〜Q6である。E0の全試験台帳からQAの個別Loadを割り当て、追加試験も含め未配布を残さない。現行必須検証、公開情報条件、再測定、記録差へのDesigner回答が揃い、歴史比較以外の不足を解消した後、Game Directorが歴史的確認不能を保持した評価継続の条件を判断する。認められた場合、限定Art Verify→独立Play→Designer実測後判断→Reviewへ進む。各StepのLoadは個別ファイル指定。全文保存先・別実行枠・変更前ビルドを待たない。明白な対処不能・到達不能や規定外の比較差はDesignerへ戻す。並列Stepは開かない。

## Route changes

76をE1連続partial 3回目として受領し、75のStepを完了記録する。予算超過規則が再計画ループに優先するため、新たなTechnical Director Stepは追加せず、77でGame Directorの範囲判断を開く。160件成功をE1完了や独立QA合格に読み替えず、後続工程は判断まで開かない。

## Next action

Game Directorが77-studio-to-game-director.mdで、Owner requestに必要な残作業へ範囲を絞る。継続必須・省略可能・Owner判断が必要な項目を区別し、残す工程と終了条件を明示する。技術方式は決めず、基準未確認を免除・合格にしない。

## Outcome

未完了。76で診断試験を追加し、runtimeはsource e99408d647c7の160件成功を確認したが、実dodger接続と被弾差の原因確定は未完了。E1は連続partial 3回となり、予算も80/40 operationsへ超過している。77でGame DirectorがOwner requestに必要な残作業を絞る。独立QA・体験評価は未完了で、歴史的確認不能と未表示の証拠を保持する。現時点で基準合格やGoal達成とは判定しない。project.mdは変更しない。
>>>END

<<<FILE design/final-boss-and-continuous-run.md
# G-002 最終ボスと連続ラン仕様

Status: Designと基準適用整理を確定。§11でV1補足3件（旧経路のボス表示、弾ID・消滅理由、長時間観測）を確定（D-022）。未実装・未検証。詳細契約はD-017、D-018に基づく旧基準の適用変更はD-019に記録する。

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

## 11. V1補足の確定（D-022）

Engineer handoff 46の3件への回答。D-017の契約、第1〜4部屋、共有戦闘規則、入力、HP、時間は変更しない。以下はいずれも30 FPSと60 FPSで別々に判定する。

### 11.1 旧経路（run指令なしのスクリプト）のボス表示

**採択：現行のmanualの注記を受け入れる。** §6の完全な表示契約が適用される経路は公開ドライバ（`mode run`、`mode room`）である。旧経路は旧来の独立部屋診断として60秒上限と`Player.describe`を保持し、旧経路へボス部屋を公開ドライバへ委譲する変更はしない（旧60秒挙動を変えるためD-017／D-021の範囲外）。

ただし、旧経路で`room 5`を選んだ場合に、完全な表示と誤認させないため次を必須とする。

- player viewの先頭（最初の盤面描画の前）に1行だけ出す：`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`
- この行は表示のみ。ゲーム状態、イベント、時刻、結果、上限を変えない。旧経路の第1〜4部屋とtrace viewには追加しない。

受け入れ基準：
- L1：旧経路`room 5`の同一スクリプトを30／60 FPSで実行し、注記行を除く出力とゲーム結果・終了時刻が変更前と一致する。60秒上限も不変。
- L2：旧経路`room 1`〜`4`と`room empty`の出力に注記行が出ない。
- L3：同じ入力列に`mode room`と`room 5`を足すと、§6の常設表示とボスメッセージが出る（V1）。
- L4：manualの旧経路注記は上記の一致を保つ。

### 11.2 弾IDと消滅理由

**要求範囲：trace view（開発者状態）と公開ドライバのイベントログ。player viewには新しい文言を足さない。** 理由：ボスの弾は同時最大1個で、player viewは既に`*`、活動中の弾数、被弾・吸収の既存メッセージを持つ。IDの露出は読み取りの助けにならない。旧経路は対象外。

- ID：`S<n>`。試行ごとに`S1`から作成順で連番、再利用しない。retryで`S1`へ戻る。ボスの弾とスピッターの弾で同じ連番を共有する。
- 発射イベントに`id`と`source`（`boss`またはスピッター識別）を含める。
- 消滅は弾1個につきちょうど1回の`shot_removed`で、`id`、`source`、`reason`、ラン時刻、部屋時刻を持つ。`reason`は次の5種のみ：
  - `lifetime`：寿命到達
  - `edge`：部屋端
  - `hit`：ダメージを与えた接触
  - `absorbed`：ダッシュまたは被弾保護による接触消費（ダメージなし）
  - `cleared`：部屋クリア・勝利・死亡確定による全消去
- 既存の`lifetime`／`edge`ログに`hit`、`absorbed`、`cleared`を追加する。接触消費は現在ログされていないため追加が必要。
- 弾が消えたフレームに、その`id`は活動中の弾数から外れる。同一フレームの発射と消滅の順序を保つ。

受け入れ基準：
- S1：B4の短射を未接触、通常命中、ダッシュ吸収、保護中接触の各場合で実行し、各弾が発射1回・消滅1回、理由がそれぞれ`lifetime`（または`edge`）、`hit`、`absorbed`、`absorbed`である。
- S2：どの場合も回復開始は発射の1.0秒後（B4）で、消滅理由に依存しない。
- S3：終端確定時に残る弾は`cleared`で1回ずつ消え、その後に`hit`が出ない（T1）。
- S4：retry後の最初の弾は`S1`。旧試行の`shot_removed`は再発しない。
- S5：player viewの出力にID文字列（`S<n>`）が現れず、既存のメッセージ文言が変更されない（V1、step94の文言保持）。

### 11.3 長時間観測

**必要な出力形と量の上限：既存の既定を保ったまま、周期出力の間隔を指定でき、最後に要約を出す。**

- `view-every <seconds>`：player viewの周期描画間隔（既定0.5、許容0.5〜60）。イベント契機の描画（§6）は間引かない。
- `trace-every <seconds>`：trace viewの周期状態行（`trace-every frame`も従来どおり許容）。イベント行は常に出す。
- `trace-every frame`は出力量の上限を設けない。使用者の選択として許容する。
- 出力間隔の指定はゲーム結果・時刻・イベント列に影響しない。
- 実行の最後に1ブロックの要約を常に出す（player／trace共通）：終了理由（clear／death／unfinished）、試行数、各試行のラン時刻、各部屋の部屋時間、ボス初入場hearts、被弾数、攻撃数、ポーズ時間を除く経過とドライバ時間、processing_seconds。
- 出力量の上限：周期行は`ceil(limit / 間隔) + 1`行以下。それ以外の行はイベント数に比例するだけで、時間に比例する出力を増やさない。

受け入れ基準：
- O1：`limit 1200`、`view-every 10`、`trace-every 5`の通常ランで、player周期描画は121以下、trace周期行は241以下。
- O2：同じスクリプトで`view-every`を0.5、10に変えても、イベントメッセージの列と最終結果が一致する。
- O3：指定なしの出力は変更前と同じ（周期0.5秒）。
- O4：要約ブロックが、勝利・死亡・limit到達（unfinished）の各終了で1回ずつ出て、数値が状態観測と一致する。
- O5：範囲外（0.5未満、60超、数値以外）の指定は実行前に拒否し、理由を出す。
- O6：20分（`limit 1200`）の通常ランを30／60 FPSで実行でき、出力は途中で切れない。

具体的な構文は上記名称を既定とするが、manualへの反映はEngineerが行う。
>>>END

<<<FILE design/g002-historical-comparison-evidence.md
# G-002 変更前一致要求の証拠適用補足

Status: D-024により確定。実装・実行・QA判定は行っていない。

本書は`final-boss-and-continuous-run.md`§7〜8・§11と、保持対象のstep68・72・94にある変更前比較の証拠の扱いを補足する。ゲーム規則、戦闘パラメータ、難度、Goal範囲は変更しない。D-019の適用終了部分を復活させない。

## 意図と判定区分

現行の読み取り・回避・反撃と連続ランを検証しつつ、過去資料で証明できる範囲を明示する。

- 記録比較：出典にある条件・精度の数値との比較。
- 確認不能：必要な変更前資料がなく、歴史的一致を判定できない。
- 現行検証：現在の仕様値、文字列、または同一ビルド内の対照条件を検証する。

一つの基準に複数の区分が併存する。現行検証の成功で確認不能部分をpassにしない。

## 基準別の扱い

| 基準 | 従来要求 | 採用する扱い | 根拠資料 | 比較条件・精度 | 未確認として残る点 |
|---|---|---|---|---|---|
| D-022 L1 | 旧room 5で注記以外の出力、結果、終了時刻が変更前と一致。60秒上限不変 | 歴史的一致は確認不能。注記の内容・位置・回数、現行の60秒上限は検証する | 仕様§11.1、D-022、62のテスト所見 | 同一入力を各FPSで実行。注記抑制との比較は現行内対照として記録 | 注記以外の過去出力全文、過去結果・終了時刻との一致 |
| D-022 L4 | manualの注記がL1の一致を保つ | 文書と経路説明は現行照合。L1の歴史的一致を保証する部分は確認不能 | 仕様§11.1、60の文書判定 | manualと表示条件・対象経路を照合 | 文書の一致から旧実装の不変性は証明できない |
| D-022 O3 | 指定なしの出力が変更前と同じ、周期0.5秒 | 変更前出力一致は確認不能。既定0.5秒と明示0.5秒の現行内対照は検証する | 仕様§11.3、62のテスト所見 | 各FPSで同一入力。追加要約等はD-022の契約として別に照合 | 過去出力全文・描画順の一致 |
| step68 V-a／V-b | 予兆・被弾表示の時点とhearts suffixを保持 | 定義済み文言、接触フレーム、予兆時間、suffix形式は現行検証。「以前と同時点」の実測一致は確認不能 | step68 §4、combat.md、step94 | 各variant・各FPS。現行時間は該当仕様の±1フレーム | 過去の個別表示フレームとの一致 |
| step68 V-c | 指定語以外の出力が0.6.1とbyte単位で一致 | 確認不能 | step68 §4 | 比較用旧出力がない。数値一致をbyte一致へ拡張しない | 出力全文の同一性 |
| step68 V-e末尾 | 共有基準保持、bot結果不変 | 共有基準は現行検証。独立1〜4 dodgerは下表の記録比較。それ以前のbot結果不変は確認不能 | D-019、40、56 | 下記の条件と精度。旧5番・終了した集計は対象外 | 0.6.1等の旧方針・全bot結果との一致 |
| step94 W3／W4 | 反応が以前どおり、吸収時のhit表示なし | prefix、反応動作、吸収時の無表示は現行検証。過去の全反応行動列一致は確認不能 | step94、D-005のcombat.md反映、D-019 | 指定substringと接触条件を各FPSで確認 | 過去スクリプトの全行動列との一致 |
| step94 W7 | 変更前と時刻・hearts・弾数等が同じ、bot方針・結果不変 | 歴史的一致は確認不能。現行共有基準は保持。独立1〜4 dodgerだけ下表の記録比較 | step94、D-019、40、56 | 過去の各イベント時刻・弾数記録がなく、±1フレーム比較は成立しない | 変更前挙動、全bot方針、未記録結果の一致 |
| 独立1〜4 dodger保持、40・56の比較記述 | ボス対応が既存部屋へ影響しないこと | 40の記録数値との比較を採択 | 40の保存実行、56の保持回帰報告 | 同一部屋・FPS・3 hearts・通常初期状態・limit 60秒。下表参照 | ボス対応前の厳密一致、全行動列、未丸め時刻 |
| R2、step72 R3-1の保持部分 | 第1〜4部屋の構成・配置・既存パラメータを保持 | 正本仕様への現行照合。変更前ビルド待ちは不要 | combat.md、step72、仕様§8、D-019 | 敵種・座標・順序・数値を仕様へ照合 | ソース全文の歴史的一致は主張しない |
| step72 R3-6 | 同じ静止入力でgrub有無のcue開始時刻が一致 | 同一現行ビルド内の対照試験として保持 | step72 R3-6 | 最初のlungeまで、各FPSで±1フレーム。制御fixtureと明示 | 過去ビルドとの比較ではない |
| combat16c／新5番FPS比較 | 同条件で30/60 FPSの結果が一致 | 現行ビルド内比較として保持 | D-019、仕様§8、60・62 | 独立1〜4保持。新5番は公開情報対応後、開始3/2 hearts別に再測定 | 対応前ボス数値は新しいpass根拠にならない |

L2、L3、S1〜S5、O1、O2、O4〜O6、その他の現行仕様検証は継続する。S5の既存文言保持は正本文字列へ照合できるが、旧出力全文一致まで証明するものではない。

step72の位置変更の説明、過去の観測値、combat.mdの歴史的結果は変更説明・記録として保存する。D-019で適用終了した旧集計、旧第5部屋、過去G-001の合格判断を新たな比較ゲートにしない。

## 独立1〜4 dodgerの採択記録

出典は40、保存source id `5145454ab956`。各部屋・各FPSは1試行。開始3 hearts、通常位置(8,4)・右向き、独立部屋、limit 60秒。全行clear、損失0、終了3 heartsである。

| FPS | 部屋 | 秒数（小数1桁） | dash回数 |
|---|---:|---:|---:|
| 30 | 1 | 6.6 | 3 |
| 30 | 2 | 20.7 | 10 |
| 30 | 3 | 15.6 | 6 |
| 30 | 4 | 18.3 | 7 |
| 60 | 1 | 9.6 | 5 |
| 60 | 2 | 25.1 | 14 |
| 60 | 3 | 15.0 | 6 |
| 60 | 4 | 17.0 | 8 |

現在の時間を最も近い0.1秒へ丸めて比較する。ちょうど中間の場合は大きい側へ丸める。これ以上細かい過去時刻を復元しない。整数の結果・hearts・dashは記録値と照合する。丸め一致は±1フレーム一致を意味しない。

56はsource `04fa2b1c168a`で全clear・損失0、同じdash数を報告し、時間も40の精度で一致する。56の小数2桁時間と攻撃回数は後続記録として識別を保つ。40にない部屋1・2の攻撃回数を40の値として扱わない。

この比較は新しい難度・秒数ゲートではなく、保持回帰の記録比較である。差があれば条件・方針・共有処理への影響を報告しDesignerへ返す。現行の共有規則違反はQAが別途判定する。比較のために戦闘やbot行動を数値へ合わせない。

## 証拠の限界と後続への受け渡し

各比較の報告には基準ID、FPS、入力・初期条件、limit、現在のソース識別、参照記録、測定値、丸め値、結論と未確認範囲を記載する。歴史比較と現行内対照を別列にする。

D-023の最大3回・各出力2万字という条件で、検証対象を絞った出力と直列分割を使う。切断された部分や表示されなかった判定を確認済みと扱わない。存在しない全文保存先や変更前ビルドを要求しない。具体的な試験構成はTechnical Directorが決める。

確認不能項目を最終Reviewへ渡す一覧から削除しない。QAの60のfailを本書で上書きせず、全基準passも宣言しない。Goalの意味・範囲の判断が必要ならStudioからGame Directorへ返す。

難度・追加数値ゲートと15〜20分Visionの判断は、対応bot再測定・独立QA・独立Play後の予定Stepに残す。本書の内容を独立Playの資料へ転記しない。
>>>END

<<<FILE goals/G-002-final-boss/68-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 68
from: technical-director
to: studio
stage: Route
outcome: done
---
# 68: technical-director → studio — 供給上限内での直列検証計画

## Task

62の計画を本計画へ置き換え、試験道具対応、診断、再測定、保持回帰、通常ラン入力再生成、独立QAを直列にルーティングする。歴史的一致の確認不能を保持し、技術検証の完了とGoal達成判断を分離する。

## Context

60はfailであり、本計画はその判定を変更しない。D-023で本文・実行・出力の供給条件が確定し、D-024で歴史比較と現行検証の扱いが確定した。

今回の担当範囲は再計画である。製品コード、bot、テスト、仕様は変更していない。実行、ソース識別の再算出、再測定、独立QA判定は行っていない。

## Findings

### 1. 計画の置換範囲と影響システム

62の変更前ビルド探索、完全ログ保存先の確保、保存・再読込み試験を開始条件から外す。利用できるのは個別Load、各Step一度最大8件の@need、最大3回の@run、各実行最大2万字の出力である。

影響対象は次のとおり。

- `repo/bots.py`：ボス判断への公開情報境界、判断記憶、突進診断。
- `repo/tests/test_bots_boss.py`：公開情報限定の全判断経路と記憶の試験。
- `repo/tests/test_split_c.py`：測定精度、記録比較、通常ラン入力生成、出力分割。
- D-022試験2ファイル：現行内対照と歴史比較のラベル、長時間出力の検証方法。
- `repo/play.py`、`repo/run_driver.py`：公開観測と再生の照合対象。
- `repo/game.py`、`repo/session.py`：戦闘・境界・終端の照合対象。試験道具対応だけを理由に変更しない。
- `repo/source_id.py`と全tests：実行集合の識別と独立QAの網羅性確認。

全工程を直列とする。bot変更が測定、入力生成、再生結果、source_idへ連鎖し、共有されたrepoで並列に変更すると証拠の対象が混ざるためである。独立QAは実装者とは別RoleのStepで行う。

### 2. 共通の証拠単位と出力契約

各Stepは担当範囲を次の列で報告する。

| 列 | 必須内容 |
|---|---|
| 対象 | 基準ID、現行検証／現行内対照／記録比較／歴史的確認不能 |
| 実行条件 | FPS、モード、部屋、開始hearts、位置・向き・タイマー等、limit、fixtureの有無 |
| 再現情報 | 完全な入力または生成手順、実行コマンド、対象テスト名、方針版 |
| 識別 | 実行時source_id、対象ファイル一覧。BUILDだけで識別しない |
| 検証内容 | 操作、assert、全件評価の対象集合、比較・丸め方法 |
| 表示証拠 | 対象の前後状態、イベント、判断入力・選択、実際の測定値 |
| 結論 | FPS別の結果、失敗理由、未表示・未実行・確認不能の範囲 |

必要な証拠本文を成功件数・ハッシュ・summaryだけで置き換えない。一方、全実行の無関係な状態行を出す必要はない。テストは全対象を内部で検査し、報告対象を明示した前後状態や判断列を出す。表示した抜粋だけから全判断の適合を主張しない。

出力には対象開始・終了、列定義、連番、対象件数、表示件数、除外対象を出す。判断列等は一行を短くし、予定出力を概ね1万2千字以内に収める。2万字は上限であり、切断がない保証ではない。開始・終了や連番が欠けた場合、欠けた範囲は未確認とする。

大きい対象は、同じ初期条件から再実行して判断番号・部屋・攻撃種等で表示範囲を限定する。途中状態を注入して通常到達の証拠にしない。再実行時は入力・source_id・総判断数を照合し、異なる結果を一つの連続列へ継ぎ合わせない。

各Stepは最大3回を使い切る必要はない。残りが既知の試験・表示範囲だけならpartialで次の同Role Stepへ渡す。必要本文や道具が欠ける場合は、その不足を明記してStudioへ返す。

### 3. 本文供給と試験棚卸しを先行するEngineer Step E0

現在供給されているテスト本文は4ファイルであり、全testsの一覧・本文ではない。存在が不明なテスト名を推測してLoad案へ書かない。`repo/tests/`の@needは使わない。

E0の個別Load案：

- `repo/source_id.py`
- `repo/game.py`
- `repo/session.py`
- `repo/bots.py`
- `repo/play.py`
- `repo/run_driver.py`
- `repo/tests/test_bots_boss.py`
- `repo/tests/test_split_c.py`
- `repo/tests/test_d022_observation.py`
- `repo/tests/test_d022_shots_and_note.py`
- 本Handoff、60、D-019、D-021〜D-024、補足仕様

Engineerは通常の書込許可をStudioから割り当てられた試験ファイルに、unittest実行で使える棚卸し・対象別証拠出力を用意する。追加ファイル名の提案は `repo/tests/test_g002_evidence.py` とする。これは今回作成済みではない。

実行配分：

1. tests：実在する`tests/*.py`の個別名、discoverされた全テストID、source_idを出す。通常のsuiteも実行する。
2. tests：一覧が長ければ残りの範囲。基準と試験IDの暫定対応を出す。
3. tests：必要な棚卸し漏れの補完・出力道具の確認。

固定コマンドは`python3 -m unittest discover -s tests`を維持する。対象別出力は試験道具側で選ぶ。trace枠に任意のPython実行を仮定しない。

完了条件は、実在ファイル名とテストIDの一覧、未対応基準、旧5番試験の保持・置換先が分かること。Engineerが作った対応表だけでQA済みにはしない。

StudioはE0の一覧を使い、後続QAのLoadを実在する個別ファイル名へ展開する。全ファイルをどのQA単位へ配るかの台帳を作り、未配布を残さない。各Stepの追加本文は最大8件以内とし、超える場合はLoadで先に供給するか別Stepへ分ける。

### 4. 公開情報bot対応 E1

E0の後、ボス専用の観測データと判断処理の境界を設ける。判断処理には内部Game／Enemyを渡さず、全分岐が公開観測とその履歴だけを読む形にする。ログ専用の内部状態取得は判断後の独立した観測経路に置く。

公開情報の各フィールドを`Output.emit`の表示または既存公開観測へ対応付ける。active残時間、struck等の未表示内部値は判断入力に入れない。warningで見えた固定経路を保持し、active中は全経路を保守的に扱う。recovery等の公開変化で解除する。warning履歴がないactive開始では固定最大範囲を保守的に扱い、履歴不足を記録する。表示追加は行わない。

全判断について、判断番号・反応grid・時刻、公開入力、記憶の由来、候補、除外理由、選択、発行したボタンを短い構造化列にする。stunによる判断省略も別に記録する。共有補助関数を介して未表示値へ戻る経路も監査対象とする。

個別LoadはE0の6ソース、`test_bots_boss.py`、`test_split_c.py`、新しい証拠試験、仕様§6・8、本HandoffとD-019・D-024。

実行配分：

1. tests：同一公開入力・異なる内部active残時間で全ボス判断が一致すること、許可外属性へアクセスできないこと。
2. tests：warning→active→recovery、距離0、壁、dash待ち、stun、部屋入場・retryでの記憶初期化。
3. tests：修正後suiteと、判断全経路・公開フィールド対応の不足確認。

完了条件は全分岐の公開情報対応、試験assert、独立1〜4への変更範囲が明示されること。実装者の自己評価は独立QAの代用にしない。

### 5. 突進診断・接触試験 E2

E1の後、`_hurt_lines`のboss被弾をshot診断から分離する。無傷の接触消費も記録し、hurt件数だけで接触を推測しない。

各フレームの移動前後のボス・プレイヤー座標、照準、実際の移動後距離、active、保護、消費前後、hurtを試験用観測で取得する。試験用観測値をbot判断へ戻さない。接触しなかった場合はその距離も出す。

個別Loadは`game.py`、`session.py`、`bots.py`、`source_id.py`、`test_bots_boss.py`、新しい証拠試験、E0で判明した該当接触試験の個別名、B3・B6・B7・B10とcombat17・20・21。

実行配分：

1. tests：30 FPS、通常命中・dash・被弾保護・非接触。
2. tests：60 FPSで同条件。
3. tests：保護終了後の追加被害なし、次攻撃の通常命中、帯内外・上端の不足分。

完了条件は両FPSの実接触・消費を追え、誤ったshot補助文がないこと。帯外差は規則違反としてQAへ渡す。帯内差や帯幅超過、bot比較超過の判断先はDesignerとし、自動免除しない。

### 6. ボス4条件の再測定 E3群

E1・E2完了後、同じ測定ソース集合と方針を固定して開始3/2 hearts×30/60 FPSを各1試行以上測る。位置(8,4)、右向き、通常初期戦闘状態、独立5番、limit 120秒を4条件で揃える。120秒は測定条件であり、撃破秒数の合否ゲートではない。

個別Loadは`bots.py`、`game.py`、`source_id.py`、`test_bots_boss.py`、`test_split_c.py`、新しい証拠試験、E1・E2の成果、D-019・D-024。

E3は原則1条件1Stepとし、各Stepで：

1. tests：当該条件の結果と全判断列の最初の範囲。
2. tests：同条件再実行で次の判断範囲。
3. tests：残範囲または差の接触診断。

3回で全判断が表示できなければ同条件のpartial継続を開く。サンプル5件を全判断の証明にしない。測定途中で試験コードを変えsource_idが変わった場合は旧・新結果を混ぜず、新しい集合で4条件を揃え直す。

報告はclear／death／unfinished、終了hearts・損失、時間、被弾源、攻撃・dash、判断件数と全判断の検査範囲を含む。開始heartsごとにFPSを比較し、同じclear結果・損失差1以下を検査する。一方のみunfinishedなら比較未完了。両方death／unfinishedの一致を攻略可能性にしない。

対応前の既報値との一致は要求しない。明白な対処不能、反撃不能、到達不能は後続Playを待たずDesignerへ返す。

### 7. 保持回帰と記録比較 E4群

個別Loadは`bots.py`、`game.py`、`source_id.py`、`test_split_c.py`、新しい証拠試験、補足仕様、combat.md、D-019・D-024、およびE0で特定した既存bot試験の個別ファイル。

実行配分：

1. tests：独立1〜4 dodger、開始3 hearts、通常初期状態、limit 60秒、両FPSの8行を全表示。
2. tests：独立1〜2 walkerとcombat14、独立3・4の3bot×両FPS、combat15・16c。
3. tests：終了、ログ有無結果一致、ログ観測、walker比較距離、brute方針等の保持試験。差があれば対象別の継続Stepへ渡す。

記録比較は補足仕様の40の表を正本とする。clear・損失0・終了3 hearts・dash数を整数比較し、時間は未丸めの測定時刻から最寄り0.1秒、ちょうど中間は大きい側へ丸める。現行`test_split_c.py`のPython `round`と、`play_room`の小数2桁化をこの丸め規約の証明には使わない。未丸め時刻を測定用に保持し、指定の丸めを明示的に試験する。

40のsource `5145454ab956`、56の`04fa2b1c168a`、今回sourceを別列にする。40にない攻撃数を40の期待値にしない。既存の攻撃数assertを残すなら後続記録または現行試験の位置付けを明記する。

差が出た場合はFPS、初期条件、limit、方針変更、共有関数への到達、判断分岐・接触差を整理してDesignerへ返す。数値に合わせてbotや戦闘を調整しない。共有規則違反は記録差と別にQAへ渡す。

### 8. 通常ラン再生成・公開再生 E5群

E3・E4の後、新botで入力を生成する。公開再生はtimed inputsのみで実行し、状態注入・ライブbotを使わない。通常到達の証拠と制御fixtureを分離する。

個別Loadは`test_split_c.py`、新しい証拠試験、`bots.py`、`play.py`、`run_driver.py`、`session.py`、`source_id.py`、`manual.md`、`public-driver.md`、R1〜R5・T1〜T4・C1〜C3・V1。

既存のpause時刻7/10、retry時刻120/140、driver-limit141は、bot変更後の進行と一致する保証がない。生成時に実測したclear・勝利・自然死亡の時刻から、公開制御列を組み立て直す。生成時に状態を観測することと、再生時の状態注入を区別する。

FPSごとのStepで：

1. tests：生成手順、完全な公開入力、入力の生成元source、境界・終端・制御時刻を出す。
2. testsまたはtrace：同じ公開入力の対象別状態列。入場・正規敵全撃破・各clear・勝敗・retryと両時刻を全表示。
3. tests：同じ公開入力のplayer出力と状態の対照。表示対象を分ける必要があればpartial継続。

player viewは試験内で公開出力を捕捉して対象画面・メッセージを出せる。実行コマンドにないplayer枠やbot枠を別枠として要求しない。traceを使う場合は公開構文の入力を完全に提示する。

旧未来入力破棄はpending破棄列の直接観測、または新attemptが旧入力時刻を越える条件で証明する。終端後の待機時間だけでは足りない。

同一試行のラン時刻、部屋別時間、4遷移、pause、終端待機、driver時間、processing_seconds、ボス入場hearts、hurt・反撃・retryを別々に報告する。独立部屋時間を合算しない。対応前の約87／104秒を新しいpass基線にしない。

### 9. 独立QAの分割

E0で得た全testsを、以下の担当範囲へ個別名で割り当てる。複数範囲を持つファイルは複数Stepへ供給する。追加された試験も一覧へ追記し、未配布ファイルがないことを最終照合する。

各QAには60、本Handoff、D-019・D-021〜D-024、担当仕様、担当ソース、担当テスト本文を渡す。Engineerの自己評価を判定根拠にせず、独立にassertと観測を照合して実行する。

| QA単位 | 主対象 | 個別Loadの核 | 最大3回の配分 |
|---|---|---|---|
| Q1 | 公開情報bot、突進診断、4条件比較 | bots.py、game.py、source_id.py、test_bots_boss.py、test_split_c.py、新証拠試験 | 公開境界／3 hearts対／2 hearts対。全判断表示は必要に応じ直列継続 |
| Q2 | B1〜B10、S1〜S5 | game.py、session.py、play.py、run_driver.py、test_d022_shots_and_note.py、新証拠試験と棚卸し済みボス試験 | 30 FPS／60 FPS／不足条件 |
| Q3 | R1〜R5、T1〜T4、C1〜C3 | game.py、session.py、play.py、run_driver.py、test_split_c.py、新証拠試験と棚卸し済みsession・driver試験 | 境界／終端・retry／通常公開再生。FPS・view別に継続可 |
| Q4 | L1〜L4、O1〜O6、V1 | play.py、run_driver.py、manual.md、public-driver.md、test_d022_observation.py、test_d022_shots_and_note.py、新証拠試験 | 注記・現行内対照／30 FPS長時間／60 FPS長時間。表示・summary不足は継続 |
| Q5 | combat1〜11・17〜21、R2、step68保持部分 | game.py、play.py、bots.py、combat.md、combat-step68.md、およびE0で特定した共有戦闘・bot試験の全個別名 | grub／spitter・cap・gap／接触・variant |
| Q6 | step72 R3-1〜10、step94 W1〜8保持部分、記録比較 | game.py、play.py、bots.py、test_split_c.py、combat-step72.md、combat-step94.md、補足仕様、およびE0で特定した該当試験の全個別名 | room3／文言・方向／8行記録比較と保持bot |

Q5・Q6の未知のファイル名はE0後にStudioが確定する。今回の4テストだけで割当完了とはしない。QAが本文を追加で必要とすれば一度最大8件の@needを使い、それ以上は次Stepへ分割する。

共有回帰では通常静止12秒の最大3だけでcap遅延の一般上限5を合格にしない。room4の実gap、強制同時射撃、cap遅延、practiceの非gap条件を区別する。旧5番依存はD-019の置換先へ追跡する。

O6の1200秒試験は観測用生存fixtureと明記する。内部で全出力を検査する試験本文、出力欠落検査、周期数、イベント消費範囲、開始・中間・終了の必要本文を出す。これで何を検証したかを限定し、全文がStudioへ収録されたとは主張しない。通常ラン到達はE5／Q3の別証拠である。

### 10. 歴史的確認不能と後続工程の条件

全QA結果は単一のpassに潰さず、次を別表にする。

1. 現行仕様・現行内対照のFPS別判定。
2. 独立1〜4の記録比較。
3. D-024による歴史的確認不能。
4. その他の未実行・未表示・実装依存。
5. Designer判断待ち。

歴史的確認不能一覧にはL1、L4の保証部分、O3、step68 V-a／V-bの過去時点・V-c・V-eの未記録bot不変、step94 W3／W4の過去全行動列・W7、その他補足仕様の未確認範囲を残す。現行検証の成功でも削除しない。

技術上の後続準備条件は、現行必須検証が完了し、公開情報条件と再測定が揃い、記録差があればDesignerの回答があり、歴史比較以外の不足を解消したことである。これは全基準passやGoal達成ではない。

歴史的確認不能を残して限定Art Verify以降へ進める工程条件は、StudioからGame Directorへ明示して判断を求める。Technical Directorは「全QA合格後」を独断で緩和しない。判断待ちでも上記のEngineer・QAは進められる。

Game Directorが未解決一覧を保持した評価継続を認めた場合、限定Art Verify→独立Play→Designer実測後判断→Game Director Reviewへ進む。表示修正が入れば該当QAを再実行してからPlayへ進む。認められない場合は方向・範囲の判断をGame Directorへ返し、QAに免除を依頼しない。

独立Playへ渡すのはplayer-facing manual、実行方法、試行を記録する中立な依頼だけとする。本計画、設計比較値、実装履歴、QA判定、期待結果、Review用体験信号は渡さない。

Designerには再測定、独立QA、独立Play、同一試行の時間を渡し、追加数値ゲートの要否、反撃・回復・retry負担、15〜20分Visionとの差について回答を求める。人間の時間とbot時間を同一視しない。承認範囲で解消できないVision不整合はGame Directorへ返す。

### 11. リスクと対策

- 保守的なボス経路で成績が変わる：再測定し、ゲームを旧値へ合わせない。
- 判断境界外からの内部値流入：全呼出経路の監査と、許可外属性を持たない観測データで試験する。
- ログの切断：短い列・固定範囲・直列継続を使い、欠落を未確認に残す。
- source_idの混在：tests変更も識別を変えるため、測定集合を固定し、変更時は該当比較をやり直す。
- suite成功と基準充足の混同：全テスト本文、assert、観測対象、未対応基準を照合する。
- 歴史比較の確認不能による工程停止の反復：存在しない資料を再要求せず、未解決一覧と具体的な工程判断をGame Directorへ渡す。

## Decisions already made

- D-019：保持回帰、公開情報限定ボス比較、開始3/2 hearts別FPS比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト検証。実機対応済みとはしない。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を維持。
- D-023：個別Load、@need一度最大8件、@run最大3回、出力最大2万字、全文保存先・変更前ビルドなし。
- D-024：歴史的確認不能、記録精度に限定した独立1〜4比較、現行検証を分離。
- 本Stepは新しい仕様Decisionを採択せず、62の実行計画を置き換える。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal範囲を変更しない。60のfailを上書きしない。確認不能をpass・免除・適用終了にしない。

限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewを省略しない。実機検証と変更前ビルド、全文保存機構を再要求しない。未表示・切断部分を確認済みにしない。

## Open questions

1. E0で判明する全テストファイルと基準の対応は何か。Studioは後続Loadを実在する個別名へ展開すること。
2. 公開情報境界の対応後、4条件の成績・判断列・保持記録比較にどの差が出るか。
3. 現行検証完了後、歴史的確認不能を残して評価工程を継続する条件をGame Directorはどう判断するか。
4. 再測定・独立QA・独立Play後、Designerは追加ゲートと時間Visionについて何を判断するか。

## Expected output

StudioはまずE0をEngineerへルートし、本文棚卸しと対象別出力を整える。その後E1→E2→E3群→E4群→E5群→独立Q1〜Q6群の順に進め、各Stepを最大3回・最大2万字へ収まる単位に分ける。

歴史的確認不能を残す後続工程条件はGame Directorへ別途ルートする。現行検証、記録比較、確認不能、判断待ちを最終Reviewまで分離して保持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/source_id.py
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/play.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting plan: goals/G-002-final-boss/62-technical-director-to-studio.md
- Supporting handoff: goals/G-002-final-boss/65-game-designer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/66-studio-to-technical-director.md
>>>END

<<<FILE goals/G-002-final-boss/60-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 60
from: qa
to: studio
stage: Verify
outcome: fail
---
# 60: qa → studio — ソース照合の追加所見と独立検証の供給不足

## Task

不足しているテスト本文・省略されていないログ・追加実行枠を供給し、独立QAを継続する。ボスbotの観測情報条件について、以下のソース所見を確認して検証経路を整理する。

## Context

59の依頼に従い、packet内の仕様、保存ソース本文、今回の収録実行結果を独立に照合した。実装者の自己評価は根拠にしていない。

今回も実行枠は0回である。Loadに指定されたrepo/tests/の本文はpacketに含まれていない。追加実行、ファイルからのsource_id再算出、完全ログの保存は実施できていない。収録結果の再評価だけで独立検証完了とはしない。

## Findings

### 総合判定

**fail：全基準の独立検証は未完了。加えて、ボスbotの条件付きFPS比較にはソース上の不適合所見がある。**

152 tests成功は今回の収録でも確認できる。ただしテスト本文がないため、条件・操作・assertを基準へ対応付けられない。未確認項目をsuite成功でpassにしていない。

### 識別と証拠の所在

- 保存ソース本文のBUILD：`0.6-g002-public-32`。
- 今回の全収録出力のsource_id：`04fa2b1c168a`。
- 保存ファイルからの独立ハッシュ再算出：未実施。本文と収録出力が同一ソース集合であることは未確定。
- 完全ログ：packetには供給されていない。Round 2 traceとRound 3 botsは明示的に中段が切断されている。

使用した実行証拠は今回の`@run-results`である。

| 参照 | コマンド・入力 | 観測範囲 |
|---|---|---|
| Round 1 tests | `python3 -m unittest discover -s tests` | 152 tests、Exit 0、2.886秒。本文・個別assertなし |
| Round 2 boss-zero-30/60 | `python3 play.py --view trace SCRIPT` | 両FPS。距離0開始、直交移動、driver時刻0.4〜2.4のpause。中段省略 |
| Round 3 retained-and-boss-30/60 | `python3 bots.py SCRIPT` | camper/walker/dodger、rooms 1-5、limit 120、hearts 3,2、log on。中段省略 |
| Round 3 boss-zero-player-60 | `python3 play.py --view player SCRIPT` | 60 FPSの上記距離0診断、view-every 10。表示全文あり |

入力列は各参照のScript欄にある。今回新たに実行したコマンドはない。

### 追加所見：D-019のボスbot観測条件

`repo/bots.py::_dangers`のactive charge分岐は、次の内部値を使う。

```python
e.phase_left * LUNGE_SPEED + 0.6
```

これを危険経路の残長として`_threat`へ渡し、`ahead > length`なら危険候補から外す。したがって、この値は単なるログではなく、回避・停止・その後の行動選択に影響する。

一方、`repo/run_driver.py::Output.emit`のplayer viewは、active中の残時間を表示していない。残時間を表示するのはwarningとrecoveryだけである。botも、表示済み発動時刻を記憶して残時間を算出する経路ではなく、内部`phase_left`を直接読む。

D-019項目6および仕様§8の「player viewで読める情報」「未表示の将来状態を使わない」という比較条件に対し、この判断経路は適合を確認できない。**現状のボスbot比較を条件付きpassにはできない。** 全判断経路を見たとの主張もできないが、この分岐だけで公開情報限定の条件には具体的な問題が残る。

これはゲーム戦闘結果の再現済み不具合とは区別する。対応は試験道具の情報取得経路を整理し、両FPS・開始hearts 3/2を再測定すること。秒数や難度の調整要求ではない。

また、`_hurt_lines`はboss被弾をshot側の診断分岐へ送り、収録にも`source boss`と`shot position not found (fired in this frame)`が併記される。被弾イベントのsourceは読めるが、この補助文から突進の接触位置を証明できない。

### ソースから確認できた事項

- `game.py::ROOMS`の第1〜4部屋は保持仕様の構成・位置・順序と一致する。第5部屋はboss (12,4)だけ。GRUBSと共有定数も提示仕様の値と一致する。
- 境界は`session.py::_enter`で新しいGameを生成する。heartsは入場時に`min(3, old_hearts + 1)`となる。反応記憶の初期化は`run_driver.py::drive`のgeneration変更時に実装されている。
- 同フレームの結果判定は`Game.step`で敵、既発射弾、結果の順。`_resolve_result`は死亡優先で残弾と照準を消す。
- retry時のpending破棄処理は`drive`に存在する。ただし処理の存在と、要求された独立実行証拠は別である。
- D-022の旧room 5注記はlegacy playerだけに置かれ、manualも一致する。
- 公開driverのinterval検証、shot ID採番、消滅理由、summaryの実装経路は読める。ただし全条件の実行確認は未完了。

### 基準別・FPS別判定

「未確認」は部分証拠があっても基準全体を合格にできない場合を含む。

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| R1 | 未確認 | 未確認 | SPLIT_C_PUBLICは通常入力再生の完走を支持。正規敵全撃破・全入場を両viewで対照する完全ログがない |
| R2 | pass（静的） | pass（静的） | ROOMS、GRUBS、共有定数を仕様と照合。FPSによるデータ分岐なし。挙動回帰の判定は下段に分離 |
| R3 | 未確認 | 未確認 | 1/2/3/0 heartsの境界実行なし |
| R4 | 未確認 | 未確認 | 新Game生成と反応初期化は確認。残存全状態を置いた境界前後assertなし |
| R5 | 未確認 | 未確認 | 構造化結果の遷移は各1秒。境界入力破棄・入場同時刻1回適用の独立証拠なし |
| B1 | 未確認 | 未確認 | 初期値・固定交互順はソースにある。各3回・低HPを満たす観測なし |
| B2 | 未確認 | 未確認 | 距離0 charge右固定と移動後の固定方向は収録で確認。short shot距離0など全条件は不足 |
| B3 | 未確認 | 未確認 | ソースは速度8、active 0.3、壁クランプ。毎フレーム位置・壁比較が不足 |
| B4 | 未確認 | 未確認 | 発射速度3・寿命1の実装。60 FPS playerは発射3.633→回復4.633を確認。全消費条件不足 |
| B5 | 未確認 | 未確認 | chargeの直交回避は部分確認。30 FPSは量子化で1.0667 tiles、60 FPSは1 tile。両攻撃の指定条件は不足 |
| B6 | 未確認 | 未確認 | botのdash件数は接触消費の証明にならない |
| B7 | 未確認 | 未確認 | 保護終了を攻撃途中に置く条件と次攻撃の通常命中が未観測 |
| B8 | 未確認 | 未確認 | 全フェーズのswipe前後比較・致死時新発動なしの実行不足 |
| B9 | 未確認 | 未確認 | 60 FPS playerで回復1.2/1.4秒。開始から4回攻撃のassertなし |
| B10 | 未確認 | 未確認 | 帯内外・上端の実軌道と接触距離なし |
| T1 | 未確認 | 未確認 | 残弾を持つ終端とその後2秒比較なし |
| T2 | 未確認 | 未確認 | 同フレーム致死swipe＋致死既発射弾のfixtureなし |
| T3 | 未確認 | 未確認 | 終端待機の集計はあるが、入力を伴う全状態比較なし |
| T4 | 未確認 | 未確認 | 勝利／死亡retry集計あり。完全初期状態比較・旧入力時刻を越える生存試験なし |
| C1 | 未確認 | 未確認 | 同一試行の時間集計は整合。全入場時刻0の完全列なし |
| C2 | 未確認 | 未確認 | warning中pauseは部分確認。dash・保護・clear表示等の全対象比較不足 |
| C3 | 未確認 | 未確認 | driver-limitとoutcomeの分離は観測。game limit同フレーム優先fixture不足 |
| V1 | 未確認 | 未確認 | 60 FPS診断表示は二攻撃・HP・回復・実弾数を確認。通常run終端・retryを含む両FPS対照不足 |
| V2 | 対象外 | 対象外 | D-021の今回範囲。実機対応済みとは判定しない |

Round 2の距離0 chargeは、30 FPSでwarning 0.033333、60 FPSで0.016667、aim (1,0)。60 FPS playerでは発動0.716667、回復1.016667、追跡再開2.216667を確認する。charge回避後にshort shotで被弾しており、試行全体の無傷を示さない。

### D-019保持回帰とbot測定

| 対象 | 30 FPS | 60 FPS | 判定 |
|---|---|---|---|
| combat14 walker側 | room 1で損失3 | room 1で損失3 | 損失下限1は既に充足。ただし独立1〜2の全成績表は省略部分にあり供給不足 |
| combat14 dodger側 | rooms 1/2 clear、損失0/0 | rooms 1/2 clear、損失0/0 | 収録数値上pass |
| combat15 rooms 3/4 | dash 6/7 | dash 6/8 | 収録数値上pass |
| combat16c rooms 1〜4 | 全clear、損失0 | 全clear、損失0 | 収録数値上pass |
| 新boss比較、開始3/2 | 両方clear、損失0 | 両方clear、損失0 | 数値条件は充足。観測情報条件は上記所見によりfail |
| 共有combat1〜11、17〜21 | 未確認 | 未確認 | 個別テスト本文・assert対応なし |
| step68保持部分 | 未確認 | 未確認 | 文字列定義はソース一致。全実行・旧出力比較不足 |
| step72 R3-1〜10保持部分 | 未確認 | 未確認 | R3-1の配置は静的一致。他の条件・assert不足 |
| step94 W1〜8保持部分 | 未確認 | 未確認 | 方向算出・文言はソース一致。W1〜6全ケース・旧出力比較不足 |

独立3/4のcamperは、開始3 hearts、limit 120、同一初期位置・向き。

| FPS・部屋 | 結果 | 終了hearts／損失 | 秒 | 被弾源 | 攻撃／dash |
|---|---|---|---:|---|---|
| 30・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 30・4 | death | 0／3 | 6.73 | shot 3 | 1／0 |
| 60・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 60・4 | death | 0／3 | 6.75 | shot 3 | 1／0 |

独立3/4のwalker成績と判断ログ全文は今回も省略されている。数値を推定しない。camperの行動分岐はソースで読めるが、判断文言をnoteへ記録していないため、実行ログには主に被弾・stunが残る。

cap遅延の一般上限5は、通常静止試験の最大3やsuite greenからは合格にできない。旧第5部屋依存の試験がどこで置換されたかも、tests本文なしでは追跡できない。

### D-022

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| L1 | 未確認 | 未確認 | 注記以外の変更前出力一致・60秒上限実行比較なし |
| L2 | 未確認 | 未確認 | ソースの表示条件は一致。各旧部屋出力未収録 |
| L3 | 未確認 | 未確認 | 指定された同一入力のmode room＋room 5比較なし |
| L4 | pass（文書） | pass（文書） | manualと旧経路注記条件が一致 |
| S1 | 未確認 | 未確認 | 正常命中の発射／消滅抜粋あり。未接触・dash・保護の全列不足 |
| S2 | 未確認 | 未確認 | hit時の1秒維持は部分確認。他の理由不足 |
| S3 | 未確認 | 未確認 | 残弾終端のcleared全列なし |
| S4 | 未確認 | 未確認 | retry後S1と旧removed再発なしの列なし |
| S5 | 未確認 | 未確認 | 60 FPS player診断にID露出なし。全条件・両FPS不足 |
| O1 | 未確認 | 未確認 | 収録カウンタは121/241で上限内。数え方を含むテスト本文なし |
| O2 | 未確認 | 未確認 | 間隔0.5/10のイベント・結果比較なし |
| O3 | 未確認 | 未確認 | 既定実装値は確認。変更前出力比較なし |
| O4 | 未確認 | 未確認 | deathと構造化3 attemptsのsummaryは整合。全終了条件の状態対照不足 |
| O5 | 未確認 | 未確認 | parserの範囲検証は確認。拒否実行出力なし |
| O6 | 未確認 | 未確認 | suiteは1200秒完了を報告。全出力とテスト本文がなく切断なしを独立確認できない |

### 同一試行の時間と後続判断

通常入力再生attempt 1の収録値は次のとおり。独立部屋の時間合算ではない。

| 項目 | 30 FPS | 60 FPS |
|---|---:|---:|
| ラン時刻 | 86.966667秒 | 103.533333秒 |
| 部屋1/2/3/4/5 | 6.633333 / 20.733333 / 15.633333 / 18.333333 / 21.633333秒 | 9.616667 / 25.066667 / 15.016667 / 16.966667 / 32.866667秒 |
| 遷移 | 4回、各1秒 | 4回、各1秒 |
| pause | 2秒 | 2秒 |
| driver経過 | 120秒 | 120秒 |
| 終端待機 | 31.033333秒 | 14.466667秒 |
| boss入場hearts／hurt | 3／0 | 3／0 |
| 攻撃／boss命中／dash | 41／12／34 | 41／12／45 |

部屋時間＋遷移はラン時刻、ラン時刻＋pause＋終端待機はdriver経過に一致する。retryは勝利後と死亡後の2回。attempt 2は自然死亡、attempt 3はunfinishedである。

15〜20分Visionとの差はDesignerへ保持する。人間の体験時間と同一視せず、新たな秒数ゲートは設けない。

### 具体的な供給不足

59が要求する追加実行に対して、packetは最初から0 roundsである。また以下が欠けている。

1. `repo/tests/*.py`全本文。個別テストの条件・assert・対応IDを読むために必要。
2. Round 2/3の省略されていないログと、公開連続入力再生の両FPS・両view完全出力。
3. 保存ソース識別を独立算出し、不足fixtureと公開再生を実行できる枠。
4. L1/O3等の変更前比較に使える基線出力、または比較可能な保存ソース。
5. 完全ログと検証入力を永続参照できる供給経路。今回の許可書込先はhandoff一件だけである。

これは実機ホストやgamepad供給の要求ではない。明確な基準未定義を示す所見もない。今回をpartialとしない理由は、継続に必要な入力・実行枠が具体的に欠けているためである。

## Decisions already made

- D-017：二攻撃、境界、終端、pause・retry・時刻の契約を保持。
- D-019：旧集計を終了し、保持回帰・条件付きbot比較・実測後Designer判断を要求。
- D-021：今回の対象はテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。

## Constraints

- 製品コード・仕様は変更していない。
- 未確認をpassにしない。静的確認、収録実行、fixture、生成入力再生、bot、独立Playを区別する。
- ボスbotの比較条件の所見を、戦闘難度やゲーム本体の再現済み不具合へ拡張しない。
- 新たな難度・秒数ゲートを置かない。
- QA結果・期待値・Review用体験信号を独立Play資料へ転記しない。

## Open questions

1. tests本文、完全ログ、追加実行枠を次の独立QAへ供給できるか。
2. ボスbotのactive残時間参照を、公開情報だけに基づく試験道具としてどう扱うか。整理後の両FPS・hearts 3/2再測定が必要。
3. 変更前一致を要求するL1/O3等について、比較基線を供給できるか。

## Expected output

Studioは供給不足を解消して独立QAを再ルートする。ボスbot所見は試験道具の担当へ渡し、公開情報限定条件を満たす具体的な経路と再測定証拠を用意する。

次のQAは保存source_idを独立算出し、tests本文のassertを基準に対応付け、不足条件を両FPSで実行する。旧未来入力破棄は新attemptが旧入力時刻を越える条件、または破棄列の直接観測で証明する。

全基準合格後に限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewへ進める。本Stepでは合格ルートへ進めない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/tests/*.py（次Stepでは本文を必ず供給）
- Project: 今回の@run-results、および省略のないログ・入力・基線比較資料
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/59-studio-to-qa.md
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

<<<FILE decisions/D-021-owner-authorizes-text-build.md
---
kind: decision
id: D-021
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-20
supersedes: D-020
---
# D-021: テキストビルドとStudio内検証でBuildへ進む

## Decision

Ownerは22の案Aを選択し、供給・検証・予算の回答権限者をすべてOwnerとした。実機ホスト・実gamepad・外部配員を今回の開始条件から除き、既存のテキスト表示とスクリプト実行によるBuildを承認した。

Ownerの回答全文：

> 案A。回答の権限者はすべて Owner（私）で、ここで回答します。(1) 実行経路: project.md の build: と run_tests / run_play / run_trace / run_bots がそのまま実行経路です。gameplay-engineer と qa は Step の中で @run を使い、サンドボックスでテスト・プレイ・トレース・ボットを実行できます（G-001 と同じ）。基線は repo/ の現状で、指定 sha の確認は不要です。project.md の「build 0.4」は古い記述で、repo/ が正です。(2) 実機・gamepad・デスクトップの表示環境はなく、用意もしません。Constraints の「Desktop, keyboard and gamepad」は製品の対象環境で、今回の検証環境の要求ではありません。検証は G-001 と同じく、テキスト表示のビルドとスクリプト実行で行います。(3) 独立した QA と Play は、Studio の qa と playtester の Step が担います。外部の配員はありません。(4) 費用: 購入・外部委託・追加の金銭は一切ありません。予算は Studio の通常の Step の範囲で、人日の見積もりは不要です。以上で D-020 の条件は満たされたものとして、Build へ進んでください。

実行基線は作業開始時のrepo/とし、指定shaとの照合は要求しない。project.mdのbuild 0.4表記は基線の根拠にしない。購入・外部委託・追加金銭支出は認めない。人日見積もりや外部検証枠の取得を開始条件にしない。

D-020に代わる開始条件として本Decisionを適用する。D-020に由来する実機ホスト、実gamepad、外部配員、費用見積もり取得の要求は後続計画より本Decisionを優先する。D-015〜D-019のゲーム体験、共有戦闘回帰、30/60 FPS、実測後Designer判断は維持する。独立QA・限定Art Verify・独立PlayはStudio内の別Stepで行う。

これはOwnerによる開始許可と検証範囲の変更であり、実行成功、受け入れ基準合格、体験Goal達成の証拠ではない。

## Rationale

Owner自身から不足していた供給・実行経路・予算方針への回答があり、今回の検証をG-001と同じテキストビルド方式に限定した。Studioが同じ供給確認を繰り返す必要はなく、既存仕様・計画に基づくBuildへ進める。

## Alternatives considered

- 実機ホストと実gamepadを用意する：Ownerが用意しないと明示したため採らない。
- 見積もり・調達条件を取得する案B：追加金銭を使わず通常Step内で進めるため採らない。
- 条件整備まで停止する案C：OwnerがBuild開始を明示したため採らない。

## Revisit when

通常のStudio Stepでは実行できない具体的な障害、追加支出の必要性、またはテキスト方式では仕様の意味を定められない矛盾が判明したとき。製品の実機対応を検証する別のGoalを開始するとき。
>>>END

<<<FILE decisions/D-022-g002-v1-supplements.md
---
kind: decision
id: D-022
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-022: V1補足の確定（旧経路表示、弾ID・消滅理由、長時間観測）

## Decision

詳細は`design/final-boss-and-continuous-run.md`§11。D-017の契約、第1〜4部屋、共有戦闘規則は変更しない。

1. 旧経路のボス表示：現行manualの注記を受け入れる。§6の完全表示は公開ドライバの経路に適用し、旧経路を委譲しない（旧60秒挙動を保つ）。旧経路`room 5`のplayer viewだけに誤認防止の注記1行を先頭に出す。
2. 弾IDと消滅理由：trace viewと公開ドライバのイベントログに限り要求する。ID `S<n>`、消滅は弾1個につき1回、理由は`lifetime`／`edge`／`hit`／`absorbed`／`cleared`。player viewの文言は変更しない。
3. 長時間観測：`view-every`と`trace-every <seconds>`で周期出力の間隔を指定でき、既定は変更しない。終了時に要約を出す。周期出力の行数に上限を置く。間隔指定は結果に影響しない。

## Rationale

最小の変更でD-017とG-002の検証要求を満たす。旧経路を変えるとD-017／D-021で承認した範囲外の挙動変更になる。ボスの弾は最大1個で、player viewでは数と既存メッセージで足りるため、IDは検証用のtraceに限る。20分の実行では0.5秒周期の描画が大量になるため、間隔指定で量を制限する。

## Alternatives considered

- 旧経路にも完全なボス表示を出す：旧60秒挙動とPlayer.describeを変えるため不採択。
- 注記なしで現状維持：旧経路でボス部屋を見た利用者が表示の欠落を契約違反と誤認するため不採択。
- player viewにIDと消滅文言を出す：読み取りを増やさず、既存文言の保持（step94）を乱すため不採択。
- 長時間は`trace-every frame`のみ：20分では出力が膨大で検証に使えないため不採択。

## Revisit when

旧経路でボスを観測する利用が多く、注記では不足とわかった場合。独立QAでIDや消滅理由の不足が出た場合。20分実行で周期間隔の指定だけでは出力が扱えない場合。
>>>END

<<<FILE decisions/D-023-owner-confirms-verification-supply.md
---
kind: decision
id: D-023
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-023: 実際の供給上限に合わせてテキスト検証を継続する

## Decision

Ownerは63の案Aを選び、D-021を維持して進めると決定した。ただし、利用可能な供給は以下に限られる。

- Loadに個別指定したファイルは本文が届く。ディレクトリ指定では中のファイル名だけが届く。
- Stepは@needを一度、最大8ファイルまで使用できる。
- @runは1 Stepにつき最大3回。別の実行枠はない。
- 実行結果は先頭と末尾を含む最大2万字。全文保存先はない。長い出力は確認対象の行を出すスクリプトで絞る。
- 変更前ビルドは保存されていない。変更前一致の基準について、記録数値との比較にするか、確認不能として扱うかはGame Designerが決める。

案Aに記載された全文保存・再閲覧機構の新設は実行条件としない。利用可能な出力から何を検証できるかは各担当Roleが判断し、未確認を合格として扱わない。製品仕様、難度、秒数ゲート、Goal達成の判断を本Decisionで変更しない。

Ownerの原文：

> 案A。供給の事実を答えます。(1) 本文: Load に書いたファイルは本文が届きます。ディレクトリ（repo/ など）を書くと本文は届かず、中のファイル名だけが届きます。足りない本文は、Step が @need で 1 回、8 ファイルまで追加で求められます。Route は、検証に要るテストなどのファイルを 1 つずつ Load に書いてください。(2) 実行: 1 回の Step で @run を 3 回まで使えます。別の実行の枠はありません。(3) ログ: 実行結果は先頭と末尾を含む 2 万字までで、全文の保存先はありません。長い出力は、確かめたい行だけを出すスクリプトで絞ってください。(4) 変更前のビルドは保存されていません。変更前との一致を求める基準は、記録にある数値と比べるか、確かめられないものとして扱うかを Designer が決めてください。以上の範囲で、D-021 のまま進めてください。

## Rationale

Ownerが利用可能な供給条件を確定した。存在しない実行枠、保存機構、変更前ビルドを待つ反復を止め、本文の個別指定、出力の絞り込み、必要な直列分割で進める。変更前一致の扱いは、指定された仕様責任者の判断を先行させる。

## Alternatives considered

- 案BのGoal縮小：Ownerは選択していない。検証未完了を理由にStudioが範囲や基準を免除しない。
- 案Cの停止：Ownerは継続を指示した。
- 全文保存先や変更前ビルドの供給を再要求する：確定した供給事実と合わないため採らない。

## Revisit when

担当Roleが、出力の絞り込みや直列分割でも必要な判断を成立させられない具体的な理由を示した場合。または供給条件が変わった場合。変更前一致の個別基準の扱いは、まずGame Designerが判断する。
>>>END

<<<FILE decisions/D-024-g002-historical-comparison-evidence.md
---
kind: decision
id: D-024
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-024: 変更前一致要求の証拠と確認不能の扱い

## Decision

D-023の委任に従い、変更前ビルドが存在しないG-002の比較基準を個別に確定する。詳細な適用表と比較条件は`design/g002-historical-comparison-evidence.md`を正本とする。

1. L1の注記以外の変更前出力・結果・終了時刻の一致、O3の変更前出力一致、step68 V-cの旧出力一致、step94 W7の変更前挙動一致は、対応する比較原本・必要な測定記録がなく、確認不能として残す。現行実装内の比較やsuite成功で置き換えない。
2. 独立1〜4のdodger成績については、40の記録数値との比較を採択する。これは保存ソース`5145454ab956`の記録との比較であり、ボス対応前の実装・方針との一致証明ではない。56の保存ソース`04fa2b1c168a`の報告は後続の補助記録として区別する。
3. 時間は40の小数1桁の報告精度へ丸めて比較し、結果・hearts lost・dash回数は記録値と比較する。記録のない行動列・位置・照準・未丸め時間の一致は確認不能とする。記録差はEngineerが条件と変更影響を整理しDesignerへ返し、製品の規則違反とは区別する。
4. 現行仕様へ直接照合できる要求と、同一現行ビルド内の対照試験は引き続き検証する。歴史的一致の確認不能によって、60秒上限、既定0.5秒、共有戦闘、公開文字列、FPS比較等を免除しない。
5. 非公開active残時間に依存する既報のボスbot数値、およびそれから生成した通常ラン入力・時間は診断資料に留め、新たな合格基線にしない。対応後に再測定する。

確認不能は合格、免除、適用終了、Goal達成を意味しない。QAは該当部分を他の検証結果から分離して記録する。全基準passを前提とする後続工程については、Studioが未解決部分を明示して扱う。Goalの再解釈や範囲縮小が必要になればGame Directorへ戻し、Designerが決定しない。

## Rationale

出力全文の同一性は少数の数値から復元できない。一方、独立1〜4のdodgerには、FPS・開始条件・limit・部屋別結果が明記された数値記録があり、その精度に限定した比較は成立する。

現行実装の注記を抑制した比較や、既定値と明示値の比較は現在の挙動を検証できるが、保存されていない過去実装を再現しない。

## Alternatives considered

- 現行suite成功で変更前一致も合格とする：比較対象がないため不採択。
- 全項目を記録数値比較にする：L1等の出力・行動の同一性に必要な記録がないため不採択。
- 全項目を確認不能とする：独立1〜4の記録精度で成立する比較まで捨てるため不採択。
- 基線不在を理由に仕様・難度・秒数ゲートを変更する：D-023の委任範囲外であり不採択。

## Revisit when

由来・入力・測定条件を確認できる追加の過去記録が届いた場合。記録比較で差が出た場合。確認不能部分がGoalの最終判断を妨げ、方向・範囲の判断が必要になった場合。
>>>END

<<<FILE goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 76
from: gameplay-engineer
to: studio
stage: Route
outcome: partial
---
# 76: gameplay-engineer → studio — 再生互換診断を保存、E1の分割・再計画へ

## Task

E1連続partialの3回目としてTechnical Directorへ分割・再計画を戻す。公開境界の実接続、互換失敗の原因確定、記憶・全分岐・判断本文を完了単位へ分ける。E2以降は開かない。

## Context

75を受領した。保存済み出発点はsource b0770a4180c9、159 tests OK。72・74がE1 partialで、70のE0 partialは回数に含めない。60のfailを維持する。

packet内Round 1は未保存のtest_split_c.py案を実行したsource 9b4f6722e7df、160 tests OKである。実dodgerは旧経路のままであり、公開境界接続案の成功を意味しない。

## Findings

### 保存変更と挙動範囲

変更は次の2ファイル。製品・botの行動変更はない。

- repo/tests/test_split_c.py：test_generated_inputs_replay_without_controlsを追加。
- repo/tests/test_g002_evidence.py：窓helperの自己試験で捕捉・assertした本文を外側へ再表示する。

前者はpacketの未保存案を基に、比較状態へheading、facing、dash、cooldown、stun、攻撃recovery、保護、敵phase・timer・aim・接触消費状態を追加した。この内部観測は診断専用で、判断入力へ戻さない。今回の保存集合は9b4f6722e7dfと異なる。最終source_id・結果はruntime Build checkで識別する。

既存assert・既存対象集合は削除・緩和していない。未保存の接続案eddd95dd5926／189dbf689d7eは採用していない。

### 再生互換診断の再現とassert

追加完全ID：

test_split_c.SplitCTest.test_generated_inputs_replay_without_controls

両FPSについて、通常初期状態、開始3 hearts、mode run、limit 1200、driver-limit 1205で実施する。生成中は_Proxy.pressの全呼出を時刻・action・directionとして捕捉し、RunSession.step後の全フレームを記録する。生成側wonを要求する。

生成入力は小数12桁の時刻で公開構文へ変換し、play.read_scriptで解析する。入力件数・順序・ボタン一致、時刻差1e-9以内をassertする。再生はdriveでtimed inputsのみを使い、ライブbot・状態注入・pause・retryを使わない。全フレーム数と全記録状態の完全一致、再生clear、生成と再生のhurt件数一致をassertする。

出力列はfps、inputs、generated_frames、replayed_frames、first_difference、replay_hurts、generated_outcome、replay_outcome。FPSごとにemit_rowsで総1行・表示1行、BEGIN/END・列・除外を出す。first_differenceがあれば元集合のフレーム番号と両状態をassert前に出す。状態の位置とshot位置を含むが、接触直前後の実距離・消費専用列は未実装である。

この試験は同じ旧方針の生成・再生一致を切り分ける道具である。未保存接続案の被弾1の原因、公開境界適合、E5通常ラン受け入れの証明にはしない。

### 収録実行と表示の限界

固定コマンド：

```text
cd repo
python3 -m unittest discover -s tests
```

packet内Round 1はsource 9b4f6722e7df、160 tests OK。今回の比較項目追加前の集合である。INVENTORYは13ファイル・160IDを表示したが、後続には5335文字の切断がある。今回必要なEVIDENCE_BEGIN/ENDと診断行を収録本文で照合できず、生成・再生の具体的な一致本文は未確認とする。切断部分を推測で補わない。

今回新たな@run要求は出していない。最終集合の自己試験結果はruntime Build checkへ委ねる。予想discover数は保存済み159＋新規1＝160。件数成功で必要本文を代替しない。

識別対象はgame.py、session.py、play.py、run_driver.py、bots.py、source_id.pyとtests/*.pyの13ファイル、計19ファイル。Handoff・設計・manualは対象外。

### 公開フィールドと実経路監査の現状

prototypeの対応は維持する。

| 入力 | 公開対応 |
|---|---|
| t | room time |
| x,y,boss_x,boss_y | 既存sprites/Viewの連続位置観測 |
| phase,attack | Output.emitのboss status、next |
| aim,warning_left | warningのlocked方向・残時間 |
| shots | 実弾sprite位置 |
| lane,attack,warning_time | warning履歴 |

文字セルから連続座標を復元できたとはしない。

observe_bossとchoose_bossの限定監査は既存5IDが担当する。実dodgerは依然として_dangers→_threat→_escapeと_face_and_swing等の旧経路を使い、active chargeのphase_leftを読む。したがって公開情報限定は未成立である。直接呼出・_Proxy・play_room・play_runの実ボス判断を境界へ接続したとはしない。

warning記憶の実所有・寿命・入場/retry初期化、実経路の許可外参照禁止、両FPS・両攻撃の距離0・境界・端点・全壁・dash待ち・stun・履歴不足各方向、全判断番号・grid・公開入力・記憶由来・候補/除外・選択・実発行ボタンの統一記録は未完了。状態・判断の専用emit_rowsアダプタも残る。

### 窓helper確認本文

test_g002_evidence.EvidenceToolTest.test_bounded_selection_reports_missing_rangesは、3行中2番だけを表示し、total3/shown1、前後未表示各1、002 [2]、END、不正start拒否をassertする。今回、その捕捉本文をassert後に外側へ出すようにした。全件評価と表示窓の違いは維持する。この変更だけで判断列アダプタや出力欠落検査が完成したとはしない。

### 試験・QA配布台帳

13ファイルの割当は71のまま維持する。新規ファイル0、追加ID1、変更ファイル2。未割当ファイル0。既存159IDは維持する。

| QA | repo/tests/配下の配布ファイル |
|---|---|
| Q1 | test_bots_boss.py, test_g002_evidence.py, test_game.py, test_play_run_controls.py, test_split_c.py |
| Q2 | test_boss.py, test_boss_contract.py, test_boss_contract_details.py, test_d022_shots_and_note.py, test_g002_evidence.py |
| Q3 | test_boss_contract_details.py, test_g002_evidence.py, test_play_run_controls.py, test_run_driver.py, test_session.py, test_split_c.py, test_terminal.py |
| Q4 | test_bots_boss.py, test_d022_observation.py, test_d022_shots_and_note.py, test_g002_evidence.py, test_game.py, test_run_driver.py |
| Q5 | test_g002_evidence.py, test_game.py |
| Q6 | test_g002_evidence.py, test_game.py, test_split_c.py |

新規IDはQ1主担当、Q3・Q6にも配布する。変更したhelper試験はQ1〜Q6へ更新本文を配布する。既存追加5IDもQ1主担当・Q4への配布を保持する：

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches
- test_bots_boss.PublicBoundaryAuditTest.test_all_escape_candidates_are_enumerated
- test_bots_boss.PublicBoundaryAuditTest.test_adapter_rejects_forbidden_attribute_reads

### 再計画に渡す実装単位と依存

1. 接続単位：実dodgerのボス分岐を公開観測・記憶へ接続し、所有を直接呼出・_Proxy・部屋入場/retryで統一する。旧1〜4方針を維持する。
2. 互換診断単位：接続後、今回の全フレーム対照で入力解析差とシミュレーション差を分ける。既存pause/retry試験でのみ差が出るなら、その制御前後と被弾フレームの接触条件へ絞る。既存hits0を弱めない。
3. 監査単位：接続済み全経路のguard、不変性、記憶・全分岐をassertする。接続と独立したprototype成功を代用しない。
4. 証拠単位：判断番号・grid・省略を統一し、状態/判断アダプタで全件検査と表示窓を分ける。既存長文印字との出力予算も整理する。

1が2・3・4の実経路成立条件であり、2の解消と3・4の充足までE1完了とはしない。今回は診断道具とhelper本文露出を保存したが、接続と原因確定は未成立である。

70の後続残作業を保持する。E2実接触・消費診断、E3四条件再測定、E4正本との完全対応・未丸めhalf-up記録比較、E5入力再生成・通常到達・player対照・旧未来入力破棄、長時間出力の不足、独立Q1〜Q6、歴史的確認不能の工程判断、Art Verify、独立Play、Designer判断、Reviewは未完了。

### Sender assessment

旧経路用の再生互換診断を具体化した。接続案の被弾差の根因は確定していない。未保存案の切断出力を接合せず、保存済み基線から変更した。E1は連続partial3回目として再計画を要する。自己試験成功が得られても独立QAやGoal達成を意味しない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較。
- D-021・D-023：Studio内テキスト検証と確定供給上限を維持。
- D-022：表示・弾・長時間観測契約を維持。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離。
- 68：E1完了確認後にE2を別Handoffで開く。

## Constraints

製品仕様・戦闘パラメータ・難度・秒数ゲート・表示契約・Goal範囲を変更しない。60のfail、切断・未表示、歴史的確認不能を自己確認で上書きしない。既存assertを弱めない。

## Open questions

新しい仕様質問・Ownerへの供給質問はない。Technical Directorには上記4単位の依存と供給上限に適合する分割を求める。被弾差の根因は未確定の技術課題として残す。

## Expected output

StudioはE1連続partial3回目としてTechnical Directorへ分割・再計画を戻す。完了部分と未成立条件を維持し、E2以降・独立QAを先行させない。同じ供給質問をOwnerへ戻さない。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.5 s).

```text
c-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3419690530281514, "source_id": "e99408d647c7"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "e99408d647c7", "trial_count_per_room_fps": 1}
................................................................................................................................................................
----------------------------------------------------------------------
Ran 160 tests in 3.453s

OK
```

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/implement-change.md
- Project: repo/bots.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting handoff: goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
- Supporting handoff: goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
- Supporting handoff: goals/G-002-final-boss/74-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/75-studio-to-gameplay-engineer.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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
   short kebab-case slug, ISO dates) with its **budget**: the operations the Goal should need,
   about two per planned stage (its Step and the Route after it) plus room for one return. Then
   write the first Handoff `01-studio-to-<role>.md`; mark that
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
- **Budget.** The runtime counts a Goal's operations and shows them against `goal.md`'s budget.
  Once the budget is used, a Route adds no stages but one: a `game-director` step that cuts the
  remaining work to what the Owner request needs (scope within the Goal; the rest is then
  `skipped`), or an `owner` step that escalates the cost. Planned steps may still be opened, and
  the loop limits' re-plan steps give way to the scope decision. Only the Owner changes the
  budget, in a Resume.
- `partial` is not a question: nothing is missing, so route the rest of the work back to the same
  Role and never escalate for it. The same work handed back `partial` three times in a row →
  route to `technical-director` to split or re-plan it.
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/78-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
