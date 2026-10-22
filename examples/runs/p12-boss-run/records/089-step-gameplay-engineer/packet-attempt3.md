# Studio operation packet

operation: Step
goal: G-002
role: gameplay-engineer
incoming_handoff: goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
next_seq: 74
runs: tests, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-final-boss/74-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 73
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 73: studio → gameplay-engineer — E1実dodger接続・全分岐試験の継続

## Task

68§4と71のE1を継続する。72の公開境界prototypeを実dodgerへ接続し、公開観測だけによる全判断、記憶の寿命・初期化、全分岐試験と必要な表示証拠を揃える。

## Context

72はpartialで、新しい仕様質問や供給不足はない。公開観測・純粋判断のprototypeと3試験は保存されたが、実dodgerは旧経路のままでありE1未完了。60のfailを維持する。

runtime Build checkはsource 8fe9bcc21225で157 tests、OK。これは独立QAや公開情報限定bot完成の証拠ではない。未保存prototypeのsource 5c62a1c7e18eと混同しない。

## Findings

今回の作業・証拠契約は68§2・4および71。E2〜E5と独立QAはまだ開かない。

既知の残作業：

- 実dodgerを公開観測と記憶だけを受ける判断経路へ接続する。_dangers、_threat、_escape、_face_and_swing等を含む全呼出経路を監査し、非公開active残時間・struck等への依存を除く。ログ専用内部観測は判断後の別経路に置く。
- 全入力フィールドをplayer表示または既存公開観測へ対応付ける。座標を文字セルから復元できたとの未証明の主張をしない。
- warningで観測した固定経路をactive中は全体として保持し、公開されたrecovery等で解除する。履歴なしactiveでは固定最大範囲を保守的に扱い、不足を記録する。
- 記憶の所有と寿命を実経路へ接続し、部屋入場・retry初期化を検査する。直接dodger呼出、通常run、_Proxy入力捕捉との互換を確認する。
- 判断番号、反応grid、時刻、公開入力、記憶の由来、候補・除外理由、選択・実際の発行ボタンを記録する。stunによる判断省略も記録する。
- 両FPS、両攻撃の遷移、距離0・距離境界・端点、各壁、dash待ち、stun、入場・retry、履歴不足の各方向を含む全判断分岐を試験する。許可外属性を読むと失敗するfixtureと、同じ公開入力・異なる内部値での実経路の判断不変を示す。slotsだけで全経路監査済みとはしない。
- E1の状態・判断emit_rowsアダプタと窓helperの確認本文を出す。候補の途中採択だけを全候補列挙としない。既存印字の抑制でassertや検証対象を減らさない。

72で追加した完全IDは次の3件。いずれもrepo/tests/test_bots_boss.py内で、Q1を主担当、Q4にも更新本文を配布する。

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches

71の13ファイルQA配布台帳を維持する。追加・変更試験を完全IDで追跡し、未配布を残さない。配布と基準充足は区別する。70の正本との完全対応、E4の未丸め時刻・half-up、E5公開再生、長時間観測等の残作業を消さない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較。
- D-021/D-023：Studio内テキスト検証。個別Load、@need一度最大8件、@run最大3回、各出力最大2万字。全文保存先・変更前ビルドなし。
- D-022：表示・弾・長時間観測契約を保持。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離。
- 68：E1完了確認後にStudioがE2を別Handoffで開く。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、表示契約、Goal範囲を変更しない。独立1〜4の方針を保持し、共有関数への影響を報告する。

書込対象はrepo/bots.py、repo/tests/test_bots_boss.py、repo/tests/test_split_c.py、repo/tests/test_g002_evidence.py。test_split_c.pyはE1境界接続・互換・対象別出力に必要な範囲のみ。他ファイル変更が不可欠なら具体的理由と対象を返す。game.py、session.py、play.py、run_driver.pyは照合対象であり変更しない。

repo/での固定コマンドは `python3 -m unittest discover -s tests`。最大3回を公開境界不変、記憶・境界条件、suite・不足確認へ配分する。出力は概ね12000字以内を目指し、対象BEGIN/END、列定義、連番、総件数・表示件数・未表示・除外を明示する。再実行の入力・source_id・総判断数を照合し、異なる集合を継ぎ合わせない。

未表示・切断を確認済みにせず、件数やsource_idだけで必要本文を置き換えない。60のfail、歴史的確認不能を自己確認で上書きしない。

## Open questions

新しい仕様質問はない。実経路の全分岐が公開情報境界を通ること、記憶の初期化、判断ログと許可外参照禁止をどのassert・表示本文で示すか。

## Expected output

studio宛Handoffへ変更ファイル、公開フィールド対応、全呼出経路の監査範囲、完全試験IDとassert、対象別状態・判断本文、コマンド、最終source_idと識別対象を記録する。実装者の評価・理由・自試験の解釈はSender assessmentにまとめる。

全試験件数・追加ID・QA配布先、今回解消分、残作業、未表示範囲を明示する。E1完了とE2以降・独立QA完了を区別する。既知の残作業があればpartialで返し、供給条件をOwnerへ再質問しない。同じE1が3回連続partialとなった場合、StudioはTechnical Directorへ分割・再計画を戻す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Supporting handoff: goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/72-gameplay-engineer-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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
    "5": [("boss", 12, 4)],
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


class Shot(list):
    """Keep indexed coordinates compatible with existing practice fixtures."""

    def __init__(self, x, y, vx, vy, source="spitter", lifetime=SHOT_LIFE):
        super().__init__([x, y, vx, vy, 0.0])
        self.source = source
        self.lifetime = lifetime


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind not in ("spitter", "boss"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "boss":
            self.hp = 12
            self.phase = "approach"
            self.phase_left = 0.0
            self.attack_name = "charge"
            self.struck = self.spent = False
        elif kind == "spitter":
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
        if self.kind == "boss":
            return "B"
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
        self.shot_sequence = None  # Public sessions opt in; legacy logs stay unchanged.
        self.last_shot = None  # time of the last shot fired in the room (cue gap rule)
        self.hurt_kinds = []  # who dealt each hurt event, in order (text view names, D-011)
        self.events = []  # (time, kind, details)
        self.cleared = False
        self.outcome = None
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
        if self.outcome is not None or self.hearts <= 0:
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
        if self.outcome is not None:
            return
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        if self.recovery <= EPS:
            self.recovery = 0.0
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
        self._resolve_result()

    def _resolve_result(self):
        """Existing shots resolve before the single, death-first frame result."""
        if self.outcome is not None:
            return
        if self.hearts <= 0:
            self.outcome = "dead"
        elif self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.outcome = "cleared"
            self.cleared = True
            self.log("cleared")
        else:
            return
        for shot in self.shots:
            self._shot_removed(shot, "cleared")
        self.shots.clear()
        for enemy in self.enemies:
            enemy.aim = None
            if enemy.kind == "spitter":
                enemy.cueing = False

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
            if enemy.kind == "boss":
                if enemy.hp <= 0:
                    enemy.aim = None
                elif enemy.phase == "warning":
                    self.log("boss_swipe")
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
            elif enemy.kind == "boss":
                self._update_boss(enemy, dt)
            else:
                self._update_spitter(enemy, dt)

    def _update_boss(self, e, dt):
        if e.phase == "approach":
            dx, dy = self.x - e.x, self.y - e.y
            distance = math.hypot(dx, dy)
            if distance <= WINDUP_RANGE + EPS:
                e.aim = (dx / distance, dy / distance) if distance else (1.0, 0.0)
                e.phase = "warning"
                e.phase_left = 0.7 if e.attack_name == "charge" else 0.8
                self.log("boss_warning", attack=e.attack_name, aim=e.aim)
            else:
                distance_moved = min(dt, distance - WINDUP_RANGE)
                e.x += dx / distance * distance_moved
                e.y += dy / distance * distance_moved
            return
        if e.phase == "warning":
            e.phase_left = max(0.0, e.phase_left - dt)
            if e.phase_left <= EPS:
                e.phase = "active"
                e.phase_left = 0.3 if e.attack_name == "charge" else 1.0
                e.struck = e.spent = False
                self.log("boss_active", attack=e.attack_name)
                if e.attack_name == "short shot":
                    shot = Shot(
                        e.x, e.y, e.aim[0] * SHOT_SPEED,
                        e.aim[1] * SHOT_SPEED, "boss", 1.0,
                    )
                    shot.born_frame = self.frame
                    self._emit_shot(shot, "boss")
            return
        if e.phase == "active":
            span = min(dt, e.phase_left)
            if e.attack_name == "charge":
                e.x, e.y = self._clamp(
                    e.x + e.aim[0] * LUNGE_SPEED * span,
                    e.y + e.aim[1] * LUNGE_SPEED * span,
                )
                if (
                    not e.struck and not e.spent
                    and math.hypot(e.x - self.x, e.y - self.y) <= GRUB_REACH
                ):
                    if self.invulnerable:
                        e.spent = True
                    else:
                        e.struck = True
                        self._hurt("boss", "boss's charge")
                    self.log("boss_contact", blocked=e.spent)
            e.phase_left = max(0.0, e.phase_left - span)
            if e.phase_left <= EPS:
                e.phase = "recovery"
                e.phase_left = 1.2 if e.attack_name == "charge" else 1.4
                e.aim = None
                self.log("boss_recovery", attack=e.attack_name)
            return
        e.phase_left = max(0.0, e.phase_left - dt)
        if e.phase_left <= EPS:
            e.phase = "approach"
            e.attack_name = "short shot" if e.attack_name == "charge" else "charge"
            self.log("boss_pursuit", attack=e.attack_name)

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
                source = "spitter" + str(
                    [enemy for enemy in self.enemies if enemy.kind == "spitter"].index(e) + 1
                )
                self._emit_shot(
                    Shot(e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED),
                    source,
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _emit_shot(self, shot, source):
        if self.shot_sequence is not None:
            self.shot_sequence += 1
            shot.id = f"S{self.shot_sequence}"
            shot.event_source = source
            self.log("shot_fired", id=shot.id, source=source)
        self.shots.append(shot)

    def _shot_removed(self, shot, reason):
        if self.shot_sequence is not None:
            if hasattr(shot, "id"):
                self.log(
                    "shot_removed", id=shot.id,
                    source=shot.event_source, reason=reason,
                )
        elif reason in ("lifetime", "edge"):
            self.log(
                "shot_removed", source=getattr(shot, "source", "spitter"),
                reason=reason,
            )

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            # Emission starts the boss's active interval. Movement and aging
            # begin on the next frame, so expiry coincides with recovery.
            if getattr(shot, "born_frame", None) == self.frame:
                kept.append(shot)
                continue
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            source = getattr(shot, "source", "spitter")
            if shot[4] >= getattr(shot, "lifetime", SHOT_LIFE) - EPS:
                self._shot_removed(shot, "lifetime")
                continue
            bounds = (0, ROOM_W - 1, 0, ROOM_H - 1) if source == "boss" else (-1, ROOM_W, -1, ROOM_H)
            if not (bounds[0] <= shot[0] <= bounds[1] and bounds[2] <= shot[1] <= bounds[3]):
                self._shot_removed(shot, "edge")
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                blocked = self.invulnerable
                if not blocked:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                self._shot_removed(shot, "absorbed" if blocked else "hit")
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
        self.log("hurt", source=source, hearts=self.hearts, name=name or source)
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

<<<FILE repo/session.py
"""Continuous-run progression; Game remains the authority for room combat."""

from game import EPS, HEARTS, Game


class RunSession:
    """Separate combat, room-clear display, terminal state and pause.

    Drivers must reset reaction memory when generation changes and route
    timed inputs by attempt. This class does not implement the script driver.
    """

    def __init__(self, fps=60):
        self.fps = fps
        self.dt = 1.0 / fps
        self.attempt = 1
        self.shot_sequence = 0
        self.generation = 0
        self.events = []
        self.sequence = 0
        self.paused = False
        self.run_frame = 0
        self.state = "combat"
        self.clear_frames = 0
        self.stop_reason = None
        self._enter("1", HEARTS)

    @property
    def t(self):
        return self.run_frame / self.fps

    @property
    def room_t(self):
        return self.game.t

    def log(self, kind, **details):
        self.sequence += 1
        self.events.append({
            "sequence": self.sequence,
            "attempt": self.attempt,
            "room": self.game.room,
            "run_time": self.t,
            "room_time": self.room_t,
            "frame": self.game.frame,
            "kind": kind,
            "details": details,
        })

    def _enter(self, room, hearts):
        self.game = Game(fps=self.fps, room=room)
        self.game.shot_sequence = self.shot_sequence
        self.game.hearts = hearts
        self.generation += 1
        self.game_seen = 0
        self.state = "combat"
        self.clear_frames = 0
        self.log("entry", hearts=hearts)

    def press(self, action, direction=None):
        if self.paused or self.state != "combat" or self.stop_reason:
            self.log(
                "input_rejected",
                action=action,
                direction=direction,
                reason="paused" if self.paused else (
                    "stopped" if self.stop_reason else self.state
                ),
            )
            return False
        first = len(self.game.events)
        self.game.press(action, direction)
        self._collect()
        accepted = not any(
            kind == "ignored" for _, kind, _ in self.game.events[first:]
        )
        self.log("input", action=action, direction=direction, accepted=accepted)
        return accepted

    def control(self, action):
        if action == "pause":
            if not self.paused and self.state in ("combat", "room_clear") and not self.stop_reason:
                self.paused = True
                self.game.heading = (0, 0)
                self.log("pause")
                return True
        elif action == "resume":
            if self.paused and not self.stop_reason:
                self.paused = False
                self.log("resume")
                return True
        elif action == "retry":
            if self.state in ("won", "dead"):
                self.attempt += 1
                self.shot_sequence = 0
                self.run_frame = 0
                self.paused = False
                self.stop_reason = None
                self._enter("1", HEARTS)
                self.log("retry")
                return True
        else:
            raise ValueError(f"unknown control {action}")
        self.log("control_rejected", action=action, state=self.state)
        return False

    def _collect(self):
        self.shot_sequence = self.game.shot_sequence
        for _, kind, details in self.game.events[self.game_seen:]:
            self.log(kind, **details)
        self.game_seen = len(self.game.events)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state in ("won", "dead"):
            return
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
            return
        self.run_frame += 1
        if self.state == "room_clear":
            self.clear_frames += 1
            if self.clear_frames >= self.fps:
                old_hearts = self.game.hearts
                room = str(int(self.game.room) + 1)
                self._enter(room, min(HEARTS, old_hearts + 1))
                self.log("recovery", gained=self.game.hearts - old_hearts)
        else:
            self.game.step()
            self._collect()
            if self.game.outcome == "dead":
                self.state = "dead"
                self.log("run_dead")
            elif self.game.outcome == "cleared":
                if self.game.room == "5":
                    self.state = "won"
                    self.log("run_won")
                else:
                    self.state = "room_clear"
                    self.clear_frames = 0
                    self.log("room_clear", next_room=int(self.game.room) + 1)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
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
from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class BossObservation:
    """Public sprites, boss status and room clock; no internal object references."""
    t: float
    x: float
    y: float
    boss_x: float
    boss_y: float
    phase: str
    attack: str
    aim: tuple | None
    warning_left: float | None
    shots: tuple


@dataclass(frozen=True, slots=True)
class BossMemory:
    lane: tuple | None = None
    attack: str | None = None
    warning_time: float | None = None


@dataclass(frozen=True, slots=True)
class BossChoice:
    memory: BossMemory
    provenance: str
    candidates: tuple
    excluded: tuple
    selected: str
    buttons: tuple


def observe_boss(game):
    """Read adapter; active aim, timer and contact flags never cross the boundary."""
    boss = next((e for e in game.enemies
                 if e.kind == "boss" and e.hp > 0), None)
    if boss is None:
        return None
    warning = boss.phase == "warning"
    return BossObservation(
        game.t, game.x, game.y, boss.x, boss.y, boss.phase,
        boss.attack_name, tuple(boss.aim) if warning and boss.aim else None,
        boss.phase_left if warning else None,
        tuple((s[0], s[1]) for s in game.shots),
    )


def choose_boss(observation, memory):
    """Pure prototype, not installed in dodger.

    Retain the complete warning lane throughout active. Without warning
    history, use a maximum radial envelope rather than an undisplayed aim.
    """
    o = observation
    candidates, excluded = [], []
    provenance = "none"
    if o.phase == "warning" and o.aim is not None:
        length = 2.4 if o.attack == "charge" else 3.0
        memory = BossMemory(
            (o.boss_x, o.boss_y, *o.aim, length), o.attack, o.t,
        )
        provenance = "warning"
    elif o.phase == "active":
        if memory.lane is not None and memory.attack == o.attack:
            provenance = "warning-history"
        else:
            memory = BossMemory()
            provenance = "missing-warning-history"
    else:
        memory = BossMemory()

    dangerous = False
    if o.phase in ("warning", "active"):
        if memory.lane is not None:
            ox, oy, ux, uy, length = memory.lane
            along = max(0.0, min(length,
                                (o.x - ox) * ux + (o.y - oy) * uy))
            radius = 0.6 if o.attack == "charge" else 0.4
            dangerous = math.hypot(
                o.x - ox - along * ux, o.y - oy - along * uy,
            ) <= radius + 0.3
        else:
            radius = 3.0 if o.attack == "charge" else 3.4
            dangerous = math.hypot(
                o.x - o.boss_x, o.y - o.boss_y,
            ) <= radius + 0.3
        excluded.append(("attack", "warning-or-active"))

    dangerous = dangerous or any(
        math.hypot(o.x - x, o.y - y) <= 1.1 for x, y in o.shots
    )
    if dangerous:
        if memory.lane is not None:
            _, _, ux, uy, _ = memory.lane
            preferred = ("down", "up") if abs(ux) >= abs(uy) else ("right", "left")
        else:
            preferred = ("up", "down", "left", "right")
        for direction in preferred:
            dx, dy = DIRECTIONS[direction]
            inside = (0 <= o.x + dx * 1.5 <= ROOM_W - 1
                      and 0 <= o.y + dy * 1.5 <= ROOM_H - 1)
            candidates.append(("move", direction, inside))
            if inside:
                return BossChoice(memory, provenance, tuple(candidates),
                                  tuple(excluded), "escape",
                                  (("move", direction),))
            excluded.append((direction, "wall"))
        return BossChoice(memory, provenance, tuple(candidates),
                          tuple(excluded), "hold", (("stop", None),))
    if o.phase in ("warning", "active"):
        return BossChoice(memory, provenance, (("hold",),),
                          tuple(excluded), "hold", (("stop", None),))
    dx, dy = o.boss_x - o.x, o.boss_y - o.y
    if math.hypot(dx, dy) > 1.1:
        return BossChoice(memory, provenance, (("approach",),), (),
                          "approach", (("move", _toward(dx, dy)),))
    # Input authority enforces attack recovery; no internal recovery is read.
    return BossChoice(memory, provenance, (("swipe",),), (), "swipe",
                      (("move", _toward(dx, dy)), ("stop", None),
                       ("attack", None)))


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


class PublicBoundaryPrototypeTest(unittest.TestCase):
    def test_active_internal_values_do_not_cross_boundary(self):
        from dataclasses import fields
        names = {field.name for field in fields(bots.BossObservation)}
        self.assertFalse(names & {"phase_left", "struck", "spent", "game", "enemy"})
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            warning = bots.observe_boss(game)
            remembered = bots.choose_boss(warning, bots.BossMemory()).memory
            boss = game.enemies[0]
            boss.phase = "active"
            observations, choices = [], []
            for left, struck, spent, aim in (
                (0.001, False, False, (-1, 0)),
                (99.0, True, True, (0, 1)),
            ):
                boss.phase_left, boss.struck, boss.spent = left, struck, spent
                boss.aim = aim
                observation = bots.observe_boss(game)
                observations.append(observation)
                choices.append(bots.choose_boss(observation, remembered))
                self.assertIsNone(observation.aim)
                self.assertIsNone(observation.warning_left)
            self.assertEqual(observations[0], observations[1])
            self.assertEqual(choices[0], choices[1])

    def test_warning_memory_active_and_recovery(self):
        from dataclasses import replace
        game = boss_warning("charge", (8, 4))
        warning = bots.observe_boss(game)
        first = bots.choose_boss(warning, bots.BossMemory())
        active = replace(warning, phase="active", aim=None, warning_left=None,
                         boss_x=8.5)
        second = bots.choose_boss(active, first.memory)
        self.assertEqual(second.memory, first.memory)
        self.assertEqual(second.provenance, "warning-history")
        self.assertEqual(second.selected, "escape")
        recovery = bots.choose_boss(replace(active, phase="recovery"), second.memory)
        self.assertEqual(recovery.memory, bots.BossMemory())
        missing = bots.choose_boss(active, bots.BossMemory())
        self.assertEqual(missing.provenance, "missing-warning-history")
        self.assertEqual(missing.selected, "escape")

    def test_slots_only_input_and_visible_branches(self):
        from dataclasses import replace
        o = bots.BossObservation(0, 8, 4, 10, 4, "recovery",
                                 "charge", None, None, ())
        self.assertFalse(hasattr(o, "__dict__"))
        self.assertEqual(bots.choose_boss(o, bots.BossMemory()).selected, "approach")
        close = replace(o, boss_x=8)
        self.assertEqual(bots.choose_boss(close, bots.BossMemory()).selected, "swipe")
        warning = replace(o, phase="warning", aim=(-1, 0), warning_left=0.5)
        off = replace(warning, y=7)
        self.assertEqual(bots.choose_boss(off, bots.BossMemory()).selected, "hold")
        wall = replace(warning, y=8, boss_y=8)
        choice = bots.choose_boss(wall, bots.BossMemory())
        self.assertIn(("down", "wall"), choice.excluded)
        self.assertEqual(choice.buttons, (("move", "up"),))
        shot = replace(o, shots=((8, 4),))
        self.assertEqual(bots.choose_boss(shot, bots.BossMemory()).selected, "escape")


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

<<<FILE repo/tests/test_g002_evidence.py
"""E0 inventory and bounded evidence selection; no product or bot changes.

Run from repo: python3 -m unittest discover -s tests
Inventory IDs use module.class.method; group headers supply module.class.
To select existing evidence, import emit_rows from a later evidence test.
Selection never changes the collection being evaluated by that test.
"""
import json
from pathlib import Path
import unittest

from source_id import source_id


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def emit_rows(target, columns, rows, start=1, stop=None, excluded=()):
    """Print a numbered, explicitly bounded window over already evaluated rows.

    Callers must evaluate/assert their complete target collection before calling.
    This helper reports selection and completeness, not criterion success.
    Numbers are one-based inclusive. Empty collections are supported.
    Missing END or numbered rows in collected output means incomplete evidence.
    """
    rows = list(rows)
    if start < 1 or (stop is not None and stop < start):
        raise ValueError("invalid one-based inclusive evidence window")
    last = len(rows) if stop is None else min(stop, len(rows))
    selected = list(enumerate(rows, 1))[start - 1:last]
    metadata = {
        "target": target, "source_id": source_id(),
        "columns": columns, "total": len(rows), "shown": len(selected),
        "window": [start, last],
        "unshown_before": min(start - 1, len(rows)),
        "unshown_after": max(0, len(rows) - max(last, start - 1)),
        "excluded": list(excluded),
        "meaning": "display only; assertions and conditions belong to caller",
    }
    print("EVIDENCE_BEGIN " + json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    for number, row in selected:
        print(f"{number:03d} " + json.dumps(row, ensure_ascii=False, sort_keys=True))
    print("EVIDENCE_END " + json.dumps({
        "target": target, "total": len(rows), "shown": len(selected),
    }, sort_keys=True))


class EvidenceToolTest(unittest.TestCase):
    def test_bounded_selection_reports_missing_ranges(self):
        import contextlib
        import io

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            emit_rows("tool-self-check", ["value"], [[1], [2], [3]], 2, 2,
                      excluded=["outside target"])
        lines = output.getvalue().splitlines()
        metadata = json.loads(lines[0].split(" ", 1)[1])
        self.assertEqual((metadata["total"], metadata["shown"]), (3, 1))
        self.assertEqual((metadata["unshown_before"], metadata["unshown_after"]), (1, 1))
        self.assertEqual(lines[1], "002 [2]")
        self.assertTrue(lines[-1].startswith("EVIDENCE_END "))
        with self.assertRaises(ValueError):
            emit_rows("invalid", [], [], 0)

    def test_inventory_all_files_and_discovered_ids(self):
        root = Path(__file__).resolve().parent.parent
        files = sorted((root / "tests").glob("*.py"))
        loader = unittest.TestLoader()
        # Use a fresh loader, and inspect without executing the discovered tests.
        suite = loader.discover(str(root / "tests"))
        ids = [case.id() for case in flatten(suite)]
        self.assertEqual(loader.errors, [])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn(self.id(), ids)
        source_files = [
            "game.py", "session.py", "play.py", "run_driver.py",
            "bots.py", "source_id.py",
        ] + [str(path.relative_to(root)) for path in files]
        print("INVENTORY_BEGIN source=" + source_id())
        print("columns: F number path; G module.class; I number method; "
              "full test ID = current G + '.' + method")
        for number, path in enumerate(files, 1):
            print(f"F {number:02d} {path.relative_to(root)}")
        group = None
        for number, test_id in enumerate(sorted(ids), 1):
            parent, method = test_id.rsplit(".", 1)
            if parent != group:
                print("G " + parent)
                group = parent
            print(f"I {number:03d} {method}")
        print("IDENTIFIED_FILES " + json.dumps(source_files))
        print(f"INVENTORY_END files={len(files)} ids={len(ids)} "
              f"shown_files={len(files)} shown_ids={len(ids)} "
              "excluded=non-Python-files; unshown=none")


if __name__ == "__main__":
    unittest.main()
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

<<<FILE goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 70
from: gameplay-engineer
to: studio
stage: Route
outcome: partial
---
# 70: gameplay-engineer → studio — E0棚卸しと対象別証拠出力道具

## Task

E0の棚卸し・暫定対応・出力道具を確認し、68に従ってE1へ進める。後続QAには下記台帳の個別ファイル本文を配布する。

## Context

69から受領したE0のみを実施した。製品で観測できる挙動の変更はない。製品ソース、bot方針、既存テストは変更していない。

60のfailは維持する。公開情報botの修正、接触診断、再測定、通常ラン入力の再生成は今回行っていない。本文供給と既知の試験不足を分離し、未確認をsuite成功でpassにしない。

## Findings

### 1. 成果と識別

変更ファイルは `repo/tests/test_g002_evidence.py` のみ。packetに「proposed in a run round; not written」として供給された全文を、そのまま最終成果として保存する。これにより収録Round 1と同じ試験道具を保持する。Handoffはsource_idの対象外である。

収録Round 1の固定コマンド：

```text
cd repo
python3 -m unittest discover -s tests
```

実行時source_idは `c12166443a05`。Exit 0、154 tests、unittest報告2.971秒、実行枠表示3.1秒。これは実装者側の確認であり独立QAではない。最終保存後の識別・実行結果はruntimeのBuild checkと照合する。過去source `04fa2b1c168a` と今回の識別を混同しない。

識別対象は次の19ファイル。F番号の13ファイルに、`game.py`、`session.py`、`play.py`、`run_driver.py`、`bots.py`、`source_id.py`を加える。source_idは相対パスと本文を順番にハッシュする。manual、設計資料、Handoff、非Pythonファイルはこの識別の対象外であり、同一性を保証しない。

### 2. 実在ファイル棚卸し

以下は予定一覧ではなく、Round 1で実在を列挙した結果。全13件表示、未表示0件。69の既存12ファイルに証拠道具1件が追加され、既存一覧との差はこの1件のみだった。

```text
FILES_BEGIN
columns: F number repo-relative-path
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_g002_evidence.py
F 08 tests/test_game.py
F 09 tests/test_play_run_controls.py
F 10 tests/test_run_driver.py
F 11 tests/test_session.py
F 12 tests/test_split_c.py
F 13 tests/test_terminal.py
FILES_END total=13 shown=13 unshown=0 excluded=non-Python-files
```

ファイル列挙の対象はsource_idと同じ `tests/*.py`。discoverはunittestの標準探索を使用する。今回discoverした全IDは次節にある。将来サブディレクトリへ試験を追加する場合、現行source_idのglob対象との差を別途解消する必要がある。今回そのような追加試験が存在するとの主張はしない。

### 3. discoverされた全テストID

列Gは `module.class`、列Iは連番とmethod。完全なテストIDは直前のGに `.` とmethodを連結したもの。以下の番号は本Handoffの対応表でも使用する。総154件、全154件表示、重複0、loader.errorsは空。FPS別subTest件数を154に加算していない。

```text
TEST_IDS_BEGIN
columns: G module.class; I number method; full-ID=G+"."+method
G test_boss.BossTest
I 001 test_boss_kill_and_existing_lethal_shot_is_death_only
I 002 test_charge_contact_keeps_full_active_duration
I 003 test_four_swipes_fit_in_recovery
I 004 test_initial_single_boss
I 005 test_lifetime_expiration_precedes_contact
I 006 test_nonlethal_swipe_preserves_warning
I 007 test_short_shot_contact_does_not_accelerate_recovery
I 008 test_wall_and_blocked_contact_keep_full_charge
I 009 test_warning_duration_and_locked_aim
G test_boss_contract.BossAdditionalContractTest
I 010 test_attack_order_survives_low_hp
I 011 test_lethal_warning_swipe_prevents_new_attack
I 012 test_nonlethal_swipe_preserves_every_phase
I 013 test_one_tile_sidestep_during_each_warning
I 014 test_zero_distance_locks_right_for_both_attacks
G test_boss_contract.BossContractTest
I 015 test_early_contact_does_not_advance_recovery
I 016 test_uncontacted_shot_expiry_coincides_with_recovery
G test_boss_contract_details.B10ContactBandTest
I 017 test_charge_inside_and_outside_the_band
I 018 test_shot_inside_and_outside_the_band
G test_boss_contract_details.B3ChargeMovementTest
I 019 test_open_charge_moves_2_4_tiles_in_0_3_s
I 020 test_wall_clamps_without_moving_recovery_start
G test_boss_contract_details.B6DashContactTest
I 021 test_dash_through_charge_is_spent_and_harmless_afterwards
I 022 test_dash_through_shot_consumes_it_and_no_later_damage
G test_boss_contract_details.B7ProtectionExpiryTest
I 023 test_charge_touched_in_protection_cannot_hit_when_it_ends
G test_boss_contract_details.B9RecoveryTest
I 024 test_recovery_contact_is_harmless
I 025 test_recovery_lengths
G test_boss_contract_details.C2PauseTest
I 026 test_pause_freezes_protection_timer
I 027 test_pause_in_warning_freezes_and_resume_continues
G test_boss_contract_details.C3LimitTest
I 028 test_limit_in_combat_is_unfinished_with_no_result
I 029 test_same_frame_death_or_victory_is_recorded_beside_the_limit
G test_boss_contract_details.TerminalTest
I 030 test_t1_clear_removes_shots_and_refuses_chasing_damage
I 031 test_t2_same_frame_death_wins_over_victory
I 032 test_t2_survivor_wins_only
I 033 test_t3_terminal_state_is_frozen
I 034 test_t4_retry_from_win_and_death_equals_a_new_run
G test_bots_boss.BossPolicyTest
I 035 test_dodger_in_the_lane_holds_or_dodges_and_never_swipes
I 036 test_dodger_off_the_lane_holds_during_the_warning
I 037 test_threat_follows_the_displayed_locked_lane
G test_bots_boss.OutcomeTest
I 038 test_log_changes_no_result_in_the_boss_room
I 039 test_start_hearts_and_outcome_fields
I 040 test_unfinished_is_reported_at_the_limit
G test_bots_boss.RunDriverTest
I 041 test_play_run_smoke
I 042 test_read_script_hearts_and_mode
G test_bots_boss.SourceIdTest
I 043 test_source_id_is_stable_hex
G test_d022_observation.ObservationTest
I 044 test_controlled_twenty_minutes_at_each_rate
I 045 test_default_player_cadence_is_explicit_half_second
I 046 test_dispatch_and_validation
I 047 test_interval_preserves_events_and_result
I 048 test_legacy_note_only_changes_leading_line
I 049 test_public_spitter_and_boss_share_sequence
I 050 test_retry_resets_periodic_schedule
I 051 test_summary_clocks_counts_pause_and_retry
I 052 test_summary_once_for_clear_death_and_limit
G test_d022_shots_and_note.LegacyNoteTest
I 053 test_note_scope_and_position
G test_d022_shots_and_note.ShotLifecycleTest
I 054 test_clear_room_sequence_and_retry
I 055 test_legacy_emission_has_no_new_events
I 056 test_player_messages_hide_ids
I 057 test_short_shot_removal_and_fixed_recovery
G test_g002_evidence.EvidenceToolTest
I 058 test_bounded_selection_reports_missing_ranges
I 059 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 060 test_bot_log_adds_state_and_changes_no_result
I 061 test_dodger_agrees_at_30_and_60_fps
I 062 test_dodger_never_swipes_a_brute_in_wind_up
I 063 test_every_bot_finishes_a_room
I 064 test_retained_criteria_14_and_15_at_each_rate
I 065 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 066 test_a_swipe_does_not_cancel_the_wind_up
I 067 test_a_swipe_in_recovery_changes_nothing_else
I 068 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 069 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 070 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 071 test_grub_lunge_costs_a_heart
I 072 test_grub_walking_alone_does_not_hurt
I 073 test_spitter_fires_every_2_4_seconds_from_1_8
I 074 test_swipe_misses_behind_the_player
I 075 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 076 test_a_cancelled_cue_is_not_a_shot
I 077 test_a_cap_delay_only_lengthens_the_gap
I 078 test_forced_simultaneous_first_shots_still_keep_the_gap
I 079 test_other_rooms_keep_the_0_8_s_offset
I 080 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 081 test_attack_during_dash_fires_when_it_ends
I 082 test_dash_covers_four_tiles_at_both_frame_rates
I 083 test_dash_has_a_cooldown
G test_game.GrubTest
I 084 test_a_sidestep_avoids_the_lunge
I 085 test_a_swipe_during_windup_stops_the_lunge
I 086 test_dash_from_cue_into_the_lunge_takes_no_damage
I 087 test_only_one_grub_winds_up_or_lunges
I 088 test_recovery_is_safe
I 089 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 090 test_rooms_match_the_spec
I 091 test_standing_still_is_punished
I 092 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 093 test_variants_swipes_to_defeat
I 094 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 095 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 096 test_late_swipe_line_comes_before_the_hit
I 097 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 098 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 099 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 100 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 101 test_a_kill_in_wind_up_prints_no_message
I 102 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 103 test_swipes_at_a_grub_or_runner_print_no_message
I 104 test_the_banner_shows_0_6
I 105 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 106 test_a_bad_rule_says_how_rules_read
I 107 test_a_rule_acts_at_most_every_reaction_time
I 108 test_cues_show_in_the_player_view
I 109 test_marks_r_and_G_are_drawn
I 110 test_rules_and_timed_inputs_mix
I 111 test_rules_ignore_what_is_not_drawn
I 112 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 113 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 114 test_a_shot_after_the_window_hits_again
I 115 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 116 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 117 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 118 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 119 test_absorbed_shot_prints_no_message
I 120 test_direction_words_at_both_rates
I 121 test_player_view_line
G test_game.SpitterTest
I 122 test_a_standing_player_is_hit_by_the_shot
I 123 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 124 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 125 test_a_shot_hit_message_is_unchanged
I 126 test_manual_has_the_new_wording
I 127 test_rears_back_rule_matches_all_variants
I 128 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 129 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 130 test_no_pause_arguments_keep_the_old_result_shape
I 131 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 132 test_retries_start_new_attempts_and_reset_reaction_memory
I 133 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 134 test_boundary_discards_input_and_accepts_entry_time
I 135 test_control_precedes_combat_input_and_resume_uses_driver_time
I 136 test_limit_exceeds_sixty_seconds
I 137 test_public_parser_dispatch
I 138 test_run_rejects_diagnostic_setup
I 139 test_same_time_source_order
I 140 test_shot_direction_message
G test_session.SessionTest
I 141 test_boundary_healing_and_clocks
I 142 test_boundary_replaces_all_combat_state
I 143 test_limit_records_result_separately
I 144 test_pause_freezes_boundary
I 145 test_pause_freezes_dash_and_queued_attack
I 146 test_retry_rejected_outside_terminal
I 147 test_terminal_retry_matches_new_run
I 148 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 149 test_boss_actual_decision_logs_and_hearts_comparisons
I 150 test_public_normal_pause_victory_retry_death_retry
I 151 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 152 test_clear_cleans_hazards_and_freezes_every_combat_field
I 153 test_death_precedes_clear_and_existing_shot_still_hits
I 154 test_player_runner_returns_after_terminal_clock_freezes
TEST_IDS_END total=154 shown=154 unshown=0 excluded=subTest-expansion
```

### 4. 暫定対応表：新仕様

全13テストファイルの本文が今回Inputsに届いたため、下表は名前だけからの推測ではなく、供給された操作・assertを読んだ暫定対応である。ただし独立判定でも、仕様の全条件充足宣言でもない。番号は§3の完全IDへ対応する。

| 基準 | 試験番号 | assert・観測と不足 |
|---|---|---|
| R1 | 150 | 公開生成入力再生で3試行、初回clear・全5部屋・ボス入場3 hearts・hurt0。旧bot生成なのでD-024では診断資料。全正規敵撃破とplayer対照列は不足 |
| R2 | 090 | 全部屋の敵種・順序・座標、新5番B/HP12をassert。共有定数の全値照合はこのassertだけでは不足 |
| R3 | 141,148 | hearts1/2/3→2/3/3、回復1回、0で死亡・遷移なし |
| R4 | 142,132,150 | 境界で列挙14フィールドのfresh一致、generation増加、bot retry時Brain生成数。弾・予兆等の残存を全て実際に仕込む試験ではなく、公開driverの境界反応記憶全項目も不足 |
| R5 | 134,139,141,150 | 境界1秒、途中dash拒否、入場同時刻move、同時入力順。入場同時刻処理の厳密な1回件数assertは不足 |
| B1 | 004,010,090 | B位置・HP・1体、HP6で各3回交互予兆。通常HPと低HPの全時間比較は別途 |
| B2 | 009,014,016 | 両warningの移動後aim固定、active到達、距離0右固定。両攻撃の発動時刻列を対象別出力する必要あり |
| B3 | 002,008,019,020 | 2.4移動、壁clamp、最後の前フレームactive・終了recovery。毎フレーム座標列なし |
| B4 | 005,007,015,016,057 | 発射直後位置/age0、速度3、寿命1、期限優先、早期接触と回復1秒不変。057で全消滅理由。実行本文の対象別表示は未整備 |
| B5 | 013 | 両攻撃、ceil(0.25*fps)で1 tile以上・0.4秒以内、aim不変、hearts3 |
| B6 | 021,022,057 | charge spent/blocked1回・無傷、shot実接触消費・後も無傷。実軌道距離と消費前後列はE2へ |
| B7 | 023,057 | charge保護終了後無傷、次charge通常被弾。shot保護吸収は057。shotの保護終了後・次弾の通常命中の連続条件は不足 |
| B8 | 006,011,012 | 全phase・両攻撃でhp以外のenemy辞書不変、warning文言イベント数、warning致死時新発動なし。致死の全phase条件は網羅していない |
| B9 | 003,024,025 | 両回復で4swipe、接触無傷、回復イベント時差。30 FPSは0.35秒を11/30へ量子化 |
| B10 | 017,018 | 内側・外側・上端のhearts。上端は(2,3)いずれも許容。実横ずれ・移動後距離列なし |
| T1 | 030,054,152 | 残弾消去・cleared1回・2秒freeze。通常部屋の全戦闘辞書比較は152 |
| T2 | 001,031,032,153 | 既発射弾と致死swipeで死亡のみ、生存なら勝利のみ、終端件数 |
| T3 | 033,152 | 2秒stepで時刻等不変、入力拒否。152は通常部屋で全辞書と敵辞書比較。033の比較は全状態ではない |
| T4 | 034,129,132,147,150 | win/dead retryのfresh辞書比較、予約破棄、Brain再生成。129は旧入力時刻5より新試行limit1が先なので未来入力破棄の十分な証明にならない |
| C1 | 141,150 | 入場room_t0、境界room_t凍結、run1秒進行、4遷移。全入場時刻列は未表示 |
| C2 | 026,027,131,135,144,145,150 | warning/保護/dash予約/clearのpause凍結とresume、driver2秒、paused入力拒否。全観測状態の対象別表示が必要 |
| C3 | 028,029,040,143 | unfinishedとoutcome分離、limit同フレームdead/won/clear保存 |
| V1 | 108,119–121,125,128,140,150 | 既存cue・印・文字列等の部分試験。ボス全イベント即時画面・重なり・終端retryの両FPS player対照は不足 |
| V2 | なし | D-021の今回テキスト範囲。実機同等性をheadlessでpassにしない |
| L1 | 048,053 | note先頭1回、現行note抑制対照、保護fixtureで60秒上限。歴史的一致は確認不能 |
| L2 | 053 | 全旧部屋・emptyと両viewでnote対象限定 |
| L3 | なし | 同一入力のlegacy/publicボス表示対照assertは未対応 |
| L4 | なし | manual本文が今回未供給。文書現行照合は未実施、歴史保証部分は確認不能 |
| S1,S2 | 049,057 | 共通連番、lifetime/edge/hit/dash/protectionの各発射1回・消滅1回・理由・回復1秒 |
| S3,S4 | 054 | 2部屋の残弾clearedとretry後S1、直後removed再発なし。勝利時全弾等の全終端ケースは不足 |
| S5 | 056,119,125 | messages_forがIDイベントを非表示、旧文言・吸収無hitの部分確認。実player全文のID非露出検査は不足 |
| O1,O6 | 044 | 生存hearts10000 fixture、両FPS・両view1200秒、周期上限、out.seen=全events。内部捕捉全文はStudio収録されず、中間画面・欠落検査も十分ではない |
| O2 | 047 | 間隔0.5/10で全events・結果・playerメッセージ列一致、trace frame/5対照 |
| O3 | 045 | 現行既定と明示0.5の全文一致。歴史的一致は確認不能 |
| O4 | 051,052 | 全終了・両view summary1回、時刻対照、pause/retry/count検査。全数値の独立再計算は部分的 |
| O5 | 046 | 範囲外/NaN/inf/非数/欠損拒否、境界値受理 |
| 道具 | 043,058,059 | source安定hex、窓選択件数・欠落数・END・不正窓拒否、全ID重複/loader errorなし |

### 5. 保持回帰・旧5番・本文未確認

| 対象 | 試験番号・本文で確認した内容 | 未対応・適用整理 |
|---|---|---|
| combat共有 | 066–075,081–088,091–095,113–118,122,124 | 攻撃、grub、dash、保護、弾等。combat.md本文未供給なのでcombat1〜10/17等への厳密な項目別完全対応は未確認 |
| combat11/18 gap | 076–080 | 4番実配置、強制同時、cue中撃破、cap遅延gap、practice offset。077はgapを検査し一般cap上限5をassertしない |
| combat19 | 066–070,101–105 | brute非中断、kill例外、回復、表示回数/時点。105はdescribe文字列のみで「表示がsimulationを変えない」全対照ではない |
| combat20/21 | 098–100,113–118 | 保護接触消費、後続攻撃、同時弾。ボスはB6/B7へ別対応 |
| combat14/15/16c | 061,064,151 | 独立1〜2walker/dodger条件、独立3/4dash、1〜4FPS損失差。151の時間比較は丸め方法未対応 |
| その他BotsTest | 060,062,063,065 | ログ有無結果一致・状態要素・hurt件数・比較距離・brute方針。063はresultにclearedキーがあることだけで終了理由・停止性を厳密には検査しない |
| step68保持文字列 | 093,094,101–105,125–128 | variantHP/時間/文言/suffix/prefix反応の現行部分。step68本文未供給のためV-a〜e全項目対応は未確定 |
| step72 R3-1 | 090 | 現行全配置。1/2/4保持、3と5は正本の適用整理に従う |
| step72 R3-2〜10 | 089,123ほか候補 | room3全敵死亡条件、初射/cue/静止最大3。正本本文未供給で番号別assert対応は未確定。grub有無のcue比較R3-6専用assertは発見できていない |
| step94 W1/W8 | 120,121,140 | 6方向のshot由来語、player例、public文字列。全8方位境界を網羅しない |
| step94 W3/W4 | 119,127ほか候補 | 吸収時hurtなし、rears back substring反応。119は実player全文での無表示をassertしない。step94本文未供給で全条件対応は未確定 |
| step94 W5/W6 | 096,097 | late swipeの順序・文字列・誤prefix禁止、windup/kill/recovery例外 |
| step94 W2/W7 | 108,123–128ほか候補 | 専用全経路対応は未確定。歴史的一致はD-024で確認不能 |
| 記録比較 | 151 | 40の8行数値を期待値として持つが、play_roomの2桁値にPython roundを適用。指定half-up/未丸め時刻の証明は不足。攻撃数は40由来とはしない |

旧5番依存の現行本文追跡：

- 090は旧brute配置を保持せず、`[("boss",12,4)]` とB/HP12をassertしている。置換先R2/B1。
- CueGapTestの実roomループは4番のみ。旧5番spitter固有の経路は現行assert集合にない。4番とpracticeの共有回帰を保持し、新5番はB2/B4・015/016/057へ置換。ただし歴史的な削除差分を検証したという意味ではない。
- 064は旧13集計を外し、14と3/4の15を保持。061のFPS比較は1〜4のみ。新5番は149だが公開情報条件未適合のため診断値。
- step94 W2の4番/practiceと新5番短射の表示置換を完全に追える専用assertは不足。後続Q6/Q4で確認する。
- 旧5番fixture維持を新しい必須条件にしない。旧集計の適用終了を共有基準の免除へ広げない。

歴史的確認不能はL1、L4保証部分、O3、step68 V-a/V-b過去時点・V-c・V-e未記録bot不変、step94 W3/W4過去全行動列・W7、および補足仕様の未記録範囲。現行内対照・記録比較と別管理する。

### 6. 証拠道具の選択・再現・確認

`emit_rows(target, columns, rows, start=1, stop=None, excluded=())` を後続試験からimportして使用する。選択は試験コード内の引数で固定する。環境変数やtrace枠の任意Python実行は前提としない。

例：

```python
from test_g002_evidence import emit_rows

# 当該試験が先に全rowsの条件・assertを評価した後で呼ぶ。
emit_rows(
    "B3/30/current/fixture",
    ["fps", "frame", "before", "after", "distance", "events"],
    evaluated_rows,
    start=1,
    stop=30,
    excluded=["60 FPS is a separate target"],
)
```

対象名には基準・FPS・証拠区分を入れ、rowsには68§2の実行条件・操作・測定本文を渡す。全集合評価は呼出側の責任で、この関数が成功判定や全判断監査を行うわけではない。source_idだけで本文を置き換えない。

出力はBEGINに列定義・source・総件数・表示件数・窓・前後未表示数・除外、各行に1始まりの元集合連番、ENDに対象・総件数・表示件数を持つ。再実行ではsource・入力・総件数を照合し、異なる結果を接合しない。BEGIN/ENDと予定連番を受信側で照合し、欠落を未確認にする。

058は3行中2番だけを捕捉し、total3/shown1、前後未表示各1、`002 [2]`、END、不正start拒否をassertした。Round 1で成功。ただし確認本文は内部捕捉され、外側にはその5行を再表示していない。

059は全ファイルと全IDを表示した。Round 1はINVENTORY_BEGINからENDまで連番001〜154が収録され、棚卸し部分の未表示はない。一方、その後のSPLIT_C_BOSSとSPLIT_C_PUBLIC付近には明示的に3665文字の切断がある。そこは未確認であり、今回のgreenや棚卸し完全性から補完しない。

道具は行数を限定するが、1行の文字数上限や自動的な1万2千字予算は持たない。後続は短い列と窓を選ぶ必要がある。既存SPLIT_C等の出力を全体として自動抑制する仕組みもない。必要な出力が固定suite内の既存印字と競合する場合は、具体的な変更対象をStudioが許可してから対応する。E0の許可外ファイルを変更していない。

今回の154件は旧152件と道具2件。追加の製品仕様試験を実装したという意味ではない。

### 7. QA配布台帳案

F番号は§2の実在パスへ展開する。全13件を少なくとも1単位へ割当済み、未割当ファイル0。追加試験は今後の各Stepで台帳へ追記する。範囲を跨ぐファイルは重複配布する。

| QA | 配布テストF番号 | 主対象 |
|---|---|---|
| Q1 | 04,07,08,09,12 | 公開情報bot、全判断、4条件、bot共有回帰 |
| Q2 | 01,02,03,06,07 | B1〜B10、弾S1〜S5 |
| Q3 | 03,07,09,10,11,12,13 | 境界、終端、retry、時刻、通常再生 |
| Q4 | 04,05,06,07,08,10 | 識別、注記、長時間、V1、文字列 |
| Q5 | 07,08 | 共有combat、cap/gap、variant、R2 |
| Q6 | 07,08,12 | step72/94、保持bot、記録比較 |

各QAの最大8件@needに頼らず、上記を最初から個別Loadする。製品・正本資料の核は68§9を併用する。Q5/Q6で正本照合後に未対応試験が判明した場合は、実装か直列継続を明記し、既存ファイル配布済みを基準充足と同一視しない。

E1用の個別Load候補は以下。いずれも実在確認済み：

- repo/game.py
- repo/session.py
- repo/play.py
- repo/run_driver.py
- repo/bots.py
- repo/source_id.py
- repo/tests/test_bots_boss.py
- repo/tests/test_split_c.py
- repo/tests/test_g002_evidence.py

これに仕様§6/8、68、60、D-019/D-024、本Handoffを加える。E1の必要本文に新たな不明ファイルはない。

### 8. 残作業・partialの理由

E0の全ID棚卸しと汎用窓出力の初版は保存した。基準対応は暫定であり、共有正本combat/step68/72/94とmanualの本文未供給部分、必要状態本文の出力、欠落検知の追加確認が残る。各基準向けの実測行を作るアダプタは未実装であり、汎用helperだけで後続証拠整備完了とはしない。

これらを既知の直列残作業としてpartialで渡す。Ownerへ供給条件の再質問は不要。StudioはE0棚卸しを採用してE1へ進め、正本の番号別完全対応は該当E4/Q5/Q6へ個別本文とともに引き継げる。E0の追加確認を先に行う場合も同Roleの継続で扱う。

E1以降では特に次を残す：

1. 公開情報境界の全分岐試験とbot修正。
2. boss突進をshot補助文から分離し、無傷接触を含む実距離・消費診断。
3. 新方針の3/2 hearts別FPS再測定、全判断列。
4. 未丸め時刻とhalf-upの記録比較、保持回帰の不足assert。
5. 通常公開入力再生成、全入場・正規敵撃破・player対照、旧未来入力破棄の十分な検証。
6. 長時間観測の開始・中間・終了本文と出力欠落検査。
7. 独立Q1〜Q6、歴史的確認不能の工程判断、Art Verify・Play・Designer判断・Review。

## Decisions already made

- D-019：旧集計を終了し、保持回帰・公開情報限定ボス比較・開始hearts別比較を維持。
- D-021：テキスト・スクリプトとStudio内独立検証で進める。
- D-022：旧経路注記、弾ライフサイクル、長時間観測契約を維持。
- D-023：個別Load、最大8件の一度の追加要求、最大3回の実行、出力最大2万字。存在しない全文保存先を要求しない。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離。
- 68：E0→E1→E2→E3群→E4群→E5群→独立QAを直列に実施。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal範囲を変更しない。今回の実装変更はF07のみ。

60のfailを上書きせず、今回の自己確認を独立QAとして扱わない。収録切断・未表示・本文未確認をpassにしない。旧bot数値と通常ラン時間は診断資料に留める。

歴史的確認不能を後続Reviewまで保持する。実機供給・変更前ビルド・全文保存機構を再要求しない。

## Open questions

- 正本combat/step68/72/94と個別assertの完全対応・未対応は、後続の個別Loadで確定する。
- 汎用helperを使った各対象の状態・判断列と出力予算は、E1以降で具体化する。
- 必要状態行が既存suite印字と競合する場合、どの既存試験出力を変更するかは具体的対象をStudioへ提示する。

E1開始を妨げる新しい仕様質問やOwnerへの質問はない。

## Expected output

Studioは実在13ファイル・154IDと配布台帳を確認してE1をルートする。必要ならE0の道具確認を同Roleへ直列継続する。

E1では公開観測専用データ・記憶・判断境界を実装し、全分岐の許可フィールド対応、内部値差に対する判断不変、履歴不足時の保守的処理、入場/retry初期化を試験する。今回E1へ着手済みとは扱わない。

後続QAへはEngineerの評価を合格根拠として渡さず、担当正本・ソース・テスト本文と再現条件を個別Loadする。新規試験が増えたらsource_idと全試験配布台帳を更新する。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (2.2 s).

```text
public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.33191144798183814, "source_id": "c12166443a05"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "c12166443a05", "trial_count_per_room_fps": 1}
..........................................................................................................................................................
----------------------------------------------------------------------
Ran 154 tests in 2.901s

OK
```

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/source_id.py
- Project: repo/tests/test_g002_evidence.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_boss_contract_details.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_terminal.py
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/69-studio-to-gameplay-engineer.md
>>>END

<<<FILE goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 71
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 71: studio → gameplay-engineer — E1公開情報bot境界と全分岐試験

## Task

68§4のE1を実施する。ボス判断を公開観測とその履歴だけに分離し、全判断分岐の許可フィールド対応、記憶、初期化、内部値差に対する判断不変を試験する。70の窓出力helperを使い、今回の確認に必要な本文を供給上限内で出す。

## Context

Goalは連続ランの最後に手応えのあるボス戦を成立させること。60のfailは維持されており、非公開active残時間を使うbot判断と証拠不足を整理してから独立QAを再開する。

70はE0のpartial。棚卸しは13ファイル・154IDで、runtimeのsuiteはsource c12166443a05、154件OK。これは独立QAでも全基準充足でもない。新たな入力不足は報告されていないため、同Roleの直列継続としてE1へ進む。

## Findings

68§2・4を今回の作業・証拠契約とする。E2の突進診断、E3の4条件測定、E4の保持回帰・記録比較、E5の通常ラン再生成には今回着手しない。

E1の要件：

- ボス専用観測データと判断処理を分離し、判断処理へ内部Game／Enemyを渡さない。
- 全入力フィールドをplayer表示または既存公開観測へ対応付ける。共有補助関数から未表示値へ戻る経路も調べる。
- active残時間、struck等を判断へ渡さない。ログ専用内部観測は判断後の別経路に置く。
- warningで見えた固定経路を記憶し、active中は全経路を保守的に扱う。recovery等の公開変化で解除する。
- warning履歴なしのactive開始では固定最大範囲を保守的に扱い、履歴不足を記録する。表示追加はしない。
- 判断番号、反応grid・時刻、公開入力、記憶由来、候補・除外理由、選択・発行ボタンを記録する。stunによる判断省略も記録する。

70の残作業を次のように引き継ぐ：

- 今回：E1用の状態・判断出力アダプタ、helperの窓・欠落表示の確認本文、公開境界の全分岐試験。
- E2以降：実接触・消費診断、4条件再測定、保持回帰、未丸め時刻とhalf-up比較、公開入力再生成、長時間観測の不足。
- E4/Q5/Q6：combat/step68/72/94本文との番号別完全対応。70の暫定表を完全対応としない。

後続QAの配布台帳は70§7を基礎として固定する：

| 単位 | 個別テストファイル |
|---|---|
| Q1 | test_bots_boss.py, test_g002_evidence.py, test_game.py, test_play_run_controls.py, test_split_c.py |
| Q2 | test_boss.py, test_boss_contract.py, test_boss_contract_details.py, test_d022_shots_and_note.py, test_g002_evidence.py |
| Q3 | test_boss_contract_details.py, test_g002_evidence.py, test_play_run_controls.py, test_run_driver.py, test_session.py, test_split_c.py, test_terminal.py |
| Q4 | test_bots_boss.py, test_d022_observation.py, test_d022_shots_and_note.py, test_g002_evidence.py, test_game.py, test_run_driver.py |
| Q5 | test_g002_evidence.py, test_game.py |
| Q6 | test_g002_evidence.py, test_game.py, test_split_c.py |

全パスはrepo/tests/配下。既存13ファイルの未割当は0。追加試験は担当単位へ追記し、配布済みと基準充足を区別する。

## Decisions already made

- D-019：公開情報限定ボス方針、反応間隔0.15秒、開始3/2 hearts別FPS比較、保持回帰を要求。
- D-021：テキスト・スクリプトとStudio内独立検証で進める。
- D-022：表示・弾・長時間観測契約を保持。
- D-023：個別Load、@need一度最大8件、@run最大3回、各出力最大2万字。全文保存先・変更前ビルドなし。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離。
- 68：E0→E1→E2→E3群→E4群→E5群→独立QAを直列実行。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal範囲、表示契約を変更しない。

書込対象はrepo/bots.py、repo/tests/test_bots_boss.py、repo/tests/test_split_c.py、repo/tests/test_g002_evidence.py。test_split_c.pyの変更はE1の境界接続・試験互換・対象別出力に必要な範囲とし、E3〜E5の測定対応は先取りしない。既存印字の変更は、この4ファイル内で証拠切断を避ける対象選択・抑制に必要な範囲を許可する。assertや検証対象を減らして成功させない。他ファイルの変更が不可欠なら具体的理由と対象を返す。

独立1〜4の方針を保持し、共有関数への変更影響を報告する。game.py、session.py、play.py、run_driver.pyは照合対象であり変更しない。

固定コマンドはrepo/で `python3 -m unittest discover -s tests`。最大3回を公開境界不変、記憶・境界条件、suite・不足確認へ配分する。既存出力も含め予算を見積もる。必要なら同Roleのpartial継続に分割する。

出力は概ね1万2千字以内を目指し、対象開始・終了、列定義、連番、総件数・表示件数・未表示・除外を明示する。欠落・切断は未確認。source_idや成功件数だけで必要な状態・判断本文を置き換えない。

## Open questions

- 全ボス判断と共有補助関数の参照が、どの公開フィールド・履歴に対応するか。
- 許可外属性を持たない入力と、同じ公開入力で異なる内部状態を与えた試験で判断不変を示せるか。
- warning→active→recovery、距離0、壁、dash待ち、stun、入場・retry初期化をどう検査したか。
- E1後の追加試験、出力不足、共有回帰への影響は何か。

## Expected output

studio宛Handoffに、変更ファイル、公開フィールド対応表、全判断経路の監査範囲、試験IDとassert、状態・判断の表示証拠、コマンド、source_id、識別対象、未表示範囲を記録する。実装者の自己評価・理由・自試験結果はSender assessmentにまとめる。

全テスト一覧・件数の変更とQA配布台帳への追記を示す。70の未対応事項を消さず、今回解消分と後続担当を分ける。今回の結果をボス4条件の測定済み・独立QA合格とはしない。

残りが既知の作業ならpartialで同Roleへ継続し、同じ供給条件をOwnerへ再質問しない。E1完了後の次工程はE2だが、Studioが結果を確認して別Handoffで開く。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_g002_evidence.py
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
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

<<<FILE goals/G-002-final-boss/72-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 72
from: gameplay-engineer
to: studio
stage: Build
outcome: partial
---
# 72: gameplay-engineer → studio — E1公開境界prototype保存、実経路接続は継続

## Task

同Roleの直列継続でE1を完了する。公開境界prototypeを実dodgerへ接続し、記憶の寿命、全判断ログ、全分岐試験と表示証拠を揃える。E2はまだ開かない。

## Context

71と68§4を受領した。今回保存するのは公開観測・純粋判断のprototypeと3試験であり、実際のボスbot修正完了ではない。60のfailを維持する。新しい仕様質問や供給不足はない。

## Findings

### 保存変更と挙動

変更はrepo/bots.py、repo/tests/test_bots_boss.pyのみ。packetの未保存prototypeを基に、独立したBossObservation、BossMemory、BossChoice、observe_boss、choose_bossと3試験を保存する。

プレイヤー表示、戦闘、実dodger、camper、walker、独立1〜4の実行方針は変更していない。prototypeは未接続で、判断候補の実用性や攻略可能性も未検証である。ゲーム仕様の新しい挙動を追加しない。

### 公開フィールド対応

| 入力 | 根拠 | 制限 |
|---|---|---|
| t | 公開driverのroom time | 判断履歴の出典時刻 |
| x,y,boss_x,boss_y | play.spritesと既存公開Viewの位置観測 | 文字セルだけから連続座標を復元した証明ではない |
| phase,attack | Output.emitのboss status、next | HPは生存対象の選択だけに使用 |
| aim,warning_left | warningのlocked方向、残時間 | warning以外はNone。activeの値は読み取らない |
| shots | 公開spriteの弾位置 | velocity、age、ID、source、lifetimeなし |
| memory.lane,attack,warning_time | 過去warning観測 | active中は全固定経路を保持。recovery/approachで解除 |

固定危険幅、射程、盤面寸法、方向は仕様値・既存定数を使う。0.3 tileの余裕、弾近傍1.1 tile、移動先1.5 tile、接近閾値1.1 tileはprototypeの方針値であり製品パラメータではない。

### 監査範囲と未解消経路

choose_bossは観測と記憶だけを受け、Game/Enemyやpressを受け取らない。参照補助はmath.hypot、_toward、DIRECTIONS、ROOM_W/Hのみで、内部状態へ戻らない。warningから固定経路を作り、activeでは短縮しない。履歴不足はmissing-warning-historyを返し、最大半径で扱う。候補、壁除外、選択、予定ボタンをBossChoiceに返す。

ただし実dodgerは従来経路のままである。_dangersのactive phase_left参照、_threat、_escape、_face_and_swing等を通る旧判断は未修正。新境界の不変試験は旧経路の不適合を解消しない。

prototypeにはdash判断がなく、warning残時間も保持するだけで選択には使わない。stun省略、判断番号/grid、発行済みボタン、入場/retry初期化との接続はない。候補の全件列挙ではなく、最初に採択した候補で返る。これらを全分岐監査済みとしない。

### 試験追加

追加IDは以下の3件。既存試験のassert・対象は削減していない。

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary：
  両攻撃でactive残時間0.001/99、struck/spent、非表示aimを変えても観測と選択が一致。activeのaim/warning_leftはNone。
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery：
  chargeのwarning履歴保持、activeの全経路判断、recovery解除、履歴なしactiveの不足表示をassert。
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches：
  slots入力、approach/swipe/hold/escape、距離0、下壁除外と上移動、近傍弾をassert。

不足は両FPSの実経路、短射の遷移全条件、左右・上壁、端点、距離境界、dash待ち、stun、入場/retry、警告履歴なし範囲の全方向、許可外属性を読むと失敗するadapter fixture、全選択分岐ごとの内部値不変である。slotsだけで全呼出経路の許可外参照禁止を証明しない。

### 収録実行と識別

packetのRound 1は、未保存prototypeを使った固定コマンド
`python3 -m unittest discover -s tests`、Exit 0、157 tests、source_id 5c62a1c7e18eを報告している。

今回保存したprototypeはコメント等も整理しているため、このsource_idを最終保存集合の識別として流用しない。最終集合の識別とsuite結果はruntime Build checkで照合する。識別対象は6ソースとtests/*.pyの13ファイル、計19ファイル。設計資料とHandoffは対象外。

Round 1の棚卸しは13ファイル・157IDを全表示しENDあり。旧154から上記3件増加。SPLIT_C出力は3865文字切断されており、切断部分は未確認。表示された旧実dodgerのボス成績もE3の新測定ではない。

状態・判断本文のemit_rowsアダプタ、窓helperの外側への確認本文再表示は未実装。今回その本文を収録したとの主張はしない。repo/tests/test_g002_evidence.pyとtest_split_c.pyは変更していない。

### 継続手順と配布台帳

次のE1継続では実装前に境界接続の失敗試験を追加し、実dodgerが内部Gameを純粋判断へ渡さないことを検査する。Brain等に記憶を所有させ、部屋入場・retryで初期化する。直接dodger呼出と通常run、_Proxyによる入力捕捉の互換も試験する。

判断番号、grid、時刻、公開入力、記憶出典、候補・除外、選択・発行ボタン、stun省略を出す。内部ログ観測は選択後に別経路で取得する。既存印字はassertを保ったまま対象別に抑制し、概ね12000字以内でemit_rowsのBEGIN/ENDと欠落範囲を確認する。

追加3IDは既存F04内であり、新ファイルは0。71の台帳に従いQ1とQ4へ更新本文を配布する。Q1が公開境界の主担当。13ファイルの未割当0は維持するが、配布済みは基準充足を意味しない。70の番号は追加によりずれるため、対応は完全IDで追跡する。

70の未解決事項は保持する。E2接触診断、E3四条件、E4未丸め/half-upと共有正本の完全対応、E5公開再生再生成、長時間観測、独立QA以降には着手していない。D-024の歴史的確認不能一覧も解消していない。

### Sender assessment

prototypeの境界形状と限定した不変assertは準備できたが、実判断経路は旧実装でありE1未完了と評価する。収録157件成功はこの限定的な自己確認であり、独立QA、公開情報限定botの完成、ボス四条件測定、Goal達成の証拠ではない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較を維持。
- D-021/D-023：Studio内テキスト検証と供給上限内の直列継続。
- D-022：表示・弾・長時間観測契約は変更しない。
- D-024：現行検証、記録比較、歴史的確認不能を分離。
- 68：E1完了後、Studioが別HandoffでE2を開く。

## Constraints

製品仕様、難度、戦闘パラメータ、表示、秒数ゲート、Goal範囲を変更しない。実装者の自己確認で60のfailを上書きしない。未表示や切断をpassにしない。実機、変更前ビルド、全文保存先を再要求しない。

## Open questions

新しい仕様質問はない。残作業は既知のE1実装・試験・表示であり、同Roleへ継続する。

## Expected output

StudioはE1 partialとして同Roleの直列継続をルートする。実経路接続、全判断分岐の公開対応、記憶初期化、内部差不変、必要本文と最終source識別を揃えてからE1完了を確認する。E2〜E5および独立QAの完了とは区別する。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.1 s).

```text
ublic-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.332541857031174, "source_id": "8fe9bcc21225"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "8fe9bcc21225", "trial_count_per_room_fps": 1}
.............................................................................................................................................................
----------------------------------------------------------------------
Ran 157 tests in 2.963s

OK
```

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
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
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting handoff: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
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

<<<FILE repo/bots.py (proposed in a run round; not written)
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
from dataclasses import dataclass

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


def _legacy_dodger(game, note):
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


@dataclass(frozen=True, slots=True)
class BossObservation:
    """Public sprites, boss status and room clock; no internal object references."""
    t: float
    x: float
    y: float
    boss_x: float
    boss_y: float
    phase: str
    attack: str
    aim: tuple | None
    warning_left: float | None
    shots: tuple


@dataclass(frozen=True, slots=True)
class BossMemory:
    lane: tuple | None = None
    attack: str | None = None
    warning_time: float | None = None


@dataclass(frozen=True, slots=True)
class BossChoice:
    memory: BossMemory
    provenance: str
    candidates: tuple
    excluded: tuple
    selected: str
    buttons: tuple


def observe_boss(game):
    """Read adapter; active aim, timer and contact flags never cross the boundary."""
    boss = next((e for e in game.enemies
                 if e.kind == "boss" and e.hp > 0), None)
    if boss is None:
        return None
    warning = boss.phase == "warning"
    return BossObservation(
        game.t, game.x, game.y, boss.x, boss.y, boss.phase,
        boss.attack_name, tuple(boss.aim) if warning and boss.aim else None,
        boss.phase_left if warning else None,
        tuple((s[0], s[1]) for s in game.shots),
    )


def choose_boss(observation, memory):
    """Pure decision for the boss dodger; accepts only observation and memory.

    Retain the complete warning lane throughout active. Without warning
    history, use a maximum radial envelope rather than an undisplayed aim.
    """
    o = observation
    candidates, excluded = [], []
    provenance = "none"
    if o.phase == "warning" and o.aim is not None:
        length = 2.4 if o.attack == "charge" else 3.0
        memory = BossMemory(
            (o.boss_x, o.boss_y, *o.aim, length), o.attack, o.t,
        )
        provenance = "warning"
    elif o.phase == "active":
        if memory.lane is not None and memory.attack == o.attack:
            provenance = "warning-history"
        else:
            memory = BossMemory()
            provenance = "missing-warning-history"
    else:
        memory = BossMemory()

    dangerous = False
    if o.phase in ("warning", "active"):
        if memory.lane is not None:
            ox, oy, ux, uy, length = memory.lane
            along = max(0.0, min(length,
                                (o.x - ox) * ux + (o.y - oy) * uy))
            radius = 0.6 if o.attack == "charge" else 0.4
            dangerous = math.hypot(
                o.x - ox - along * ux, o.y - oy - along * uy,
            ) <= radius + 0.6
        else:
            radius = 3.0 if o.attack == "charge" else 3.4
            dangerous = math.hypot(
                o.x - o.boss_x, o.y - o.boss_y,
            ) <= radius + 0.3
        excluded.append(("attack", "warning-or-active"))

    dangerous = dangerous or any(
        math.hypot(o.x - x, o.y - y) <= 1.1 for x, y in o.shots
    )
    if dangerous:
        if memory.lane is not None:
            _, _, ux, uy, _ = memory.lane
            preferred = ("down", "up") if abs(ux) >= abs(uy) else ("right", "left")
        else:
            preferred = ("up", "down", "left", "right")
        selected_direction = None
        for direction in preferred:
            dx, dy = DIRECTIONS[direction]
            inside = (0 <= o.x + dx * 1.5 <= ROOM_W - 1
                      and 0 <= o.y + dy * 1.5 <= ROOM_H - 1)
            candidates.append(("move", direction, inside))
            if not inside:
                excluded.append((direction, "wall"))
            elif selected_direction is None:
                selected_direction = direction
            else:
                excluded.append((direction, "lower-priority"))
        if selected_direction is not None:
            return BossChoice(memory, provenance, tuple(candidates),
                              tuple(excluded), "escape",
                              (("move", selected_direction),))
        return BossChoice(memory, provenance, tuple(candidates),
                          tuple(excluded), "hold", (("stop", None),))
    if o.phase in ("warning", "active"):
        return BossChoice(memory, provenance, (("hold",),),
                          tuple(excluded), "hold", (("stop", None),))
    dx, dy = o.boss_x - o.x, o.boss_y - o.y
    if math.hypot(dx, dy) > 1.1:
        return BossChoice(memory, provenance, (("approach",),), (),
                          "approach", (("move", _toward(dx, dy)),))
    # Input authority enforces attack recovery; no internal recovery is read.
    return BossChoice(memory, provenance, (("swipe",),), (), "swipe",
                      (("move", _toward(dx, dy)), ("stop", None),
                       ("attack", None)))


def dodger(game, note):
    """Choose boss actions before entering any legacy combat helper.

    The current room owns the memory. Room replacement and retry therefore
    discard it, including for direct calls and the session input proxy.
    """
    observation = observe_boss(game)
    if observation is None:
        return _legacy_dodger(game, note)
    memory = getattr(game, "_boss_memory", BossMemory())
    choice = choose_boss(observation, memory)
    game._boss_memory = choice.memory
    issued = []
    for action, direction in choice.buttons:
        game.press(action, direction)
        issued.append((action, direction))
    label = {
        "approach": "walk to boss",
        "swipe": "face and swing at boss",
        "hold": "hold off the boss's locked " + observation.attack + " line",
        "escape": "escape from " + observation.attack,
    }[choice.selected]
    # Diagnostic acquisition through note happens after action selection.
    note(label + " | public " + repr({
        "input": observation,
        "memory_before": memory,
        "memory_after": choice.memory,
        "provenance": choice.provenance,
        "candidates": choice.candidates,
        "excluded": choice.excluded,
        "selected": choice.selected,
        "issued": tuple(issued),
    }))


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

    @property
    def _boss_memory(self):
        return getattr(self._s.game, "_boss_memory", BossMemory())

    @_boss_memory.setter
    def _boss_memory(self, value):
        self._s.game._boss_memory = value

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

<<<FILE repo/tests/test_bots_boss.py (proposed in a run round; not written)
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


class PublicBoundaryPrototypeTest(unittest.TestCase):
    def test_active_internal_values_do_not_cross_boundary(self):
        from dataclasses import fields
        names = {field.name for field in fields(bots.BossObservation)}
        self.assertFalse(names & {"phase_left", "struck", "spent", "game", "enemy"})
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            warning = bots.observe_boss(game)
            remembered = bots.choose_boss(warning, bots.BossMemory()).memory
            boss = game.enemies[0]
            boss.phase = "active"
            observations, choices = [], []
            for left, struck, spent, aim in (
                (0.001, False, False, (-1, 0)),
                (99.0, True, True, (0, 1)),
            ):
                boss.phase_left, boss.struck, boss.spent = left, struck, spent
                boss.aim = aim
                observation = bots.observe_boss(game)
                observations.append(observation)
                choices.append(bots.choose_boss(observation, remembered))
                self.assertIsNone(observation.aim)
                self.assertIsNone(observation.warning_left)
            self.assertEqual(observations[0], observations[1])
            self.assertEqual(choices[0], choices[1])

    def test_warning_memory_active_and_recovery(self):
        from dataclasses import replace
        game = boss_warning("charge", (8, 4))
        warning = bots.observe_boss(game)
        first = bots.choose_boss(warning, bots.BossMemory())
        active = replace(warning, phase="active", aim=None, warning_left=None,
                         boss_x=8.5)
        second = bots.choose_boss(active, first.memory)
        self.assertEqual(second.memory, first.memory)
        self.assertEqual(second.provenance, "warning-history")
        self.assertEqual(second.selected, "escape")
        recovery = bots.choose_boss(replace(active, phase="recovery"), second.memory)
        self.assertEqual(recovery.memory, bots.BossMemory())
        missing = bots.choose_boss(active, bots.BossMemory())
        self.assertEqual(missing.provenance, "missing-warning-history")
        self.assertEqual(missing.selected, "escape")

    def test_slots_only_input_and_visible_branches(self):
        from dataclasses import replace
        o = bots.BossObservation(0, 8, 4, 10, 4, "recovery",
                                 "charge", None, None, ())
        self.assertFalse(hasattr(o, "__dict__"))
        self.assertEqual(bots.choose_boss(o, bots.BossMemory()).selected, "approach")
        close = replace(o, boss_x=8)
        self.assertEqual(bots.choose_boss(close, bots.BossMemory()).selected, "swipe")
        warning = replace(o, phase="warning", aim=(-1, 0), warning_left=0.5)
        off = replace(warning, y=7)
        self.assertEqual(bots.choose_boss(off, bots.BossMemory()).selected, "hold")
        wall = replace(warning, y=8, boss_y=8)
        choice = bots.choose_boss(wall, bots.BossMemory())
        self.assertIn(("down", "wall"), choice.excluded)
        self.assertEqual(choice.buttons, (("move", "up"),))
        shot = replace(o, shots=((8, 4),))
        self.assertEqual(bots.choose_boss(shot, bots.BossMemory()).selected, "escape")


class PublicBoundaryConnectionTest(unittest.TestCase):
    def test_actual_dodger_bypasses_legacy_helpers(self):
        from unittest import mock
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                game = boss_warning(attack, (8, 4))
                notes = []
                with mock.patch.object(bots, "_legacy_dodger",
                                       side_effect=AssertionError("legacy read")), \
                     mock.patch.object(bots, "_threat",
                                       side_effect=AssertionError("threat read")), \
                     mock.patch.object(bots, "_escape",
                                       side_effect=AssertionError("escape read")), \
                     mock.patch.object(bots, "_face_and_swing",
                                       side_effect=AssertionError("swing read")):
                    game.fps, game.dt = fps, 1 / fps
                    bots.dodger(game, notes.append)
                    lane = game._boss_memory
                    boss = game.enemies[0]
                    boss.phase = "active"
                    outputs = []
                    for left, aim, struck in ((0.001, (1, 0), False),
                                              (99, (0, 1), True)):
                        boss.phase_left, boss.aim = left, aim
                        boss.struck = boss.spent = struck
                        game._boss_memory = lane
                        game.events.clear()
                        game.heading = (0, 0)
                        bots.dodger(game, notes.append)
                        outputs.append((game.heading, list(game.events),
                                        game._boss_memory, notes[-1]))
                    self.assertEqual(outputs[0], outputs[1])
                    self.assertEqual(game._boss_memory, lane)
                    boss.phase = "recovery"
                    bots.dodger(game, notes.append)
                    self.assertEqual(game._boss_memory, bots.BossMemory())

    def test_proxy_memory_is_owned_by_current_room(self):
        from session import RunSession
        session = RunSession()
        proxy = bots._Proxy(session)
        remembered = bots.BossMemory((10, 4, -1, 0, 2.4),
                                     "charge", 0.0)
        proxy._boss_memory = remembered
        self.assertEqual(session.game._boss_memory, remembered)
        session._enter("5", 3)
        self.assertEqual(proxy._boss_memory, bots.BossMemory())
        session.state = "dead"
        proxy._boss_memory = remembered
        self.assertTrue(session.control("retry"))
        self.assertEqual(proxy._boss_memory, bots.BossMemory())

    def test_all_escape_candidates_are_enumerated(self):
        game = boss_warning("charge", (8, 4))
        choice = bots.choose_boss(bots.observe_boss(game), bots.BossMemory())
        self.assertEqual(choice.candidates,
                         (("move", "down", True), ("move", "up", True)))
        self.assertIn(("up", "lower-priority"), choice.excluded)

    def test_active_adapter_rejects_forbidden_attribute_reads(self):
        from unittest import mock

        class Guard:
            def __init__(self, values):
                object.__setattr__(self, "values", values)

            def __getattr__(self, name):
                values = object.__getattribute__(self, "values")
                if name not in values:
                    raise AssertionError("forbidden read: " + name)
                return values[name]

        for attack in ("charge", "short shot"):
            for phase in ("approach", "warning", "active", "recovery"):
                enemy_values = {
                    "kind": "boss", "hp": 12, "x": 10, "y": 4,
                    "phase": phase, "attack_name": attack,
                }
                if phase == "warning":
                    enemy_values.update(aim=(-1, 0), phase_left=0.5)
                pressed = []
                game = Guard({
                    "t": 0, "x": 8, "y": 4,
                    "enemies": [Guard(enemy_values)], "shots": [],
                    "_boss_memory": bots.BossMemory(),
                    "press": lambda a, d=None: pressed.append((a, d)),
                })
                with mock.patch.object(
                        bots, "_legacy_dodger",
                        side_effect=AssertionError("legacy path")):
                    bots.dodger(game, lambda text: None)
                self.assertTrue(pressed, (attack, phase))


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

<<<FILE @run-results
### Round 1: @run/tests/public-boundary-connection — `python3 -m unittest discover -s tests`

Exit: 1 (2.1 s). Output:

```text
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=eddd95dd5926
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=eddd95dd5926
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=eddd95dd5926
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=eddd95dd5926
INVENTORY_BEGIN source=eddd95dd5926
columns: F number path; G module.class; I number method; full test ID = current G + '.' + method
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_g002_evidence.py
F 08 tests/test_game.py
F 09 tests/test_play_run_controls.py
F 10 tests/test_run_driver.py
F 11 tests/test_session.py
F 12 tests/test_split_c.py
F 13 tests/test_terminal.py
G test_boss.BossTest
I 001 test_boss_kill_and_existing_lethal_shot_is_death_only
I 002 test_charge_contact_keeps_full_active_duration
I 003 test_four_swipes_fit_in_recovery
I 004 test_initial_single_boss
I 005 test_lifetime_expiration_precedes_contact
I 006 test_nonlethal_swipe_preserves_warning
I 007 test_short_shot_contact_does_not_accelerate_recovery
I 008 test_wall_and_blocked_contact_keep_full_charge
I 009 test_warning_duration_and_locked_aim
G test_boss_contract.BossAdditionalContractTest
I 010 test_attack_order_survives_low_hp
I 011 test_lethal_warning_swipe_prevents_new_attack
I 012 test_nonlethal_swipe_preserves_every_phase
I 013 test_one_tile_sidestep_during_each_warning
I 014 test_zero_distance_locks_right_for_both_attacks
G test_boss_contract.BossContractTest
I 015 test_early_contact_does_not_advance_recovery
I 016 test_uncontacted_shot_expiry_coincides_with_recovery
G test_boss_contract_details.B10ContactBandTest
I 017 test_charge_inside_and_outside_the_band
I 018 test_shot_inside_and_outside_the_band
G test_boss_contract_details.B3ChargeMovementTest
I 019 test_open_charge_moves_2_4_tiles_in_0_3_s
I 020 test_wall_clamps_without_moving_recovery_start
G test_boss_contract_details.B6DashContactTest
I 021 test_dash_through_charge_is_spent_and_harmless_afterwards
I 022 test_dash_through_shot_consumes_it_and_no_later_damage
G test_boss_contract_details.B7ProtectionExpiryTest
I 023 test_charge_touched_in_protection_cannot_hit_when_it_ends
G test_boss_contract_details.B9RecoveryTest
I 024 test_recovery_contact_is_harmless
I 025 test_recovery_lengths
G test_boss_contract_details.C2PauseTest
I 026 test_pause_freezes_protection_timer
I 027 test_pause_in_warning_freezes_and_resume_continues
G test_boss_contract_details.C3LimitTest
I 028 test_limit_in_combat_is_unfinished_with_no_result
I 029 test_same_frame_death_or_victory_is_recorded_beside_the_limit
G test_boss_contract_details.TerminalTest
I 030 test_t1_clear_removes_shots_and_refuses_chasing_damage
I 031 test_t2_same_frame_death_wins_over_victory
I 032 test_t2_survivor_wins_only
I 033 test_t3_terminal_state_is_frozen
I 034 test_t4_retry_from_win_and_death_equals_a_new_run
G test_bots_boss.BossPolicyTest
I 035 test_dodger_in_the_lane_holds_or_dodges_and_never_swipes
I 036 test_dodger_off_the_lane_holds_during_the_warning
I 037 test_threat_follows_the_displayed_locked_lane
G test_bots_boss.OutcomeTest
I 038 test_log_changes_no_result_in_the_boss_room
I 039 test_start_hearts_and_outcome_fields
I 040 test_unfinished_is_reported_at_the_limit
G test_bots_boss.PublicBoundaryConnectionTest
I 041 test_actual_dodger_bypasses_legacy_helpers
I 042 test_all_escape_candidates_are_enumerated
I 043 test_proxy_memory_is_owned_by_current_room
G test_bots_boss.PublicBoundaryPrototypeTest
I 044 test_active_internal_values_do_not_cross_boundary
I 045 test_slots_only_input_and_visible_branches
I 046 test_warning_memory_active_and_recovery
G test_bots_boss.RunDriverTest
I 047 test_play_run_smoke
I 048 test_read_script_hearts_and_mode
G test_bots_boss.SourceIdTest
I 049 test_source_id_is_stable_hex
G test_d022_observation.ObservationTest
I 050 test_controlled_twenty_minutes_at_each_rate
I 051 test_default_player_cadence_is_explicit_half_second
I 052 test_dispatch_and_validation
I 053 test_interval_preserves_events_and_result
I 054 test_legacy_note_only_changes_leading_line
I 055 test_public_spitter_and_boss_share_sequence
I 056 test_retry_resets_periodic_schedule
I 057 test_summary_clocks_counts_pause_and_retry
I 058 test_summary_once_for_clear_death_and_limit
G test_d022_shots_and_note.LegacyNoteTest
I 059 test_note_scope_and_position
G test_d022_shots_and_note.ShotLifecycleTest
I 060 test_clear_room_sequence_and_retry
I 061 test_legacy_emission_has_no_new_events
I 062 test_player_messages_hide_ids
I 063 test_short_shot_removal_and_fixed_recovery
G test_g002_evidence.EvidenceToolTest
I 064 test_bounded_selection_reports_missing_ranges
I 065 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 066 test_bot_log_adds_state_and_changes_no_result
I 067 test_dodger_agrees_at_30_and_60_fps
I 068 test_dodger_never_swipes_a_brute_in_wind_up
I 069 test_every_bot_finishes_a_room
I 070 test_retained_criteria_14_and_15_at_each_rate
I 071 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 072 test_a_swipe_does_not_cancel_the_wind_up
I 073 test_a_swipe_in_recovery_changes_nothing_else
I 074 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 075 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 076 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 077 test_grub_lunge_costs_a_heart
I 078 test_grub_walking_alone_does_not_hurt
I 079 test_spitter_fires_every_2_4_seconds_from_1_8
I 080 test_swipe_misses_behind_the_player
I 081 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 082 test_a_cancelled_cue_is_not_a_shot
I 083 test_a_cap_delay_only_lengthens_the_gap
I 084 test_forced_simultaneous_first_shots_still_keep_the_gap
I 085 test_other_rooms_keep_the_0_8_s_offset
I 086 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 087 test_attack_during_dash_fires_when_it_ends
I 088 test_dash_covers_four_tiles_at_both_frame_rates
I 089 test_dash_has_a_cooldown
G test_game.GrubTest
I 090 test_a_sidestep_avoids_the_lunge
I 091 test_a_swipe_during_windup_stops_the_lunge
I 092 test_dash_from_cue_into_the_lunge_takes_no_damage
I 093 test_only_one_grub_winds_up_or_lunges
I 094 test_recovery_is_safe
I 095 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 096 test_rooms_match_the_spec
I 097 test_standing_still_is_punished
I 098 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 099 test_variants_swipes_to_defeat
I 100 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 101 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 102 test_late_swipe_line_comes_before_the_hit
I 103 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 104 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 105 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 106 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 107 test_a_kill_in_wind_up_prints_no_message
I 108 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 109 test_swipes_at_a_grub_or_runner_print_no_message
I 110 test_the_banner_shows_0_6
I 111 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 112 test_a_bad_rule_says_how_rules_read
I 113 test_a_rule_acts_at_most_every_reaction_time
I 114 test_cues_show_in_the_player_view
I 115 test_marks_r_and_G_are_drawn
I 116 test_rules_and_timed_inputs_mix
I 117 test_rules_ignore_what_is_not_drawn
I 118 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 119 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 120 test_a_shot_after_the_window_hits_again
I 121 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 122 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 123 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 124 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 125 test_absorbed_shot_prints_no_message
I 126 test_direction_words_at_both_rates
I 127 test_player_view_line
G test_game.SpitterTest
I 128 test_a_standing_player_is_hit_by_the_shot
I 129 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 130 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 131 test_a_shot_hit_message_is_unchanged
I 132 test_manual_has_the_new_wording
I 133 test_rears_back_rule_matches_all_variants
I 134 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 135 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 136 test_no_pause_arguments_keep_the_old_result_shape
I 137 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 138 test_retries_start_new_attempts_and_reset_reaction_memory
I 139 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 140 test_boundary_discards_input_and_accepts_entry_time
I 141 test_control_precedes_combat_input_and_resume_uses_driver_time
I 142 test_limit_exceeds_sixty_seconds
I 143 test_public_parser_dispatch
I 144 test_run_rejects_diagnostic_setup
I 145 test_same_time_source_order
I 146 test_shot_direction_message
G test_session.SessionTest
I 147 test_boundary_healing_and_clocks
I 148 test_boundary_replaces_all_combat_state
I 149 test_limit_records_result_separately
I 150 test_pause_freezes_boundary
I 151 test_pause_freezes_dash_and_queued_attack
I 152 test_retry_rejected_outside_terminal
I 153 test_terminal_retry_matches_new_run
I 154 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 155 test_boss_actual_decision_logs_and_hearts_comparisons
I 156 test_public_normal_pause_victory_retry_death_retry
I 157 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 158 test_clear_cleans_hazards_and_freezes_every_combat_field
I 159 test_death_precedes_clear_and_existing_shot_still_hits
I 160 test_player_runner_returns_after_terminal_clock_freezes
IDENTIFIED_FILES ["game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py", "tests/test_boss.py", "tests/test_boss_contract.py", "tests/test_boss_contract_details.py", "tests/test_bots_boss.py", "tests/test_d022_observation.py", "tests/test_d022_shots_and_note.py", "tests/test_g002_evidence.py", "tests/test_game.py", "tests/test_play_run_controls.py", "tests/test_run_driver.py", "tests/test_session.py", "tests/test_split_c.py", "tests/test_terminal.py"]
INVENTORY_END files=13 ids=160 shown_files=13 shown_ids=160 excluded=non-Python-files; unshown=none
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 0, "decision_count": 75, "decision_samples": ["  0.00 s  walk to boss | public {'input': BossObservation(t=0.0, x=8.0, y=4.0, boss_x=12.0, boss_y=4.0, phase='approach', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('approach',),), 'excluded': (), 'selected': 'approach', 'issued': (('move', 'right'),)} | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", null, "  2.70 s  escape from short shot | public {'input': BossObservation(t=2.7, x=9.86666666666666, y=4.533333333333335, boss_x=9.199999999999994, boss_y=4.0, phase='warning', attack='short shot', aim=(0.780868809443029, 0.6246950475544257), warning_left=0.7666666666666667, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=(9.199999999999994, 4.0, 0.780868809443029, 0.6246950475544257, 3.0), attack='short shot', warning_time=2.7), 'provenance': 'warning', 'candidates': (('move', 'down', True), ('move', 'up', True)), 'excluded': (('attack', 'warning-or-active'), ('up', 'lower-priority')), 'selected': 'escape', 'issued': (('move', 'down'),)} | frame 81, grid 2.700 s, frame time 2.700000 s, player (9.866667, 4.533333), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.853749898 (exact 0.8537498983243804), shots in flight: none", "  0.77 s  hold off the boss's locked charge line | public {'input': BossObservation(t=0.7666666666666667, x=9.86666666666666, y=5.200000000000004, boss_x=11.600000000000001, boss_y=4.0, phase='warning', attack='charge', aim=(-1.0, 0.0), warning_left=0.3666666666666667, shots=()), 'memory_before': BossMemory(lane=(11.600000000000001, 4.0, -1.0, 0.0, 2.4), attack='charge', warning_time=0.6), 'memory_after': BossMemory(lane=(11.600000000000001, 4.0, -1.0, 0.0, 2.4), attack='charge', warning_time=0.7666666666666667), 'provenance': 'warning', 'candidates': (('hold',),), 'excluded': (('attack', 'warning-or-active'),), 'selected': 'hold', 'issued': (('stop', None),)} | frame 23, grid 0.750 s, frame time 0.766667 s, player (9.866667, 5.200000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 2.108185107 (exact 2.108185106778928), shots in flight: none", "  1.67 s  face and swing at boss | public {'input': BossObservation(t=1.6666666666666667, x=9.86666666666666, y=4.533333333333335, boss_x=9.199999999999994, boss_y=4.0, phase='recovery', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('swipe',),), 'excluded': (), 'selected': 'swipe', 'issued': (('move', 'left'), ('stop', None), ('attack', None))} | frame 50, grid 1.650 s, frame 
[... 9533 characters cut ...]
arest boss at (11.600000, 4.000000) distance 2.163330765 (exact 2.163330765278392), shots in flight: none", "  1.65 s  face and swing at boss | public {'input': BossObservation(t=1.65, x=9.799999999999994, y=4.599999999999998, boss_x=9.200000000000003, boss_y=4.0, phase='recovery', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('swipe',),), 'excluded': (), 'selected': 'swipe', 'issued': (('move', 'up'), ('stop', None), ('attack', None))} | frame 99, grid 1.650 s, frame time 1.650000 s, player (9.800000, 4.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.848528137 (exact 0.848528137423849), shots in flight: none"], "hearts_end": 2, "hearts_lost": 1, "hearts_start": 3, "hits_by": {"boss": 1}, "limit": 120, "outcome": "clear", "seconds": 12.47}}}, "source": "eddd95dd5926", "trial_count_per_fps_hearts": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 26, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 11.133333333333333}, "run_seconds": 76.46666666666667, "terminal_wait_seconds": 41.53333333332908, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.1}, "run_seconds": 5.1, "terminal_wait_seconds": 14.900000000000153, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 11.133333333333333}, "run_seconds": 76.46666666666667}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.10974051698576659, "source_id": "eddd95dd5926"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "eddd95dd5926", "trial_count_per_room_fps": 1}
...........................................................................................................................................................F....
======================================================================
FAIL: test_public_normal_pause_victory_retry_death_retry (test_split_c.SplitCTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_split_c.py", line 72, in test_public_normal_pause_victory_retry_death_retry
    self.assertEqual(first["hits"], 0)
AssertionError: 1 != 0

----------------------------------------------------------------------
Ran 160 tests in 2.790s

FAILED (failures=1)
```

### Round 2: @run/tests/public-boundary-clearance — `python3 -m unittest discover -s tests`

Exit: 1 (2.1 s). Output:

```text
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=189dbf689d7e
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=189dbf689d7e
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=189dbf689d7e
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=189dbf689d7e
INVENTORY_BEGIN source=189dbf689d7e
columns: F number path; G module.class; I number method; full test ID = current G + '.' + method
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_g002_evidence.py
F 08 tests/test_game.py
F 09 tests/test_play_run_controls.py
F 10 tests/test_run_driver.py
F 11 tests/test_session.py
F 12 tests/test_split_c.py
F 13 tests/test_terminal.py
G test_boss.BossTest
I 001 test_boss_kill_and_existing_lethal_shot_is_death_only
I 002 test_charge_contact_keeps_full_active_duration
I 003 test_four_swipes_fit_in_recovery
I 004 test_initial_single_boss
I 005 test_lifetime_expiration_precedes_contact
I 006 test_nonlethal_swipe_preserves_warning
I 007 test_short_shot_contact_does_not_accelerate_recovery
I 008 test_wall_and_blocked_contact_keep_full_charge
I 009 test_warning_duration_and_locked_aim
G test_boss_contract.BossAdditionalContractTest
I 010 test_attack_order_survives_low_hp
I 011 test_lethal_warning_swipe_prevents_new_attack
I 012 test_nonlethal_swipe_preserves_every_phase
I 013 test_one_tile_sidestep_during_each_warning
I 014 test_zero_distance_locks_right_for_both_attacks
G test_boss_contract.BossContractTest
I 015 test_early_contact_does_not_advance_recovery
I 016 test_uncontacted_shot_expiry_coincides_with_recovery
G test_boss_contract_details.B10ContactBandTest
I 017 test_charge_inside_and_outside_the_band
I 018 test_shot_inside_and_outside_the_band
G test_boss_contract_details.B3ChargeMovementTest
I 019 test_open_charge_moves_2_4_tiles_in_0_3_s
I 020 test_wall_clamps_without_moving_recovery_start
G test_boss_contract_details.B6DashContactTest
I 021 test_dash_through_charge_is_spent_and_harmless_afterwards
I 022 test_dash_through_shot_consumes_it_and_no_later_damage
G test_boss_contract_details.B7ProtectionExpiryTest
I 023 test_charge_touched_in_protection_cannot_hit_when_it_ends
G test_boss_contract_details.B9RecoveryTest
I 024 test_recovery_contact_is_harmless
I 025 test_recovery_lengths
G test_boss_contract_details.C2PauseTest
I 026 test_pause_freezes_protection_timer
I 027 test_pause_in_warning_freezes_and_resume_continues
G test_boss_contract_details.C3LimitTest
I 028 test_limit_in_combat_is_unfinished_with_no_result
I 029 test_same_frame_death_or_victory_is_recorded_beside_the_limit
G test_boss_contract_details.TerminalTest
I 030 test_t1_clear_removes_shots_and_refuses_chasing_damage
I 031 test_t2_same_frame_death_wins_over_victory
I 032 test_t2_survivor_wins_only
I 033 test_t3_terminal_state_is_frozen
I 034 test_t4_retry_from_win_and_death_equals_a_new_run
G test_bots_boss.BossPolicyTest
I 035 test_dodger_in_the_lane_holds_or_dodges_and_never_swipes
I 036 test_dodger_off_the_lane_holds_during_the_warning
I 037 test_threat_follows_the_displayed_locked_lane
G test_bots_boss.OutcomeTest
I 038 test_log_changes_no_result_in_the_boss_room
I 039 test_start_hearts_and_outcome_fields
I 040 test_unfinished_is_reported_at_the_limit
G test_bots_boss.PublicBoundaryConnectionTest
I 041 test_active_adapter_rejects_forbidden_attribute_reads
I 042 test_actual_dodger_bypasses_legacy_helpers
I 043 test_all_escape_candidates_are_enumerated
I 044 test_proxy_memory_is_owned_by_current_room
G test_bots_boss.PublicBoundaryPrototypeTest
I 045 test_active_internal_values_do_not_cross_boundary
I 046 test_slots_only_input_and_visible_branches
I 047 test_warning_memory_active_and_recovery
G test_bots_boss.RunDriverTest
I 048 test_play_run_smoke
I 049 test_read_script_hearts_and_mode
G test_bots_boss.SourceIdTest
I 050 test_source_id_is_stable_hex
G test_d022_observation.ObservationTest
I 051 test_controlled_twenty_minutes_at_each_rate
I 052 test_default_player_cadence_is_explicit_half_second
I 053 test_dispatch_and_validation
I 054 test_interval_preserves_events_and_result
I 055 test_legacy_note_only_changes_leading_line
I 056 test_public_spitter_and_boss_share_sequence
I 057 test_retry_resets_periodic_schedule
I 058 test_summary_clocks_counts_pause_and_retry
I 059 test_summary_once_for_clear_death_and_limit
G test_d022_shots_and_note.LegacyNoteTest
I 060 test_note_scope_and_position
G test_d022_shots_and_note.ShotLifecycleTest
I 061 test_clear_room_sequence_and_retry
I 062 test_legacy_emission_has_no_new_events
I 063 test_player_messages_hide_ids
I 064 test_short_shot_removal_and_fixed_recovery
G test_g002_evidence.EvidenceToolTest
I 065 test_bounded_selection_reports_missing_ranges
I 066 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 067 test_bot_log_adds_state_and_changes_no_result
I 068 test_dodger_agrees_at_30_and_60_fps
I 069 test_dodger_never_swipes_a_brute_in_wind_up
I 070 test_every_bot_finishes_a_room
I 071 test_retained_criteria_14_and_15_at_each_rate
I 072 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 073 test_a_swipe_does_not_cancel_the_wind_up
I 074 test_a_swipe_in_recovery_changes_nothing_else
I 075 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 076 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 077 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 078 test_grub_lunge_costs_a_heart
I 079 test_grub_walking_alone_does_not_hurt
I 080 test_spitter_fires_every_2_4_seconds_from_1_8
I 081 test_swipe_misses_behind_the_player
I 082 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 083 test_a_cancelled_cue_is_not_a_shot
I 084 test_a_cap_delay_only_lengthens_the_gap
I 085 test_forced_simultaneous_first_shots_still_keep_the_gap
I 086 test_other_rooms_keep_the_0_8_s_offset
I 087 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 088 test_attack_during_dash_fires_when_it_ends
I 089 test_dash_covers_four_tiles_at_both_frame_rates
I 090 test_dash_has_a_cooldown
G test_game.GrubTest
I 091 test_a_sidestep_avoids_the_lunge
I 092 test_a_swipe_during_windup_stops_the_lunge
I 093 test_dash_from_cue_into_the_lunge_takes_no_damage
I 094 test_only_one_grub_winds_up_or_lunges
I 095 test_recovery_is_safe
I 096 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 097 test_rooms_match_the_spec
I 098 test_standing_still_is_punished
I 099 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 100 test_variants_swipes_to_defeat
I 101 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 102 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 103 test_late_swipe_line_comes_before_the_hit
I 104 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 105 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 106 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 107 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 108 test_a_kill_in_wind_up_prints_no_message
I 109 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 110 test_swipes_at_a_grub_or_runner_print_no_message
I 111 test_the_banner_shows_0_6
I 112 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 113 test_a_bad_rule_says_how_rules_read
I 114 test_a_rule_acts_at_most_every_reaction_time
I 115 test_cues_show_in_the_player_view
I 116 test_marks_r_and_G_are_drawn
I 117 test_rules_and_timed_inputs_mix
I 118 test_rules_ignore_what_is_not_drawn
I 119 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 120 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 121 test_a_shot_after_the_window_hits_again
I 122 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 123 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 124 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 125 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 126 test_absorbed_shot_prints_no_message
I 127 test_direction_words_at_both_rates
I 128 test_player_view_line
G test_game.SpitterTest
I 129 test_a_standing_player_is_hit_by_the_shot
I 130 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 131 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 132 test_a_shot_hit_message_is_unchanged
I 133 test_manual_has_the_new_wording
I 134 test_rears_back_rule_matches_all_variants
I 135 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 136 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 137 test_no_pause_arguments_keep_the_old_result_shape
I 138 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 139 test_retries_start_new_attempts_and_reset_reaction_memory
I 140 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 141 test_boundary_discards_input_and_accepts_entry_time
I 142 test_control_precedes_combat_input_and_resume_uses_driver_time
I 143 test_limit_exceeds_sixty_seconds
I 144 test_public_parser_dispatch
I 145 test_run_rejects_diagnostic_setup
I 146 test_same_time_source_order
I 147 test_shot_direction_message
G test_session.SessionTest
I 148 test_boundary_healing_and_clocks
I 149 test_boundary_replaces_all_combat_state
I 150 test_limit_records_result_separately
I 151 test_pause_freezes_boundary
I 152 test_pause_freezes_dash_and_queued_attack
I 153 test_retry_rejected_outside_terminal
I 154 test_terminal_retry_matches_new_run
I 155 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 156 test_boss_actual_decision_logs_and_hearts_comparisons
I 157 test_public_normal_pause_victory_retry_death_retry
I 158 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 159 test_clear_cleans_hazards_and_freezes_every_combat_field
I 160 test_death_precedes_clear_and_existing_shot_still_hits
I 161 test_player_runner_returns_after_terminal_clock_freezes
IDENTIFIED_FILES ["game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py", "tests/test_boss.py", "tests/test_boss_contract.py", "tests/test_boss_contract_details.py", "tests/test_bots_boss.py", "tests/test_d022_observation.py", "tests/test_d022_shots_and_note.py", "tests/test_g002_evidence.py", "tests/test_game.py", "tests/test_play_run_controls.py", "tests/test_run_driver.py", "tests/test_session.py", "tests/test_split_c.py", "tests/test_terminal.py"]
INVENTORY_END files=13 ids=161 shown_files=13 shown_ids=161 excluded=non-Python-files; unshown=none
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 0, "decision_count": 76, "decision_samples": ["  0.00 s  walk to boss | public {'input': BossObservation(t=0.0, x=8.0, y=4.0, boss_x=12.0, boss_y=4.0, phase='approach', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('approach',),), 'excluded': (), 'selected': 'approach', 'issued': (('move', 'right'),)} | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", null, "  2.70 s  escape from short shot | public {'input': BossObservation(t=2.7, x=9.86666666666666, y=4.533333333333335, boss_x=9.199999999999994, boss_y=4.0, phase='warning', attack='short shot', aim=(0.780868809443029, 0.6246950475544257), warning_left=0.7666666666666667, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=(9.199999999999994, 4.0, 0.780868809443029, 0.6246950475544257, 3.0), attack='short shot', warning_time=2.7), 'provenance': 'warning', 'candidates': (('move', 'down', True), ('move', 'up', True)), 'excluded': (('attack', 'warning-or-active'), ('up', 'lower-priority')), 'selected': 'escape', 'issued': (('move', 'down'),)} | frame 81, grid 2.700 s, frame time 2.700000 s, player (9.866667, 4.533333), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.853749898 (exact 0.8537498983243804), shots in flight: none", "  0.77 s  hold off the boss's locked charge line | public {'input': BossObservation(t=0.7666666666666667, x=9.86666666666666, y=5.200000000000004, boss_x=11.600000000000001, boss_y=4.0, phase='warning', attack='charge', aim=(-1.0, 0.0), warning_left=0.3666666666666667, shots=()), 'memory_before': BossMemory(lane=(11.600000000000001, 4.0, -1.0, 0.0, 2.4), attack='charge', warning_time=0.6), 'memory_after': BossMemory(lane=(11.600000000000001, 4.0, -1.0, 0.0, 2.4), attack='charge', warning_time=0.7666666666666667), 'provenance': 'warning', 'candidates': (('hold',),), 'excluded': (('attack', 'warning-or-active'),), 'selected': 'hold', 'issued': (('stop', None),)} | frame 23, grid 0.750 s, frame time 0.766667 s, player (9.866667, 5.200000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 2.108185107 (exact 2.108185106778928), shots in flight: none", "  1.67 s  face and swing at boss | public {'input': BossObservation(t=1.6666666666666667, x=9.86666666666666, y=4.533333333333335, boss_x=9.199999999999994, boss_y=4.0, phase='recovery', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('swipe',),), 'excluded': (), 'selected': 'swipe', 'issued': (('move', 'left'), ('stop'
[... 9564 characters cut ...]
), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 2.545584412 (exact 2.545584412271567), shots in flight: none", "  1.80 s  face and swing at boss | public {'input': BossObservation(t=1.8, x=9.799999999999994, y=4.599999999999998, boss_x=9.200000000000003, boss_y=4.0, phase='recovery', attack='charge', aim=None, warning_left=None, shots=()), 'memory_before': BossMemory(lane=None, attack=None, warning_time=None), 'memory_after': BossMemory(lane=None, attack=None, warning_time=None), 'provenance': 'none', 'candidates': (('swipe',),), 'excluded': (), 'selected': 'swipe', 'issued': (('move', 'up'), ('stop', None), ('attack', None))} | frame 108, grid 1.800 s, frame time 1.800000 s, player (9.800000, 4.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.848528137 (exact 0.848528137423849), shots in flight: none"], "hearts_end": 2, "hearts_lost": 1, "hearts_start": 3, "hits_by": {"boss": 1}, "limit": 120, "outcome": "clear", "seconds": 12.92}}}, "source": "189dbf689d7e", "trial_count_per_fps_hearts": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 26, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 11.3}, "run_seconds": 76.63333333333334, "terminal_wait_seconds": 41.36666666666241, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.1}, "run_seconds": 5.1, "terminal_wait_seconds": 14.900000000000153, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 11.3}, "run_seconds": 76.63333333333334}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.10916719597298652, "source_id": "189dbf689d7e"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "189dbf689d7e", "trial_count_per_room_fps": 1}
............................................................................................................................................................F....
======================================================================
FAIL: test_public_normal_pause_victory_retry_death_retry (test_split_c.SplitCTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_split_c.py", line 72, in test_public_normal_pause_victory_retry_death_retry
    self.assertEqual(first["hits"], 0)
AssertionError: 1 != 0

----------------------------------------------------------------------
Ran 161 tests in 2.808s

FAILED (failures=1)
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/74-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
