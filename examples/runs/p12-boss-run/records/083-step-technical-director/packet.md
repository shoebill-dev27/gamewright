# Studio operation packet

operation: Step
goal: G-002
role: technical-director
incoming_handoff: goals/G-002-final-boss/66-studio-to-technical-director.md
next_seq: 68
runs: tests, trace (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-final-boss/68-technical-director-to-<recipient>.md
- decisions/D-025-<name>.md
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-002-final-boss/66-studio-to-technical-director.md
---
kind: handoff
goal: G-002
seq: 66
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 66: studio → technical-director — 検証計画を供給上限と証拠区分へ適合

## Task

62の技術計画をD-023・D-024へ適合させ、試験道具対応、再測定、独立QAを実行可能な直列Stepへ分割する。歴史的一致の確認不能を保持したまま、後続工程へ進む条件と判断先を明示する。

## Context

60のQAはfailであり、同じ入力・実行・証拠不足のまま第三のQAを開かない。OwnerはD-023で利用可能な供給条件を確定し、その範囲で継続を指示した。65でDesignerがD-024と証拠適用補足を納品したため、予定どおり技術再計画へ進む。

今回の担当は再計画である。製品変更、再測定結果、独立QAの合否を先取りしない。

## Findings

62の技術所見と依存順序を出発点とする。ただし、変更前基線の探索・供給、完全ログの保存・再読込みの確保を開始条件にする部分は置き換える。

D-023の供給は以下に限る。

- Loadに個別指定したファイルは本文が届く。ディレクトリ指定はファイル名だけ。
- 各Stepの@needは一度、最大8ファイル。
- 各Stepの@runは最大3回。別の実行枠はない。
- 実行出力は先頭・末尾を含む最大2万字。全文保存先はない。
- 変更前ビルドは存在しない。

D-024により、以下を分離する。

- L1・O3・step68 V-c・step94 W7等の歴史的一致は確認不能。現行suite成功や同一現行ビルド内の対照で埋めない。
- 独立1〜4 dodgerは40の記録との比較。各FPS・部屋、開始3 hearts、通常初期状態、limit 60秒を揃える。clear、損失0、dash数、小数1桁へ所定の方法で丸めた時間を比較する。補足仕様の表を正本とする。
- 40は既にボス対応後のsource 5145454ab956の記録であり、ボス対応前の厳密一致を証明しない。56は別の後続記録として扱う。
- 現行仕様照合、現行内対照、保持共有基準、FPS比較は継続する。

62の公開情報限定ボス判断境界、突進接触診断の訂正、開始3/2 hearts×30/60 FPSの再測定、独立1〜4保持比較、新botによる通常ラン入力再生成の依存関係を維持する。対応前ボス値と生成再生時間を新たなpass基線にしない。

## Decisions already made

- D-019：保持回帰、公開情報限定ボス比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト方式で進める。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- D-023：実際の本文・実行・出力上限に適合させ、存在しない保存機構や変更前ビルドを待たない。
- D-024：歴史的一致の確認不能、記録精度に限定した比較、現行検証を分離する。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goalの解釈を変更しない。60のfailを上書きせず、確認不能をpass・免除・適用終了にしない。

未表示・切断部分は確認済みにしない。ハッシュ、summary、成功件数だけで必要な証拠本文を代用しない。一方、出力全文の永続保存を再び要求せず、検証対象を絞る出力と直列分割で構成する。

限定Art Verify、独立Play、実測後Designer判断、Game Director Reviewを維持する。独立Playへ実装履歴、QA判定、期待結果、本補足の比較値を渡さない。

## Open questions

1. どの基準をどのStepで扱い、各Stepの本文・最大3回の実行・出力上限をどう割り当てるか。
2. 全判断を対象とする公開情報条件の検証と突進接触診断を、表示範囲・集計方法・未表示範囲が明確な証拠へどう構成するか。
3. 歴史的一致の確認不能を残す場合、62の「全QA合格後」をどの工程条件へ整理するか。技術上の進行可否とGoal達成判断を分離し、方向・範囲の判断が必要ならGame Directorへ返すこと。
4. 記録比較に差が出た場合、条件と共有処理への影響をどう整理してDesignerへ返すか。

## Expected output

Studio宛のHandoffに、62を置き換える適合計画をまとめる。

- 影響システム、順序、各Stepの完了条件、リスクと対策、逐次実行の理由。
- 各Engineer・QA Stepが必要とするファイルを個別名で列挙したLoad案。追加本文が必要なら、各Stepの@need上限を踏まえて配置する。
- 基準ID・FPS・初期条件・入力・source識別・試験assert・出力対象・結論・未確認を対応付ける証拠構成。
- 各Stepの最大3回の実行配分と、出力切断を避ける対象別出力。残作業だけならpartialで直列継続できる単位。
- 公開情報bot対応→診断・試験→4条件再測定→保持回帰・通常ラン再生成→独立QAの順序と受渡し。
- 歴史的確認不能を含むQA結果から、限定Art Verify以降へ進む条件。未解決事項を最終Reviewへ残し、必要な権限判断は適切なRoleへ返す。

後続QAは実装者の自己評価から独立させ、全tests本文を必要な検証単位へ個別に割り当てる。今回の8つのコード・テスト本文だけで全QA資料が揃ったとは扱わない。

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
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/65-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
runs: tests, trace
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

<<<FILE design/combat-step68.md
# Combat design addendum, step 68 (stale sentences, manual wording, variant messages)

Status: wording and message strings only. No rule, parameter, timing or room change. Where this file differs from `design/combat.md`, `design/combat-step59.md` or `repo/manual.md`, this file governs. Decisions: D-007 (unchanged), D-011 (accepts and completes D-008).

## 1. Stale sentences, superseded (room 3 in-flight bound)

`design/combat-step-46-room3-cap.md` (amended criterion 11, D-007) governs the cap. These sentences are superseded and must be folded out the next time the files are edited:

- `combat.md`, Cap paragraph: "In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3". Replacement: in rooms 4–5 the count stays at 3 or fewer; in room 3 up to 5 is accepted after a cap delay (2 plus the living spitters).
- `combat.md`, criterion 11: "In rooms 1–5 never more than 3 shots in flight". Replacement: criterion 11 as amended in the step 46 note (a–e).
- `repo/manual.md`, spitter paragraph: "and no more than 3 are in the air at once". Replacement (exact text): "A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once."

## 2. Manual wording for late swipes (step 59, point 1, unchanged rules)

Replace the sentence in the grub warning bullet "or swipe a grub or runner (within 1.5 tiles) to cancel it" with this exact text:

"or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. One swipe is enough to cancel a grub or a runner. A brute is never cancelled."

This covers every point of the step 59 acceptance list.

## 3. Runner cancel vs kill

No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. A late swipe on a runner in reach is therefore a kill, not a cancel, and QA cannot and need not distinguish them. Criterion 6 for the runner reads: an in-reach swipe during wind-up kills it with no lunge.

## 4. Variant messages (D-011; supersedes the message table in step 59 point 2)

| Variant | Mark | Wind-up message | Hit message |
|---|---|---|---|
| Standard grub | `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner grub | `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute grub | `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | n/a | unchanged | `YOU ARE HIT by a shot` (unchanged) |

Rules:
- All three wind-up messages contain `rears back`. Rules keyed on `text "rears back"` match all variants. Rules keyed on `a grub rears back` or `by a grub` match only the standard grub after the change.
- The hit message keeps its current hearts suffix. Only the noun changes.
- Applies in the player view and any other text view that prints these strings. The `cue:` line, `~` line, all timings, the swipe, kill and shrug messages, and spitter messages are unchanged.
- Graphical presentation is not affected.
- Tests and bots that match the old strings are updated by the Build.

Acceptance (verification), at 30 and 60 FPS, practice room, one case per variant:
- V-a. Each wind-up prints its message once, at the same moment as today (±1 frame).
- V-b. A hit by each variant prints the matching hit message on the frame of contact, with unchanged hearts text.
- V-c. All other output is byte-identical to 0.6.1 in the same scripts, apart from these words.
- V-d. `text "rears back"` reacts to all three variants.
- V-e. Criteria 1–11 and 17–21 of `combat.md` hold. No bot result changes.

Experience signal (Review and playtest, not for the Playtester's handoff): a text-view player can say from the message line which kind of grub is attacking or hit them.

## Open questions

- Whether the variant name changes behaviour or only moves a wasted dash is for the next playtest.
- Build timing: only after Review 65, stating the build number if a playtest follows (D-009 item 5).
>>>END

<<<FILE design/combat-step72.md
# Combat design note, step 72: room 3 gets a second ask (a standard grub) and a tighter spitter layout

Status: room content only (room 3 table row). No rule, parameter, cap, cue, timing or input change. Where this note and `design/combat.md` differ on the room 3 row, criterion 12 or the room 3 purpose, this note governs. Fold into `combat.md` the next time it is edited. Decision: D-012. D-001, D-004 to D-007 and D-011 are untouched.

## Intent

Room 3 still teaches the aim cue first, with the verified schedule (first shots 1.8, 2.6, 3.4 s). After that it asks a second, different question: a lunge lane on top of aim lines. The player must move toward and through the room instead of repeating "aim, dash, shot lands behind me". The last spitter is never far from the others, and a hunting grub keeps the player moving, so the room does not become a long standoff against one spitter in a far corner.

## Diagnosis (design terms)

1. One ask. Room 3 has only the aim-line ask, answered the same way each time (sidestep or dash). With nothing else to answer, attention drops after the third or fourth repeat (playtests 53 and 63).
2. A standoff has no pressure to end it. Spitters are stationary, HP 2, and fire every 2.4 s. A player who kills two and leaves the third far away loses nothing by dodging for a long time. The east spitter at (14,7) is 12 tiles from the west spitter at (2,7), so reaching it is a long walk. Shots take about 4 s to cross, so each dodge is slow and the whole thing reads as a wait.
3. Rooms 4–5 held attention because several different asks overlap. Room 3 is the only room with a single ask.

## Options considered

| Option | Second ask | Pressure on a lone spitter | Touches cap or cue rule? | Verdict |
|---|---|---|---|---|
| A. Add one standard grub, far from the player's start, and move the third spitter closer | Lunge lane (step aside or dash) | The grub hunts the player, so staying still costs hearts. The spitters are closer together. | No | **Chosen** |
| B. Add one runner instead | Fast short lane (0.35 s warning) | Same | No | Rejected: the 0.35 s warning on top of 0.6 s aim cues in the teaching room is a harsh jump. Rooms 2 and 4 already cover the runner. |
| C. Add a brute | "Step aside, then punish" | Strong | No | Rejected: HP 4 and a 1.2 s recovery add a long fight to a room that is meant to teach. The brute stays in rooms 2 and 5. |
| D. Replace one spitter with a grub (two spitters plus grub) | Same as A | Strong | Yes. It changes the 1.8/2.6/3.4 s schedule and the in-flight bound. | Rejected: breaks criterion 11a and forces the D-007 verification to be redone. |
| E. Gap rule 0.2 s in room 3 (D-007 prepared fallback) | None | None | Yes | Rejected: fixes a different problem and changes a verified room. |
| F. New mechanics (reinforcements arriving later, a spitter that speeds up when alone, healing) | n/a | n/a | n/a | Outside this step: a new system or new enemy behavior. Not specified. |

## Chosen option: A

### Room 3 contents (replaces the room 3 row)

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 3 | Spitters at (2,1), (10,6), (2,7), in that room-table order (k = 0, 1, 2). Standard grub at (15,0). | 0.8 s / none (unchanged) | Learn the aim cue first, then answer an aim line and a lunge lane together |

Changes against the old row:
- The second spitter moves from (14,7) to (10,6). The order of the spitter list is the same, so k = 0, 1, 2 and the first-shot times are unchanged.
- One standard grub is added at (15,0), in the far corner away from the spitters and from the usual start.

All other room 3 parameters are unchanged: spitter interval 2.4 s, offset 0.8 s, cap 3, no gap rule, the D-007 bound (up to 2 plus the living spitters, so at most 5), and the grub parameters of the standard variant (HP 2, walk 1.0, wind-up 0.5 s, lunge 8.0 for 0.3 s, recovery 0.8 s, swipe cancels wind-up).

### Why these choices

- **Standard grub, not runner or brute.** Its answer is "either" (sidestep, dash or cancel). It is the gentlest lunge, so it is the right second ask for a room that is still teaching. It does not need new text; D-011 names it `a grub rears back`.
- **The grub walks at 1.0 tile/s from the far corner.** The distance gives the delay with no new system: it should not reach 2.0 tiles of the player, and so not start its first wind-up, until well after the third spitter's first cue. Criterion R3-3 checks this and tells QA what to do if the geometry says otherwise.
- **Spitter (10,6).** The largest distance between any two spitters becomes 9.4 tiles (between (2,1) and (10,6)), against 12.4 before. A player at 4 tiles/s covers that in about 2.4 s, or sooner with a dash. Spitter position affects only where the shot starts, not any cue time.
- **The grub pressures a stationary or kiting player.** A player who stands off and dodges shots is hunted by the grub, which asks for a lane answer or a kill. The room does not end until the grub is dead too, and it is a 2 HP target that can be swiped in recovery.
- **The one-at-a-time rule is untouched.** It applies among grubs. With one grub it changes nothing in room 3. Spitters are not gated by the grub and the grub is not gated by spitters.

### Edge cases

- **Grub wind-up while a spitter cue is running (or the reverse).** Allowed. They are two separate cues: a thin line and a 1.2-tile lane. A dash clears both. A sidestep must clear both. Readable threats holds because each cue is visible for its full duration. This is the same overlap that rooms 4–5 already have, except there the gap rule spaces the spitter cues from each other, which does not matter for a grub.
- **Cap and in-flight bound.** The grub does not count as a shot and does not delay a cue. D-007 stands: shots in flight never exceed 2 plus the living spitters.
- **Blocked contact (D-005).** Unchanged. A lunge that touches a protected player is spent. A shot that touches a protected player is consumed.
- **Grub killed early.** Room 3 continues with the spitters only. The standoff risk then returns for the last spitter, but the layout keeps it close (see R3-8).
- **All spitters killed first.** The grub fights as a single standard grub, as in room 1.
- **Player dies or room cleared.** Existing handling.
- **Player start position.** I could not check the start position in this packet. R3-3 is written so QA measures it from a trace.

## Acceptance criteria

### Verifiable (QA, `play` and `bots`; every check at both 30 and 60 FPS)

- **R3-1. Contents.** Room 3 contains exactly three spitters at (2,1), (10,6), (2,7) and one standard grub at (15,0). Room 3 contains no other enemy. Rooms 1, 2, 4, 5 are unchanged (criterion 12).
- **R3-2. Teaching schedule intact.** With a still player, the first spitter shots are at 1.8, 2.6 and 3.4 s ±1 frame, each cue 0.6 s ±1 frame before its shot (criteria 9, 11a). The grub changes none of these.
- **R3-3. The grub comes after the lessons.** With a player standing still at the room's start position, the grub's first wind-up message (`a grub rears back`) appears no earlier than 4.0 s after the room starts. Expected from geometry: the grub has to cover several tiles at 1.0 tile/s before it is within 2.0 tiles (derived, not measured). If QA's trace shows an earlier start, QA reports the measured time and the start position to `game-designer`, who moves the grub (tuning, no new spec step).
- **R3-4. The grub obeys the existing grub criteria in room 3.** The cue is at least 0.5 s before the hit (1); a 1-tile sidestep within 0.4 s of the cue avoids it (2); a dash from the cue until 0.1 s before the lunge ends avoids it and the player takes no damage after the dash (3, 21); a swipe in reach during the wind-up cancels it (6); two swipes kill it (6, 8); the recovery is safe (5).
- **R3-5. Spitter criteria hold with the grub alive.** Criteria 9 and 10 (cue and dodge) and 17 hold for shots fired in room 3.
- **R3-6. The D-007 bound is unchanged.** Criterion 11 as amended (step 46 note a–e) holds: the derived count of shots in flight in room 3 is 3 to 5 after a cap delay, and above 5 is a defect. No cue start is delayed or advanced by the grub: cue start times with the grub are equal to the times without it, ±1 frame, for the same still-player script until the grub's first lunge.
- **R3-7. Room end.** Room 3 is cleared only when the three spitters and the grub are all defeated. Killing the last spitter with the grub alive does not clear the room, and the reverse.
- **R3-8. The last spitter is close.** The distance between any two spitters in room 3 is at most 9.5 tiles. In a scripted run that kills the grub and two spitters, a player that then walks straight to the last spitter (dashing when a cue is on) and swipes it clears the room within 6 s of the previous kill (derived: about 2.4 s of walking plus two swipes, so about 3 s). This checks that the layout allows a quick finish. It does not force the player to take it.
- **R3-9. Messages.** The grub's wind-up and hit use whatever messages the build has (`a grub rears back`, `YOU ARE HIT by a grub`), whether or not Build 22a (D-011) is in. A rule `text "rears back"` reacts to it.
- **R3-10. Frame-rate independence (16).** Criteria 1–12 and 17–21 hold at both rates in room 3. No new tolerance is introduced.

Bots (criteria 13–15): the walker faces one more lunge in room 3, so the sum of its hearts lost in rooms 3–5 is expected to rise. At 60 FPS it was already at the upper limit of 6 (criterion 13). The limit may be exceeded, and the clear count may fall below 2. The dodger should be unaffected or have slightly more use for the dash. These are **expected effects, not verified**. QA measures them on the Build and reports values outside the limits to `game-designer` as a tuning question, not a build defect, as in steps 22, 35 and 38. If the bots key on room 3 contents, the Build updates them (test tooling).

### Experience signals (playtest and Review, not for the Playtester's handoff)

- In room 3 the player describes two kinds of threat: "the lines from the spitters" and "the grub that comes for me", and answers each differently.
- The first minute of room 3 is still described as learning the aim line, with the grub appearing as a new thing after that, not as a surprise during the first cues.
- The room is not described as "the same thing again" for most of its length, and no stretch of about 10 s consists of dodging one far-off spitter.
- A player who hears or sees a lunge cue during a shot cue can say which one to answer first, or that one move answered both.
- Nobody reports a shot or lunge that "came out of nowhere".

## Changed design documents

This note (new). `combat.md` is not edited here. The room 3 row, criterion 12 and the room 3 purpose line are governed by this note until folded in. D-012 records the choice.

## Open questions

1. The player start position in room 3 was not available to me. R3-3 is the guard; QA reports the measured grub arrival time.
2. Whether a human still produces a long single-spitter standoff cannot be known from scripts. A live or hand-timed playtest of room 3 is the check (D-010 item 5). If a standoff persists, the next levers are a runner in place of the standard grub (Option B) or a second grub, then a larger room change. A new enemy or new behavior would go to `game-director`.
3. Whether the grub on top of aim cues is too much for a room that teaches. If the playtest says so, move the grub later (further away) before changing anything else.
>>>END

<<<FILE design/combat-step94.md
# Combat text view: shot-hit source and late-swipe wording (G-001 step 94)

Owner: game-designer. Basis: handoff 93, Review 92, QA 90, playtest 88, D-005, D-007, D-011, D-013. Wording only. No rule, number, timing, cap, cue or input changes. Where this note and `combat.md` differ on these two messages, this note governs.

## Intent

The player can tell why they got hurt. A shot hit says which way the shot came from. A swipe that was too late says so. The build already behaves correctly in both cases; only the text view hides the cause.

## Message A: shot-hit source

**Format.** The damaging-hit message becomes:

`YOU ARE HIT by a shot from the <direction>`

and the existing suffix (` — hearts n/3`) follows unchanged. The prefix `YOU ARE HIT by a shot` is untouched, so reaction rules and `bots.py` that match it keep working.

`<direction>` is one of eight words: `north`, `north-east`, `east`, `south-east`, `south`, `south-west`, `west`, `north-west`. North is the top of the drawn room (smaller y). East is the right (larger x).

**What the direction means.** It is the side the shot came from, relative to the player: the reverse of the shot's travel direction. A shot travelling west was fired from the east, so the message says `from the east`.

**How to compute it.** Take the shot's locked travel vector (vx, vy) at the contact frame, and let (dx, dy) = (-vx, -vy). Let a = |dx| and b = |dy|.
- If min(a, b) / max(a, b) <= 0.4142 (tan 22.5°), the direction is the cardinal word for the larger axis.
- Otherwise it is the diagonal word for the signs of dx and dy.

This depends only on the shot's fixed velocity, so it is identical at 30 and 60 FPS and independent of the hit frame.

**What the engineer must carry.** Nothing new. The shot already has a locked travel direction in order to move. The engineer reads it at the contact frame, before the shot is removed, when building the message. No spitter id, origin, fire time or position needs to be stored.

**Why this reveals nothing new.** The `cue:` line already gives the line's direction, and the `~` line already draws it for 0.6 s before the shot. The message repeats that same locked direction, from the player's side. It gives no distance, no time and no spitter identity, and the graphical build shows the same direction by sight.

**Scope.**
- It applies only to a hit that deals damage.
- A shot absorbed by a dash or the hurt window still shows no message (D-005, unchanged).
- Grub, runner and brute hit messages are unchanged.

## Message B: swipe too late to stop a lunge

**Trigger.** A swipe damages a grub, runner or brute that is in its Lunge phase and does not kill it. Hits in other phases and kills are unchanged.

**Format.** One line, at the moment of the swipe result and before any `YOU ARE HIT by` line of the same frame:

- `the grub's lunge had already started, the swipe was too late to stop it`
- `the runner's lunge had already started, the swipe was too late to stop it`
- `the brute's lunge had already started, the swipe was too late to stop it`

The line uses the variant name, as in D-011. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`, so no existing reaction rule fires on it. A runner has 1 HP, so a damaging swipe kills it and the runner line appears only if a future HP change allows it. The text is still defined for all three variants.

**Unchanged.**
- The brute's wind-up line `the brute shrugs off the swipe` and its rules (criterion 19).
- The lunge itself. A swipe in the lunge does not cancel, shorten or delay it, and the swipe's 1 damage applies as before.
- A swipe that kills a grub in its lunge shows no new line.

**Why this reveals nothing new.** It states a fact the player could already see: the `cue:` line and `~` lane end when the lunge starts. It gives no prediction.

## Edge cases

- Two shots hit in one frame: only one damages (D-005). One message, with the direction of the shot that dealt the damage.
- Swipe and hit in the same frame: the swipe line comes first, then the hit line.
- Swipes in recovery, approach or stagger: no new line.
- One message per swipe. No batching and no repeat suppression.

## Acceptance criteria (QA, 30 and 60 FPS, `play.py --view player`)

Practice room (`room empty`, `spawn`, `player`), all at both rates.

- **W1. Direction words.** A still player at (8,4) is hit by a single spitter's shot. Check these placements:
  - spitter at (15,4): `from the east`;
  - spitter at (8,0): `from the north`;
  - spitter at (1,4): `from the west`;
  - spitter at (8,8): `from the south`;
  - spitter at (15,0): `from the north-east` (ratio 4/7 = 0.57 > 0.4142);
  - spitter at (15,7): `from the south-east` (shot travel vector about (-0.92,-0.39); reversed (0.92,0.39); ratio 3/7 = 0.43, which is above 0.4142, so the diagonal applies; QA checks the traced value against this).
  
  In every case the full line begins `YOU ARE HIT by a shot from the `.
- **W2. Real room.** In room 4 and room 5 a damaging shot hit shows a direction word consistent with the `cue:` line direction of the spitter that fired it (the reverse of the cue direction).
- **W3. Prefix kept.** `text "YOU ARE HIT by"` and `text "by a shot"` match, and `rears back` and `takes aim` still match their lines. A reaction-rule script using each of the three substrings behaves as before the change.
- **W4. Absorbed shots.** A shot absorbed by a dash or the hurt window produces no hit message, as before.
- **W5. Late swipe.** A standard grub at (10,4), player at (8,4) facing it, one swipe timed from the trace during the lunge (0.3 s long, after the 0.5 s wind-up; for the brute, after its 0.7 s wind-up) so it lands on the grub in reach. The player view shows `the grub's lunge had already started, the swipe was too late to stop it`, and it appears before `YOU ARE HIT by a grub`. The grub loses 1 HP and still finishes the lunge. Repeat once with a brute and the `brute` wording.
- **W6. No line elsewhere.** The late-swipe line does not appear for a swipe in wind-up (the grub is cancelled; the brute shows `shrugs off`), in recovery, in approach or in stagger, and not for a kill.
- **W7. No behavior change.** Compared with the build before the change, with the same scripts at the same rate: hit times, hearts, cue times, shot fire and contact times, lunge and recovery times and the in-flight counts are identical to ±1 frame. Criteria 1–21 of `combat.md` hold. `bots.py` runs unchanged with the suite green, and the bots' hearts and clears are as before.
- **W8. Frame-rate independence.** W1 to W6 give the same wording at 30 and 60 FPS.

## Experience signals (Review and playtest, not for the Playtester's handoff)

- A player can say which side a hitting shot came from, and can connect it to a cue line they saw.
- A player who swiped a lunging grub and was hit can say "I was too late", and does not ask what makes a swipe cancel.

## Rejected alternatives

- Naming the spitter by coordinates or an ordinal: needs the shot to carry an origin, and adds identity the cue lines never showed. Not chosen.
- Showing distance or fire time in the hit message: gives the text view more than the graphical build gives. Not chosen.
- Keeping the shot visible after contact: touches D-005. Not chosen.
- A line for every swipe that does not cancel: noise, and it explains nothing in the other phases. Not chosen.
- No Decision record: none of these alternatives constrains later work beyond this note.

## Changed documents

- New: this note.
- `design/combat.md`: pointer added at the top (done, the "Step 94" paragraph).
- **`repo/manual.md` could not be edited (not in my write paths).** The text to apply is given below.

### Manual wording (for the Build step)

Replace the sentence "Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`." with:

"Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot)."

After "A swipe that lands after the lunge has begun does not cancel it." add:

"When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute)."
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual, including public run, pause, resume and retry scripts.
- `session.py`: continuous progression, boundary healing, clocks, pause and terminal retry.
- `run_driver.py`: public `mode run` / `mode room` driver. Run
  `python3 play.py --view player SCRIPT` or use `--view trace`.
  `public-driver.md` records its implementation gaps. Scripts without new directives retain
  the legacy independent-room route and its 60-second limit.
- D-022 observation controls and summaries are implemented. `view-every 10` and `trace-every 5`
  reduce periodic output while preserving events; public executions print one summary covering
  every attempt. Controlled 1200-second acceptance probes run separately at 30 and 60 FPS.
  D-022's final-source Build check is recorded in handoff 54. Split C measurements,
  reproducible public scripts and retained regression coverage are delivered in handoff 56
  and tests/test_split_c.py. Inspect handoff 56's appended final-source Build check before
  routing independent QA, Art Verify, Play and Designer judgment.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  use the same decision grid at 30 and 60 FPS, with frame rounding. The dodger now has a boss policy
  (v1, submitted in step 38 and executed in step 40): it reads only displayed boss fields (B, attack
  name, locked direction, seconds left, phase, shots), dodges or dashes across the locked line,
  never swipes to stop a warning, and swipes in recovery. Rooms 1-4 behaviour is unchanged.
  Extra script lines: `hearts 3,2` (start hearts, run once per value), `mode run` (one normal run
  from room 1, default limit 1200 s). Output states start/end hearts and clear/death/unfinished,
  and prints a source id (hash of the executed sources and tests). Its results are not yet a
  D-019 comparison until the QA/measurement run has been done.
  Only the dodger reads the existing grub/spitter cues; against
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

## Continuous run and diagnostic rooms

Run a script with `python3 play.py --view player SCRIPT`; use `--view trace` for developer
state. Start a normal run with:

```text
mode run
fps 60
limit 1200
driver-limit 1205
0 move left
0.5 stop
0.5 attack
```

A normal run starts in room 1 with 3 hearts and advances through rooms 1–5. Defeat every enemy
to advance. Rooms 1–4 show a clear screen for 1 second, then restore 1 heart up to 3 on entry.
Position, movement, combat timers and queued attacks reset on entry. Room 5 contains one boss.
Death ends the run; defeating the boss while alive wins.

`mode room` selects an independent diagnostic room. Add `room 5` to inspect the boss. This
is a fresh diagnostic session, not a checkpoint. Normal runs reject `room`, `spawn` and `player`
setup.

| Public directive | Meaning |
|---|---|
| `limit 1200` | Per-attempt simulation time limit; reports unfinished separately from combat outcome. |
| `driver-limit 1205` | Driver duration including pauses and terminal screens. |
| `control 2 pause` | Pause at driver time 2; held movement stops. |
| `control 4 resume` | Resume at driver time 4, while simulation clocks are frozen. |
| `control 20 retry` | After normal-run victory or death, restart at room 1 with 3 hearts. |
| `attempt 2` | Following timed combat inputs belong to the second attempt. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, permitted 0.5–60. Event pictures and messages remain immediate. |
| `trace-every 5` | Trace periodic state every 5 game seconds; permitted 0.5–60. Event records are always emitted. Default trace is event-driven. |
| `trace-every frame` | Emit developer state every driver tick, without an output bound. |

Controls use driver time. Combat inputs use run time in normal runs and room time in diagnostics.
Equal-time inputs run in source order, after controls and before reaction rules. Combat inputs
due during pause or a clear screen are discarded. Retry discards pending inputs from the old
attempt. Reaction definitions persist; cooldown and previous-view memory reset on entry.

Driver seconds are simulated elapsed time, including pause and terminal waiting.
`processing_seconds` measures headless processing time; it is not human play time.

Public player and trace executions end with exactly one `summary:` block. It records the
execution stop separately from the final outcome (`clear`, `death`, `unfinished`), source id,
attempt count, and every attempt's run time, visited room times, first boss-entry hearts
(`None` if never entered), hurt count (`hits`), successful attack starts (`attacks`), pause
count and duration, driver duration, and driver elapsed time excluding pauses.
Driver duration includes terminal waiting; room and run clocks exclude terminal waiting.
An unfinished pause contributes its elapsed driver ticks through execution stop.
Retry resets periodic scheduling along with the attempt clocks. Numeric periodic output is
bounded per attempt by `ceil(limit / interval) + 1`; event output remains proportional to
events. Intervals do not change the simulation or event order. Invalid intervals are rejected
before simulation. The summary is for the public driver; legacy output remains unchanged
except for the room-5 note.

Scripts with none of the new directives retain the legacy independent-room route described
below, including its 60-second maximum and default duration. Add `mode room` explicitly to use
the public driver and its longer limit. Legacy room 5 does not yet provide the complete boss
messages and status display; use explicit `mode room` for boss observation.
Legacy room 5 player output begins with:
`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`.
Other legacy rooms and legacy trace output omit this note.

Public trace and session event logs identify emitted shots as `S1`, `S2`, and so on,
sharing one sequence across boss and spitter shots and across rooms in an attempt.
Retry restarts numbering at `S1`. `shot_fired` records ID and source (`boss` or a
room-local spitter identifier such as `spitter1`). Each removed emitted shot records
one `shot_removed` event with its ID, source, and reason: `lifetime`, `edge`, `hit`,
`absorbed`, or terminal `cleared`. Session events include run and room times.
Player messages do not display shot IDs.

## Boss and public display

`B` is the boss, with 12 HP. Swipes deal 1 damage in every phase. A nonlethal swipe does not
interrupt its warning. It alternates charge and short shot, approaching before each attack.

- Charge: a fixed-direction 0.7-second warning, then 2.4 tiles of movement over 0.3 seconds.
  Contact radius is 0.6 tile. Recovery lasts 1.2 seconds.
- Short shot: a fixed-direction 0.8-second warning, then one projectile at 3 tiles/second,
  with a 1-second lifetime and contact radius 0.4 tile. Recovery starts 1 second after firing
  and lasts 1.4 seconds, even if the shot hits or is absorbed earlier.
- Move sideways off the locked line or dash through contact. Recovery is harmless and permits
  approaching and swiping. Warnings cannot be stopped by repeated nonlethal swipes.

The public player view displays room, hearts, both simulation clocks, boss HP, phase and next
attack. Warning text gives the locked direction, time remaining and danger dimensions.
`~` cells approximate the fixed path; they are not the exact continuous collision boundary.
Charge path length is 2.4 tiles with rounded ends of radius 0.6; short-shot range is 3 tiles
with contact radius 0.4. The active-shot count includes projectiles hidden beneath another mark.

Victory and death messages name retry and its return to room 1. In diagnostic mode retry is
rejected. These commands describe the text/script build; keyboard and gamepad operation has
not been verified.

D-022 observation controls, shot lifecycle logging and automated acceptance probes are implemented.
See `public-driver.md` for the remaining measurement and independent verification work.

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
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In room 4 the two spitters
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

<<<FILE repo/public-driver.md
# Public Session driver — build 0.6-g002-public-32

D-022 observation and shot lifecycle support are implemented with automated Build probes.
Independent verification remains outstanding. The legacy script route remains available.

Run `python3 play.py --view player SCRIPT` or replace `player` with `trace`.
A script containing any new directive below selects the Session driver.

| Directive | Meaning |
|---|---|
| `mode run` | Normal run from room 1; room, spawn and player setup are rejected. |
| `mode room` | Independent diagnostic room; default for the new driver. |
| `room 5` | Diagnostic room selection, not a checkpoint. |
| `fps 30` / `fps 60` | Fixed simulation rate. |
| `attempt 2` | Subsequent timed combat inputs belong to attempt 2. |
| `control 2 pause` | Pause at driver time 2 seconds. |
| `control 4 resume` | Resume at driver time 4 seconds, even while game time is frozen. |
| `control 20 retry` | Retry at driver time 20; accepted only at a normal-run terminal. |
| `limit 1200` | Per-attempt game-time limit; distinct from combat result. |
| `driver-limit 1205` | Driver duration, including pause and terminal screens. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, range 0.5–60. |
| `trace-every 5` | Trace periodic state every 5 game seconds, range 0.5–60; default is events only. |
| `trace-every frame` | Emit trace state every driver tick without a periodic output bound. |

Timed combat inputs and existing reaction rules retain their syntax. Timed inputs use run time
in run mode and room time in diagnostic mode. Equal-time inputs retain source order.
Controls run first. Inputs due during pause or room-clear display are consumed and rejected.
Retry discards previous attempts' pending inputs. Rule cooldown and previous-view memory reset
on entry. Driver time is simulated elapsed time, not wall-clock elapsed time.

Example:

```text
mode run
fps 60
limit 10
driver-limit 13
0 dash right
control 0.1 pause
0.1 attack
control 2.1 resume
```

For a diagnostic boss display:

```text
mode room
room 5
fps 30
limit 8
trace-every frame
```

The public player view displays both game clocks, room, hearts, boss phase and next attack,
warning direction and dimensions, recovery time, and active shot count. The `~` cells approximate
the fixed path: they are not the exact continuous collision boundary. Charge path length is
2.4 tiles with contact radius 0.6; short-shot range is 3.0 tiles with contact radius 0.4.

The public syntax and boss instructions are now included in manual.md and linked from README.md.
The legacy route remains separate and lacks complete boss presentation.

Periodic scheduling resets on retry. Numeric intervals bound periodic output per attempt to
`ceil(limit / interval) + 1`; event messages and event-triggered pictures are preserved.
Default player scheduling retains the existing half-second cadence after event pictures.

Exactly one final `summary:` block reports execution stop, clear/death/unfinished outcome,
source id, processing seconds, total driver seconds, and every attempt's run and room times,
first boss-entry hearts, hurt and attack counts, pauses, paused seconds, driver seconds and
elapsed driver seconds excluding pauses. Terminal waiting is included only in driver elapsed
time. See manual.md for shot IDs, removal reasons and legacy-route limitations.

Split C integration scripts are generated by tests/test_split_c.py. From repo, run:

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
python3 play.py --view player run60.txt
```

Either script supports either view. Generation records the unchanged dodger's buttons;
public replay uses timed inputs without a live bot or state injection. The first attempt
pauses for two driver seconds during the first clear display, then completes normally.
Controls retry at driver seconds 120 and 140. Explicit second-attempt input leaves the
player stationary until natural death; explicit third-attempt inputs move and attack.
The final driver limit is 141 seconds; the game limit is 1200 seconds per attempt.

The suite checks frozen pause clocks, fresh room-1 entries, both terminal retries, and
absence of old-attempt dashes after retry. Existing driver/session tests cover pending
input discard, fresh-state equality, queued attacks, warning/protection pause and limits.
Independent rooms 1–4 retain FPS comparison and fixed measurements; the historical
one-decimal comparison does not establish equality with an unavailable pre-boss policy.

Handoff 56 records executed proposal evidence separately from its appended saved-source
Build check. Remaining work is independent QA, limited Art Verify, Play and Designer judgment.
Legacy boss presentation remains intentionally limited under D-022; delegation to the public
driver is not required. No real keyboard or gamepad verification is claimed under D-021.
>>>END

<<<FILE repo/source_id.py
"""Source identification for measurements: a short hash over the executed source set."""

import hashlib
from pathlib import Path

_NAMES = ("game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py")


def source_id():
    """12 hex digits over game, session, play, run_driver, bots, source_id and tests/*.py.

    Reads files only. The BUILD string alone does not identify a source set.
    """
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    files = [root / name for name in _NAMES] + sorted((root / "tests").glob("*.py"))
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()[:12]
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  pause_at 30                 mode run: pause once when run time reaches this many seconds
  pause_seconds 5             mode run: driver seconds spent paused (never added to run time)
  retries 2                   mode run: retries allowed after a won/dead attempt (default 0)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys
import time

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
from session import RunSession
from source_id import source_id

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
        elif e.kind == "spitter" and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
        elif e.kind == "boss" and e.aim and e.phase == "warning":
            # Displayed: locked direction, seconds left, lane size (charge 2.4 + 0.6; shot 3.0 + 0.4).
            charge = e.attack_name == "charge"
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], 3.0 if charge else 3.4,
                e.phase_left, LUNGE_SPEED if charge else SHOT_SPEED, e.attack_name,
            ))
        elif e.kind == "boss" and e.aim and e.phase == "active" and e.attack_name == "charge":
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], e.phase_left * LUNGE_SPEED + 0.6,
                0.0, LUNGE_SPEED, "charge",
            ))
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
    boss = next((e for e in game.enemies if e.hp > 0 and e.kind == "boss"), None)
    if boss and boss.phase in ("warning", "active"):
        # Boss policy v1: only displayed fields (B, attack name, locked direction, seconds left,
        # phase, shots) are read. Never swipe to stop a warning; swipe only while it recovers.
        note(f"hold off the boss's locked {boss.attack_name} line")
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


def play_room(bot, room, fps, limit, log=None, hearts=HEARTS):
    game = Game(fps=fps, room=room)
    game.hearts = hearts  # start hearts: 3 standard; 2 is the run-boundary case (D-019)
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
        "hearts_lost": hearts - game.hearts,
        "hearts_start": hearts,
        "hearts_end": game.hearts,
        "outcome": "clear" if game.cleared else ("death" if game.hearts <= 0 else "unfinished"),
        "limit": limit,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


class _Proxy:
    """Lets a bot act on a RunSession: reads come from the current room, presses go through the
    session (so they are logged, rejected during clear screens and attributed to the run)."""

    def __init__(self, session):
        self._s = session

    def press(self, action, direction=None):
        return self._s.press(action, direction)

    def __getattr__(self, name):
        return getattr(self._s.game, name)


def play_run(bot, fps, limit, log=False, pause_at=None, pause_seconds=0.0, retries=0):
    """Normal run(s) from room 1 (3 hearts), regular enemies only.

    pause_at: run time (s) at which to pause once, through RunSession.control; the pause lasts
    pause_seconds of driver time and is never added to run time. retries: how many times to
    retry (RunSession.control) after a won/dead attempt; each retry starts attempt n+1 and the
    per-room figures describe the final attempt. The limit applies to each attempt. Reaction
    memory is reset whenever the session generation changes (room entry or retry).

    Returns run/room times from the session clocks, driver seconds (ticks / fps) and processing
    seconds (wall clock) separately. Terminal waiting and pause are never added to combat time.
    """
    s = RunSession(fps)
    lines = [] if log else None
    brain, generation, ticks = Brain(lines), s.generation, 0
    proxy = _Proxy(s)
    paused_ticks, pause_done, retries_used = 0, pause_at is None, 0
    started = time.perf_counter()
    while not s.stop_reason:
        if s.state in ("won", "dead"):
            if retries_used >= retries:
                break
            s.control("retry")
            retries_used += 1
            continue
        if s.generation != generation:  # new room or new attempt: reaction memory resets
            generation = s.generation
            brain = Brain(lines)
        if not pause_done and s.state in ("combat", "room_clear") and s.t >= pause_at - 1e-9:
            pause_done = True
            if s.control("pause"):
                paused_ticks = round(pause_seconds * fps)
                for _ in range(paused_ticks):
                    s.step(limit=limit)  # frozen: only the driver clock moves
                    ticks += 1
                s.control("resume")
        if s.state == "combat" and not s.paused:
            game = s.game
            if game.stun_left <= 0:
                if brain.due(game.t):
                    bot(proxy, lambda text, g=game, b=brain: b.note(g, text))
            else:
                brain.skip(game)
        s.step(limit=limit)
        ticks += 1
    processing = time.perf_counter() - started
    rooms, sources = {}, {}
    for e in s.events:
        if e["attempt"] != s.attempt:
            continue
        d = rooms.setdefault(e["room"], {
            "entry_hearts": None, "entry_run": None, "end": None, "end_run": None,
            "room_time": None, "hurts": 0, "attacks": 0, "boss_hits": 0, "dashes": 0,
        })
        kind = e["kind"]
        if kind == "entry":
            d["entry_hearts"], d["entry_run"] = e["details"]["hearts"], e["run_time"]
        elif kind == "hurt":
            d["hurts"] += 1
            src = e["details"]["source"]
            sources[src] = sources.get(src, 0) + 1
        elif kind == "attack":
            d["attacks"] += 1
            d["boss_hits"] += sum(1 for hit in e["details"]["hits"] if hit[0] == "boss")
        elif kind == "dash":
            d["dashes"] += 1
        elif kind in ("room_clear", "run_won", "run_dead"):
            d["end"], d["room_time"], d["end_run"] = kind, e["room_time"], e["run_time"]
    current = rooms.get(s.game.room)
    if current is not None and current["end"] is None:
        current["end"], current["room_time"], current["end_run"] = "limit", s.room_t, s.t
    transitions = []
    for n in range(1, 5):
        a, b = rooms.get(str(n)), rooms.get(str(n + 1))
        if a and b and a["end"] == "room_clear":
            transitions.append(round(b["entry_run"] - a["end_run"], 3))
    outcome = {"won": "won", "dead": "dead"}.get(s.state, "unfinished")
    return {
        "outcome": outcome, "stop_reason": s.stop_reason, "attempt": s.attempt,
        "run_seconds": s.t, "driver_seconds": ticks / fps, "processing_seconds": processing,
        "pause_seconds": paused_ticks / fps, "retries": retries_used,
        "attempt_outcomes": [e["kind"] for e in s.events if e["kind"] in ("run_won", "run_dead")],
        "controls": {k: sum(1 for e in s.events if e["kind"] == k)
                     for k in ("pause", "resume", "retry", "control_rejected")},
        "rooms": rooms, "transitions": transitions,
        "boss_entry_hearts": rooms.get("5", {}).get("entry_hearts"),
        "hurt_sources": sources, "limit": limit, "log": lines or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "limit_given": False,
        "hearts": [HEARTS],
        "mode": "room",
        "pause_at": None,
        "pause_seconds": 0.0,
        "retries": 0,
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
                setup["limit_given"] = True
            elif key == "hearts":
                setup["hearts"] = [int(v) for v in value.split(",")]
                assert all(1 <= h <= HEARTS for h in setup["hearts"])
            elif key == "mode":
                assert value in ("run", "room")
                setup["mode"] = value
            elif key == "pause_at":
                setup["pause_at"] = float(value)
                assert setup["pause_at"] >= 0
            elif key == "pause_seconds":
                setup["pause_seconds"] = float(value)
                assert setup["pause_seconds"] >= 0
            elif key == "retries":
                setup["retries"] = int(value)
                assert setup["retries"] >= 0
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | hearts 3,2 | mode run|room | log on"
            )
    return setup


def _main_run(setup):
    limit = setup["limit"] if setup["limit_given"] else 1200.0
    print(f"mode run: normal run from room 1, {setup['fps']} FPS, game-time limit {limit:.0f} s, "
          f"start hearts 3, pause_at {setup['pause_at']}, pause {setup['pause_seconds']} s, "
          f"retries {setup['retries']}")
    for name in setup["bots"]:
        r = play_run(BOTS[name], setup["fps"], limit, log=setup["log"],
                     pause_at=setup["pause_at"], pause_seconds=setup["pause_seconds"],
                     retries=setup["retries"])
        print(
            f"{name:7} run: {r['outcome']} (stop: {r['stop_reason'] or 'terminal'}); "
            f"run {r['run_seconds']:.3f} s, driver {r['driver_seconds']:.3f} s, "
            f"processing {r['processing_seconds']:.2f} s (wall clock, not play time), "
            f"pause {r['pause_seconds']:.1f} s, retries {r['retries']}, attempt {r['attempt']}"
        )
        print(f"          boss entry hearts {r['boss_entry_hearts']}; transitions (run s) "
              f"{r['transitions']}; hurt by {r['hurt_sources'] or 'none'}")
        for room, d in sorted(r["rooms"].items()):
            print(
                f"          room {room}: entry hearts {d['entry_hearts']}, end {d['end']}, "
                f"room time {d['room_time']}, hurts {d['hurts']}, attacks {d['attacks']} "
                f"(boss hits {d['boss_hits']}), dashes {d['dashes']}"
            )
        for entry in r["log"]:
            print("          " + entry)


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"source {source_id()}; policy: dodger with boss policy v1 (displayed boss fields only), "
          f"reaction {REACTION} s, start (8, 4) facing right; camper/walker unchanged")
    if setup["mode"] == "run":
        _main_run(setup)
        return
    for start in setup["hearts"]:
        _main_rooms(setup, start)


def _main_rooms(setup, start):
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {start} hearts at start")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"], hearts=start)
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}; "
                f"start hearts {r['hearts_start']}, end {r['hearts_end']}, outcome {r['outcome']}"
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

<<<FILE repo/run_driver.py
"""Public script driver. The driver clock advances while game clocks are frozen."""

import math
import time

from game import DIRECTIONS, EPS, Game
from session import RunSession
from source_id import source_id

BUILD = "0.6-g002-public-32"


def read_script(text):
    from play import Rule

    setup = {
        "mode": "room", "room": "1", "fps": 60, "spawns": [],
        "player": None, "limit": 1200.0, "driver_limit": 1205.0,
        "controls": [], "trace_every": False, "view_every": 0.5,
    }
    inputs, rules, attempt, diagnostic = [], [], 1, False
    for number, raw in enumerate(text.splitlines(), 1):
        words = raw.split("#", 1)[0].split()
        if not words:
            continue
        key = words[0]
        try:
            if key == "when":
                rules.append(Rule(raw.split("#", 1)[0].strip()))
            elif key == "mode":
                assert len(words) == 2 and words[1] in ("run", "room")
                setup["mode"] = words[1]
            elif key == "room":
                assert len(words) == 2
                setup["room"], diagnostic = words[1], True
            elif key == "fps":
                assert len(words) == 2 and int(words[1]) in (30, 60)
                setup["fps"] = int(words[1])
            elif key in ("limit", "end", "driver-limit"):
                assert len(words) == 2
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["driver_limit" if key == "driver-limit" else "limit"] = value
            elif key == "attempt":
                assert len(words) == 2 and int(words[1]) >= 1
                attempt = int(words[1])
            elif key == "control":
                assert len(words) == 3 and words[2] in ("pause", "resume", "retry")
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["controls"].append((value, words[2]))
            elif key in ("view-every", "trace-every"):
                assert len(words) == 2
                if key == "trace-every" and words[1] == "frame":
                    setup["trace_every"] = True
                else:
                    value = float(words[1])
                    assert math.isfinite(value) and 0.5 <= value <= 60
                    setup["view_every" if key == "view-every" else "trace_every"] = value
            elif key == "spawn":
                assert len(words) == 4
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
                diagnostic = True
            elif key == "player":
                assert len(words) == 3
                setup["player"] = (float(words[1]), float(words[2]))
                diagnostic = True
            else:
                assert 2 <= len(words) <= 3
                value, action = float(words[0]), words[1]
                direction = words[2] if len(words) == 3 else None
                assert math.isfinite(value) and value >= 0
                assert action in ("move", "stop", "attack", "dash")
                assert direction is None or direction in DIRECTIONS
                assert action != "move" or direction is not None
                assert action not in ("stop", "attack") or direction is None
                inputs.append((attempt, value, action, direction))
        except (AssertionError, ValueError, IndexError) as error:
            hint = ("; interval must be finite and between 0.5 and 60 seconds; "
                    "trace-every also accepts frame"
                    if key in ("view-every", "trace-every") else "")
            raise ValueError(f"script line {number}: invalid instruction {raw!r}{hint}") from error
    if setup["mode"] == "run" and diagnostic:
        raise ValueError("mode run cannot use room, spawn or player setup")
    setup["controls"].sort(key=lambda item: item[0])
    inputs.sort(key=lambda item: (item[0], item[1]))
    return setup, inputs, rules


class RoomSession(RunSession):
    """Independent diagnostic room; retry never creates a checkpoint."""

    def __init__(self, setup):
        super().__init__(setup["fps"])
        self.events.clear()
        self.sequence = 0
        self.game = Game(self.fps, setup["room"])
        self.game.shot_sequence = self.shot_sequence
        for kind, x, y in setup["spawns"]:
            self.game.spawn(kind, x, y)
        if setup["player"] is not None:
            self.game.place_player(*setup["player"])
        self.game_seen = 0
        self.log("entry", hearts=self.game.hearts)

    def control(self, action):
        if action == "retry":
            self.log("control_rejected", action=action, reason="diagnostic mode")
            return False
        return super().control(action)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state != "combat":
            return
        if limit is None or self.t < limit - EPS:
            self.run_frame += 1
            self.game.step()
            self._collect()
            if self.game.outcome:
                self.state = self.game.outcome
                self.log("diagnostic_result", outcome=self.state)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)


def messages_for(event):
    from play import Player

    kind, details, room = event["kind"], event["details"], event["room"]
    fixed = {
        "entry": f"entered room {room}/5",
        "run_won": "run won — boss defeated — retry: start from room 1",
        "run_dead": "you went down — run lost — retry: start from room 1",
        "retry": "new attempt — room 1/5",
        "pause": "paused", "resume": "resumed",
        "boss_swipe": "the boss takes the swipe; the warning continues",
        "boss_recovery": "the boss is recovering — safe to approach and swipe",
        "boss_pursuit": "the boss resumes pursuit",
    }
    if kind in fixed:
        return fixed[kind]
    if kind == "room_clear":
        return f"room {room} cleared — next room {details['next_room']}"
    if kind == "recovery":
        return "recovered 1 heart" if details["gained"] else "hearts already full"
    if kind in ("boss_warning", "boss_active"):
        charge = details["attack"] == "charge"
        if kind == "boss_warning":
            return "the boss prepares a charge" if charge else "the boss aims a short shot"
        return "the boss charges" if charge else "the boss fires a short shot"
    if kind == "hurt" and details["source"] == "boss":
        return f"YOU ARE HIT by the boss's charge — hearts {details['hearts']}/3"
    return Player.describe(kind, details, details.get("name"))


class Output:
    def __init__(self, session, setup, view):
        self.session, self.setup, self.view = session, setup, view
        self.seen, self.next_picture = 0, 0.0
        self.next_trace = 0.0
        self.attempt = session.attempt
        self.periodic_count = 0

    def emit(self, force=False):
        from play import cue_lines, draw

        s, g = self.session, self.session.game
        events = s.events[self.seen:]
        self.seen = len(s.events)
        if self.attempt != s.attempt:
            self.attempt = s.attempt
            self.next_picture = self.next_trace = 0.0
            self.periodic_count = 0
        if self.view == "trace":
            interval = self.setup["trace_every"]
            periodic = interval is True or (
                interval is not False and s.t >= self.next_trace - EPS
            )
            if periodic:
                self.periodic_count += 1
                if interval is not True:
                    self.next_trace = (math.floor((s.t + EPS) / interval) + 1) * interval
            if events or force or periodic:
                print({
                    "build": BUILD, "mode": self.setup["mode"],
                    "attempt": s.attempt, "room": g.room,
                    "run_time": s.t, "room_time": g.t, "frame": g.frame,
                    "state": s.state, "paused": s.paused,
                    "stop_reason": s.stop_reason,
                    "player": {key: getattr(g, key) for key in (
                        "x", "y", "hearts", "heading", "facing", "recovery",
                        "dash_left", "dash_cooldown", "hurt_left", "stun_left",
                        "invulnerable", "queued_attack",
                    )},
                    "enemies": [dict(e.__dict__) for e in g.enemies],
                    "shots": [
                        {
                            "id": getattr(shot, "id", None),
                            "source": getattr(shot, "event_source", None),
                            "state": list(shot),
                        }
                        for shot in g.shots
                    ],
                    "events": events,
                })
            return
        immediate = force
        for event in events:
            message = messages_for(event)
            if message:
                print(f"[attempt {event['attempt']} room {event['room']} "
                      f"run {event['run_time']:.3f} room-time {event['room_time']:.3f}] {message}")
                immediate = True
        periodic = s.t >= self.next_picture - EPS
        if not immediate and not periodic:
            return
        if periodic:
            self.periodic_count += 1
        interval = self.setup["view_every"]
        if interval == 0.5:
            # Retain the pre-supplement default cadence after event pictures.
            self.next_picture = s.t + interval
        elif periodic:
            self.next_picture = (math.floor((s.t + EPS) / interval) + 1) * interval
        print(f"{self.setup['mode']} — room {g.room}/5 — hearts {g.hearts}/3 "
              f"— run {s.t:.3f} s — room {g.t:.3f} s "
              f"— {s.state}{' — paused' if s.paused else ''}")
        for row in draw(g):
            print("|" + row + "|")
        print(f"active shots: {len(g.shots)}")
        for line in cue_lines(g):
            print(line)
        for boss in (e for e in g.enemies if e.kind == "boss"):
            print(f"boss B — HP {max(0, boss.hp)}/12 — {boss.phase} — next: {boss.attack_name}")
            if boss.hp > 0 and boss.phase == "warning":
                print(f"cue: B {boss.attack_name} — locked {boss.aim} — {boss.phase_left:.3f} left")
                print("danger: charge lane, radius 0.6 tile, rounded ends"
                      if boss.attack_name == "charge" else
                      "danger: one shot, contact radius 0.4 tile, range 3.0 tiles")
            if boss.hp > 0 and boss.phase == "recovery":
                print(f"recovery: {boss.phase_left:.3f} left")


def drive(setup, inputs, rules=(), observe=None):
    """Observer hooks permit labelled fixtures, not normal-run reachability claims."""
    from play import REACTION, View, sprites

    s = RunSession(setup["fps"]) if setup["mode"] == "run" else RoomSession(setup)
    pending, controls = list(inputs), list(setup["controls"])
    before, messages, generation, seen = [], [], None, 0
    tick, started = 0, time.perf_counter()
    attempts = {}

    def record(elapsed=0.0, paused=False):
        item = attempts.setdefault(s.attempt, {
            "attempt": s.attempt, "outcome": "unfinished",
            "run_seconds": 0.0, "rooms": {}, "boss_entry_hearts": None,
            "hits": 0, "attacks": 0, "pauses": 0,
            "pause_seconds": 0.0, "driver_seconds": 0.0,
            "elapsed_excluding_pauses": 0.0,
        })
        item["run_seconds"] = s.t
        item["rooms"][s.game.room] = s.room_t
        item["outcome"] = {
            "won": "clear", "cleared": "clear", "dead": "death",
        }.get(s.state, "unfinished")
        item["driver_seconds"] += elapsed
        item["pause_seconds"] += elapsed if paused else 0.0
        item["elapsed_excluding_pauses"] = (
            item["driver_seconds"] - item["pause_seconds"]
        )

    record()

    def collect():
        nonlocal seen
        new = s.events[seen:]
        seen = len(s.events)
        return [message for event in new if (message := messages_for(event))]

    while tick / s.fps < setup["driver_limit"] - EPS:
        while controls and controls[0][0] <= tick / s.fps + EPS:
            _, action = controls.pop(0)
            previous_attempt = s.attempt
            s.control(action)
            if previous_attempt != s.attempt:
                pending = [item for item in pending if item[0] >= s.attempt]
        entered = generation != s.generation
        if entered:
            generation = s.generation
            before, messages = [], []
            for rule in rules:
                rule.last = -math.inf
            if observe:
                observe(s, True)
        messages += collect()
        due, remaining = [], []
        for item in pending:
            (due if item[0] == s.attempt and item[1] <= s.t + EPS else remaining).append(item)
        pending = remaining
        for _, _, action, direction in due:
            s.press(action, direction)
        messages += collect()
        if not s.paused and s.state == "combat" and not s.stop_reason:
            view = View(s.game, messages, before)
            for rule in rules:
                target = rule.matches(view)
                if target and s.room_t - rule.last >= REACTION - EPS:
                    rule.last = s.room_t

                    class Actions:
                        x, y = s.game.x, s.game.y
                        press = s.press

                    rule.act(Actions(), target)
                    break
            before = sprites(s.game)
        paused = s.paused
        s.step(limit=setup["limit"])
        record(1 / s.fps, paused)
        messages = collect()
        if observe:
            observe(s, False)
        tick += 1
        terminal = s.state in ("won", "dead", "cleared")
        if s.stop_reason or (terminal and not controls):
            break
    reason = s.stop_reason or (
        "terminal" if s.state in ("won", "dead", "cleared") else "driver limit"
    )
    record()
    for event in s.events:
        item = attempts[event["attempt"]]
        if event["kind"] == "entry" and event["room"] == "5":
            if item["boss_entry_hearts"] is None:
                item["boss_entry_hearts"] = event["details"]["hearts"]
        if event["kind"] == "hurt":
            item["hits"] += 1
        elif event["kind"] == "attack":
            item["attacks"] += 1
        elif event["kind"] == "pause":
            item["pauses"] += 1
    return s, {
        "attempt_count": len(attempts), "attempts": list(attempts.values()),
        "outcome": attempts[s.attempt]["outcome"],
        "build": BUILD, "source_id": source_id(), "driver_seconds": tick / s.fps,
        "processing_seconds": time.perf_counter() - started,
        "execution_stop": reason,
    }


def play(setup, inputs, view, rules=()):
    print(f"Lantern Depths {BUILD} — mode {setup['mode']} — {setup['fps']} FPS "
          f"— timed inputs use {'run' if setup['mode'] == 'run' else 'room'} time")
    output = None

    def observe(session, force):
        nonlocal output
        if output is None:
            output = Output(session, setup, view)
        output.emit(force)

    session, measurement = drive(setup, inputs, rules, observe)
    print(f"summary: {measurement}")
    return session, measurement
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
    directives = {"mode", "attempt", "control", "limit", "driver-limit", "trace-every", "view-every"}
    for raw in text.splitlines():
        words = raw.split("#", 1)[0].split()
        if words and words[0] in directives:
            from run_driver import read_script as read_public_script
            return read_public_script(text)
    return read_legacy_script(text)


def read_legacy_script(text):
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
    if "mode" in setup:
        from run_driver import play as play_public
        return play_public(setup, inputs, view, rules)
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
    if view == "player" and game.room == "5":
        print('note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display')
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
        if game.outcome is not None:
            # Terminal game time is frozen. Do not wait on that clock for a display tail.
            break
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
        elif e.kind == "spitter" and e.cueing:
            length = ROOM_W + ROOM_H
        elif e.kind == "boss" and e.phase == "warning":
            length = 2.4 if e.attack_name == "charge" else 3.0
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
        elif e.kind == "spitter" and e.cueing:
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
            + (
                f"{e.phase}:{e.phase_left:.3f},attack={e.attack_name},aim={e.aim}"
                if e.kind == "boss"
                else f"{e.phase}:{e.phase_left:.3f}" if e.is_grub
                else f"fire_in={e.fire_in:.3f},cue={e.cueing}"
            )
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

<<<FILE repo/tests/test_bots_boss.py
"""Boss-aware dodger, start hearts, outcomes and the normal-run bot driver.

These tests check mechanics and reporting only. They do not claim the boss can be beaten.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
from game import Game  # noqa: E402
from source_id import source_id  # noqa: E402


def boss_warning(attack, player):
    game = Game(room="5")
    boss = game.enemies[0]
    boss.x, boss.y = 10.0, 4.0
    boss.phase, boss.attack_name = "warning", attack
    boss.aim, boss.phase_left = (-1.0, 0.0), 0.5
    game.place_player(*player)
    return game


class BossPolicyTest(unittest.TestCase):
    def test_threat_follows_the_displayed_locked_lane(self):
        for attack in ("charge", "short shot"):
            threat = bots._threat(boss_warning(attack, (8, 4)))
            self.assertIsNotNone(threat, attack)
            self.assertEqual(threat[6], attack)
            self.assertGreaterEqual(threat[0], 0.5)
            self.assertIsNone(bots._threat(boss_warning(attack, (8, 5.5))), attack)

    def test_dodger_in_the_lane_holds_or_dodges_and_never_swipes(self):
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            notes = []
            bots.dodger(game, notes.append)
            self.assertTrue(notes, attack)
            self.assertFalse(any("swipe" in n for n in notes), notes)
            self.assertFalse(any(k == "attack" for _, k, _ in game.events))

    def test_dodger_off_the_lane_holds_during_the_warning(self):
        game = boss_warning("charge", (8, 5.5))
        notes = []
        bots.dodger(game, notes.append)
        self.assertTrue(any("hold off" in n for n in notes), notes)
        self.assertFalse(any(k == "attack" for _, k, _ in game.events))


class OutcomeTest(unittest.TestCase):
    def test_start_hearts_and_outcome_fields(self):
        for fps in (30, 60):
            for hearts in (3, 2):
                r = bots.play_room(bots.BOTS["dodger"], "5", fps, 5, hearts=hearts)
                self.assertEqual(r["hearts_start"], hearts)
                self.assertIn(r["outcome"], ("clear", "death", "unfinished"))
                self.assertEqual(r["hearts_lost"], hearts - r["hearts_end"])

    def test_unfinished_is_reported_at_the_limit(self):
        r = bots.play_room(bots.BOTS["dodger"], "1", 60, 0.5)
        self.assertEqual(r["outcome"], "unfinished")
        self.assertFalse(r["cleared"])

    def test_log_changes_no_result_in_the_boss_room(self):
        for fps in (30, 60):
            quiet = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, hearts=2)
            loud = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, log=True, hearts=2)
            for key in ("outcome", "seconds", "hearts_end", "hits_by", "attacks", "dashes"):
                self.assertEqual(quiet[key], loud[key], (fps, key))


class RunDriverTest(unittest.TestCase):
    def test_play_run_smoke(self):
        for fps in (30, 60):
            r = bots.play_run(bots.BOTS["dodger"], fps, 2.0)
            self.assertEqual(r["outcome"], "unfinished")
            self.assertAlmostEqual(r["run_seconds"], 2.0, delta=1.0 / fps + 1e-9)
            self.assertEqual(r["retries"], 0)
            self.assertIn("1", r["rooms"])

    def test_read_script_hearts_and_mode(self):
        setup = bots.read_script("hearts 3,2\nmode run\nlimit 10\n")
        self.assertEqual(setup["hearts"], [3, 2])
        self.assertEqual(setup["mode"], "run")
        self.assertTrue(setup["limit_given"])
        with self.assertRaises(SystemExit):
            bots.read_script("hearts 4\n")


class SourceIdTest(unittest.TestCase):
    def test_source_id_is_stable_hex(self):
        a, b = source_id(), source_id()
        self.assertEqual(a, b)
        self.assertEqual(len(a), 12)
        int(a, 16)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_split_c.py
"""Split C: public control integration and retained independent-room regressions.

Generate a public script from repo:
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt

Repeat with 60. Generation records dodger button inputs; replay uses the public
parser and driver, without a bot, observer actions, or combat-state injection.
"""
import json
import unittest
from unittest import mock

import bots
import play
from run_driver import drive
from source_id import source_id


def public_script(fps):
    recorded = []
    original = bots._Proxy.press

    def capture(proxy, action, direction=None):
        recorded.append((proxy._s.t, action, direction))
        return original(proxy, action, direction)

    with mock.patch.object(bots._Proxy, "press", capture):
        result = bots.play_run(bots.dodger, fps, 1200)
    if result["outcome"] != "won":
        raise AssertionError(result)
    pause = 7 if fps == 30 else 10
    lines = [
        "mode run", f"fps {fps}", "limit 1200", "driver-limit 141",
        "view-every 10", "trace-every 5",
        f"control {pause} pause", f"control {pause + 2} resume",
        "control 120 retry", "control 140 retry",
    ]
    lines += [
        f"{t:.12f} {action}" + (f" {direction}" if direction else "")
        for t, action, direction in recorded
    ]
    lines += [
        "1100 dash left", "attempt 2", "0 stop",
        "attempt 3", "0 move up", "0.1 stop", "0.1 attack",
    ]
    return "\n".join(lines) + "\n"


class SplitCTest(unittest.TestCase):
    def test_public_normal_pause_victory_retry_death_retry(self):
        for fps in (30, 60):
            setup, inputs, rules = play.read_script(public_script(fps))
            frozen = []

            def observe(s, force):
                if s.paused:
                    frozen.append((s.t, s.room_t, s.game.frame,
                                   s.clear_frames, s.state))

            session, summary = drive(setup, inputs, rules, observe)
            self.assertEqual([a["outcome"] for a in summary["attempts"]],
                             ["clear", "death", "unfinished"])
            self.assertTrue(frozen)
            self.assertEqual(len(set(frozen)), 1)
            self.assertEqual(frozen[0][-1], "room_clear")
            self.assertEqual((session.attempt, session.game.room,
                              session.game.hearts), (3, "1", 3))
            first = summary["attempts"][0]
            self.assertAlmostEqual(first["pause_seconds"], 2)
            self.assertEqual(first["boss_entry_hearts"], 3)
            self.assertEqual(first["hits"], 0)
            self.assertEqual(set(first["rooms"]), set("12345"))
            self.assertEqual(sum(e["kind"] == "retry" for e in session.events), 2)
            self.assertFalse(any(e["attempt"] > 1 and e["kind"] == "dash"
                                 for e in session.events))
            entries = [e for e in session.events
                       if e["kind"] == "entry" and e["attempt"] > 1]
            self.assertEqual([(e["room"], e["run_time"], e["room_time"],
                               e["details"]["hearts"]) for e in entries],
                             [("1", 0, 0, 3), ("1", 0, 0, 3)])
            evidence = []
            for attempt in summary["attempts"]:
                events = [e for e in session.events
                          if e["attempt"] == attempt["attempt"]]
                transitions = []
                for room in "1234":
                    clear = next((e for e in events if e["kind"] == "room_clear"
                                  and e["room"] == room), None)
                    entry = next((e for e in events if e["kind"] == "entry"
                                  and e["room"] == str(int(room) + 1)), None)
                    if clear and entry:
                        gap = entry["run_time"] - clear["run_time"]
                        self.assertAlmostEqual(gap, 1)
                        transitions.append(gap)
                evidence.append({
                    **attempt, "transitions": transitions,
                    "hurt_sources": [e["details"] for e in events
                                     if e["kind"] == "hurt"],
                    "dashes": sum(e["kind"] == "dash" for e in events),
                    "boss_hits": sum(hit[0] == "boss" for e in events
                                     if e["kind"] == "attack"
                                     for hit in e["details"]["hits"]),
                    "terminal_wait_seconds": (
                        attempt["elapsed_excluding_pauses"] - attempt["run_seconds"]
                        if attempt["outcome"] != "unfinished" else 0),
                    "retry_count_before_attempt": attempt["attempt"] - 1,
                })
            print("SPLIT_C_PUBLIC " + json.dumps({
                "fps": fps, "summary": summary, "attempt_evidence": evidence,
                "trial_count": 1, "state_injection": False,
            }, sort_keys=True))

    def test_retained_independent_dodger_baseline_and_fps_comparison(self):
        # Historical rounded comparison; no claim of pre-boss policy identity.
        historical = {
            30: [(6.6, 3), (20.7, 10), (15.6, 6), (18.3, 7)],
            60: [(9.6, 5), (25.1, 14), (15.0, 6), (17.0, 8)],
        }
        measured = {}
        for fps in (30, 60):
            measured[fps] = {}
            for room, (seconds, dashes) in zip("1234", historical[fps]):
                r = bots.play_room(bots.dodger, room, fps, 60)
                self.assertEqual(r["outcome"], "clear")
                self.assertEqual(r["hearts_lost"], 0)
                self.assertEqual(round(r["seconds"], 1), seconds)
                self.assertEqual(r["dashes"], dashes)
                self.assertEqual(r["attacks"], {"1": 6, "2": 8, "3": 8, "4": 7}[room])
                if room in "34":
                    self.assertGreaterEqual(r["dashes"], 1)
                measured[fps][room] = r
        for room in "1234":
            a, b = measured[30][room], measured[60][room]
            self.assertEqual(a["cleared"], b["cleared"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_RETAINED " + json.dumps({
            "source": source_id(), "trial_count_per_room_fps": 1,
            "results": measured,
        }, sort_keys=True))

    def test_boss_actual_decision_logs_and_hearts_comparisons(self):
        results = {}
        for fps in (30, 60):
            results[fps] = {}
            for hearts in (3, 2):
                r = bots.play_room(bots.dodger, "5", fps, 120,
                                   log=True, hearts=hearts)
                self.assertEqual(r["outcome"], "clear")
                self.assertTrue(any("charge" in line for line in r["log"]))
                self.assertTrue(any("short shot" in line for line in r["log"]))
                self.assertFalse(any("swipe boss wind-up" in line for line in r["log"]))
                logs = r.pop("log")
                samples = []
                for fragment in ("walk to boss", "dash up from charge",
                                 "from short shot", "hold off", "face and swing"):
                    samples.append(next((line for line in logs if fragment in line), None))
                r["decision_samples"] = samples
                r["decision_count"] = len(logs)
                results[fps][hearts] = r
        for hearts in (3, 2):
            a, b = results[30][hearts], results[60][hearts]
            self.assertEqual(a["outcome"], b["outcome"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_BOSS " + json.dumps({
            "source": source_id(), "trial_count_per_fps_hearts": 1,
            "results": results,
        }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_d022_observation.py
"""D-022 observation acceptance; survival fixtures are not reachability evidence."""
import contextlib
import io
import unittest
from unittest import mock

import play
import run_driver
from session import RunSession


class ObservationTest(unittest.TestCase):
    def execute(self, text, view="player", fixture=None):
        setup, inputs, rules = play.read_script(text)
        stream = io.StringIO()
        output = None

        def observe(s, force):
            nonlocal output
            if fixture:
                fixture(s, force)
            if output is None:
                output = run_driver.Output(s, setup, view)
            output.emit(force)

        with contextlib.redirect_stdout(stream):
            s, result = run_driver.drive(setup, inputs, rules, observe)
        return s, result, stream.getvalue(), output

    def test_dispatch_and_validation(self):
        for key in ("view-every", "trace-every"):
            for value in ("0.49", "60.01", "nan", "inf", "wrong", ""):
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, "interval"):
                        play.read_script(f"{key} {value}\n")
            for value in ("0.5", "5", "60"):
                self.assertIn("mode", play.read_script(f"{key} {value}\n")[0])
        self.assertIs(play.read_script("trace-every frame\n")[0]["trace_every"], True)

    def test_interval_preserves_events_and_result(self):
        for fps in (30, 60):
            results = []
            for interval in (0.5, 10):
                s, result, text, _ = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\nview-every {interval}\n")
                results.append((
                    s.events, s.t, s.state, s.game.hearts,
                    [line for line in text.splitlines() if line.startswith("[attempt")],
                    result["attempts"],
                ))
            self.assertEqual(*results)
            traces = []
            for interval in ("frame", "5"):
                s, _, _, out = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\ntrace-every {interval}\n", "trace")
                self.assertEqual(out.seen, len(s.events))
                traces.append((s.events, s.t, s.state, s.game.hearts))
            self.assertEqual(*traces)

    def test_default_player_cadence_is_explicit_half_second(self):
        for fps in (30, 60):
            base = f"mode run\nfps {fps}\nlimit 8\n"
            self.assertEqual(self.execute(base)[2],
                             self.execute(base + "view-every 0.5\n")[2])

    def test_controlled_twenty_minutes_at_each_rate(self):
        for fps in (30, 60):
            for view, bound in (("player", 121), ("trace", 241)):
                with self.subTest(fps=fps, view=view):
                    def survival(s, force):
                        if force:
                            s.game.hearts = 10000

                    s, result, text, out = self.execute(
                        f"mode run\nfps {fps}\nlimit 1200\n"
                        "view-every 10\ntrace-every 5\n", view, survival)
                    self.assertAlmostEqual(s.t, 1200)
                    self.assertEqual(result["outcome"], "unfinished")
                    self.assertLessEqual(out.periodic_count, bound)
                    self.assertGreater(out.periodic_count, 1)
                    self.assertTrue(text)
                    self.assertEqual(out.seen, len(s.events))
                    self.assertEqual(result["attempts"][0]["rooms"]["1"], 1200)
                    print(f"D022 long observation fps={fps} view={view} "
                          f"run={s.t} periodic={out.periodic_count}/{bound} "
                          f"source={result['source_id']}")

    def test_summary_clocks_counts_pause_and_retry(self):
        for fps in (30, 60):
            def die_first(s, force):
                if force and s.attempt == 1:
                    s.game.hearts = 0

            s, result, _, _ = self.execute(
                f"mode run\nfps {fps}\nlimit 1\ndriver-limit 5\n"
                "control 0.5 retry\ncontrol 0.6 pause\ncontrol 1.6 resume\n"
                "attempt 2\n0 attack\n", fixture=die_first)
            self.assertEqual(result["attempt_count"], 2)
            first, second = result["attempts"]
            self.assertEqual(first["outcome"], "death")
            self.assertEqual(second["outcome"], "unfinished")
            self.assertAlmostEqual(second["run_seconds"], 1)
            self.assertAlmostEqual(second["rooms"]["1"], 1)
            self.assertEqual(second["attacks"], 1)
            self.assertEqual(second["pauses"], 1)
            self.assertAlmostEqual(second["pause_seconds"], 1)
            self.assertAlmostEqual(
                second["elapsed_excluding_pauses"],
                second["driver_seconds"] - 1)
            self.assertAlmostEqual(
                sum(a["driver_seconds"] for a in result["attempts"]),
                result["driver_seconds"])
            self.assertGreaterEqual(result["processing_seconds"], 0)
            self.assertEqual(second["hits"],
                             sum(e["kind"] == "hurt" for e in s.events
                                 if e["attempt"] == 2))

    def test_summary_once_for_clear_death_and_limit(self):
        for fps in (30, 60):
            for case in ("clear", "death", "unfinished"):
                setup, inputs, rules = play.read_script(
                    f"mode room\nroom empty\nfps {fps}\nlimit 0.1\n"
                    + ("spawn runner 9 4\n0 attack\n" if case == "clear" else ""))
                real = run_driver.RoomSession

                def session(config):
                    s = real(config)
                    if case == "death":
                        s.game.hearts = 0
                    return s

                for view in ("player", "trace"):
                    output = io.StringIO()
                    with mock.patch.object(run_driver, "RoomSession", session), \
                            contextlib.redirect_stdout(output):
                        s, result = run_driver.play(setup, inputs, view, rules)
                    self.assertEqual(output.getvalue().count("summary: "), 1)
                    self.assertEqual(result["outcome"], case)
                    self.assertEqual(result["attempts"][0]["run_seconds"], s.t)

    def test_retry_resets_periodic_schedule(self):
        setup, _, _ = play.read_script("mode run\nview-every 10\ntrace-every 5\n")
        for view in ("player", "trace"):
            s = RunSession()
            out = run_driver.Output(s, setup, view)
            with contextlib.redirect_stdout(io.StringIO()):
                out.emit(True)
                s.run_frame = 600
                out.emit()
                s.state = "dead"
                s.control("retry")
                out.emit(True)
            self.assertEqual(out.attempt, 2)
            self.assertEqual(out.periodic_count, 1)

    def test_legacy_note_only_changes_leading_line(self):
        note = ('note: legacy route — boss status and messages are incomplete; '
                'add "mode room" for the full boss display')
        for fps in (30, 60):
            for duration in (2, 120):
                setup, inputs, rules = play.read_script(
                    f"room 5\nfps {fps}\nend {duration}\n")
                captured = []
                real_game = play.Game

                def make_game(**kwargs):
                    g = real_game(**kwargs)
                    g.hurt_left, g.invulnerable = 1000, True
                    captured.append(g)
                    return g

                outputs = []
                for suppress in (False, True):
                    stream = io.StringIO()
                    original = print

                    def filtered(*args, **kwargs):
                        if args != (note,):
                            original(*args, **kwargs)

                    with mock.patch.object(play, "Game", make_game), \
                            contextlib.redirect_stdout(stream):
                        if suppress:
                            with mock.patch("builtins.print", filtered):
                                play.play(setup, inputs, "player", rules)
                        else:
                            play.play(setup, inputs, "player", rules)
                    outputs.append(stream.getvalue())
                self.assertEqual(outputs[0], note + "\n" + outputs[1])
                a, b = captured
                self.assertEqual((a.t, a.outcome, a.events), (b.t, b.outcome, b.events))
                self.assertEqual(a.t, min(duration, 60))

    def test_public_spitter_and_boss_share_sequence(self):
        for fps in (30, 60):
            def fixture(s, force):
                if force:
                    s.game.hurt_left, s.game.invulnerable = 100, True
                    s.game.spawn("boss", 10, 4)
                    boss = s.game.enemies[-1]
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = s.dt, (-1, 0)

            s, _, _, _ = self.execute(
                f"mode room\nroom empty\nfps {fps}\nlimit 4\n"
                "spawn spitter 1 1\n", "trace", fixture)
            fired = [e["details"] for e in s.events if e["kind"] == "shot_fired"]
            self.assertIn("boss", [e["source"] for e in fired])
            self.assertIn("spitter1", [e["source"] for e in fired])
            self.assertEqual([e["id"] for e in fired],
                             [f"S{i + 1}" for i in range(len(fired))])


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_d022_shots_and_note.py
"""D-022 controlled probes; these are not continuous-reachability evidence."""

import contextlib
import io
import unittest

import play
from game import Game, Shot
from session import RunSession


NOTE = ('note: legacy route — boss status and messages are incomplete; '
        'add "mode room" for the full boss display')


class LegacyNoteTest(unittest.TestCase):
    def test_note_scope_and_position(self):
        for fps in (30, 60):
            for room in ("1", "2", "3", "4", "5", "empty"):
                for view in ("player", "trace"):
                    with self.subTest(fps=fps, room=room, view=view):
                        setup, inputs, rules = play.read_script(
                            f"room {room}\nfps {fps}\nend 0.1\n")
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output):
                            play.play(setup, inputs, view, rules)
                        lines = output.getvalue().splitlines()
                        expected = room == "5" and view == "player"
                        self.assertEqual(lines.count(NOTE), int(expected))
                        if expected:
                            self.assertEqual(lines[0], NOTE)


class ShotLifecycleTest(unittest.TestCase):
    def test_short_shot_removal_and_fixed_recovery(self):
        for fps in (30, 60):
            for case in ("lifetime", "edge", "hit", "dash", "protection"):
                with self.subTest(fps=fps, case=case):
                    s = RunSession(fps)
                    s._enter("5", 3)
                    g, boss = s.game, s.game.enemies[0]
                    boss.x, boss.y = (0.05 if case == "edge" else 10), 4
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = g.dt, (-1, 0)
                    g.place_player(0, 0)
                    s.step()
                    fired = s.t
                    if case in ("hit", "protection"):
                        g.place_player(9.7, 4)
                    elif case == "dash":
                        # Dash toward the shot, so actual protected contact occurs.
                        g.place_player(9.4, 4)
                        s.press("dash", "right")
                    if case == "protection":
                        g.hurt_left, g.invulnerable = 0.8, True
                    for _ in range(fps):
                        s.step()
                    emitted = [e for e in s.events if e["kind"] == "shot_fired"]
                    removed = [e for e in s.events if e["kind"] == "shot_removed"]
                    self.assertEqual(len(emitted), 1)
                    self.assertEqual(len(removed), 1)
                    self.assertEqual(emitted[0]["details"],
                                     {"id": "S1", "source": "boss"})
                    expected = "absorbed" if case in ("dash", "protection") else case
                    self.assertEqual(removed[0]["details"],
                                     {"id": "S1", "source": "boss", "reason": expected})
                    self.assertEqual(g.shots, [])
                    recovery = [e for e in s.events if e["kind"] == "boss_recovery"]
                    self.assertEqual(len(recovery), 1)
                    self.assertAlmostEqual(recovery[0]["run_time"] - fired, 1)
                    self.assertEqual(g.hearts, 2 if case == "hit" else 3)

    def test_clear_room_sequence_and_retry(self):
        for fps in (30, 60):
            s = RunSession(fps)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            for enemy in s.game.enemies:
                enemy.hp = 0
            s.step()
            for _ in range(fps):
                s.step()
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S2")
            s.game.hearts = 0
            s.step()
            removed = [e for e in s.events if e["kind"] == "shot_removed"]
            self.assertEqual([e["details"]["id"] for e in removed], ["S1", "S2"])
            self.assertTrue(all(e["details"]["reason"] == "cleared" for e in removed))
            self.assertTrue(s.control("retry"))
            mark = len(s.events)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S1")
            s.step()
            self.assertFalse(any(e["kind"] == "shot_removed" for e in s.events[mark:]))

    def test_legacy_emission_has_no_new_events(self):
        for fps in (30, 60):
            g = Game(fps, "empty")
            g._emit_shot(Shot(8.2, 4, 0, 0), "spitter1")
            g.step()
            self.assertFalse(any(k in ("shot_fired", "shot_removed")
                                 for _, k, _ in g.events))

    def test_player_messages_hide_ids(self):
        from run_driver import messages_for
        for kind in ("shot_fired", "shot_removed"):
            self.assertIsNone(messages_for({
                "kind": kind, "room": "5",
                "details": {"id": "S1", "source": "boss", "reason": "hit"},
            }))


if __name__ == "__main__":
    unittest.main()
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

<<<FILE goals/G-002-final-boss/62-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 62
from: technical-director
to: studio
stage: Route
outcome: question
---
# 62: technical-director → studio — 検証供給の復旧と試験道具対応の計画

## Task

下記のOwner宛Escalation案を提示し、検証資料・実行・完全証拠の供給条件を調整する。回答後は供給確認、Engineerの試験道具対応、再測定、独立QAの順で進める。

## Context

58・60は独立検証未完了を報告し、59で要求した入力・実行・完全ログの供給が60でも不足した。同じ資料だけで第三のQAを開かない。

D-021によるテキスト・スクリプト方式とStudio内検証の承認は維持する。今回必要なのは承認の取り直しではなく、その実行経路と証拠参照を利用可能にする調整である。

## Findings

### このStepで確認した範囲

packetのソース本文・テスト4ファイル・仕様・報告を静的に照合した。製品コード、bot、仕様は変更していない。tests・traceは実行しておらず、保存ファイルからのsource_id再算出、保存基線の探索、完全ログの永続化も未実施である。

本packetではtests・traceに最大3 roundsが明示され、以前不足していたテスト本文の一部も供給された。この改善を60の「0枠」の継続と混同しない。一方、次のQAにも実行枠が付くこと、全tests本文、完全ログの保存先・再閲覧手段、変更前基線の存在は確認できない。以前0枠になった生成・配布機構の根本原因はpacketからは特定できない。

収録出力のsource_id `04fa2b1c168a`とBUILD `0.6-g002-public-32`は60の報告値であり、現在の保存repo/と一致するとの独立確認ではない。

### 技術所見

1. `bots.py::_dangers`のactive chargeは内部`phase_left`から危険経路残長を計算し、`_threat`の候補除外へ使う。`Output.emit`のplayer viewにはactive残時間がない。表示済み情報を記憶・計算する経路も当該分岐にはないため、D-019項目6の公開情報条件に不適合な判断依存がある。現状のボス比較値をpass根拠にはしない。
2. `_hurt_lines`はsourceがbossの場合もshot側へ入り、突進接触の位置・距離・消費を証明できない。被弾源イベントと補助文を分けて扱う。
3. `test_split_c.py`はボス判断ログ全文を結果に残さず、サンプルへ縮約する。完全ログの別保存が必要である。同ファイルの公開再生入力は現在のbotから生成されるため、bot修正後は入力生成と通常ラン測定も更新対象になる。
4. `test_legacy_note_only_changes_leading_line`は同じ現行実装の注記抑制との比較である。`test_default_player_cadence_is_explicit_half_second`も現行の既定値と明示値の比較であり、いずれも変更前基線との一致を単独では証明しない。
5. 長時間試験はheartsを変更した観測用fixtureである。長時間出力の検証と、正規敵を倒した通常連続到達の証拠を分離する。

これらは試験道具・証拠の問題であり、ゲーム本体の戦闘不具合、対処不能、難度不合格を意味しない。

### 影響システムと順序

並列Stepは開かない。試験道具の変更が入力生成・測定・証拠識別へ連鎖するため、次の順序で固定する。

1. **Studio／Owner：供給条件の確認。** 次の担当Stepに全必要本文、独立実行枠、入力・完全出力を書ける許可先、後続packetから参照可能な経路を具体的に割り当てる。Loadへのパス記載だけで本文供給済みと扱わない。全件を一packetへ収められなければ、依存を明記した直列分割にする。
2. **Engineer：証拠台帳と基線調査。** 使用ソース集合を保存し、`source_id.py`の対象全ファイルとtestsを列挙して識別する。変更前保存ソース・出力が供給された場合は由来、入力、FPS、比較可能範囲を確認する。存在しなければL1/O3等を未確認としてStudioへ返す。要件変更の要否はDesignerへ、Goal範囲の判断はGame Director経由でOwnerへ戻す。
3. **Engineer：ボス判断経路の限定。** ボス判断用に公開情報だけの観測データを作り、判断処理へ内部Game／Enemyを渡さない。warningの固定方向・範囲と、発動時の公開イベントから観測済みの経路を保持し、active中はその全経路を保守的に危険候補とする。内部残時間による残長短縮は使わない。recovery等の公開状態変化で解除する。warningを観測せずactiveから開始する診断では、現在の公開情報から固定最大範囲を保守的に扱い、履歴不足を記録する。プレイヤー表示の追加は不要とする。公開契約変更が必要と判明した場合だけDesignerへ返す。
4. **Engineer：診断ログと試験。** 意思決定入力・計算根拠・候補・選択行動を全判断について記録する。接触診断は判断用データから分離し、boss突進のフレーム前後位置、固定方向、距離、保護、接触消費、被弾を記録する。既存イベントで不足する場合は試験用観測で補い、推定値を実接触値と表記しない。
5. **Engineer：再測定。** 同一保存ソース・同一方針・初期位置／向き／状態・limitで、独立5番を30/60 FPS、開始3/2 heartsの4条件で実行する。全判断ログ、終了理由、hearts、被弾源、攻撃・dash、時間を保存する。数値が閾値を超えた場合は診断後Designerへ返し、自動免除しない。
6. **Engineer：保持回帰と公開再生。** 独立1〜4は既存方針を保持する。共有関数に変更が及べば変更前後の行動列・結果と全保持基準を確認する。独立1〜2のcombat14、3・4の各bot成績・dash、独立1〜4のFPS比較、終了・ログ有無一致・brute対応を追跡する。新botで通常ラン入力を再生成し、両FPS・両viewの公開再生と同一試行時間を再取得する。
7. **独立QA：基準ごとの検証。** 実装者の自己評価を根拠にせず、保存識別を再算出し、全testsの条件・assert・基準IDを照合する。不足fixture、公開再生、共有回帰、D-022を両FPSで独立実行する。
8. **全QA合格後：** 限定Art Verify→独立Play→Designer実測後判断→Game Director Review。Artの表示変更があれば該当QAを再確認してからPlayへ進む。初回再測定で明白な対処不能・到達不能が判明した場合はPlay前にもDesignerへ戻す。

### 試験と証拠保存

Engineerが通常Roleの成果として作るもの：

- 基準ID／FPS→ソース・テスト名・条件・assert・入力・完全ログ参照の対応表。
- 公開情報が同じで内部active残時間だけ異なる場合に、ボス判断が変わらない試験。公開データに存在しない属性を読めない境界も確認する。
- warning→active→recovery、距離0、壁、dash待ち、stun、room境界・retryの判断記憶初期化を確認する試験。
- boss突進の通常被弾・保護接触・非接触で、診断がshotとして誤記されず、接触位置と消費を追えるログ。
- 新attemptが旧未来入力時刻を越える試験、またはpending破棄列の直接観測。
- 共有combat、step68／72／94、cap遅延上限、旧5番からの置換先の追跡表。

保存方式は供給側が許可する実パスを確定してから使用する。実行ごとに、完全入力、コマンド、作業ディレクトリ、FPS、開始条件、limit、ソース識別、終了コード、stdout／stderr全文を保存する。台帳にはファイルのハッシュ・バイト数・行数と分割順を記録し、summaryや抜粋だけで全文を代用しない。

大きい出力は完全原本を保持して連番分割し、後続Stepへ必要部分を全文供給する。ハッシュは同一性確認に使い、閲覧可能性の代用にはしない。保存・再読込みの小規模確認に成功するまで、長大な再測定を始めない。

### リスクと対策

- 保守的な危険経路保持でbot成績・反撃機会が変わる：実測を更新し、ゲームのHP・時間・表示をbotに合わせて変えない。
- 共有判断処理への影響：ボス専用境界を優先し、独立1〜4の変更範囲と回帰結果を明記する。
- source_idはtests変更でも変わる：測定前にソースを固定し、異なる識別の結果を混ぜない。
- 完全ログの再切断：原本保存と再閲覧を先に確認し、収録不能なら直列分割して未確認を残す。
- 変更前資料の不在：現行greenや同一コード内比較で埋めず、該当基準を未確認として判断先へ返す。
- 約87／104秒という既報と15〜20分Visionの差：人間の所要時間と同一視せず、再測定と独立Play後にDesignerへ渡す。新たな秒数ゲートを設けない。

### 独立QAの再開条件

次の全項目をStudioが確認してから、60の未確認表を添えて再開する。

- 全必要ソース・全tests・仕様本文が実際に閲覧できる。
- QA自身が必要な追加実行を行える枠とコマンドが割り当てられている。
- 入力・完全ログの書込先と後続参照経路が確認されている。
- ボス公開情報対応と4条件の再測定資料が揃い、独立1〜4への影響が追跡できる。
- 変更前比較資料が供給されているか、不在と判断待ちの基準が明示されている。

基線不在でも他項目の検証は進められるが、L1/O3等を含む全基準passは保留する。枠を使い切り、入力・機能の不足なく残作業だけがある場合は、完了条件を示して直列の継続Stepへ渡す。

### Owner宛Escalation案（Studio Routeで提示する）

---
kind: escalation
goal: G-002
seq: 62
from: technical-director
to: owner
status: open
decision: none
---

# 62: Owner decision needed — 承認済み検証の供給をどう整えるか

#### Question

G-002について、承認済みのテキスト方式を維持して全資料・独立実行枠・完全ログの保存参照経路を調整する案A、検証可能な範囲へGoalを狭める案B、供給が整うまで停止する案Cのどれを選びますか。

#### Why this needs the Owner

58・60で同じ供給不足が二度報告されたことが、再び同じQA依頼を出さずEscalationする手続上の理由です。修正後に同じ受入基準が二度失敗した事例ではありません。

Roleが解消できない具体的な障害は、担当Stepに付与される実行枠、packetへの全必要本文の収録、許可書込先、完全ログを後続Stepへ届ける参照経路を、このTechnical Director Stepから設定できないことです。以前のQAでは実行枠0、tests本文不足、ログ切断が報告されました。今回のStepには最大3 roundsと一部tests本文があり改善していますが、次のQAで必要機能が揃うとの確認はありません。0枠の根本原因と保存基線の所在も不明です。

D-021が再検討条件とする「通常のStudio Stepでは実行できない具体的な障害」に関する調整です。bot修正、試験作成、基準対応表、ログ生成は通常Roleの仕事として計画済みであり、Ownerへ技術方式の選択は求めません。実機、gamepad、外部配員、追加金銭、旧指定sha照合も求めません。

#### Options

**案A — D-021を維持して供給条件を整える（推奨）**

全必要ソース・tests本文、担当Step内の追加実行枠、完全入力・stdout／stderrを書ける場所、後続Stepが全文を参照できる経路を調整します。一度に収まらなければ直列Stepに分割します。L1/O3等の変更前保存ソース・出力は、所在と提供可否を回答対象に含めます。

失う検証範囲は予定しません。ただし基線がなければ該当基準は未確認として残り、別途判断が必要です。費用は通常Step内で、追加金銭は使いません。リスクは供給機構の制約が残ることで、実現性はまだ確認できていません。計画・資料分割は変更可能です。

選択後：Studioが供給担当・具体的経路・利用可能な枠を確定し、小規模な保存／再閲覧確認→Engineerの試験道具対応→再測定→独立QAへ進みます。

**案B — 今回のGoalを検証できる範囲へ狭める**

利用可能な本文、実行枠、保存参照経路を明示したうえで、Game DirectorとDesignerが検証可能な成果へGoal・該当基準を再定義します。最低限、残す成果の入力と証拠を保存・再閲覧できる供給が必要です。

変更前基線が得られなければL1/O3等の変更前一致を、独立実行・全証拠が得られなければ該当する全基準検証と体験判断を、今回の完了範囲から外す可能性があります。具体的な除外一覧は再計画で確定します。従来G-002全体の合格は主張できません。通常Step内で調整できますが、後日の再検証と判断のやり直しがリスクです。未検証の記録を保持すれば範囲の再拡大は可能です。

選択後：Studio→Game Director→Designerによる範囲・Decision整理→Technical Director再計画。QAへ基準免除を直接依頼しません。

**案C — 供給が整うまで停止する**

新たな実行・保存機能の即時供給は求めず、現状の資料と未確認一覧を維持します。今回失うのは残りの検証を進める機会で、基準自体は維持します。追加金銭は不要ですが、Goal達成時期は未定となります。供給再開条件を満たせば再開可能です。

選択後：StudioがOwner待ちとして停止を管理し、資料・実行・保存参照経路が確認できた時点でTechnical Directorへ戻します。

#### Studio recommendation

案Aを推奨します。D-021の承認を維持し、ゲーム仕様やGoalを狭める前に、承認済みの検証経路を実際に供給できるか確認するためです。これはTechnical Directorの提案であり、Ownerの決定済み事項ではありません。

#### Reasoning

今回のpacketには実行枠と一部tests本文があり、供給改善の兆候があります。しかし次のQAの枠、全文収録、永続参照は未確認なので、復旧可能とは断定しません。

供給機構が完全証拠の保存・再読込みや必要な独立実行を提供できないと確認された場合は、案BまたはCへ推奨を見直します。変更前基線だけが存在しない場合は、その基準に限定した再判断を先に検討します。

回答待ちの間に通常Roleが進められるのは、既供給本文に基づく基準対応表と試験道具修正briefの準備です。新規の並列Stepは開かず、第三のQA再依頼や合格後の工程へは進めません。

#### Owner decision required

A／B／Cと条件を回答してください。Aの場合は、全本文・実行枠・完全ログ保存参照経路を誰がどう調整するか、および変更前資料の提供可否を指定してください。現時点で不明な項目は、確認担当と確認方法の指定で構いません。

## Decisions already made

- D-019：公開情報限定のボスbot、開始3/2 hearts別FPS比較、独立1〜4保持回帰、実測後Designer判断を維持。
- D-021：テキスト・スクリプト方式とStudio内独立QA・Playを承認。実機供給・旧指定sha照合・追加金銭は要求しない。
- 仕様§11／D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- 本Stepは新Decisionを採択せず、上記の技術計画と未決Escalation案を返す。

## Constraints

- QAのfailと未確認を上書きしない。実行・保存・基線探索を実施済みと扱わない。
- 製品コード・bot・仕様は変更しない。後続Engineerで試験道具を対応する。
- プレイヤー向け契約変更はDesigner、Goal範囲変更はGame Director経由で判断する。
- 新たな難度・時間ゲートを設けず、変更前比較を現行suite成功で代用しない。
- QA用資料と独立Play資料を分ける。Playへ期待結果、QA判定、実装履歴、Review用体験信号を渡さない。
- Ownerへの実際の提示とGoalのblocked-on-ownerへの変更はStudio Routeが行う。

## Open questions

1. 次のEngineer・QA Stepへ全必要本文、実行枠、完全ログの保存参照経路を具体的に供給できるか。
2. 以前のQAで0枠・本文未収録・出力切断となった配布上の原因と、再発防止を確認する担当は誰か。
3. L1/O3等に比較可能な変更前ソース・完全出力は存在するか。不在なら該当基準の扱いをDesignerへどう戻すか。
4. Ownerは案A／B／Cのどれを選ぶか。

## Expected output

Studioは本Handoff内のEscalation案をOwnerへ提示し、供給障害に対する選択と条件を記録する。回答前に同じQA依頼を繰り返さない。

案Aなら具体的な供給確認を先に行い、本計画をEngineerの試験道具対応briefへ落とす。再測定と独立QAの再開条件を満たしてから検証を再ルートする。全QA合格後の限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewを保持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/escalation.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/61-studio-to-technical-director.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting report: goals/G-002-final-boss/58-qa-to-studio.md
- Supporting request: goals/G-002-final-boss/59-studio-to-qa.md
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

<<<FILE goals/G-002-final-boss/65-game-designer-to-studio.md
---
kind: handoff
goal: G-002
seq: 65
from: game-designer
to: studio
stage: Route
outcome: done
---
# 65: game-designer → studio — 変更前一致の記録比較と確認不能を確定

## Task

D-024と証拠適用補足を受領し、Technical Directorへ62のD-023適合再計画をルーティングする。確認不能部分を残したまま検証を進める工程と、最終判断への引継ぎを整理する。

## Context

D-023でOwnerはテキスト方式の継続を指示し、変更前ビルドは保存されていないと確定した。Designerには、変更前一致要求を記録数値との比較にするか、確認不能として扱うかが委任された。

今回はこの委任範囲だけを判断した。実装、play／bots実行、独立QA判定、実測後の難度判断は行っていない。

## Findings

新規成果物：

- `decisions/D-024-g002-historical-comparison-evidence.md`
- `design/g002-historical-comparison-evidence.md`

補足仕様の表に、従来要求、採択した扱い、出典、条件・精度、未確認範囲を記載した。

### 確定した扱い

L1の変更前出力・結果・終了時刻、O3の変更前出力、step68 V-cのbyte一致、step94 W7の変更前イベント・挙動一致は確認不能とした。L4、step68 V-a／V-b／V-e、step94 W3／W4に含まれる歴史的一致も、現在の仕様へ直接照合できる部分と分離した。

独立1〜4 dodgerは40の記録数値との比較を採択した。各FPS・部屋、3 hearts、通常初期状態、limit 60秒を揃え、clear・損失0・dash回数と小数1桁時間を比較する。時間の丸め方法も補足仕様で定義した。56の保存実行報告は後続記録として区別する。

40は既にボス対応後の保存ソース`5145454ab956`である。40も提出前一致を確認できなかったと明記しており、この記録からボス対応前の厳密な同一性は証明しない。56の`04fa2b1c168a`での152件成功も、その不足を埋めない。

R2・step72 R3-1の保持部分は元仕様の配置・パラメータへの現行照合であり、変更前実装を必要としない。step72 R3-6のgrub有無比較、combat16c、現行の注記抑制対照、既定値と明示0.5秒の対照は、現在のビルド内比較として継続できる。

### Technical Directorへの仕様上の入力

62の「変更前基線を探索・供給する」「全文原本の保存・再読込みを再開条件にする」部分はD-023へ適合させる。存在しない基線・保存先を待つ計画にはしない。

最大3回、各出力2万字の範囲で、対象を絞った証拠出力と必要な直列Stepへ再構成する。表示した証拠の範囲、集計・判定の方法、未表示部分を区別できる計画が必要である。試験構造と技術方式は本Stepでは選ばない。

ボスbotの公開情報限定対応、突進診断の訂正、開始3/2 hearts別FPS再測定、通常ラン入力の再生成は62の依存順序を保持する。対応前ボス数値と生成再生時間を新たなpass基線にしない。独立1〜4の保持比較とは分離する。

確認不能を合格・免除・Goal達成にしない。62の「全QA合格後」という工程条件は、歴史比較の確認不能を含めて再整理する必要がある。Goal再解釈や範囲変更が必要ならGame Directorへ返す。QAに直接免除を求めない。

## Decisions already made

- D-019：保持回帰、公開情報限定のボス比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- D-023：個別本文供給、@need一度最大8件、@run最大3回、出力最大2万字、全文保存先・変更前ビルドなし。
- D-024：歴史的一致の確認不能と、独立1〜4 dodgerの記録精度に限定した比較を確定。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲートを変更しない。60のQA判定を上書きしない。未確認をpassにしない。

ボスbot対応前の数値から戦闘不具合・難度不合格を断定しない。追加数値ゲートと時間Visionの判断は再測定・独立QA・独立Play後に残す。

本Handoffと補足仕様の検証結果・期待値を独立Play資料へ転記しない。

## Open questions

1. Technical Directorは、供給上限の中で基準別の証拠と独立実行をどの単位へ分割するか。
2. 歴史比較の確認不能を保持した工程条件をどう整理するか。Goalの再解釈が必要ならGame Directorへ返すこと。
3. 対応後の保持記録比較に差が出た場合、その条件と影響は何か。差が出る前の推測で仕様を変えない。

## Expected output

StudioはTechnical Directorへ、62をD-023・D-024へ適合させる再計画を依頼する。基線探索・全文保存機構の確保を開始条件から外し、対象別の本文供給、限定出力、直列分割、未確認の受渡しを具体化する。

その後、試験道具対応→再測定→独立QAへ進む条件を確定する。確認不能項目は最終Reviewにも渡す。限定Art Verify、独立Play、実測後Designer判断、Game Director Reviewを省略しない。

次の技術再計画で追加本文が必要な個別ファイル名：

- `repo/source_id.py`
- `repo/bots.py`
- `repo/run_driver.py`
- `repo/play.py`
- `repo/tests/test_bots_boss.py`
- `repo/tests/test_split_c.py`
- `repo/tests/test_d022_observation.py`
- `repo/tests/test_d022_shots_and_note.py`

この8件は62の主要所見を再計画へ結び付けるための本文であり、全QAに十分なファイル一覧ではない。後続QAの全tests本文はStudioが個別ファイル名で別途割り当てる。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/g002-historical-comparison-evidence.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/60-qa-to-studio.md
- Project: goals/G-002-final-boss/62-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/64-studio-to-game-designer.md
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

- Write the outgoing Handoff as goals/G-002-final-boss/68-technical-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
