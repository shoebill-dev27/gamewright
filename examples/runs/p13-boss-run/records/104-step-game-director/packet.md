# Studio operation packet

operation: Step
goal: G-002
role: game-director
incoming_handoff: goals/G-002-final-boss/83-studio-to-game-director.md
next_seq: 84
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-final-boss/84-game-director-to-<recipient>.md
- decisions/D-027-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

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

<<<FILE goals/G-002-final-boss/83-studio-to-game-director.md
---
kind: handoff
goal: G-002
seq: 83
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 83: studio → game-director — 残工程と残予算の不一致をOwner判断へ整える

## Task

82の残工程見積もりと残予算を照合し、費用・範囲についてOwnerが判断できるエスカレーションを準備する。既存の後続工程条件を再審議するStepではない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。D-025で重複工程を削減し、D-026でbudget 123を承認済み。現在87/123 operationsで残36。E1は未完了で、82は実装・測定を行わずA〜Dへの分割計画を提出した。

## Findings

82は残必須作業を22〜24 Stepと見積もる。各Step後のRouteを含め最低44〜48 operationsとなり、失敗修正・追加表示窓・本判断とOwner Resume等を含める前から残36を超える。

82の「まずAだけを開始」という推奨より先に、同報告の停止条件「残必須工程が上限内に収まらない具体的見通しが出た場合」を適用する。これはStudioによる工程数の照合であり、技術見積もりの確定やゲーム範囲の変更ではない。

E1のA〜D、E2〜E5、独立Q1〜Q6、限定Art Verify、独立Play、Designer実測後判断、Reviewは未完了。Aもまだ開いていない。必須評価を省いてGoal達成とする根拠はない。

## Decisions already made

- D-021・D-023：Studio内のテキスト検証と現実の供給上限で進める。
- D-024：歴史的一致の確認不能を現行検証・記録比較と分離する。
- D-025：必須検証と独立評価を維持し、重複工程を省く。
- D-026：budget 123。完成保証ではなく、追加継続はOwner判断。

## Constraints

StudioもGame Directorも予算を変更しない。必須検証の免除やGoal解釈の変更を既存承認に読み込まない。

存在しない環境・外部スタッフ・変更前ビルド・全文保存先を求めない。購入や外部委託は提案の前提にしない。すでに省略した重複工程を再追加しない。

まだ上限到達ではないが、費用見通しが具体化したため判断する。依存Buildは判断まで保留する。

## Open questions

- 82の必須成果を保ったまま、既存の供給上限とRole分離を守って残36以内へ収められる、根拠ある工程削減があるか。
- それが示せない場合、追加operationsでの継続と、未達を明示した打切りをどうOwnerへ提示するか。

## Expected output

原則として日本語のOwner向けEscalationを作成し、studioへ返す。追加継続と未達打切りの選択肢、推奨、各選択後の経路を示す。

追加継続案ではStepとRouteをともに数え、見積もりと失敗・表示継続の余裕を分け、完成保証ではないと明示する。追加予算はOwnerが決める。

残36以内で必須成果を維持できると判断する場合は、単なる期待ではなく、担当Role・依存・StepとRouteの総数・供給上限への適合を具体的に示してstudioへ返す。技術計画を独自に置換せず、技術判断が必要な点を明記する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
- Previous handoff: goals/G-002-final-boss/82-technical-director-to-studio.md
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
budget: 123
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
- Build（試験道具・再測定）：未完了。80で突進被弾をshot診断から分離し、両FPSの通常命中fixtureを保存。runtimeはsource fc07c7db6383の161 tests OKを確認した。実dodger接続、被弾差の原因確定、記憶・全分岐・判断出力は未完了で、E1は72・74・76・80とpartialが続く。生成・再生の必要本文は切断により未確認。13ファイルのQA配布台帳と80の追加IDを維持する。E2全体・E3以降は未実施。
- Plan（E1分割・再計画）：done。82でE1をA出力整備→B実接続・記憶→C差分分類→D実経路監査へ分割。未実装・未測定であり、全項目完了までE2へ進めない。
- Decide（残工程と予算）：open。82の見積もりは必須作業だけで22〜24 Step。各Step後のRouteを含め最低44〜48 operationsとなり、現在87/123の残36を超える。Game Directorが費用・範囲のOwner判断に必要なbriefを準備する。予算、必須検証、Goal解釈は変更しない。
- Decide（予算超過時の範囲）：done。D-025の削減を適用。重複する後続条件判断、存在しない資料の再探索、旧構成の任意検証、重複整形と追加の磨き込みは省く。必須検証と独立評価は維持する。
- Decide（追加予算）：done。Ownerは案Aを選択。D-026によりResume時点の累計83に40を加えbudget: 123とする。上限を使い切ったら範囲か費用をOwnerへ再確認する。完成保証ではない。
- Decide（後続工程条件）：skipped。D-025による既存判断を適用し、同じ条件判断だけの別Stepは開かない。歴史的確認不能以外の必須不足を解消して後続評価へ進む。確認不能は最終Reviewへ残し、合格・免除やGoal達成に読み替えない。
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
| 7b-scope | Decide | game-director | make-decision, prepare-owner-escalation | done | 77-studio-to-game-director.md → 結果: 78-game-director-to-owner.md |
| 7b-cost | Decide | owner | — | done | 78-game-director-to-owner.md → D-026 |
| 7b-build | Build | gameplay-engineer | implement-change | done | 79-studio-to-gameplay-engineer.md → 結果: 80-gameplay-engineer-to-studio.md（partial、突進診断の限定修正） |
| 7b-replan | Plan | technical-director | technical-plan | done | 81-studio-to-technical-director.md → 結果: 82-technical-director-to-studio.md |
| 7b-budget | Decide | game-director | prepare-owner-escalation | open | 83-studio-to-game-director.md（残工程の費用・範囲brief） |
| 7b-e1-A | Build | gameplay-engineer | implement-change | planned | 82のA。費用・範囲判断後に開始 |
| 7b-e1-B | Build | gameplay-engineer | implement-change | planned | 82のB。A完了後 |
| 7b-e1-C | Build | gameplay-engineer | implement-change | planned | 82のC。Bの保存接続集合または具体的失敗を受ける |
| 7b-e1-D | Build | gameplay-engineer | implement-change | planned | 82のD。B・C後 |
| 7c | Verify | qa | verify-change | planned | E0の全試験台帳を使い68のQ1〜Q6を直列分割 |
| 7d | Decide | game-director | make-decision, prepare-owner-escalation | skipped | D-025により重複条件判断を省略 |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

D-026によりD-025の範囲を維持する。82のE1分割計画を受領したが、必須作業の見積もりにRouteを加えると残予算を超えるため、83でGame Directorへ費用・範囲briefを依頼する。判断まではAを含む依存Buildを開かない。独立QA、限定Art Verify、独立Play、Designer判断、Reviewは削除しない。歴史的一致の確認不能を合格や免除にしない。

## Route changes

82を受領して81を完了記録し、E1のA〜D分割を採用する。現在87/123、残36に対し、82の必須22〜24 StepはRoute込み最低44〜48 operations。上限内に収まらない具体的見通しが出たため、A開始に先立ち83でGame Directorへ費用・範囲briefを戻す。必須検証・予算・達成条件は変更しない。

## Next action

Game Directorが83-studio-to-game-director.mdで残工程と残予算の不一致を評価し、Owner向け費用・範囲エスカレーションをstudioへ返す。依存Buildは保留。

## Outcome

未完了・継続中。OwnerはD-026でD-025の範囲とbudget: 123を承認した。連続ランと最終ボスは実装報告済みだが、公開情報限定の実dodger接続、被弾差の原因確定、必須証拠、独立QA・体験評価は未完了。source fc07c7db6383の161件の試験成功を独立検証やGoal達成とは扱わない。歴史的一致の確認不能と15〜20分Visionの未評価を保持する。追加40 operationsは完成保証ではなく、上限到達時は範囲か費用をOwnerへ再確認する。
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

<<<FILE decisions/D-025-g002-minimum-remaining-scope.md
---
kind: decision
id: D-025
status: accepted
decided_by: game-director
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-025: 必須の体験検証を残し、重複工程を省く

## Decision

Owner request「最後に手応えのあるボス戦がほしい」とD-015〜D-024を維持する。以下は残作業の範囲判断であり、予算変更、技術方式、仕様変更、QA判定、Goal達成判定ではない。継続費用は78のOwner判断へ戻す。

### 継続必須

| 残す対象 | 必要な理由・終了条件 |
|---|---|
| 実dodgerの公開情報限定対応 | D-019の比較成立条件。実経路の接続、記憶の所有・初期化、全分岐と共有補助経路の監査、判断根拠・実発行入力の証拠が必要。prototype成功では終了しない |
| 接続案の被弾差と接触診断 | 原因未確定を残して旧成績を保証できない。生成・再生差、実接触、保護、消費、被弾を区別し、該当仕様への適合を確認する。旧無被弾値への調整を目的にしない |
| ボス4条件の再測定 | 開始3/2 hearts別に30/60 FPSを比較する。公開情報条件を満たす同一方針・同一ビルドで測り、判断列と結果を揃える。不一致は規定の判断先へ返す |
| 保持回帰と記録比較 | 第1〜4部屋と共有戦闘を維持する承認条件。D-024の精度で比較し、差へのDesigner回答を残す |
| 通常ランの公開入力再生成・再生 | 到達、勝敗、pause、retryと時間はOwnerが承認した一体の体験。状態注入なしの連続到達と、制御された境界試験を区別して確認する |
| 独立QA | 60のfailは未解消。68のQ1〜Q6が担う基準、全試験本文の配布・照合、両FPSの必要観測を維持する。実装者の成功報告では置換しない |
| 限定Art Verify・独立Play | D-021の別Stepを維持する。テキストの読み取りと最終戦・到達・再挑戦の体験を、それぞれの担当が評価する |
| Designer実測後判断・Review | D-019に基づく追加ゲート・調整の要否と時間Visionへの回答を記録し、その後Game Directorが体験Goalを判断する |

依存は68を維持する。公開情報対応・診断→再測定・保持回帰→公開再生→独立QA→限定Art Verify→独立Play→Designer実測後判断→Review。具体的な分割・実装方式は本Decisionでは選ばない。表示修正等が入った場合は影響する検証を再実行する。

### 省略する対象

1. **別Stepとして予定された「歴史的確認不能を保持した後続工程条件判断」**を省く。本Decisionで次の条件を確定するため、同じ問いを再度Game Directorへ回さない。
2. **変更前ビルド・過去全文・保存先の再探索と再照会**を行わない。供給事実とD-024で既に整理済みであり、現在のGoal達成に新しい証拠を加えない。
3. **旧第5部屋fixtureの新設・拡充、適用終了した旧集計の再測定**を必須成果にしない。共有回帰の保持対象と置換先は削らない。
4. **既に確認できた同一条件の証拠を、帳票の統一や見栄えだけのために再生成する作業**を省く。対象ソース、条件、基準、観測範囲が追跡できる既存証拠は参照する。未表示本文、必要な全判断列、変更の影響範囲の再実行は削らない。
5. **限定Art Verifyを越える素材制作・表示演出の磨き込み、追加攻撃・形態・成長要素**を残作業へ加えない。可読性の契約違反や体験上の必須修正は別である。

### 歴史的確認不能を残す評価継続の条件

独立QAが現行必須検証・現行内対照を完了し、公開情報条件、再測定、保持回帰、通常ランの証拠が揃い、記録差へのDesigner回答があり、歴史比較以外の不足が解消した場合に限り、限定Art Verify以降へ進める。

D-024の歴史的確認不能は一覧のままReviewへ渡す。この条件は全基準passへの変更でも、確認不能の免除でもない。その他の未実行・未表示・不適合が残る場合には適用しない。Studioが条件充足を各担当の報告で照合し、条件を満たさない事実や新しい判断事項があれば適切なRoleへ戻す。

### 終了条件

必要な独立検証と体験観察、Designer判断を揃え、歴史的確認不能・その他の残課題を明示してReviewへ渡す。Reviewは達成を保証しない。Visionと整合せず承認範囲で解消できない場合はOwnerへ戻す。

追加予算の上限に達した場合は新たな作業を開かず、完了・未完了と残る判断をOwnerへ返す。未完了を合格に変更して終了しない。

## Rationale

手応えのある最終戦には、読み取れる危害、回避後の反撃、道中からの到達、再挑戦が必要である。残る技術課題と独立検証は、その成立を確かめるためのものであり、件数成功だけでは削れない。

削減できるのは、既に判断できる工程条件の再審議、存在しない資料の探索、旧構成の任意検証、証拠の重複整形、追加の磨き込みである。この削減だけで80/40 operationsの超過を吸収できる根拠はない。

## Alternatives considered

- 従来工程を全てそのまま再掲する：重複する工程条件判断と任意作業を残すため不採択。
- 公開情報bot、保持回帰、独立QA・Playを省く：既存Decisionと承認された体験検証を損なうため不採択。
- 単体ボスのみへ縮小する：D-015とGoal解釈の変更になるため本権限では採らない。
- 現行suite成功で完了とする：60の未解消事項と体験評価を置換できないため不採択。

## Revisit when

必須作業が供給上限内では成立しない具体的な理由、新たな規則違反、承認範囲で解消できない体験・Vision不整合が判明した場合。またはOwnerが継続費用・範囲について判断した場合。
>>>END

<<<FILE decisions/D-026-owner-extends-g002-budget.md
---
kind: decision
id: D-026
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-026: D-025の範囲で継続し、予算を123 operationsとする

## Decision

Ownerは78の案Aを選択した。D-025で絞った範囲でG-002を継続し、Resume時点の累計83 operationsに40を加え、予算を123 operationsとする。

Ownerの回答原文：

> 案A。D-025 で絞った範囲で続けてください。予算は、Resume 時点の累計（83 operations）に 40 を足した budget: 123 とします。それを使い切ったら、また範囲か費用を Owner に確認してください。

追加40 operationsは完成保証ではない。予算を使い切った場合、さらに作業を継続する前に、範囲または費用をOwnerへ確認する。追加金銭・環境・保存先の供給を承認するものではない。

必須検証と独立評価を維持する。歴史的一致の確認不能を合格・免除とせず、現行検証の完了だけでGoal達成とはしない。

## Rationale

Ownerは、実装報告済みの連続ランと最終ボスについて、未完了の成立確認と体験評価を上限付きで継続することを選択した。

## Alternatives considered

- 案B：未達・検証未完了で打ち切る。Ownerは選択しなかった。
- 無制限の継続：承認されていない。

## Revisit when

budget: 123を使い切ったとき。上限前でも、承認範囲を超える変更やOwner権限の判断が必要になった場合は再度エスカレーションする。
>>>END

<<<FILE goals/G-002-final-boss/82-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 82
from: technical-director
to: studio
stage: Route
outcome: done
---
# 82: technical-director → studio — E1を出力整備・実接続・差分診断・監査へ分割

## Task

E1残作業を下記A→B→C→Dの直列Engineer Stepとしてルートする。各単位の完了を個別に記録し、A〜Dが揃ってからE2へ進む。

今回作成したのは技術計画のみである。コード実装、実行、測定、独立QA判定は行っていない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。E1は72・74・76・80でpartialとなり、実dodgerの公開情報境界への接続は未完了である。

81時点の累計は85/123 operations。D-025の必須成果と省略対象、D-026の上限を維持する。本計画は68のE1分割・診断順序を置き換え、E2以降の必須内容を維持する。歴史的確認不能を保持した後続工程条件は再審議しない。

## Findings

### 1. 確認事実と停滞要因

供給本文から確認した実装状態：

- `dodger`は`_threat`を先に呼び、`_dangers`はactive chargeの内部`phase_left`を読む。
- `observe_boss`と`choose_boss`は存在するが、実dodgerから呼ばれていない。既存guard試験も主にprototypeを対象としている。
- `Brain`は反応時計を所有するが、ボス記憶の所有者はまだない。`play_run`はgeneration変更でBrainを再生成する一方、直接呼出と`_Proxy`を含む記憶の扱いは未実装である。
- `test_generated_inputs_replay_without_controls`は生成・再生の全フレーム比較を持つ。しかし必要な`E1/input-replay`本文は切断により未確認である。
- 既存suiteは棚卸し、SPLIT_C_BOSS、SPLIT_C_PUBLIC等を同時に長く印字する。窓helperだけではsuite全体の出力競合を防げない。
- 80のsource `fc07c7db6383`、161 tests、exit 0は既報のruntime自己確認である。突進被弾ログの通常命中fixtureは確認済みだが、接続案の被弾差の根因ではない。

作業分割上の問題は、実接続・記憶・全監査・互換性・全判断本文を一つのE1完了条件にまとめながら、出力競合を先に解消しなかった点にある。また、接続後の方針変更と、生成／再生・制御列の差を分ける判別点が実行単位として固定されていなかった。

これは本文からの技術評価であり、過去の未保存接続案の失敗原因を確定したものではない。

### 2. 共通実行・出力契約

全単位を直列とする。bot、入力生成、再生、試験変更が同じsource_idへ連鎖するため、並列変更は行わない。

固定実行は引き続き：

```text
python3 -m unittest discover -s tests
```

各Stepは最大3回。通常は第1回を対象確認、第2回を修正確認、第3回を不足本文に使い、必要がなければ使い切らない。traceは完全な公開入力を提示できる場合だけ使い、任意Pythonや別bot実行枠を仮定しない。

Aで、既存印字を呼出側で対象選択できるよう整える。全試験・全assertは毎回実行する。表示対象の選択を試験実行の省略や失敗隠蔽に使わない。

各実行は次を満たす。

- 予定出力は全体で概ね12,000字以内。対象以外の大きな成功印字は抑え、失敗情報は残す。
- 対象名、source_id、条件、列定義、総件数、表示窓、連番、BEGIN/ENDを出す。
- 判定前に出す失敗診断は、最初の差とその近傍へ限定する。巨大な状態配列全体を1行にしない。
- BEGIN/ENDまたは予定連番が欠けた範囲は未確認とする。suite成功で補わない。
- 同一条件の再実行を接合するときはsource_id、入力、件数、結果を照合する。異なる集合は別証拠とする。
- 全判断列は省略せず、短い行と固定窓で表示する。監査の全件assertと表示済み範囲は別に記録する。

### 3. 順序付き実行単位

#### A：出力競合の解消と保存済み再生診断の本文回収

入力：
現行`test_split_c.py`、`test_g002_evidence.py`、70・76・80。botは接続しない。

変更対象：
`repo/tests/test_split_c.py`、`repo/tests/test_g002_evidence.py`。必要な棚卸し印字の選択もこの2ファイル内で行う。試験対象・assertは維持する。

作業：
既存の長文成功出力を対象別に選択し、まず旧経路の`E1/input-replay`両FPSを完全に表示する。選択設定は試験内の明示値とし、使用値を出力する。入力完全性、全フレーム比較、生成・再生hurt数比較は既存試験を再利用する。

実行配分：

1. tests：出力道具と30/60 FPSのno-controls診断。
2. tests：切断・差があった対象だけの修正確認。
3. tests：必要な残本文のみ。

完了条件：
両FPSのBEGIN、診断行、END、全フレーム比較の結果が受信でき、後続で対象を選択する具体的方法が本文に残ること。旧方針での一致を公開方針の証明にしない。

失敗時：
生成側が勝てない、または最初の差がある場合は、その条件・フレームをStudioへ返す。切断だけなら行幅・対象窓を直して再実行し、同じ全量出力を繰り返さない。

#### B：実dodger接続と記憶所有の確立

入力：
Aの出力方法、現行6ソース、公開情報仕様、prototype試験。

変更対象：
主に`repo/bots.py`、`repo/tests/test_bots_boss.py`。`test_split_c.py`は接続による旧ログ表現依存の照合に限る。

実装方針：

- ボス分岐を旧`_threat`等より前に置く。ボス判断は観測値と記憶から選択し、そのボタン列だけを発行してreturnする。
- ボス分岐から旧`_dangers`、`_face_and_swing`等へ戻らない。
- 記憶は一つの明示的な判断状態に持たせる。モジュール全体の共有記憶は使わない。
- 現在のGameを記憶の寿命境界とする方式を第一案とする。直接呼出でも同じGameで保持し、新Gameで初期化する。`_Proxy`の一時属性に記憶を取り残さず、現在のGameへ所有を統一する。
- `play_room`の新規Game、`play_run`の部屋入場・retryではfresh記憶となる。pauseでは保持し、recovery・ボス不在では仕様に従って解除する。
- 0.15秒反応時計は既存Brainを保持する。直接呼出の単体試験とdriverの反応間隔を区別する。
- CLIの方針説明を実際の接続状態・方針版へ合わせる。

実行配分：

1. tests：直接呼出、play_room、_Proxy/play_runの実接続、記憶保持・新Game初期化。
2. tests：接続後no-controls生成／再生両FPS。
3. tests：失敗が出た最初の対象とsuite確認。

完了条件：
実dodgerが境界を使うこと、各入口の記憶所有、旧1〜4経路への影響範囲がassertで示されること。B時点で全監査済みとはしない。

接続によって既存試験が失敗する場合、Bを完了扱いしない。接続案と短い失敗本文を@runで具体化し、3回で収束しなければ最初の失敗を記したquestionをStudioへ返す。未保存案を適合済みとして次へ渡さない。

#### C：被弾差を生成・再生・制御・方針へ分類する

入力：
保存された接続集合、Aの診断、80の突進ログ修正。Bの失敗で保存できない場合は、失敗の具体的な接続案と本文をStudioがこの単位へ供給する。

変更対象：
`repo/tests/test_split_c.py`、必要な診断に限る`repo/tests/test_bots_boss.py`。判断修正が必要なら`bots.py`。戦闘コードは診断結果なしに変更しない。

順序と判別：

1. no-controlsの入力件数・順序・解析時刻を比較する。差があれば入力記録／直列化／parserの問題として切り分ける。
2. 入力が同じなら、生成と公開再生の最初の状態差・フレーム数差を調べる。ボタン受理順、step順、境界時刻を比較する。
3. no-controlsが一致し、pause/retryありだけで差があれば、制御前後の入力・部屋・時刻・反応記憶を出す。既存7/10秒のpause位置、120/140秒retry、141秒driver-limitが新しい進行に適合するか確認する。
4. 生成・再生が同じ被弾をするなら、再生互換差ではなく方針と実接触の診断へ進む。判断時の公開入力・選択・実発行ボタンと、接触前後の位置、距離、保護、struck/spent、hurtを対照する。

実行配分：
第1回no-controls、第2回制御ありの最初の差、第3回その差の接触または入力処理の近傍。

完了条件：
既報の被弾差について、再現条件と分類、その根拠となる最初の差または一致が残ること。単に「ログ誤分類だった」とは結論しない。過去未保存案を再現できない場合、その過去原因は確認不能と明記し、保存接続集合で現在の差を分類する。

既存`hits == 0`は維持する。新方針で真に被弾する場合、旧成績に合わせる調整やassert削除を行わず、方針・接触の根拠を添えてDesignerへ戻す。固定制御時刻の不適合なら、観測した境界・終端から公開制御列を作る試験へ修正する。変更理由とassertの保持を明記し、E5全体の証明にはしない。

帯外の同条件差、時間・フェーズ等の規則違反はEngineer修正対象としてStudioへ返し、独立QAの判定対象に残す。比較閾値・許容帯の再判断はDesignerへ返す。

#### D：実経路の監査と判断本文の完了

入力：
B・C後の保存集合と解消結果。

変更対象：
`repo/bots.py`、`repo/tests/test_bots_boss.py`、`repo/tests/test_g002_evidence.py`。統合入口の試験が必要な場合は`test_split_c.py`。

試験対象：

- 実dodgerからの全ボス経路に許可外読取guardを適用する。
- 同じ公開入力でactive残時間・内部aim・struck/spentだけを変えても、記憶更新・選択・発行ボタンが一致する。
- 両攻撃・両FPSのwarning→active→recovery、距離0、射線端点、上下左右の壁、dash待ち、stun、省略、履歴なしactiveを検査する。
- 複数Gameの交互呼出で記憶が混ざらず、部屋入場・retryで初期化し、pauseで保持する。
- 共有補助経路への迂回禁止を試験する。prototypeだけのguard成功を代用しない。

全判断は番号、grid、時刻、公開入力、記憶の由来、候補、除外理由、選択、実発行ボタンを記録する。入力の受理／拒否は発行と区別する。内部診断は判断後の別経路で取得する。

実行配分：
第1回境界・全分岐、第2回記憶・入口、第3回判断本文の残窓。全判断本文が収まらなければ、変更を増やさず、残判断番号だけを次のEngineer Stepへ渡す。

完了条件：
監査対象一覧と全件assert、公開フィールドと表示の対応、全判断の表示済み範囲、実発行入力との一致が揃うこと。Cの未解決をDの成功で埋めない。

### 4. E1終了ゲートとE2以降への再利用

Studioは次の四項目を別々に照合する。

| 項目 | 終了根拠 |
|---|---|
| A | 保存済みno-controls診断の両FPS本文、出力競合の解消 |
| B | 実接続と全入口の記憶所有・初期化 |
| C | 保存接続集合での差の分類、失敗の解消または担当Roleの回答 |
| D | 実経路の全監査、全判断と実発行入力の本文 |

全項目が揃ってE1完了とする。実装者の確認であり独立QA合格ではない。

80の通常命中診断は保持し、同条件の帳票整形だけの再実行を要求しない。source変更の影響を照合する必要がある場合は該当assertを再実行する。E2では未実施の無傷接触、保護・消費前後、非接触、保護終了後と次攻撃、実軌道と帯を補う。Cで取得した同一条件・追跡可能な接触証拠は再利用し、E2で何を補ったかを記す。

その後は68のE3四条件→E4保持回帰・記録比較→E5通常公開再生→独立Q1〜Q6を直列で実施する。E3開始前に証拠選択の仕組みを揃え、表示窓を変えるだけで試験ソースを変更して四条件のsource_idを揃え直す反復を避ける。

E5の入力全文、通常到達、player対照、旧未来入力破棄はCの限定診断では完了しない。

### 5. 配布台帳と後続必須工程

76の全13試験ファイル配布台帳と、80の追加ID・更新配布を維持する。A〜Dの変更ごとに完全テストIDと個別ファイルを更新し、配布予定と独立検証済みを別列にする。

特に：

- `test_bots_boss.py`の接続・監査・接触変更はQ1へ、接触部分はQ2へ、表示対応はQ4へ渡す。
- `test_split_c.py`の再生・制御変更はQ1・Q3・Q6へ渡す。
- `test_g002_evidence.py`の出力道具変更はQ1〜Q6へ更新配布する。
- `bots.py`更新は共有bot担当Q5・Q6にも渡す。

独立QA後はD-025の条件に従い限定Art Verify→独立Play→Designer実測後判断→Reviewを残す。60のfailは維持し、現行検証・記録比較・歴史的確認不能・その他不足・Designer判断待ちを別に記録する。

### 6. 予算への影響と停止条件

81時点の85/123からの名目残枠は38 operationsである。本Step等の消費後の正確な残数はStudioが台帳で更新する。

実行単位の目安はA〜Dの4 Engineer Step、E2の1〜2、E3の4、E4の1〜2、E5の2、独立Q1〜Q6の6、Art・Play・Designer・Reviewの4で、担当作業だけで22〜24 Stepとなる。StudioのRoute、失敗修正、判断への手戻り、表示窓の継続は含まない。完成が38枠内に収まる保証はなく、余裕は小さい。

各単位終了時に、未完了の条件・必要な次単位・残枠を更新する。同じ単位が3回の実行で収束しない場合は、具体的な失敗条件をquestionとして返し、対象を増やした曖昧なE1再開を行わない。本文だけが残る場合は、残連番を指定した限定継続とする。

現時点では技術的不成立を示す証拠はないため、Ownerへの新しい供給質問は不要である。残必須工程が上限内に収まらない具体的見通しが出た場合はStudioからGame Directorへ費用・範囲判断を戻す。123到達時は新規作業を開かない。

## Decisions already made

- D-019：公開情報限定、同一方針、0.15秒反応、開始3/2 hearts別FPS比較、保持回帰と実測後Designer判断を維持。
- D-021・D-023：Studio内テキスト検証、個別本文、最大3回実行・各2万字、追加本文一度最大8件。
- D-022：表示・弾・長時間観測の契約を維持。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離。
- D-025：必須検証・独立評価を維持し、重複工程と存在しない資料の探索を省く。後続工程条件を再審議しない。
- D-026：budget 123。上限到達後の追加継続はOwner判断。
- 本計画：68のE1をA→B→C→Dへ分割する。仕様変更を伴う新Decisionは作成しない。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal解釈を変更しない。既存hits0等のassertを理由なく緩和せず、旧成績へ合わせる調整を行わない。

実接続・監査・測定を実施済みとしない。未解決の被弾差、切断されたE1/input-replay本文、歴史的確認不能を成功扱いしない。独立QAと体験評価を自己試験で置換しない。

外部配員、追加環境、変更前ビルド、全文保存先、追加の実行枠を前提にしない。

## Open questions

1. Aで回収する保存済みno-controls本文は両FPSで完全一致を示すか。
2. 接続後の最初の差は入力記録・再生・制御列・方針と実接触のどこに生じるか。
3. 新方針の実被弾や比較差についてDesigner判断が必要になるか。

いずれも担当実行で解く技術課題であり、今回の新しいOwner質問ではない。

## Expected output

StudioはまずAだけをEngineerへルートし、書込を`repo/tests/test_split_c.py`と`repo/tests/test_g002_evidence.py`へ限定する。次のEngineer Stepで実接続まで同時に要求しない。

A用の個別Load案：

- `studio/roles/gameplay-engineer.md`
- `studio/skills/implement-change.md`
- `project.md`
- `repo/bots.py`
- `repo/game.py`
- `repo/session.py`
- `repo/play.py`
- `repo/run_driver.py`
- `repo/source_id.py`
- `repo/tests/test_split_c.py`
- `repo/tests/test_g002_evidence.py`
- `repo/tests/test_bots_boss.py`
- `design/final-boss-and-continuous-run.md`
- `design/g002-historical-comparison-evidence.md`
- `goals/G-002-final-boss/82-technical-director-to-studio.md`
- `goals/G-002-final-boss/76-gameplay-engineer-to-studio.md`
- `goals/G-002-final-boss/80-gameplay-engineer-to-studio.md`
- `decisions/D-019-g002-balance-criteria-applicability.md`
- `decisions/D-023-owner-confirms-verification-supply.md`
- `decisions/D-024-g002-historical-comparison-evidence.md`
- `decisions/D-025-g002-minimum-remaining-scope.md`
- `decisions/D-026-owner-extends-g002-budget.md`

AのHandoffには、実際の出力選択方法、変更ファイル、source_id、両FPSの必要本文と受信範囲、全assertの結果、切断・未解決、Bへの開始条件を記す。

B〜DはこのLoadの核と直前成果を引き継ぐ。記憶統合を監査するB・Dには実在する`repo/tests/test_play_run_controls.py`、`repo/tests/test_session.py`を、制御診断Cには`repo/tests/test_run_driver.py`を個別追加Loadする。未供給本文を推測して変更しない。

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/bots.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Evidence inventory: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting report: goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
- Supporting report: goals/G-002-final-boss/80-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
- Previous handoff: goals/G-002-final-boss/81-studio-to-technical-director.md
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

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/84-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
