# Studio operation packet

operation: Step
goal: G-002
role: technical-director
incoming_handoff: goals/G-002-final-boss/15-studio-to-technical-director.md
next_seq: 16

## You may write

- goals/G-002-final-boss/16-technical-director-to-<recipient>.md
- decisions/D-020-<name>.md

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

<<<FILE goals/G-002-final-boss/15-studio-to-technical-director.md
---
kind: handoff
goal: G-002
seq: 15
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 15: studio → technical-director — 確定仕様・基準移行・実測の技術計画

## Task

承認済みの連続ランと最終ボス仕様を、実装・試験・観測が可能な技術計画にする。仕様§8の試験対応と§10の依存、D-019の適用条件、実測後のDesigner再判断を含め、工数・リスクと実装開始を妨げる未決事項をStudioへ返す。

## Context

Ownerは「最後に手応えのあるボス戦がほしい」と依頼し、D-015で第1〜4部屋の連続ラン、第5部屋の単体ボス、勝敗とラン先頭からの再挑戦を承認した。詳細仕様はD-017、旧集計との整合方向はD-018、適用変更と代替評価はD-019で確定した。Design補足が完了したためPlanを開く。ゲーム変更はまだ行われていない。

## Findings

14は文書上の適用整理を報告している。旧独立3〜5のwalker合計、dodgerとの比率・clear数、camper比較とその旧報告条件を新構成のゲートから外し、第1〜4部屋と共有ルールの回帰を保持した。

独立3・4はbot別・部屋別・30/60 FPS別に報告し、新しい合計閾値は導出しない。ボスのdashは使用回数ではなくB6の接触・無傷・消費・終了後被害で検証する。対応dodgerの新5番FPS比較は同じclear結果・hearts lost差1以下とし、独立3 hearts開始と連続ランで可能な2 hearts開始を別比較する。詳細条件と試験対応の正本はD-019と仕様§8である。

追加数値ゲートは未設定。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、DesignerがReview前に必要性を判断する。追加不要でも理由を記録する。

指定shaとの一致、実行成功、難度、所要時間の新しい証拠はない。現在ビルドは `repo/`、指定shaは `27fe16268ac8`。project.mdの0.4表記と既存資料の0.6表記の関係も未確認。

## Decisions already made

- D-001：戦闘入力はattackとdash。
- D-015：連続ランと第5部屋の単体ボスをOwnerが承認。
- D-016：読み取り・位置取り・回避後の反撃を中心とする体験方向。
- D-017：ボス、回復、継承、境界、終端、時刻・表示の詳細契約。
- D-018：旧第5部屋依存の集計を新構成評価から分離。
- D-019：旧基準の限定的な適用変更、保持する回帰、dash検証、対応bot FPS比較、実測後判断。過去Decision本文・G-001の結果は保持。

## Constraints

- 第1〜4部屋の構成と共有戦闘ルールを維持する。新戦闘入力、ボスチェックポイント、既存部屋全面改修を追加しない。
- 30/60 FPS、desktop、keyboard・gamepadの制約を扱う。実機入力経路を確認できない場合は、観測可能な範囲と不足を明記する。
- 15〜20分のVisionを維持する。時間合わせだけのHP増加・待機水増しを計画しない。独立部屋時間の合算を連続ラン実測に代用しない。
- 設計の数値・振る舞いはDesignerの権限。曖昧さや実現困難な仕様は具体的な質問として返す。
- 旧fixtureの保持は必須ではないが、assert削除だけで移行完了にしない。仕様の代替試験・共有回帰へ接続する。
- Plan完了前にBuildを開始しない。承認を超える規模・費用・リスクやOwner Decision変更が必要なら実装前に返す。
- 後続はBuild→独立QA→限定Art Verify→独立Play→Designer実測後判断→Review。明白な対処不能・到達不能はPlay前にもDesignerへ返す。

## Open questions

1. 指定sha、対象ビルド、表記差、既存試験の実行基線を同定できるか。
2. 進行、攻撃切替、表示、HP・回復、終端・retry、pause/resume、両時刻・入力をどの構造と順序で実装・観測するか。共有コードへの影響と工数・リスクは何か。
3. player viewと状態観測、長時間スクリプト、境界試験、実機入力経路をどう扱うか。
4. 対応botの情報・反応・方針をどう確認し、同一ビルド・初期状態・limitで両FPSを比較するか。deathとunfinishedをどう分けるか。
5. 通常ランの同一試行計測と独立QA・Playの証拠を、いつDesignerへ戻せるか。

## Expected output

技術計画と実行基線の確認結果を、次のHandoffで `to: studio` として返す。計画には以下を含める。

- 実装順序、依存、変更対象、工数・リスク、仕様質問と実行制限。
- 仕様B1〜B10・V1、R1〜R5、T1〜T4、C1〜C3、V2、共有回帰と旧assert群の移行対応。
- 対応botの確認、独立3・4の部屋別報告、新5番の開始HP別・両FPS比較、通常ランの同一試行計測。
- 独立QA、限定Art確認、独立Playへ渡せる実行・観測方法。
- Designerの実測後判断に必要な証拠と返却時点。閾値超過や失敗一致を自動合格にしない経路。
- Buildを開けるか、先にDesign・Decideへ戻す必要があるかの明示。

実行できなかった項目は未確認として理由と次の確認方法を記録し、成功を推定しない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: goals/G-002-final-boss/04-technical-director-to-studio.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Build: repo/
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/14-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE studio/skills/technical-plan.md
---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
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
- Plan：open。確定仕様とD-019に基づき、進行・攻撃切替・表示・終端・時刻と入力の契約、共有コードへの影響、試験移行、対応bot、計測、工数と依存を確認する。指定shaと実行基線は未確認。承認超過の可能性は実装前に返す。
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
| 5 | Plan | technical-director | technical-plan | open | 15-studio-to-technical-director.md |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。D-019と仕様補足に基づくPlanを開く。Planの完了前にBuildを開かない。独立QA、Art Directorの限定Verify、独立Playの後、Designerが実測に基づく判断を記録してからReviewへ進む。初回基線やQAで明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。現時点で並列Stepは開かない。

## Route changes

14でDesign補足を完了。D-019と仕様§8・§10による適用整理を受け、15でTechnical DirectorのPlanを開く。対応bot・両FPS基線・通常ラン同一試行計測を計画対象にし、Review前のDesigner実測後判断をplannedで追加。独立検証とPlayを維持し、Owner質問は開かない。

## Next action

Technical Directorが `15-studio-to-technical-director.md` を実行し、確定仕様・D-019に基づく実装、試験移行、対応botと計測の計画、工数・リスク、Designer再判断の依存をStudioへ返す。

## Outcome

未完了・進行中。D-015で範囲、D-016で体験方向、D-017で詳細契約、D-018・D-019で旧集計と新構成の適用関係を確定した。次は実装計画。実装、独立QA・限定Art確認・独立Play、Designerの実測後判断、Reviewは未実施。指定shaとの一致、実行成功、難度、所要時間について新しい証拠はない。現時点でOwnerへの新たな質問はなく、project.mdのCurrent stateは変更しない。
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

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 94 (wording only, no rule or number changed):** the hit message for a shot now names the side the shot came from (`YOU ARE HIT by a shot from the <direction>`), and a swipe that damages a grub already in its lunge shows `the <variant>'s lunge had already started, the swipe was too late to stop it`. Exact formats and acceptance criteria W1–W8 are in `design/combat-step94.md`, which governs these two messages.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

## G-002 applicability

D-019 and `design/final-boss-and-continuous-run.md` §8 govern application to the new room 5 and continuous run. Historical G-001 rulings and results below remain records of that configuration. Rooms 1–4 and shared combat rules remain in force. Independent room tests start with 3 hearts; continuous-run inheritance follows the G-002 specification.

For the new configuration, criterion 13's old rooms 3–5 aggregates and walker/dodger/camper comparisons cease to apply. Criterion 14 remains. Criterion 15 remains for independent rooms 3–4, including reporting zero dash use to the designer; new room 5 uses actual dash-contact checks for both boss attacks. Criterion 16c remains for independent rooms 1–4; boss-adapted dodger comparisons use the conditions in §8. Criterion 16b does not restore retired criterion 13 aggregates. The old room-5 contents and spitter-specific checks are replaced as mapped in §8. These changes establish applicability, not verified difficulty or experience.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-step-44-walker-limit.md
# Combat design note: criterion 13 walker limit (step 44, build 0.6)

Status: amends criterion 13 of `design/combat.md`. Where this note and `combat.md` differ on criterion 13, this note governs. No other criterion, rule or parameter changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-006.

## G-002 applicability annotation

D-019 ends application of this note's old rooms 3–5 aggregate gates to the G-002 boss configuration and continuous run. This includes 13a–d, the old aggregate FPS checks and historical figures in 13e–f, and their aggregate reporting/revisit/re-verification requirements. The historical G-001 ruling and results remain unchanged below.

Independent rooms 1–2 comparisons, independent rooms 3–4 dash rules, shared combat regression and independent-room 3-heart starts remain. Independent rooms 3–4 bot results are reported separately at 30 and 60 FPS. No new aggregate gate is derived from 3–7 or 2/3. The complete replacement and measurement route is `design/final-boss-and-continuous-run.md` §8; it governs G-002 application over this note's historical “unchanged” references to criteria 15–16.

## Question

The walker bot on build 0.6 loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS). Criterion 13 allowed at most 6. All other criterion 13 limits hold.

## Ruling

7 hearts is not a breach of intent. The limit of 6 was too tight, and it was never derived. Step 22 recorded 6 as "exactly the upper limit" of the 0.5 observation, so it was a snapshot of one bot result.

The purpose of criterion 13 is a gradient: ignoring the aim cue is costly but not hopeless. The 0.6 evidence shows both halves:

- **Costly.** The walker loses 4 (30 FPS) and 7 (60 FPS) hearts. The dodger loses 0 and clears 3/3, and uses 7 or more dashes per room. The camper clears 0 of 3. The gap between ignoring and reading the cue is larger than in 0.5.
- **Not hopeless.** The walker still clears 2 of 3 rooms at both rates. It is not walled out.

Why the hearts ceiling was the wrong tool:

- Each room has 3 hearts. A room the walker clears must have been survived, so it costs at most 2 hearts.
- A walker that clears 2 of 3 rooms therefore loses at most 3 + 2 + 2 = 7 hearts in rooms 3–5. The clear count is what carries "not hopeless". A hearts ceiling below 7 only forbids particular distributions of the same outcome. For example, 3+2+2 at 60 FPS is forbidden, while 3+2+1 is allowed. That says nothing about the gradient.
- The walker decides on a 0.15 s grid. The engineer saw per-room totals move in opposite directions between 0.5 and 0.6. A one-frame difference in a sidestep decides whether a shot hits (criterion 16d). Tuning rooms to move a bot's total by one heart would fit the room to the bot's grid phase, not to any player-visible behavior.

I did not change a room or enemy parameter, for these reasons:

- Both D-004 and D-005 expected this movement. The brute no longer being cancelled raises the walker's losses; consumed shots lower them. The net is what the rules produce.
- Any parameter change would force QA to re-verify criteria 11, 13, 14, 15, 18, 20 and 21 for no player-visible gain.
- D-004 and D-005 stay as they are.

## Amended criterion 13 (replaces the numbers in `combat.md`)

**13. Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate (30 FPS and 60 FPS) separately, in rooms 3–5 summed:

- a. The walker clears at least 2 of the 3 rooms. This is the "not walled out" gate.
- b. The walker loses at least 3 and at most 7 hearts. The lower limit is the "costly" gate. 7 is the largest total consistent with 13a (3 hearts per room, at most 2 lost in a cleared room), so the upper limit is a consistency check and not an independent gate.
- c. The dodger loses at most half of the walker's total and clears 3/3.
- d. The camper clears fewer of rooms 3–5 than the walker.
- e. Per-room walker figures are not criteria. The 30 and 60 FPS totals need not match (16d). The two rates are checked separately and not as a range.
- f. Measured values: 0.6 walker 4 lost / 2 cleared at 30 FPS, 7 lost / 2 cleared at 60 FPS. Dodger 0 lost / 3 cleared at both. Camper 0 cleared at both (engineer's figures; QA re-measures).

Reporting rule: QA reports to `game-designer` any measured value that fails 13a–13d. A walker total anywhere in 3–7 with at least 2 rooms cleared is a pass and needs no report, even if it differs from the figures above.

Criteria 14, 15 and 16 are unchanged. Criterion 16c (dodger agrees between rates) and 16d (walker need not) still apply.

## Which figures would change this ruling

The ruling depends on the gradient, not on the exact engineer figures. These QA results would reopen it:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a room or enemy parameter change, or Director input if it touches D-004 or D-005.
2. The walker loses fewer than 3 hearts at either rate. That means ignoring the cue is not punished enough. The 30 FPS margin is only 1 heart (4 against 3).
3. The dodger loses more than half the walker's total, or fails to clear 3/3.
4. The camper clears as many rooms as the walker or more.
5. QA finds a difference between rates that comes from a rule and not from bot timing (16e). That is a build defect and not a tuning question.

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

## What QA re-verifies

Only criterion 13 against the amended limits, using `run_bots` on the unchanged 0.6 build at both rates. QA also confirms that the walker's 30/60 FPS differences come from the 0.15 s decision grid (16e). Nothing else needs re-verification, because no rule or parameter changed.

## Experience signal (playtest and Review)

A player who ignores the aim cues in rooms 3–5 is hurt often and may fail a room. They can still finish the three rooms without being locked out, and a player who reads the cues does clearly better. If the hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5, reopen this note and D-004/D-005 tuning values. Do not rely on the bot figure alone.
>>>END

<<<FILE goals/G-002-final-boss/04-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 4
from: technical-director
to: studio
stage: Diagnose
outcome: done
---
# 04: technical-director → studio — 個別部屋の終端とボス実現範囲の静的調査

## Task

調査結果をGame Directorへ渡し、ボスの配置A/B/C、既存第5部屋の扱い、今回実装する終端・再挑戦の範囲を判断できるようにする。判断後、Game Designerへ仕様化を戻す。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。初回DesignのA/B/Cは未承認であり、今回は技術的な診断のみを行った。

提供された `repo/game.py`、`repo/play.py`、`repo/bots.py`、テストおよび資料を静的に確認した。コード・仕様・Decisionは変更していない。実行結果によるQA判定、配置選択、Goal達成判定は行っていない。

## Findings

### 1. 調査の証拠と実行上の制限

対象として指定されたshaは `27fe16268ac8`。このStepで読めた証拠はパケット内のファイル本文であり、実ファイルとshaの一致は検証していない。README、manual、コードの表示はbuild 0.6で一致する。`project.md` のCurrent stateの0.4とは異なる。

実行ツールの探索を試みたが、`code-mode host is disabled` が返り、シェル実行手段を取得できなかった。したがって、以下のコマンドはすべて未実行であり、テスト件数・成功・戦闘時間の実測値は報告できない。

| 確認予定コマンド（作業ディレクトリ `repo/`） | 状態 |
|---|---|
| `python3 -m unittest discover -s tests` | 未実行 |
| `python3 play.py --view player {script}` | 未実行 |
| `python3 play.py --view trace {script}` | 未実行 |
| `python3 bots.py {script}` | 未実行 |

再現確認には、指定shaの実行可能な `repo/`、Python 3、スクリプトを渡せる実行環境が必要。以下はすべて「提供コードから確認した挙動」であり、観測した実行結果ではない。

### 2. 現行の入場・終端・再挑戦

| 項目 | 提供コードで確認した実装と根拠 |
|---|---|
| 入場 | `play.read_script()` が一つのroom値を読み、`play.play()` が一つの `Game` を生成する。room行を複数書いても順番の指定にはならず、後の値が上書きする |
| 選択範囲 | `game.ROOMS` は1〜5とempty。ボス定義・ボス部屋はない |
| 開始状態 | `Game.__init__()` で座標(8,4)、右向き、移動なし、3 hearts、各種タイマー0、キュー攻撃なし、弾なし、イベントなし、`cleared=False`。選択部屋の敵を新規生成する |
| クリア | `Game.step()` で敵リストが空でなく、全敵のHPが0以下なら `cleared=True` と `cleared` イベント。プレイヤー表示は `room cleared` |
| 死亡 | `_hurt()` でheartsが0になると `down` イベント。表示は `you went down`、盤面のプレイヤー印は `x` |
| セッション終了 | `play.play()` はクリアまたは死亡を認識してから最大1秒継続する。ただし指定endまたは60秒上限が先ならそこで終了。最後は時間・hearts・残敵数を表示する |
| 次の部屋・最終勝利 | 提供された実行経路には存在しない。第5部屋だけの勝利表示もなく、全5部屋共通の部屋クリアで終わる |
| 再挑戦 | 専用入力、再開地点、同一セッション内のリトライ処理はない。同じコマンドを再実行すると新しい `Game` が作られ、上記開始状態から始まる |
| 状態継承 | 部屋間遷移自体がなく、継承処理もない。botsも各部屋で新しい `Game` を生成する |
| ポーズ・入力機器 | `Game.press()` とplayの受理入力はmove/stop/attack/dash。pauseや実機キーボード・ゲームパッドの入力層は、提供ビルドにはない |

従って、提供された現在のビルドは個別部屋のセッション方式である。botsの1〜5実行も、独立した部屋を順に試験する処理であり、連続ランではない。この結論の範囲は提供されたファイルに限る。

**終端には注意点がある。** 資料の「死亡・クリア時はすべて停止」とコードは完全には一致しない。`_update_enemies()` は死亡時には戻るが、クリアを停止条件にしていない。`step()` 全体と `_update_shots()` も終端で停止しないため、終了後の表示用1秒間もタイマーや弾は進む。最後の敵を倒しても弾が残れば、その後に被弾・死亡する可能性をコード上は排除できない。また `press()` は死亡を拒否するが、クリアを拒否しない。勝敗の優先順位と終端後の操作・残弾処理は、新しい終端仕様で明記し、実行確認する必要がある。現段階で既存ビルドの不具合判定はしない。

emptyは敵0体のままでは自動クリアしない。時間上限の検証には使えるが、通常部屋のクリア確認の代用にはならない。

### 3. 「最後」の到達範囲による費用差

**選択可能な最終部屋としてのボス戦**であれば、ボス挙動、部屋データ、テキスト表示、スクリプト選択と検証の追加が中心となる。部屋数を増やす案でも、選択肢を増やすだけなら連続ランの実装は必要ない。ただし、それだけでは「ランの最後に到達した」というGoal解釈を実証できない。

**連続ランから最終勝利まで**を対象にする場合は、現行の部屋戦闘に加えて次が新設となる。

- 部屋順序と進行状態、次部屋へ移る条件・時点。
- hearts、位置、向き、タイマー、弾、入力・反応ルールのリセット／継承契約。
- 部屋クリアとラン勝利の区別、死亡と勝利が近接した場合の優先順位。
- 死亡後の再開地点と再挑戦手段。
- 部屋内時刻とラン時刻、スクリプト入力の時刻基準、長時間実行と集計。
- 部屋境界・最終勝利・再試行を独立確認するテスト経路。

これはA/B/Cのどれでも別途必要であり、Bだけの費用ではない。現行コードには基盤がないため、配置変更だけと同等の規模には扱えない。大幅な範囲変更に当たるかはGame Directorが判断し、必要ならOwnerへ戻す材料になる。

### 4. 配置候補別の変更範囲とリスク

攻撃構成が未確定なので、人日・絶対的な工数は見積もれない。以下は共通のボス実装に対する相対的な影響である。

| 候補 | 影響するシステム | 固有のリスク・検証 |
|---|---|---|
| A：第5部屋を単体ボスへ置換 | `ROOMS["5"]`、敵更新・攻撃判定、表示、manual、botsと部屋別テスト | 旧混成戦を失う。部屋5の構成、cue gap、既存bots集計条件のどこを置換・維持するか仕様が必要。第4部屋からの難度接続を別途評価する |
| B：第5部屋の後に追加 | 新しい部屋キー、選択説明、テスト対象、botsの部屋指定・既定対象 | 既存1〜5の構成を保持しやすい。ただし部屋を追加するだけでは「後に進む」経路はできない。連続ランを求めるなら前節の新設が必要 |
| C：第5部屋に同居 | 第5部屋データ、ボスと既存敵の更新・予兆調停、表示、bots・複合戦検証 | 最も組合せ検証が増える。グラブの同時予兆抑制、スピッターのcue gap・弾数上限と、ボス攻撃の関係を明示する必要がある。単体で回避できても混成時の回避可能性は保証されない |

第5部屋のスピッター挙動は、`ROOM_SPIT_STAGGER` と `GAP_ROOMS` が文字列の部屋番号に結び付いている。Aで敵を取り除けばその戦闘では使われなくなるが、設定を残す／変更する判断とテストの扱いは必要。Bの新しい部屋にはcue gapが自動適用されない。Cでもボス攻撃は既存スピッターの調停に自動参加しない。

既存テストには第5部屋のブルート位置、部屋4〜5のgap、1〜5のdodger比較、3〜5合計のバランス条件がある。A/Cでは旧第5部屋を含む合計をそのまま新ボスの受け入れ基準に使えない。Bでもbotsの既定対象は `ROOMS` から作られるため、新部屋追加で出力対象が変わる。旧部屋の回帰と新ボスの評価を明示して扱う必要がある。

### 5. ボス挙動・表示の再利用範囲

**再利用できる基盤**

- 秒単位の固定フレーム更新、30/60 FPS指定、移動・部屋端のクランプ。
- プレイヤーの攻撃、ダッシュ、被弾保護、キュー攻撃。
- 敵HP減少と全敵撃破判定。
- グラブの固定照準、予兆・突進・回復・中断可否の考え方。
- スピッターの固定照準、予兆後の弾生成、弾の接触消費。
- イベント、盤面の印、警告メッセージ、`cue:`行、traceという表示の入口。

**現状のままでは不足するもの**

単体敵の複数攻撃切替は未実装。`Enemy` はグラブ系かスピッターのどちらかで、各更新処理も分岐する。グラブのパラメータ追加だけでは、突進と射撃を切り替えるボスにはならない。

新種を追加する場合、`Enemy` の検証だけでなく、`is_grub`、敵更新、`mark`、`_line_cells()`、`cue_lines()`、trace、botsの脅威認識を確認する必要がある。現行には「グラブ以外はスピッター」という前提があるため、未知のkindを受理するだけでは安全に拡張できない。

HPは内部とtraceには存在するが、player viewには数値表示がない。回復状態もplayer viewでは明示されず、盤面で停止すること以外に識別情報が乏しい。ボス用の攻撃名、予兆と危険範囲、回復開始・終了、HPの表示は追加対象となる。現行の半秒ごとの定期描画に加えて、必要な状態変化で描画を発火する条件も必要。

Art Directorへ限定して依頼する場合の具体的な不足は次のとおり。

- ボスと攻撃種を区別できる印・メッセージ・`cue:`の表現。
- 狙いの固定方向と危険範囲を読める表示。新形状では既存の細い `~` 線だけで足りるか。
- 安全な攻撃機会としての回復状態と、その終了の識別。
- HP表示と、同居案で印や予兆線が重なる場合の読みやすさ。

攻撃順・危険範囲・回復時間などのルールは先にGame Designerが定める。Art Directorへゲームルールの決定を移さない。グラフィカルな実装は前提としない。

### 6. 60秒上限と計測

`play.MAX_SECONDS=60.0` は反応ルールの有無によらず、player/trace両方の `play.play()` に適用される。明示的な `end 120` でも60秒に丸められる。

反応ルールなしの既定終了は、入力ありなら最終入力時刻+3秒、入力なしなら5秒。反応ルールありなら既定60秒。いずれも終端後の表示時間はこの上限を超えない。

一方、`Game` 自体には60秒上限がない。`bots.play_room()` は指定limitまで動作し、botsのlimitは既定60秒だが上限への丸めはない。したがって、60秒超の内部シミュレーションは可能だが、現行play経路ではその全期間のplayer/trace検証ができない。ボス時間が上限に近い場合も、時間切れを勝利・死亡と区別する必要がある。時間切れの専用イベント・メッセージは現状ない。

時間設計後、必要ならplayの実行上限と終了理由表示を変更し、独立検証にも同じ長さを提供する。上限を外すだけでは連続ランは実装されない。

計測可能なのはシミュレーション上の秒数である。botsはクリア・死亡・limit到達時点を返し、playは終了時刻、traceはイベント時刻を示す。playの終了時刻には最大1秒の終端後表示が含まれるため、戦闘時間には `cleared` / `down` の時刻を使う。

15〜20分の目標との比較には、連続ランの契約、移動・部屋間時間、再挑戦の扱い、人間の入力判断と習熟を含む観察が不足している。独立した5部屋のbots時間を足しても、現行ランの実測にはならない。今回は時間数値を実測していない。

### 7. 次の調査・実装計画への依存と検証方針

方向判断前に必要な追加実行は、実行環境が得られれば次の順で行える。

1. 指定shaを確認し、既存unittestを実行する。
2. 30/60 FPSそれぞれで、第5部屋の死亡と再実行、practiceの全敵撃破をplayer/traceで対照する。
3. 空のpracticeに `end 120` を指定し、player/traceの60秒終了を確認する。反応ルールの有無も比較する。
4. 第5部屋クリアはbotsで確認し、必要ならその判断記録からplay用入力を作成して表示を確認する。
5. 最後の敵撃破時の残弾と、終端後の操作・被弾を確認する。

これは追加のQA合否判定ではなく、静的所見を実行で裏付けるための調査である。

仕様確定後の自動検証は、攻撃切替、固定照準、予兆時間、回復、安全性、中断、無敵接触、終端・再試行を30/60 FPSで対象にする。共有コードの変更に応じて既存攻撃・敵の回帰を行う。新しい攻撃形状にD-002/D-003の接触端例外は自動適用しない。

QAは同じビルドのplayer/traceで表示と内部状態を照合し、手応え・理解・所要時間は後続Play/Reviewが判断する。既存botsはボスの新攻撃を読む実装ではないため、未対応の成績を人間の難度評価に流用しない。

今回の調査と配置判断は逐次でよく、並行コード作業は行わない。後続実装の分割は仕様と敵更新・表示間の契約が定まってから判断する。現状で並行実装を始めると、kind・phase・イベント形式の共有箇所で衝突する。

## Decisions already made

- D-001：追加の戦闘入力にはOwner承認が必要。今回の調査では追加入力を提案・採択していない。
- D-002/D-003：既存の弾・突進の接触端例外。新形状への適用は別途明示が必要。
- D-004：ブルートの非中断と部屋4〜5のスピッターcue gap。
- D-005：無敵接触時の弾消費・突進の一撃消費。
- G-002の配置・攻撃・終端範囲に新規Decisionはない。D-015は作成していない。

## Constraints

- この結果は提供コードの静的調査。実行成功、sha一致、QA合格を示さない。
- A/B/C、既存第5部屋の存廃、今回の到達範囲はGame Directorの判断に残す。
- 新しい入力を追加せず、30/60 FPSと既存のプレイヤー戦闘ルールを維持する。
- ボスに不要な既存部屋の全面改修を含めない。
- player向け表示はテキストビルドで成立させる。
- 15〜20分はVision上の目標であり、現在のラン実測値ではない。
- 秘密情報・個人情報を後続資料に含めない。

## Open questions

1. A/B/Cのどれを採るか。第5部屋の旧構成と固有基準をどう扱うか。
2. 今回は選択可能な最終部屋までか、連続ラン・最終勝利・再挑戦までか。前者ならGoal解釈に残る不足をどう扱うか。
3. 連続ランを含める場合、その新設規模をOwnerへ戻す必要があるか。
4. 勝利・死亡・残弾・終端後操作の優先順位と再挑戦地点をどう定めるか。
5. ボスの攻撃構成・時間をどう定め、60秒超のplayer/trace検証を必要とするか。
6. 上記の表示不足について、Game Designerの仕様後にArt Directorへ限定した表現仕様を依頼するか。

## Expected output

Studioは本結果と初回DesignのA/B/CをGame Directorへ渡し、配置、既存第5部屋、今回の終端・再挑戦範囲を判断するStepへルーティングする。大幅な範囲変更ならOwnerへの判断材料を用意する。

判断後、Game Designerへ採択範囲と静的確認事項・実行未確認事項を渡し、ボスと終端の受け入れ基準を仕様化する。実装計画はその後に必要性を判断する。本報告を確定仕様やQA合格として扱わない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-002-final-boss/03-studio-to-technical-director.md
- Supporting handoff: goals/G-002-final-boss/02-game-designer-to-studio.md
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  behave the same at 30 and 60 FPS up to frame rounding. Only the dodger reads the new cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing.

## Script

One instruction per line; `#` starts a comment.

| Line | Meaning |
|---|---|
| `room 1` … `room 5` | Which room to play (default 1). `room empty` is the practice room. |
| `fps 30` or `fps 60` | Frame rate (default 60). |
| `end 12` | Stop the session at 12 seconds (default: 3 s after the last input; at most 60). |
| `<seconds> move left\|right\|up\|down` | Start moving at that time. |
| `<seconds> stop` | Stop moving. |
| `<seconds> attack` | Swipe. |
| `<seconds> dash [left\|right\|up\|down]` | Dash. |
| `spawn grub\|runner\|brute\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `r`, `G`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"`) |
| `hearts <= <n>` | you have n hearts or fewer |

| Action | Does |
|---|---|
| `attack` | turn to what the condition saw (if anything) and swipe |
| `face` | turn to it without moving |
| `move <dir>`, `move toward`, `move away`, `move aside`, `stop` | move (`aside` steps across its line, toward the open side of the room) |
| `dash`, `dash <dir>`, `dash toward`, `dash away`, `dash aside` | dash |

Example:

```text
room 2
when see * coming within 1.5 then move aside
when see r within 1.4 then attack
when see g within 3 then face
```

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `r` runner grub, `G` brute grub, `s` spitter, `*` projectile, `~` an orange-red
line (see warnings below). Hearts are shown above the room.

- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow,
  4 swipes, long warning, and it does not flinch: a swipe does not interrupt its warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`, `a runner rears back` or `a brute rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute). One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.6: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. All durations are in seconds and run
on accumulated time, never on frame counts.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

# Grubs: one type, parameter sets only (design/combat.md).
GRUB_REACH = 0.6
WINDUP_RANGE = 2.0  # a grub starts its wind-up when the player is this close
LUNGE_SPEED, LUNGE_TIME = 8.0, 0.3  # 2.4 tiles
STAGGER = 0.4  # after a swipe cancels a wind-up
# "cancels": does a swipe that damages the grub in wind-up cancel the wind-up (step 35)?
GRUBS = {
    "grub": {"mark": "g", "hp": 2, "speed": 1.0, "windup": 0.5, "recovery": 0.8, "cancels": True},
    "runner": {"mark": "r", "hp": 1, "speed": 1.6, "windup": 0.35, "recovery": 0.6, "cancels": True},
    "brute": {"mark": "G", "hp": 4, "speed": 0.7, "windup": 0.7, "recovery": 1.2, "cancels": False},
}

SPITTER_HP = 2
SPIT_INTERVAL = 2.4
SPIT_FIRST, SPIT_STAGGER = 1.8, 0.8  # first shot of the k-th spitter: 1.8 s + offset * k
ROOM_SPIT_STAGGER = {"4": 1.2, "5": 1.2}  # per-room offset (step 35); other rooms use SPIT_STAGGER
GAP_ROOMS = ("4", "5")  # rooms that use the cue gap rule (step 35)
CUE_GAP, GAP_TOLERANCE = 0.6, 1e-3  # seconds since the last shot in the room; 1 ms tolerance
AIM_CUE = 0.6
SHOT_SPEED, SHOT_REACH, SHOT_LIFE = 3.0, 0.4, 5.0
SHOT_CAP, CAP_WAIT = 3, 0.2

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)],
    "3": [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
    "4": [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("brute", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}

TAN_22_5 = 0.4142


def shot_source(vx, vy):
    """Compass word for the side a shot came from (reverse of its travel; north = smaller y)."""
    dx, dy = -vx, -vy
    a, b = abs(dx), abs(dy)
    if a == 0 and b == 0:
        return "north"
    ns = "south" if dy > 0 else "north"
    ew = "east" if dx > 0 else "west"
    if min(a, b) / max(a, b) <= TAN_22_5:
        return ew if a >= b else ns
    return f"{ns}-{ew}"


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind != "spitter":
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "spitter":
            self.hp = SPITTER_HP
            self.fire_in = SPIT_FIRST + stagger * index  # seconds to the next shot
            self.cueing = False
        else:
            spec = GRUBS[kind]
            self.hp = spec["hp"]
            self.phase = "approach"  # approach | windup | lunge | recovery | stagger
            self.phase_left = 0.0
            self.lunge_left = 0.0
            self.struck = False  # this lunge has damaged the player
            self.spent = False  # this lunge touched a protected player: its hit is used up (step 38)

    @property
    def is_grub(self):
        return self.kind in GRUBS

    @property
    def mark(self):
        return GRUBS[self.kind]["mark"] if self.is_grub else "s"


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.last_shot = None  # time of the last shot fired in the room (cue gap rule)
        self.hurt_kinds = []  # who dealt each hurt event, in order (text view names, D-011)
        self.events = []  # (time, kind, details)
        self.cleared = False
        for spec in ROOMS[room]:
            self.spawn(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        index = sum(1 for e in self.enemies if e.kind == "spitter")
        stagger = ROOM_SPIT_STAGGER.get(self.room, SPIT_STAGGER)
        self.enemies.append(Enemy(kind, x, y, index, stagger))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    # --- Input -------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.hearts <= 0:
            return
        if self.stun_left > 0:
            self.log("ignored", action=action, reason="stunned")
            return
        if action == "move":
            self.heading = self.facing = DIRECTIONS[direction]
        elif action == "stop":
            self.heading = (0, 0)
        elif action == "attack":
            if self.dash_left > 0:
                self.queued_attack = True
            elif self.recovery > 0:
                self.log("ignored", action=action, reason="recovering")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation --------------------------------------------------------------------------

    def step(self):
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= 1e-9:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        self._update_enemies(dt)
        self._update_shots(dt)
        if not self.cleared and self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.cleared = True
            self.log("cleared")

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        fx, fy = self.facing
        hit = []
        for enemy in self.enemies:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if (
                enemy.hp > 0
                and math.hypot(dx, dy) <= ATTACK_REACH
                and dx * fx + dy * fy > 0
            ):
                enemy.hp -= 1
                hit.append(enemy)
        for enemy in hit:
            if enemy.hp > 0 and enemy.is_grub and enemy.phase == "windup":
                if GRUBS[enemy.kind]["cancels"]:
                    enemy.phase, enemy.phase_left, enemy.aim = "stagger", STAGGER, None
                    self.log("stagger", enemy=enemy.kind)
                else:
                    # Not cancelled (step 35): wind-up, timer and aim carry on.
                    self.log("shrug", enemy=enemy.kind)
            elif enemy.hp > 0 and enemy.is_grub and enemy.phase == "lunge":
                # Step 94 (wording only): the swipe was too late; the lunge is untouched.
                self.log("late_swipe", enemy=enemy.kind)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        if self.hearts <= 0:  # the player is down: everything stops
            return
        busy = any(
            e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in self.enemies
        )
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            if enemy.is_grub:
                busy = self._update_grub(enemy, dt, busy)
            else:
                self._update_spitter(enemy, dt)

    def _update_grub(self, e, dt, busy):
        """One grub for one frame; returns whether some grub is now in wind-up or lunge."""
        spec = GRUBS[e.kind]
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        if e.phase == "approach":
            if dist <= WINDUP_RANGE + EPS and not busy:
                e.phase, e.phase_left = "windup", spec["windup"]
                # Aim locked now. Grub exactly on the player: the spec is silent; face right.
                e.aim = (dx / dist, dy / dist) if dist > 0 else (1.0, 0.0)
                self.log("windup", enemy=e.kind)
                return True
            stop = GRUB_REACH * 0.9
            if dist > stop:
                step = min(spec["speed"] * dt, dist - stop)
                e.x += dx / dist * step
                e.y += dy / dist * step
        elif e.phase == "windup":
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase, e.lunge_left = "lunge", LUNGE_TIME
                e.struck = e.spent = False
                self.log("lunge", enemy=e.kind)
            return True
        elif e.phase == "lunge":
            span = min(dt, e.lunge_left)
            e.x, e.y = self._clamp(
                e.x + e.aim[0] * LUNGE_SPEED * span, e.y + e.aim[1] * LUNGE_SPEED * span
            )
            e.lunge_left -= span
            close = math.hypot(self.x - e.x, self.y - e.y) <= GRUB_REACH
            if close and not e.struck and not e.spent:
                if self.invulnerable:
                    e.spent = True  # step 38: a blocked contact uses up the lunge's one hit
                else:
                    e.struck = True
                    self._hurt("grub", e.kind)
                    e.lunge_left = 0.0  # contact ends the lunge
            if e.lunge_left <= EPS:
                e.phase, e.phase_left, e.aim = "recovery", spec["recovery"], None
                return False
            return True
        else:  # recovery or stagger
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase = "approach"
        return busy

    def _gap_blocks(self, e):
        """Cue gap rule (step 35, rooms 4-5 only): True if spitter e may not start a cue now."""
        if self.room not in GAP_ROOMS:
            return False
        for other in self.enemies:
            if other is not e and other.hp > 0 and other.kind == "spitter" and other.cueing and other.aim:
                return True  # another spitter's cue is running
        return self.last_shot is not None and self.t - self.last_shot < CUE_GAP - GAP_TOLERANCE

    def _update_spitter(self, e, dt):
        e.fire_in -= dt
        if not e.cueing:
            if e.fire_in <= AIM_CUE + EPS:
                if len(self.shots) >= SHOT_CAP or self._gap_blocks(e):
                    e.fire_in += CAP_WAIT  # wait and check again
                    return
                e.cueing = True
                dx, dy = self.x - e.x, self.y - e.y
                dist = math.hypot(dx, dy)
                e.aim = (dx / dist, dy / dist) if dist > 0 else None
                if e.aim:
                    self.log("aim")
        elif e.fire_in <= EPS:
            e.cueing = False
            e.fire_in += SPIT_INTERVAL
            if e.aim:
                self.shots.append(
                    [e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED, 0.0]
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            if shot[4] >= SHOT_LIFE - EPS:
                continue
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                if not self.invulnerable:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source, name=None):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hurt_kinds.append(name or source)
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")

    def _set_invulnerable(self, value, why):
        if self.invulnerable != value:
            self.invulnerable = value
            self.log("invulnerable", value=value, why=why)

    def _move(self, direction, distance):
        self.x, self.y = self._clamp(
            self.x + direction[0] * distance, self.y + direction[1] * distance
        )

    @staticmethod
    def _clamp(x, y):
        return min(max(x, 0.0), ROOM_W - 1.0), min(max(y, 0.0), ROOM_H - 1.0)


def _name(direction):
    return next(k for k, v in DIRECTIONS.items() if v == direction)
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format, including reaction rules, is described in manual.md.
"""

import argparse
import math
import re
import sys

from game import (
    AIM_CUE,
    DIRECTIONS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    Game,
)

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots
REACTION = 0.15  # a rule acts at most this often, like a player's reaction time
AFTER_END = 1.0  # seconds shown after the room is cleared or the player goes down


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs, rules = [], []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "when":
                rules.append(Rule(line))
            elif words[0] == "room":
                setup["room"] = words[1]
            elif words[0] == "fps":
                setup["fps"] = int(words[1])
            elif words[0] == "end":
                setup["end"] = float(words[1])
            elif words[0] == "spawn":
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
            elif words[0] == "player":
                setup["player"] = (float(words[1]), float(words[2]))
            else:
                inputs.append(
                    (float(words[0]), words[1], words[2] if len(words) > 2 else None)
                )
        except (IndexError, ValueError) as error:
            hint = f" ({error})" if str(error) else ""
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}{hint}")
    return setup, sorted(inputs, key=lambda i: i[0]), rules


class Rule:
    """`when <condition> then <action>`, judged only from the frame as drawn and the messages shown."""

    def __init__(self, line):
        match = re.fullmatch(r"when (.+?) then (.+)", line)
        if not match:
            raise ValueError("a rule reads: when <condition> then <action>")
        self.condition, self.action = match.group(1).split(), match.group(2).split()
        c, a = self.condition, self.action
        quoted = re.fullmatch(r'text "(.+)"', match.group(1))
        if quoted:
            self.condition = ["text", quoted.group(1).lower()]
        elif not (
            (c[0] == "see" and len(c) == 4 and len(c[1]) == 1 and c[2] == "within")
            or (c[0] == "see" and len(c) == 5 and len(c[1]) == 1 and c[2:4] == ["coming", "within"])
            or (c[0] == "nothing" and len(c) == 3 and c[1] == "within")
            or (c[0] == "hearts" and len(c) == 3 and c[1] == "<=")
        ):
            raise ValueError(
                "conditions: see <mark> [coming] within <n>, nothing within <n>, text \"<words>\", hearts <= <n>"
            )
        if c[0] in ("see", "nothing", "hearts"):
            float(c[-1])
        targets = list(DIRECTIONS) + ["away", "toward", "aside"]
        if not (
            a in (["attack"], ["stop"], ["face"], ["dash"])
            or (len(a) == 2 and a[0] in ("move", "dash") and a[1] in targets)
        ):
            raise ValueError(
                "actions: attack, stop, face, move <dir|away|toward|aside>, dash [<dir|away|toward|aside>]"
            )
        self.last = -math.inf

    def matches(self, view):
        """The cell the rule reacts to (or True), if the condition holds in this view."""
        c = self.condition
        if c[0] == "text":
            return any(c[1] in m.lower() for m in view.messages) and (view.nearest() or True)
        if c[0] == "hearts":
            return view.hearts <= float(c[2]) and (view.nearest() or True)
        if c[0] == "nothing":
            return view.nearest(within=float(c[2])) is None
        return view.nearest(mark=c[1], within=float(c[-1]), coming=c[2] == "coming")

    def act(self, game, target):
        a = self.action
        toward = _toward(target, (game.x, game.y)) if isinstance(target, tuple) else None
        away = {"left": "right", "right": "left", "up": "down", "down": "up"}.get(toward)
        # Aside: across the line to the target, toward the roomier half of the room.
        if toward in ("left", "right"):
            aside = "down" if game.y < (ROOM_H - 1) / 2 else "up"
        else:
            aside = "right" if game.x < (ROOM_W - 1) / 2 else "left"
        if a == ["attack"]:
            if toward:  # turn to it and swing, as one input
                game.press("move", toward)
                game.press("stop")
            game.press("attack")
        elif a == ["stop"]:
            game.press("stop")
        elif a == ["face"]:
            if toward:
                game.press("move", toward)
                game.press("stop")
        elif a == ["dash"]:
            game.press("dash")
        else:
            direction = {"toward": toward, "away": away, "aside": aside if toward else None}.get(a[1], a[1])
            if direction:
                game.press(a[0], direction)


def _toward(cell, position):
    dx, dy = cell[0] - position[0], cell[1] - position[1]
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


class View:
    """What the player can see right now: what is on screen and where, the hearts, the messages."""

    def __init__(self, game, messages, before=()):
        self.sprites, self.hearts, self.messages = sprites(game), game.hearts, messages
        self.before = before  # the previous frame's sprites, to see what is moving
        self.me = next(((x, y) for mark, x, y in self.sprites if mark == "P"), None)

    def closing(self, mark, x, y):
        """Whether this sprite came closer since the last frame (the eye follows the nearest match)."""
        earlier = [(math.dist((x, y), (bx, by)), (bx, by)) for m, bx, by in self.before if m == mark]
        if not earlier:
            return False
        jump, (bx, by) = min(earlier)
        return jump < 0.5 and math.dist((x, y), self.me) < math.dist((bx, by), self.me) - 1e-9

    def nearest(self, mark=None, within=math.inf, coming=False):
        if self.me is None:
            return None
        seen = [
            (math.dist((x, y), self.me), (x, y))
            for m, x, y in self.sprites
            if m not in "Px"
            and (mark is None or m == mark)
            and (not coming or self.closing(m, x, y))
        ]
        seen = [place for d, place in sorted(seen) if d <= within + 1e-9]
        return seen[0] if seen else None


def react(game, rules, messages, before):
    view = View(game, messages, before)
    if view.me is None:
        return
    for rule in rules:  # the first rule that holds and is not still waiting acts
        target = rule.matches(view)
        if not target or game.t - rule.last < REACTION - 1e-9:
            continue
        rule.last = game.t
        before = len(game.events)
        rule.act(game, target)
        for _, kind, details in game.events[before:]:
            if kind == "ignored":
                details["quiet"] = True  # a held button, not news
        return


def play(setup, inputs, view, rules=()):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    default = (inputs[-1][0] + 3 if inputs else 5) if not rules else MAX_SECONDS
    end = min(setup["end"] if setup["end"] is not None else default, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    out.start()
    pending, seen, messages, over, before = list(inputs), 0, [], None, []
    hurt_seen = 0
    while game.t < end - 1e-9 and (over is None or game.t < over - 1e-9):
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        if rules:
            react(game, rules, messages, before)
            before = sprites(game)
        game.step()
        out.frame()
        new = game.events[seen:]
        seen = len(game.events)
        names = []
        for _, k, d in new:
            if k == "hurt":
                names.append(game.hurt_kinds[hurt_seen])
                hurt_seen += 1
            else:
                names.append(None)
        messages = [
            m for m in (Player.describe(k, d, n) for (_, k, d), n in zip(new, names)) if m
        ]
        if over is None and (game.cleared or game.hearts <= 0):
            over = game.t + AFTER_END
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0
        self.hurts = 0  # hurt events already printed (indexes game.hurt_kinds)

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.6 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, show = self.game, False
        for when, kind, details in g.events[self.seen :]:
            name = None
            if kind == "hurt":
                name = g.hurt_kinds[self.hurts]
                self.hurts += 1
            text = self.describe(kind, details, name)
            if text:
                print(f"{when:7.3f}  {text}")
            show = show or kind in ("hurt", "windup", "aim")
        self.seen = len(g.events)
        if show or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details, name=None):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "shrug":
            return "the brute shrugs off the swipe"
        if kind == "late_swipe":
            return (
                f"the {details['enemy']}'s lunge had already started, "
                "the swipe was too late to stop it"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {name or details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "windup":
            return f"a {details.get('enemy', 'grub')} rears back"
        if kind == "aim":
            return "a spitter takes aim"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored" and not details.get("quiet"):
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in draw(g):
            print("   |" + row + "|")
        print("   +" + "-" * ROOM_W + "+")
        for text in cue_lines(g):
            print("   " + text)


def sprites(g):
    """Everything on screen as (mark, x, y), drawn in this order (later ones on top)."""
    shown = [("*", s[0], s[1]) for s in g.shots]
    shown += [(e.mark, e.x, e.y) for e in g.enemies if e.hp > 0]
    return shown + [("P" if g.hearts > 0 else "x", g.x, g.y)]


def _line_cells(g):
    """Points of the thin orange-red lines: lunge paths during a wind-up, aim lines during a cue."""
    cells = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        if e.is_grub and e.phase == "windup":
            length = LUNGE_SPEED * LUNGE_TIME
        elif not e.is_grub and e.cueing:
            length = ROOM_W + ROOM_H
        else:
            continue
        for i in range(1, int(length / 0.25) + 1):
            cells.append((e.x + e.aim[0] * 0.25 * i, e.y + e.aim[1] * 0.25 * i))
    return cells


def cue_lines(g):
    """Text description of the flash, glow and lines (orange-red) shown under the room."""
    out = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        where = f"at ({e.x:.1f},{e.y:.1f})"
        line = f"line toward ({e.aim[0]:+.2f},{e.aim[1]:+.2f})"
        if e.is_grub and e.phase == "windup":
            out.append(
                f"cue: {e.mark} {where} flashes orange-red, lunge {line}, "
                f"{LUNGE_SPEED * LUNGE_TIME:.1f} tiles ({e.phase_left:.2f} s to the lunge)"
            )
        elif not e.is_grub and e.cueing:
            bright = min(1.0, max(0.0, (AIM_CUE - e.fire_in) / AIM_CUE))
            out.append(
                f"cue: s {where} glows orange-red, brightness {bright:.0%}, aim {line} "
                f"({e.fire_in:.2f} s to the shot)"
            )
    return out


def draw(g):
    """The room as the player sees it, one string per row ('~' is an orange-red line)."""
    grid = [[" "] * ROOM_W for _ in range(ROOM_H)]
    for x, y in _line_cells(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = "~"
    for mark, x, y in sprites(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = mark
    return ["".join(row) for row in grid]


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([("setup", {})])

    def frame(self):
        g = self.game
        new = [(kind, details) for _, kind, details in g.events[self.seen :]]
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([("end", {})])

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp},"
            + (f"{e.phase}:{e.phase_left:.3f}" if e.is_grub else f"fire_in={e.fire_in:.3f},cue={e.cueing}")
            + ")"
            for e in g.enemies
            if e.hp > 0
        )
        happened = "; ".join(
            kind + (f" {details}" if details else "") for kind, details in events
        )
        print(f"{state} | {enemies} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs, rules = read_script(f.read())
    play(setup, inputs, args.view, rules)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys

from game import (
    ATTACK_REACH,
    DIRECTIONS,
    GRUB_REACH,
    GRUBS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    ROOMS,
    SHOT_LIFE,
    SHOT_REACH,
    SHOT_SPEED,
    Game,
)

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log
        self.grid = 0.0  # log only: the last grid time passed by the last decision
        self.shadow = 0.0  # log only: a copy of the clock that also runs while the player is stunned

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.grid = self.next
            self.next += REACTION
        self.shadow = self.next
        return True

    def note(self, game, text):
        if self.log is not None:
            self.log.append(f"{game.t:6.2f} s  {text} | {_state(game, self.grid)}")

    def skip(self, game):
        """Log a grid decision that is skipped because the player is stunned (once per grid time)."""
        t = game.t
        if self.log is None or t < self.shadow - 1e-9:
            return
        grid = self.shadow
        while self.shadow <= t + 1e-9:
            grid = self.shadow
            self.shadow += REACTION
        self.log.append(
            f"{t:6.2f} s  skipped decision | frame {game.frame}, grid {grid:.3f} s, "
            f"frame time {t:.6f} s, reason: player stunned ({game.stun_left:.3f} s of stun left)"
        )


def _state(game, grid):
    """The state a decision is made from, as one line of text (log only)."""
    enemy = _nearest(game)
    if enemy:
        distance = math.hypot(enemy.x - game.x, enemy.y - game.y)  # same expression the bots compare
        near = (
            f"nearest {enemy.kind} at ({enemy.x:.6f}, {enemy.y:.6f}) "
            f"distance {distance:.9f} (exact {distance!r})"
        )
    else:
        near = "nearest none"
    shots = (
        "; ".join(f"({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in game.shots)
        or "none"
    )
    stun = f"yes ({game.stun_left:.3f} s left)" if game.stun_left > 0 else "no"
    return (
        f"frame {game.frame}, grid {grid:.3f} s, frame time {game.t:.6f} s, "
        f"player ({game.x:.6f}, {game.y:.6f}), hearts {game.hearts}, stunned {stun}, "
        f"{near}, shots in flight: {shots}"
    )


def _hurt_lines(game, first_event, shots_before, struck_before):
    """Log lines for the hearts lost in the frame just played (log only; reads, never changes)."""
    out = []
    for when, kind, details in game.events[first_event:]:
        if kind != "hurt":
            continue
        source = details["source"]
        if source == "grub":
            hit = [e for e in game.enemies if e.is_grub and e.struck and not struck_before.get(id(e))]
            there = (
                ", ".join(f"grub {e.kind} at ({e.x:.6f}, {e.y:.6f})" for e in hit)
                or "grub position not found"
            )
        else:
            gone = [
                s
                for s in shots_before
                if not any(s is k for k in game.shots)
                and s[4] < SHOT_LIFE - 1e-9
                and -1 <= s[0] <= ROOM_W
                and -1 <= s[1] <= ROOM_H
                and math.hypot(s[0] - game.x, s[1] - game.y) <= SHOT_REACH
            ]
            there = (
                ", ".join(
                    f"shot at ({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in gone
                )
                or "shot position not found (fired in this frame)"
            )
        out.append(
            f"{when:6.2f} s  HEART LOST | frame {game.frame}, source {source}, "
            f"player ({game.x:.6f}, {game.y:.6f}), {there}; hearts now {details['hearts']}"
        )
    return out


def _toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _nearest(game):
    live = [e for e in game.enemies if e.hp > 0]
    return min(live, key=lambda e: math.hypot(e.x - game.x, e.y - game.y), default=None)


def _face_and_swing(game, enemy):
    game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    game.press("stop")
    if math.hypot(enemy.x - game.x, enemy.y - game.y) <= ATTACK_REACH and game.recovery <= 0:
        game.press("attack")


def _incoming(game):
    """A shot in flight that will reach the player within 0.7 s, if any (ignores cues)."""
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        ahead = ((game.x - x) * vx + (game.y - y) * vy) / speed
        beside = abs((game.x - x) * vy - (game.y - y) * vx) / speed
        if 0 < ahead < 0.7 * speed and beside < 0.7:
            return vx, vy
    return None


def _sidestep(game, shot):
    vx, vy = shot
    if abs(vx) >= abs(vy):
        return "down" if game.y < 4 else "up"
    return "right" if game.x < 8 else "left"


def _dangers(game):
    """Lines the player can see: wind-up paths, lunges, spitter aim lines, shots in flight.

    Each is (x, y, ux, uy, length, wait, speed, kind): origin, unit direction, length of the
    dangerous stretch, seconds until it starts moving, and how fast it moves along the line.
    """
    out = []
    for e in game.enemies:
        if e.hp <= 0:
            continue
        if e.is_grub and e.phase == "windup":
            out.append((e.x, e.y, e.aim[0], e.aim[1], LUNGE_LEN + GRUB_REACH, e.phase_left, LUNGE_SPEED, "lunge"))
        elif e.is_grub and e.phase == "lunge":
            out.append((e.x, e.y, e.aim[0], e.aim[1], e.lunge_left * LUNGE_SPEED + GRUB_REACH, 0.0, LUNGE_SPEED, "lunge"))
        elif not e.is_grub and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        out.append((x, y, vx / speed, vy / speed, 40.0, 0.0, speed, "shot"))
    return out


def _threat(game):
    """The most urgent line the player stands in: (eta, ox, oy, ux, uy, beside, kind)."""
    best = None
    for ox, oy, ux, uy, length, wait, speed, kind in _dangers(game):
        rx, ry = game.x - ox, game.y - oy
        ahead = rx * ux + ry * uy
        beside = rx * -uy + ry * ux
        if ahead < -0.3 or ahead > length or abs(beside) > 0.9:
            continue
        eta = wait + max(0.0, ahead - 0.5) / speed
        if best is None or eta < best[0]:
            best = (eta, ox, oy, ux, uy, beside, kind)
    return best


def _axis(vx, vy):
    if abs(vx) >= abs(vy):
        return "right" if vx > 0 else "left"
    return "down" if vy > 0 else "up"


def _escape(game, threat):
    """The direction across the line, away from the side the player is on, with room to go."""
    _, _, _, ux, uy, beside, _ = threat
    px, py = -uy, ux
    sign = 1 if beside >= 0 else -1
    direction = None
    for _ in range(2):
        direction = _axis(sign * px, sign * py)
        dx, dy = DIRECTIONS[direction]
        x, y = game.x + dx * 1.5, game.y + dy * 1.5
        if 0 <= x <= ROOM_W - 1 and 0 <= y <= ROOM_H - 1:
            return direction
        sign = -sign
    return direction


def camper(game, note):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game, note):
    """Lets a nearby grub come and swings, walks up to anything further away, steps aside from
    shots already in flight. Never dashes and does not read the wind-up or aim cues."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.is_grub and distance < 2.5
    if shot:
        note("sidestep shot in flight")
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


def dodger(game, note):
    """Reads the cues: swipes a wind-up that is in reach when a swipe cancels it (standard grub and
    runner; never the brute, whose wind-up a swipe does not cancel: against it, sidestep or dash on
    the cue and swipe in recovery only), otherwise dashes across a line when the hit is under 0.4 s
    away, steps across it earlier if the dash is not ready, holds still while a lunge plays out,
    and walks in to swipe the rest."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    for e in game.enemies:
        if (
            e.hp > 0
            and e.is_grub
            and e.phase == "windup"
            and GRUBS[e.kind]["cancels"]
            and math.hypot(e.x - game.x, e.y - game.y) <= 1.4
            and game.recovery <= 0
        ):
            note(f"swipe {e.kind} wind-up")
            _face_and_swing(game, e)
            return
    threat = _threat(game)
    if threat and threat[0] <= 1.0:
        eta, kind = threat[0], threat[6]
        direction = _escape(game, threat)
        if ready and eta <= 0.4:
            note(f"dash {direction} from {kind} (hit in {eta:.2f} s)")
            game.press("dash", direction)
            return
        if not ready:
            note(f"step {direction} from {kind} (hit in {eta:.2f} s, dash not ready)")
            game.press("move", direction)
            return
        note(f"hold, dash ready, {kind} in {eta:.2f} s")
        game.press("stop")
        return
    if any(e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in game.enemies):
        note("hold while a grub lunges")
        game.press("stop")
        return
    enemy = _nearest(game)
    if not enemy:
        return
    if math.hypot(enemy.x - game.x, enemy.y - game.y) > 1.1:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


def play_room(bot, room, fps, limit, log=None):
    game = Game(fps=fps, room=room)
    brain = Brain([] if log else None)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0:
            if brain.due(game.t):
                bot(game, lambda text: brain.note(game, text))
        else:
            brain.skip(game)  # log only: a grid decision that the stun swallows
        if brain.log is not None:
            first_event = len(game.events)
            shots_before = list(game.shots)
            struck_before = {id(e): e.struck for e in game.enemies if e.is_grub}
        game.step()
        if brain.log is not None:
            brain.log.extend(_hurt_lines(game, first_event, shots_before, struck_before))
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": HEARTS - game.hearts,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "log": False,
    }
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(" ")
        value = value.replace(" ", "")
        try:
            if key == "bots":
                setup["bots"] = value.split(",")
                assert all(b in BOTS for b in setup["bots"])
            elif key == "rooms":
                if "-" in value:
                    first, last = value.split("-")
                    value = ",".join(str(n) for n in range(int(first), int(last) + 1))
                setup["rooms"] = value.split(",")
                assert all(r in ROOMS for r in setup["rooms"])
            elif key == "fps":
                setup["fps"] = int(value)
            elif key == "limit":
                setup["limit"] = float(value)
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | log on"
            )
    return setup


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {HEARTS} hearts each")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"])
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
            for entry in r["log"]:
                print("          " + entry)
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:7} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, ROOMS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


def has_event(kind):
    return lambda g: any(k == kind for _, k, _ in g.events)


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def busy_grubs(game):
    return sum(1 for e in game.enemies if e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge"))


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 0.4)  # the swipe cancels the grub's start; recovery passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_lunge_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_grub_walking_alone_does_not_hurt(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_spitter_fires_every_2_4_seconds_from_1_8(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.25)
        spits = times(game, "spit")
        self.assertEqual(len(spits), 2)
        self.assertAlmostEqual(spits[0], 1.8, places=6)
        self.assertAlmostEqual(spits[1], 4.2, places=6)


class GrubTest(unittest.TestCase):
    def cue(self, fps, x=10.0, kind="grub"):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, x, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_telegraph_comes_at_least_half_a_second_before_the_hit(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.5, 4)
            run(game, 2.0)
            gap = times(game, "hurt")[0] - times(game, "windup")[0]
            self.assertGreaterEqual(gap, 0.5 - 1.0 / fps - 1e-9, fps)

    def test_a_sidestep_avoids_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            run(game, 1.1)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_dash_from_cue_into_the_lunge_takes_no_damage(self):
        for fps in (30, 60):
            for offset in (0.0, 0.25, 0.5, 0.6):
                game = self.cue(fps)
                run(game, offset)
                game.press("dash", "up")
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS, (fps, offset))
                self.assertFalse(any(k == "ignored" for _, k, _ in game.events), (fps, offset))

    def test_standing_still_is_punished(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 10, 4)
            run(game, 3.0)
            self.assertLessEqual(game.hearts, HEARTS - 1, fps)

    def test_recovery_is_safe(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_a_swipe_during_windup_stops_the_lunge(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                game = self.cue(fps, x=9.2, kind=kind)
                game.enemies[0].hp = 2  # the runner would die to the swipe; keep it alive
                game.press("attack")
                self.assertEqual(game.enemies[0].phase, "stagger", (fps, kind))
                # Observe only the stagger (0.4 s): afterwards the grub may wind up again.
                run(game, 0.38)
                self.assertFalse(any(k == "lunge" for _, k, _ in game.events), (fps, kind))
                self.assertEqual(game.hearts, HEARTS)

    def test_only_one_grub_winds_up_or_lunges(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for x, y in ((9.5, 4), (8, 5.5), (6.5, 4)):
                game.spawn("grub", x, y)
            most = 0
            for _ in range(3 * fps):
                game.step()
                most = max(most, busy_grubs(game))
            self.assertEqual(most, 1, fps)

    def test_variants_swipes_to_defeat(self):
        for kind, swipes in (("grub", 2), ("runner", 1), ("brute", 4)):
            game = Game(room="empty")
            game.spawn(kind, 9.2, 4)
            if kind == "brute":  # a swipe no longer cancels its wind-up: swipe it in recovery
                game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 5.0
            for done in range(swipes):
                self.assertGreater(game.enemies[0].hp, 0, (kind, done))
                game.press("attack")
                run(game, 0.4)
            self.assertEqual(game.enemies[0].hp, 0, kind)

    def test_wind_up_lengths_differ_by_variant(self):
        windups = {}
        for kind in ("grub", "runner", "brute"):
            game = Game(room="empty")
            game.spawn(kind, 10, 4)
            run(game, 2.0)
            windups[kind] = times(game, "lunge")[0] - times(game, "windup")[0]
        self.assertAlmostEqual(windups["grub"], 0.5, delta=0.02)
        self.assertAlmostEqual(windups["runner"], 0.35, delta=0.02)
        self.assertAlmostEqual(windups["brute"], 0.7, delta=0.02)

    def test_rooms_match_the_spec(self):
        self.assertEqual(
            ROOMS["2"], [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)]
        )
        self.assertEqual(
            ROOMS["4"], [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)]
        )
        self.assertEqual(ROOMS["5"][2], ("brute", 4, 8))
        self.assertEqual(
            ROOMS["3"],
            [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
        )

    def test_room_3_clears_only_when_spitters_and_grub_are_all_dead(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            for e in game.enemies:
                if e.kind == "spitter":
                    e.hp = 0
            game.step()
            self.assertFalse(game.cleared, fps)
            for e in game.enemies:
                e.hp = 0
            game.step()
            self.assertTrue(game.cleared, fps)


class BruteTest(unittest.TestCase):
    """Criterion 19: a swipe does not cancel the brute's wind-up (step 35)."""

    def cue(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("brute", 9.0, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_a_swipe_does_not_cancel_the_wind_up(self):
        for fps in (30, 60):
            game = self.cue(fps)
            start = times(game, "windup")[0]
            game.press("attack")
            brute = game.enemies[0]
            self.assertEqual(brute.hp, 3, fps)
            self.assertEqual(brute.phase, "windup", fps)
            self.assertIsNotNone(brute.aim, fps)
            self.assertEqual(len(times(game, "shrug")), 1, fps)
            self.assertEqual(times(game, "stagger"), [], fps)
            self.assertTrue(step_until(game, has_event("lunge")))
            self.assertAlmostEqual(times(game, "lunge")[0] - start, 0.7, delta=1.0 / fps + 1e-9)
            self.assertTrue(step_until(game, has_event("hurt"), 1.0))
            self.assertEqual(game.hearts, HEARTS - 1, fps)

    def test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            run(game, 0.4)
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 2, fps)
            self.assertEqual(len(times(game, "shrug")), 2, fps)
            run(game, 1.0)
            self.assertEqual(len(times(game, "lunge")), 1, fps)

    def test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 0, fps)
            run(game, 1.5)
            self.assertEqual(times(game, "shrug"), [], fps)
            self.assertEqual(times(game, "lunge"), [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertTrue(game.cleared, fps)

    def test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            game.press("dash", "up")
            run(game, 1.5)
            self.assertEqual(game.enemies[0].hp, 3, fps)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_swipe_in_recovery_changes_nothing_else(self):
        game = Game(room="empty")
        game.spawn("brute", 9.0, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 3)
        self.assertEqual(game.enemies[0].phase, "recovery")
        self.assertEqual(times(game, "shrug"), [])


class SpitterTest(unittest.TestCase):
    def test_room_3_first_shots_are_staggered_and_cued_0_6_s_before(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            most = 0
            for _ in range(12 * fps):
                game.step()
                most = max(most, len(game.shots))
            tol = 1.0 / fps + 1e-9
            spits, aims = times(game, "spit"), times(game, "aim")
            for got, want in zip(spits, (1.8, 2.6, 3.4)):
                self.assertAlmostEqual(got, want, delta=tol, msg=fps)
            for aim, spit in zip(aims, spits):
                self.assertAlmostEqual(spit - aim, 0.6, delta=tol, msg=fps)
            self.assertLessEqual(most, 3, fps)

    def test_shot_follows_the_locked_line_and_a_sidestep_dodges_it(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 1, 4)
            self.assertTrue(step_until(game, has_event("aim")))
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            self.assertTrue(step_until(game, has_event("spit")))
            self.assertAlmostEqual(game.shots[0][3], 0.0, places=9)  # still along y = 4
            run(game, 4.0)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_standing_player_is_hit_by_the_shot(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 4)
        run(game, 5.0)
        self.assertEqual(game.hearts, HEARTS - 1)


class CueGapTest(unittest.TestCase):
    """Criteria 11 and 18: spitter offset 1.2 s and the 0.6 s cue gap in rooms 4-5 (step 35)."""

    def check_gap(self, game, fps, msg):
        tol = 1.0 / fps + 1e-9
        cueing, last_shot = False, None
        for t, kind, _ in game.events:
            if kind == "aim":
                self.assertFalse(cueing, (msg, "cue windows overlap", t))
                if last_shot is not None:
                    self.assertGreaterEqual(t - last_shot, 0.6 - tol, (msg, "gap", t, last_shot))
                cueing = True
            elif kind == "spit":
                self.assertTrue(cueing, (msg, "shot without a cue", t))
                cueing, last_shot = False, t

    def spitters_only(self, fps, room="4"):
        game = Game(fps=fps, room=room)
        game.enemies = [e for e in game.enemies if e.kind == "spitter"]
        game.hearts = 50  # keep the session going; only the spitters' pattern is looked at
        return game

    def test_rooms_4_and_5_first_shots_are_1_8_and_3_0_and_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = Game(fps=fps, room=room)
                game.hearts = 50
                run(game, 15.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertAlmostEqual(spits[1], 3.0, delta=tol, msg=(room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_other_rooms_keep_the_0_8_s_offset(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for _ in range(3):
                game.spawn("spitter", 1, 1)
            self.assertEqual([round(e.fire_in, 6) for e in game.enemies], [1.8, 2.6, 3.4])

    def test_forced_simultaneous_first_shots_still_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = self.spitters_only(fps, room)
                for e in game.enemies:
                    e.fire_in = 1.8
                run(game, 12.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertGreaterEqual(spits[1] - spits[0], 0.6 - tol, (room, fps))
                self.assertLessEqual(spits[1], 3.0 + 0.2 + tol, (room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_a_cancelled_cue_is_not_a_shot(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            for e in game.enemies:
                e.fire_in = 1.8
            run(game, 1.5)
            cueing = [e for e in game.enemies if e.cueing]
            self.assertEqual(len(cueing), 1, fps)
            cueing[0].hp = 0  # killed during its cue: no shot
            run(game, 1.5)
            spits = times(game, "spit")
            self.assertEqual(len(spits), 1, fps)
            self.assertTrue(1.9 <= spits[0] <= 2.5, (fps, spits))

    def test_a_cap_delay_only_lengthens_the_gap(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            game.hearts = 50
            for e in game.enemies:
                e.x, e.y = 15.0, 4.0
            game.place_player(0, 4)  # far away: shots stay in the air
            run(game, 20.0)
            self.check_gap(game, fps, fps)


class ShotContactTest(unittest.TestCase):
    """Criterion 20: any contact consumes a shot; only a player who can be hurt takes damage."""

    def still_shot(self, game, dx):
        game.shots.append([game.x + dx, game.y, 0.0, 0.0, 0.0])

    def test_a_shot_that_reaches_a_hurtable_player_hits_and_goes(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.45)
            game.step()
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(len(game.shots), 1, fps)

    def test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(6, 4)
            game.shots.append([9.8, 4.0, 0.0, 0.0, 0.0])  # the dash ends at x = 10, 0.2 from it
            game.press("dash", "right")
            run(game, 0.234)  # contact is at about 0.21 s, the dash ends at 0.25 s
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            run(game, 1.0)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            run(game, 1.0)  # the window (0.8 s) ends; the grub is still recovering or winding up
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(len(times(game, "hurt")), 1, fps)

    def test_a_shot_after_the_window_hits_again(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 1.0)
            self.assertFalse(game.invulnerable, fps)
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 2, fps)
            self.assertEqual(game.shots, [], fps)

    def test_two_shots_together_cost_one_heart_and_both_go(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            self.still_shot(game, -0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)


class LungeContactTest(unittest.TestCase):
    """Criterion 21: a lunge that touches a protected player is spent (step 38)."""

    def wall_lunge(self, fps, kind):
        # Player on the west wall, the grub lunging at it: a dash against the wall stays in place,
        # so the grub is still in reach when the dash ends.
        game = Game(fps=fps, room="empty")
        game.place_player(0, 4)
        game.spawn(kind, 1.5, 4)
        self.assertTrue(step_until(game, has_event("lunge")))
        return game

    def test_a_dash_spends_the_lunge_and_the_next_lunge_hurts(self):
        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.wall_lunge(fps, kind)
                game.press("dash", "left")
                run(game, 0.35)  # the dash (0.25 s) has ended, the lunge (0.3 s) is over
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))  # not cancelled
                run(game, 0.4)
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 5.0), (fps, kind))
                self.assertEqual(game.hearts, HEARTS - 1, (fps, kind))

    def test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.2  # contact at about 0.12 s is inside, the window ends at 0.2 s
            game._set_invulnerable(True, "test")
            run(game, 0.45)
            self.assertFalse(game.invulnerable, fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.enemies[0].phase, "recovery", fps)

    def test_a_lunge_that_first_touches_after_the_window_hits(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.05
            game._set_invulnerable(True, "test")
            self.assertTrue(step_until(game, has_event("hurt"), 0.5), fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)


class ShotSourceTest(unittest.TestCase):
    """Step 94 (W1, W8): the shot-hit message names the side the shot came from."""

    CASES = (
        ((15, 4), "east"),
        ((8, 0), "north"),
        ((1, 4), "west"),
        ((8, 8), "south"),
        ((15, 0), "north-east"),
        ((15, 7), "south-east"),  # ratio 3/7 = 0.43 > 0.4142
    )

    def test_direction_words_at_both_rates(self):
        for fps in (30, 60):
            for (x, y), word in self.CASES:
                game = Game(fps=fps, room="empty")
                game.spawn("spitter", x, y)
                run(game, 7.0)
                self.assertTrue(game.hurt_kinds, (fps, x, y))
                self.assertEqual(game.hurt_kinds[0], f"shot from the {word}", (fps, x, y))

    def test_player_view_line(self):
        out = ReactionTest.session(
            self, "room empty\nspawn spitter 15 4\nplayer 8 4\nend 7\n"
        )
        self.assertIn("YOU ARE HIT by a shot from the east — hearts 2/3", out)

    def test_absorbed_shot_prints_no_message(self):
        game = Game(room="empty")
        game.invulnerable = True
        game.shots.append([game.x + 0.2, game.y, 0.0, 0.0, 0.0])
        game.step()
        self.assertEqual(game.hurt_kinds, [])
        self.assertEqual(game.shots, [])


class LateSwipeTest(unittest.TestCase):
    """Step 94 (W5, W6): a damaging swipe in the lunge says it was too late."""

    def lunging(self, fps, kind):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, 10, 4)
        for _ in range(5 * fps):
            game.step()
            e = game.enemies[0]
            if e.phase == "lunge" and abs(e.x - game.x) <= 1.5:
                return game
        self.fail("no lunge in reach")

    def kinds(self, game):
        return [k for _, k, _ in game.events]

    def test_late_swipe_line_comes_before_the_hit(self):
        import play

        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.lunging(fps, kind)
                hp = game.enemies[0].hp
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, hp - 1, (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 1.0), (fps, kind))
                ks = self.kinds(game)
                self.assertEqual(ks.count("late_swipe"), 1, (fps, kind))
                self.assertLess(ks.index("late_swipe"), ks.index("hurt"), (fps, kind))
                text = play.Player.describe("late_swipe", {"enemy": kind})
                self.assertEqual(
                    text, f"the {kind}'s lunge had already started, the swipe was too late to stop it"
                )
                for bad in ("rears back", "takes aim", "YOU ARE HIT by"):
                    self.assertNotIn(bad, text)

    def test_no_line_in_windup_kill_or_recovery(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.2, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = self.lunging(fps, "grub")
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(4, 4)
            game.spawn("grub", 4.5, 4)
            game.spawn("grub", 4.5, 5)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 0.32)  # hit-stun passes, still hurt-invulnerable
            game.press("dash", "right")
            run(game, 1.5)
            hurt = times(game, "hurt")
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_dodger_agrees_at_30_and_60_fps(self):
        import bots

        for room in ("1", "2", "3", "4", "5"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    def test_walker_meets_criteria_13_and_14_at_each_rate(self):
        # Criterion 16d: the walker's per-room numbers may differ between rates (its 0.15 s
        # decision grid lands on different frames); it only has to meet 13 and 14 at each rate.
        # Build 0.6 note: the walker's UPPER limit of 6 hearts in rooms 3-5 is NOT asserted here.
        # Measured on 0.6: 7 hearts at 60 FPS. That is a tuning question for game-designer
        # (criterion 13, step 35/38 notes), reported in the build notes, not a build defect.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "12345"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 13: rooms 3-5 summed.
            walker_lost = lost("walker", "345")
            self.assertGreaterEqual(walker_lost, 3, (fps, walker_lost))
            self.assertGreaterEqual(cleared("walker", "345"), 2, fps)
            self.assertLessEqual(lost("dodger", "345"), walker_lost / 2, fps)
            self.assertEqual(cleared("dodger", "345"), 3, fps)
            self.assertLess(cleared("camper", "345"), cleared("walker", "345"), fps)
            # 15: the dodger dashes at least once in each of rooms 3-5.
            for room in "345":
                self.assertGreaterEqual(result["dodger"][room]["dashes"], 1, (fps, room))
            # 14: rooms 1-2 summed; the walker need not clear them.
            self.assertGreaterEqual(lost("walker", "12"), 1, fps)
            self.assertLessEqual(lost("dodger", "12"), 1, fps)
            self.assertEqual(cleared("dodger", "12"), 2, fps)

    def test_bot_log_adds_state_and_changes_no_result(self):
        import bots

        for name, bot in bots.BOTS.items():
            for room in ("1", "3"):
                for fps in (30, 60):
                    quiet = bots.play_room(bot, room, fps, 60)
                    loud = bots.play_room(bot, room, fps, 60, log=True)
                    for key in ("cleared", "seconds", "hearts_lost", "hits_by", "attacks", "dashes"):
                        self.assertEqual(quiet[key], loud[key], (name, room, fps, key))
                    self.assertEqual(quiet["log"], [])
                    hurt = [line for line in loud["log"] if "HEART LOST" in line]
                    self.assertEqual(len(hurt), loud["hearts_lost"], (name, room, fps))
                    for line in loud["log"]:
                        if "HEART LOST" in line:
                            self.assertIn("source", line)
                        elif "skipped decision" in line:
                            self.assertIn("reason: player stunned", line)
                        else:
                            for part in ("frame ", "grid ", "player (", "hearts ", "stunned ", "nearest ", "shots in flight"):
                                self.assertIn(part, line, (name, room, fps, line))

    def test_walker_logs_the_exact_distance_it_compared(self):
        import bots

        result = bots.play_room(bots.BOTS["walker"], "1", 60, 60, log=True)
        self.assertTrue(any("(exact " in line for line in result["log"]))

    def test_dodger_never_swipes_a_brute_in_wind_up(self):
        import bots

        for fps in (30, 60):
            result = bots.play_room(bots.BOTS["dodger"], "2", fps, 60, log=True)
            self.assertFalse(any("swipe brute wind-up" in line for line in result["log"]), fps)


class ReactionTest(unittest.TestCase):
    def session(self, script):
        import contextlib
        import io

        import play

        setup, inputs, rules = play.read_script(script)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            play.play(setup, inputs, "player", rules)
        return out.getvalue()

    def test_rules_react_to_what_is_on_screen(self):
        out = self.session("room empty\nspawn grub 9.2 4\nwhen see g within 1.4 then attack\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("YOU ARE HIT", out)

    def test_cues_show_in_the_player_view(self):
        out = self.session("room empty\nspawn grub 10 4\nspawn spitter 1 1\nend 2.5\n")
        self.assertIn("a grub rears back", out)
        self.assertIn("a spitter takes aim", out)
        self.assertIn("~", out)
        self.assertIn("cue: g", out)
        self.assertIn("cue: s", out)

    def test_marks_r_and_G_are_drawn(self):
        out = self.session("room 2\nend 0.2\n")
        self.assertIn("r", out)
        self.assertIn("G", out)

    def test_a_rule_acts_at_most_every_reaction_time(self):
        import play

        rule = play.Rule("when see g within 20 then attack")
        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        fired = 0
        for _ in range(60):  # one second at 60 FPS
            before = rule.last
            play.react(game, [rule], [], [])
            fired += rule.last != before
            game.step()
        self.assertEqual(fired, 7)  # 0.0, 0.15, ... 0.9

    def test_rules_ignore_what_is_not_drawn(self):
        import play

        game = Game(room="empty")  # nothing on screen
        view = play.View(game, [])
        self.assertIsNone(view.nearest())
        self.assertTrue(play.Rule("when nothing within 3 then stop").matches(view))

    def test_rules_and_timed_inputs_mix(self):
        out = self.session("room empty\n0.1 dash right\nwhen see g within 1.4 then attack\nend 1\n")
        self.assertIn("you dash right", out)

    def test_a_bad_rule_says_how_rules_read(self):
        import play

        with self.assertRaises(ValueError) as caught:
            play.Rule("when grub close then hit")
        self.assertIn("conditions:", str(caught.exception))


class PlayerViewMessageTest(unittest.TestCase):
    """F2 (brute shrug message, criterion 19a) and F3 (banner 0.6) in the player view."""

    SHRUG = "the brute shrugs off the swipe"

    def session(self, script):
        return ReactionTest.session(self, script)

    def brute_script(self, fps):
        return (
            f"room empty\nfps {fps}\nspawn brute 9 4\nplayer 8 4\n"
            "0.1 attack\n0.5 attack\nend 4\n"
        )

    def test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message(self):
        for fps in (30, 60):
            out = self.session(self.brute_script(fps))
            self.assertEqual(out.count(self.SHRUG), 2, fps)
            lines = [l for l in out.splitlines() if self.SHRUG in l]
            self.assertTrue(lines[0].lstrip().startswith("0.1"), (fps, lines))
            self.assertTrue(lines[1].lstrip().startswith("0.5"), (fps, lines))
            self.assertIn("you swipe: brute hit", out, fps)

    def test_a_kill_in_wind_up_prints_no_message(self):
        import contextlib
        import io

        import play

        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.enemies[0].hp = 1
            game.press("attack")
            texts = [play.Player.describe(k, d) for _, k, d in game.events]
            self.assertFalse(any(t and "shrugs" in t for t in texts), fps)
            self.assertIn("you swipe: brute defeated", texts, fps)

    def test_swipes_at_a_grub_or_runner_print_no_message(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                out = self.session(
                    f"room empty\nfps {fps}\nspawn {kind} 9 4\nplayer 8 4\n0.1 attack\nend 1\n"
                )
                self.assertNotIn("shrugs", out, (fps, kind))

    def test_the_message_does_not_change_the_simulation(self):
        import play

        self.assertEqual(
            play.Player.describe("shrug", {"enemy": "brute"}), self.SHRUG
        )

    def test_the_banner_shows_0_6(self):
        for fps in (30, 60):
            for room in ("1", "empty"):
                out = self.session(f"room {room}\nfps {fps}\nend 0.2\n")
                self.assertEqual(
                    out.splitlines()[0], f"Lantern Depths 0.6 — room {room} — {fps} FPS"
                )


class VariantMessageTest(unittest.TestCase):
    """D-011: wind-up and hit messages name the variant."""

    def session(self, script):
        return ReactionTest.session(self, script)

    def test_wind_up_and_hit_messages_name_the_variant(self):
        for fps in (30, 60):
            for kind in ("grub", "runner", "brute"):
                # Window of 1.0 s: it holds the first wind-up and its hit (grub 0.67 s, runner
                # 0.53 s, brute 0.87 s) but ends before any variant can wind up a second time
                # (earliest: the runner, about 1.15 s). So one wind-up means one message.
                out = self.session(f"room empty\nfps {fps}\nspawn {kind} 9.5 4\nend 1.0\n")
                self.assertEqual(out.count(f"a {kind} rears back"), 1, (fps, kind))
                self.assertEqual(out.count(f"YOU ARE HIT by a {kind}"), 1, (fps, kind))
                self.assertIn(f"YOU ARE HIT by a {kind} — hearts 2/3", out, (fps, kind))
                for other in ("grub", "runner", "brute"):
                    if other != kind:
                        self.assertNotIn(f"a {other} rears back", out, (fps, kind))
                        self.assertNotIn(f"by a {other}", out, (fps, kind))

    def test_a_shot_hit_message_is_unchanged(self):
        for fps in (30, 60):
            out = self.session(f"room empty\nfps {fps}\nspawn spitter 1 4\nend 5\n")
            self.assertIn("YOU ARE HIT by a shot from the west — hearts 2/3", out, fps)

    def test_rears_back_rule_matches_all_variants(self):
        import play

        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        rule = play.Rule('when text "rears back" then stop')
        for kind in ("grub", "runner", "brute"):
            view = play.View(game, [f"a {kind} rears back"])
            self.assertTrue(rule.matches(view), kind)

    def test_manual_has_the_new_wording(self):
        text = (Path(__file__).resolve().parent.parent / "manual.md").read_text(encoding="utf-8")
        self.assertIn("A brute is never cancelled.", text)
        self.assertIn("so in room 3 up to 5 can be in the air at once.", text)
        self.assertNotIn("no more than 3 are in the air at once", text)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-002-contact-edge-graze-accepted.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-002: Per-frame contact sampling is kept; the contact-edge graze is an accepted limitation of the text build

## Decision

Contact (shot reach 0.4 tile, grub lunge reach 0.6 tile) stays a distance check once per frame after that frame's movement, with no swept test. At 30 and 60 FPS the hit or miss may differ only when the path's lateral miss lies in a narrow band just inside the reach: 0.39–0.40 tile for shots, 0.57–0.60 tile for lunges. Outside the band both rates must agree and follow the geometry. The band changes hit or miss only, never timing. The limitation is recorded in `design/combat.md` (Contact sampling rule, criterion 17, 16e).

## Rationale

- The band is tiny: about 0.003 tile for shots (QA, derived) and about 0.015 tile for lunges at 30 FPS (derived, not yet run). The player-sized sidestep margins are 0.3 tile or more, and the lane is 1.2 tiles wide. A player cannot see or aim at a difference of 0.003 tile.
- Both outcomes are "fair": the shot always visibly passes within about 0.4 tile of the player.
- A swept test would be a build change for no player-observable gain, against the project constraint of a small team that reuses existing systems.
- The damage a change could cause is larger than the effect: a new contact test would shift every hit time in the verified build 0.5.

## Alternatives considered

- Swept (continuous) contact test with a tolerance between 30 and 60 FPS: removes the band but changes a verified build, and has a cost with no visible benefit. Not chosen.
- Fixed sub-step contact at 120 Hz at both rates: same objection, and it only narrows the band.
- Widening the reach slightly so the case never sits in the band: moves the band, does not remove it, and changes tuning for every cue-based criterion.

## Revisit when

- A graphical build uses different hitboxes or a different contact test (re-verify criterion 17 at 30 and 60 FPS).
- A playtest reports "I dodged it and it still hit me" or the reverse, and the cause is the edge band.
- A lunge band wider than 0.03 tile is measured (QA's close-out run).
>>>END

<<<FILE decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-003: A miss of exactly the reach is inside the contact band; measured lunge band recorded (follow-up to D-002)

## Decision

This is a follow-up to D-002. D-002 stays in force and is not edited. It is refined as follows.

1. **Exactly the reach is inside the band.** A path whose lateral miss is exactly the reach (0.400 for shots, 0.600 for lunges) belongs to the accepted band. Hit or miss is accepted at either frame rate, and 30 and 60 FPS may differ. It is not a guaranteed miss. The `distance <= reach` check in the build stays, so no Build change is needed.
2. **The band has no gap and no overlap.** It is the lateral miss more than reach − tolerance and up to and including the reach: more than 0.39 up to 0.40 for shots, more than 0.57 up to 0.60 for lunges. At reach − tolerance or less: hit at both rates. More than the reach: miss at both rates. Criterion 17 and the contact sampling rule in `design/combat.md` are reworded to this. No number changes, so criteria already verified in handoffs 20 and 24 remain valid.
3. **Measured lunge band (QA, handoff 24, derived and probed).** A lunge hit is guaranteed up to a lateral miss of about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. Probes: 0.570 hit and 0.610 miss at both rates; the rates disagreed only at 0.590 (0.580 and 0.599 agreed, because the frame phase differs between positions). **Limit:** five probes, not a full scan. There is no evidence of a band wider than 0.03 tile, which is the threshold at which QA must report back. The shot band figure (about 0.003 tile) is likewise derived.

## Rationale

- Exactly the reach cannot be made a guaranteed miss without changing `<=` to `<`. That is a Build change to a verified build, and then a re-Verify, for a case a player cannot produce or see (a difference of 0.000 tile). D-002 already rejected changing contact for no player-observable gain.
- Putting the reach inside the band matches the band definition QA read ("reach − 0.01 to reach") and makes criterion 17 unambiguous without changing what was verified.
- Recording the measured band keeps D-002's estimate ("derived, not yet run") honest. The figures are well inside the 0.03 tolerance, and the sidestep margins (0.3 tile or more, 1.2-tile lane) are far larger.

## Alternatives considered

- Guaranteed miss at exactly the reach (`<` instead of `<=`): the cleaner rule on paper, but a Build change plus re-Verify of every hit-time criterion, with no visible benefit. Not chosen.
- Leave the wording ambiguous: QA already had to make a judgment call. Not chosen.
- Run a full scan of the lunge band before recording: not needed. The decision does not depend on the exact width as long as it stays within 0.03 tile.

## Revisit when

- QA or a playtest finds a lunge band wider than 0.03 tile (report to `game-designer`).
- A graphical build uses different hitboxes or a different contact test (as in D-002); criterion 17 must then be re-verified and the band rewritten.
- A playtest reports "I dodged it and it still hit me" or the reverse, and the cause is the edge band.
>>>END

<<<FILE decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
---
kind: decision
id: D-004
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-004: Rooms 4–5 get a rule-based 0.6 s cue gap; the brute's wind-up is not cancelled by a swipe; the room 2 spitter is deferred

## Decision

1. **Cue gap as a rule (rooms 4 and 5 only).** A spitter may start a cue only when no other spitter's cue is running and the last shot in the room was at least 0.6 s ago (plus the existing cap). The first-shot offset in these rooms is 1.2 s (shots at 1.8 s and 3.0 s, then alternating every 1.2 s), which meets the rule exactly. The interval stays 2.4 s, the cap stays 3, and room 3 is unchanged.
2. **Brute is not cancelled by a swipe in wind-up.** A per-variant flag "swipe cancels wind-up": standard yes, runner yes, brute no. A swipe still damages the brute, shows "the brute shrugs off the swipe", and the lunge goes ahead. The lane geometry is the same for all variants.
3. **Option 3 (a spitter in room 2) is deferred** out of this slice.

## Rationale

- The crossfire problem (31, S4) is that a cue locks 0.2 s after the previous one ends, at the place the player dodged to. The playtest said the spitters fired "in sync", which the room table and the spec do not support. A rule on cue windows is correct either way, and a fixed offset alone would not be: a cap delay can push two cues together and the offset would not stop it. The offset is chosen so that the rule normally never has to delay anything, which keeps the verified first-shot timing style.
- The melee enemies share one answer (31, S1). A per-variant flag reuses the existing wind-up rule, keeps lane geometry and cue visuals identical (visual spec), needs no new input (D-001) and no new enemy. The brute is the best carrier: it is slow, has the longest warning and the longest recovery, so "step aside, then punish" is readable and fair.
- Option 3 would change criterion 14 and the room 2 identity at the same moment as the brute rule. Both aim at the brute dodging for 20 s, and it is not known whether the brute rule is enough. Doing both together would also make the next playtest unable to say which change worked.

## Alternatives considered

- **Only change the offset, no rule:** simpler, but not robust against a cap delay or against the unconfirmed "in sync" claim. Not chosen.
- **Lower the shot cap to 2 in rooms 4–5:** shortens the number of lines in the air, but delays cues unpredictably and makes the cue timing differ from room 3 in a way the player cannot read. Not chosen; the longer spacing already reduces shots in the air through the existing cap.
- **Gap rule in room 3 too:** room 3 teaches the cue and is verified; criterion 11 would change for no reported problem. Not chosen.
- **A new melee enemy, or widening a lane for the brute so that a dash is needed:** needs a Decide step or breaks the "identical lane geometry" rule of the visual spec. Not chosen.
- **Brute swipe cancels only with the second swipe, or cancels with a longer stagger:** a more complex rule for the player to learn, with no extra answer. Not chosen.
- **Take Option 3 in this slice:** deferred (see Rationale).

## Revisit when

- The hand-timed playtest after Build shows the crossfire in rooms 4–5 is still unfair, or the gap makes it trivial (then the gap and offset are tuning values).
- The playtest shows a human still dodges the brute without ever fighting it in room 2 (then take Option 3 or a room change in a new spec step).
- The bots show the 13/14/15 expectations cannot be met on 0.6 and the cause is the design, not bot policy.
- A graphical build changes cue presentation in a way that makes the "no flinch" signal unreadable.
>>>END

<<<FILE decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-005: A contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted

## Decision

1. **Shots are consumed by any contact.** A shot that makes contact (distance <= 0.4 tile, unchanged detection) with a player who cannot be hurt (dash, hit-stun, or hurt invulnerability up to 0.8 s after a hit) disappears on that frame and deals no damage. It does not pass through and does not wait for the window to end.
2. **A lunge has one hit, and a blocked contact spends it.** A lunge that makes contact (distance <= 0.6 tile) with a protected player deals no damage for the rest of that lunge, even if the protection ends while the grub is still in reach. The lunge is not cancelled or shortened (existing rule), and the next lunge after the recovery damages normally.
3. **Contact sampling is unchanged** (D-002, D-003). Only the consequence of a detected contact changes.
4. **The cue gap rule (D-004) is not extended** to room 3 or practice rooms. A simultaneous cue start there after a cap delay is accepted. Criteria 11 and 18 are unchanged for them.

## Rationale

- The spec said a shot "disappears on contact with the player", so consuming it is the reading closest to the existing text. QA (handoff 36) saw damage land exactly when the hurt window ended (0.15–0.2 s after the shot visibly reached the player), and chained hits at the end of each window. That breaks the pillar "every threat is visible before it can hurt": the player sees the shot touch them, nothing happens, and damage arrives later with no visible cause.
- Consuming makes the dash a clean answer: a shot or lunge that the dash overlaps is finished and cannot hit on the frame after the dash ends. The playtest reported the dash unused; one of the reasons it is unattractive can be that overlap with a threat is risky at the dash's end. This does not make the dash required, so criterion 15 stays a report-only risk.
- Difficulty: rooms 4–5 get easier only in the case of chained hits on a player who is already hurt, which is the unintended behavior. The intended difficulty (a still player is hit by each shot aimed at them that arrives after the window) stays. If the rooms become too easy, the levers are the offset, interval and cap, which are tuning values.
- Lunges: the same rule for the same reason, at a smaller scale (a lunge lasts 0.3 s, the window 0.8 s, so the case is rare but possible when a shot hit just before a lunge).
- Room 3 and practice rooms: the simultaneous start was reproduced only in a practice replica; room 3 is the room that teaches the cue and its verified timing would not change; two simultaneous lines are two readable cues that a sidestep or dash answers. The cost of extending the rule (a changed verified criterion in room 3, code for rooms that the playtest did not flag) outweighs a hypothetical gain.
- Both rulings stay inside D-001 (no new input), the pillars, and the Goal's scope: no new enemy, no healing, no new room content.

## Alternatives considered

- **Pass through (the shot continues and may hit later at a different place):** keeps the shot alive in the air for up to 5 s behind the player and can hit the player when they step back, with the same "hidden hit" problem; harder to read. Not chosen.
- **Stay and hit when the window ends (the apparent 0.5 behavior):** hidden, delayed damage; makes the hurt window a delay rather than protection, chains hits (the 0.8 s window equals the hit spacing in room 3), and weakens the dash. Not chosen.
- **Consume on hurt window but pass through during a dash (so the dash "avoids" but does not "eat"):** a more complex rule with two behaviors for the same thing. Not chosen.
- **A lunge that stops at the first contact with a protected player:** contradicts the existing "the grub finishes the lunge" rule and changes recovery timing in criteria 3 and 5. Not chosen.
- **Extend the gap rule to room 3 and practice rooms (or a smaller start-tie rule):** see Rationale. Not chosen now.
- **Change contact sampling (swept test):** rejected in D-002.

## Revisit when

- The hand-timed playtest after Build finds rooms 4–5 too easy or the dash still unused (then tuning values, or a new spec step; not a silent revert).
- A real-room trace of room 3 (or a playtest) shows simultaneous cue starts that a player cannot answer (then extend a gap or start-tie rule).
- QA's criterion 20 shows the 0.6 build cannot meet the rule for a technical reason (then `technical-director`).
- A graphical build uses a different hitbox or contact test (as in D-002).
>>>END

<<<FILE decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-006: Criterion 13's walker limit in rooms 3–5 is 3–7 hearts, with at least 2 rooms cleared; no room or enemy parameter changes

## Decision

1. The walker's hearts-lost limit in rooms 3–5 (each rate separately) changes from 3–6 to 3–7. The "clears at least 2 of 3" gate is the primary check that the player is not walled out.
2. The upper limit of 7 is the structural maximum for a walker that clears 2 rooms (3 hearts per room, at most 2 lost in a cleared room). It is kept as a consistency check, not an independent tuning target.
3. Bot results are balance proxies. Per-room walker numbers, and a 30/60 FPS difference in the walker's totals, are not criteria.
4. No room, enemy, cap, offset or interval parameter changes. D-004 and D-005 stand. Build 0.6 is unchanged.
5. The full amended wording is in `design/combat-step-44-walker-limit.md`.

## Rationale

- The limit of 6 was the 0.5 observation recorded as a limit, not a derived bound. The purpose (costly but not hopeless) is met at 7: the dodger loses 0 and clears 3/3, the camper clears 0, and the walker still clears 2 of 3 at both rates.
- A hearts ceiling below the structural maximum only forbids certain distributions of the same outcome. The walker's grid sensitivity moves single hearts between rooms without any player-visible cause. Tuning rooms against it would fit the bot, not the player.
- D-004 and D-005 predicted opposite pressures on the walker (brute no longer cancelled: more losses; consumed shots: fewer). The net result is a consequence of those rulings and is accepted.
- A parameter change would reopen verification of criteria 11, 13, 14, 15, 18, 20 and 21 with no player-visible gain.

## Alternatives considered

- **Keep 6 and change a parameter** (for example a longer brute recovery, or fewer shots in room 4): it fits the grid phase of one bot, forces a wide QA re-verify, and risks undoing D-004 or D-005. Not chosen.
- **Change the walker bot's decision grid:** it changes test tooling to hit a number, hides the real sensitivity, and is not a design answer. Not chosen.
- **Drop the hearts upper limit entirely:** equivalent in practice. Keeping 7 keeps the old criterion shape and a visible check that a walker that clears 2 rooms is within the structural bound. Not chosen, but acceptable if QA prefers.
- **Express the limit as one range across both rates:** weaker, because a rate-specific failure could be hidden. The rates stay separate. Not chosen.

## Revisit when

- QA's independent figures show the walker clearing fewer than 2 of 3 rooms at either rate, a total below 3, the dodger over half the walker's total, or the camper clearing as many rooms as the walker.
- The hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5.
- Any later change to rooms 3–5, the brute, the spitter schedule or the cap moves the bot figures. Re-measure; do not assume 7 still holds.
>>>END

<<<FILE decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
---
kind: decision
id: D-007
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-007: Simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to the real in-flight bound

## Decision

1. This is the revisit of D-005 item 4 for room 3, triggered by a real-room trace (QA, handoff 43). Outcome: **accepted as built**. D-005 items 1–4 stand unchanged, and D-004 and D-006 are not touched.
2. The cap stays a limit on cue starts (fewer than 3 shots in flight at the check). It is not rechecked at shot release.
3. Criterion 11 is reworded. Shots in flight never exceed 2 plus the living spitters. That is at most 3 in rooms 4–5 (cue windows never overlap) and up to 5 in room 3 after a cap delay. The sentence "rooms 1–5 never more than 3" is withdrawn.
4. No build change, no parameter change. The reword and the new observation check are in `design/combat-step-46-room3-cap.md`.
5. Reopen triggers are in the same note: a human hit by most of a simultaneous volley, a shot reported as "out of nowhere", or a real-room count above 5. The prepared fallback is a 0.2 s cue gap in room 3.

## Rationale

- The cue is the telegraph. Dropping or refusing a shot whose cue is already showing would make cues lie.
- Three simultaneous cues give three readable lines locked on one point. Moving about 1 tile off that point clears all three, and a dash clears any line it crosses. Shots take up to about 4 s to cross the room, so the arrivals are spread out.
- The case needs a player who keeps spitters alive and shots in the air for several seconds. It was seen only with a scripted dasher, and whether a human can answer it is not observed.
- The only consistent fix changes room 3, the room that teaches the cue, and forces re-measuring of criteria 13, 15, 16 and 18, for an unconfirmed problem.
- The conflict was in the criterion text, not in the rule. D-005 and step 22 already described the 2 plus living spitters bound.

## Alternatives considered

- **Re-check the cap at shot release:** drops or delays shots after the cue showed them, so cues lie. Not chosen.
- **Lower cap for room 3 (for example 2):** more and longer delays, and the cue timing in room 3 drifts from what the player learned. D-004 already declined this for rooms 4–5. Not chosen.
- **Fixed cue gap of 0.2 s in room 3 (the rooms 4–5 mechanism):** keeps first-shot timing and caps the count at 3, but is a change to a verified room and to D-005 item 4. Kept as the prepared fallback, not taken now.
- **Keep criterion 11 as "never more than 3":** it would make the build fail against a rule the spec has stated since step 22. Not chosen.

## Revisit when

- The hand-timed playtest of room 3 shows a human cannot answer a simultaneous volley (hit by most of it, or "came out of nowhere").
- QA's `*` count at 7.5 s or 11.7 s is above 5, or above 3 in rooms 4–5.
- A real-room trace shows simultaneous starts in room 3 before any cap delay.
- Any change to the cap, the spitter interval or the room 3 schedule.
</parameter>
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

<<<FILE goals/G-002-final-boss/14-game-designer-to-studio.md
---
kind: handoff
goal: G-002
seq: 14
from: game-designer
to: studio
stage: Plan
outcome: done
---
# 14: game-designer → studio — 基準適用を確定し、実測と再判断を含むPlanへ渡す

## Task

D-019と仕様補足の適用関係を確認し、Technical DirectorのPlanを開く。実測後のDesigner再判断をReview前の経路に含める。

## Context

D-018が採択した方向に基づき、Designer権限でD-006・step44と関連基準のG-002新構成への適用変更を確定した。過去G-001の判断・結果と既存Decision本文は変更していない。

## Findings

make-decisionとwrite-design-specに従い、以下を作成・補足した。

- `decisions/D-019-g002-balance-criteria-applicability.md`：限定的な適用変更と関連基準の採否。
- `design/final-boss-and-continuous-run.md`：冒頭、§8、§10を更新。保持・適用終了・置換先、対応bot条件、実測後の再判断経路を確定。
- `design/combat.md`、`design/combat-step-44-walker-limit.md`：G-002の適用注記を追加し、旧記載から新構成の誤判定を防ぐ。

旧独立3〜5のwalker3〜7 hearts・2/3 clear、dodgerのwalker比1/2以下・3/3 clear、camperのwalker未満clearを新構成のゲートから外した。FPS別旧集計、過去数値、旧逸脱報告・再判断条件も新構成へ移さない。

第1〜4部屋、共有ルール、独立3 hearts開始、独立1〜2比較、独立1〜4のdodger FPS比較を保持する。独立3・4は各botを部屋別・30/60 FPS別に報告する。新合計下限・上限・clear数は導出しない。

基準15は独立3・4の既存規則とゼロdash時のDesigner報告を保持する。新5番は使用回数条件を終了し、B6で各攻撃への実接触、無傷、消費、dash終了後の追加被害なしを確認する。横移動の有効性と独立Playも保持する。

ボス対応dodgerの新5番FPS比較は「同じclear結果・hearts lost差1以下」を採択した。同一方針・ビルド・初期状態・limit、playerに見える情報、0.15秒反応を条件とする。独立3 hearts開始と連続ランで可能な2 hearts開始を別比較する。対応確認前の成績は合格根拠にしない。death／unfinishedを区別し、両FPSの失敗一致を攻略可能性の証拠にしない。帯内接触による差でも数値閾値超過は自動免除せずDesignerへ戻す。

§8は関連BotsTestの各assert群、CueGapTest、構成試験、共有回帰を対応付けた。旧fixtureは必須にせず、必要なら共有回帰に限定する。削除だけで完了にせず、B1〜B10・V1、R1〜R5、T1〜T4、C1〜C3、V2、独立Playと同一試行の時間計測へ接続する。

追加数値ゲートは未設定。対応botの両FPS基線、独立QA、独立Play、通常ランの到達・終端・時間実測を受け、Review前にDesignerが必要性を判断する。追加不要の場合も理由を記録する。明白な対処不能・到達不能ならPlay前にも戻す。

本Stepは文書上の適用整理であり、play／botsは実行していない。実行成功、指定sha一致、難度、体験、所要時間の新しい証拠はない。コードとテストの実装改訂も行っていない。

## Decisions already made

- D-006：過去構成の正本として保持。G-002新構成への適用はD-019で限定変更。
- D-015／D-016：承認された連続ラン、単体ボス、体験方向と範囲を保持。
- D-017：ボス・回復・境界・終端・時刻・表示の詳細契約を保持。
- D-018：旧集計を新構成評価から分離する方向。
- D-019：その適用変更、dash検証、対応bot FPS比較、実測後の再判断を確定。

## Constraints

Owner request、Interpretation、第1〜4部屋と共有ルールを維持する。新戦闘入力、ボスチェックポイント、既存部屋全面改修は追加しない。

15〜20分のVisionを維持し、時間合わせだけのHP増加・待機水増しをしない。独立部屋時間を合算して連続ラン実測と扱わない。

技術方式、実装順序、工数、実機入力経路はTechnical Directorに残す。Plan完了前にBuildを開かない。独立QA、限定Art Verify、独立Play、Reviewを維持する。Playtester資料はStudioが作成し、設計上の期待結果・Review用体験信号を渡さない。

## Open questions

1. Technical Director：指定sha `27fe16268ac8`、対象ビルド、0.4／0.6表記差と既存試験の実行基線を同定できるか。
2. Technical Director：長時間player／状態観測、pause／resume、retry、両時刻・入力、実機操作、表示と境界試験を実現・観測する方式、工数とリスクは何か。
3. Designerへの後続再判断：実測に基づき独立3・4、新5番、連続到達・回復・retryへ追加数値ゲートや調整が必要か。現時点では未判断であり、Plan開始の権限上の衝突ではない。

## Expected output

Studioは適用整理の完了を確認し、Technical Directorへ§10の依存と§8の試験対応を含むPlanを渡す。Planは対応botの確認、両FPS計測、通常ランの同一試行計測、実測後のDesigner再判断を明示する。

Planと必要判断の後、Build→独立QA→限定Art Verify→独立Play→Designerの実測後判断→Reviewへ進む。QAまたは初回基線で問題が判明した場合は前倒しで再判断する。承認超過、Owner Decision変更、範囲内で解消不能なVision不整合はStudioからGame Directorへ返す。G-002は進行中とする。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: repo/tests/test_game.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#current-state
- Project: goals/G-002-final-boss/goal.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/13-studio-to-game-designer.md
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

- Write the outgoing Handoff as goals/G-002-final-boss/16-technical-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
