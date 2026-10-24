# Studio operation packet

operation: Step
goal: G-002
role: qa
incoming_handoff: goals/G-002-final-boss/57-studio-to-qa.md
next_seq: 58
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-002-final-boss/58-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

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

<<<FILE goals/G-002-final-boss/57-studio-to-qa.md
---
kind: handoff
goal: G-002
seq: 57
from: studio
to: qa
stage: Verify
outcome: routed
---
# 57: studio → qa — 連続ランと最終ボスの独立検証

## Task

保存ビルドを仕様・受入基準から独立検証する。30/60 FPSを別々に実行し、公開経路での連続到達・終端・再挑戦、ボス契約、共有戦闘と独立部屋の回帰を確認する。

## Context

G-002は第1〜4部屋を連続して進み、第5部屋の単体ボス、勝利・死亡・最初からの再挑戦までを成立させるGoal。Buildが完了し、独立Verifyを開始する。今回の対象はD-021が承認したテキスト表示・スクリプト実行であり、実機供給や実gamepad検証は要求しない。

## Findings

検証対象は現在のrepo/。実行はrepo/を作業ディレクトリとする。

- 全suite：`python3 -m unittest discover -s tests`
- プレイヤー表示：`python3 play.py --view player SCRIPT`
- トレース：`python3 play.py --view trace SCRIPT`
- botと判断ログ：`python3 bots.py SCRIPT`

公開構文はmanual.mdとpublic-driver.mdを使用する。既存の再現用スクリプト生成器も利用可能：

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
```

各スクリプトをplayer/trace両viewで実行する。生成済み入力の再生とcontrolled fixtureは区別し、fixtureの成功を通常到達の代用にしない。既存テストの合格だけで独立判定を終えず、仕様に照らして出力・イベント・状態を確認する。

## Decisions already made

- D-017：二攻撃のボス、連続進行、回復、終端優先、pause/retryと時計の契約。
- D-019：旧集計の適用終了、保持する独立部屋回帰とFPS比較、実測後のDesigner判断。
- D-021：Studio内のテキスト・スクリプト検証で進める。
- D-022：旧経路注記、弾ID・消滅理由、観測間隔と全attempt summary。

## Constraints

- 正本はdesign/final-boss-and-continuous-run.md、関連Decisions、共有戦闘仕様。
- 第1〜4部屋と共有戦闘ルールの保持を検証する。廃止された部屋3〜5集計ゲートを復活させない。
- 実装者の自己評価・原因説明・期待される測定値は入力に含めない。
- 通常ラン時間、pause、終端待機、headless処理時間を分ける。独立部屋の時間合計を通常ラン時間としない。
- テスト用状態設定・botの成功を人間の体験評価としない。新しい数値ゲートや難度調整はQAが決めない。
- コードや仕様を変更せず、失敗・仕様不足は具体的証拠とともにStudioへ返す。

## Open questions

1. R1/C1：通常の敵撃破から部屋1→5へ到達し、部屋5がB単体となるか。部屋時計、回復、初回ボス到達hearts、四つの遷移時間は契約どおりか。
2. B1〜B10/T1〜T4/C1〜C3：二攻撃、予兆・固定方向・実弾・接触・防御・終端優先などが仕様を満たすか。
3. C2/T4：有限pauseが戦闘、両時計、clear表示を凍結するか。勝利・自然死亡からretryでき、完全な初期状態と入力破棄が成立するか。遠い未来の入力が短い試行で出ないだけでは破棄の証明としない。
4. 各attemptのsummaryがイベントと一致するか。到達部屋、攻撃・ボス命中・dash・hurt、pause、終端待機、retry、driver-limit終了を分離して確認できるか。
5. D-019の保持基準14/15/16c、独立部屋1〜4、ボス開始hearts 3/2の両FPS比較は成立するか。判断ログの入力情報はプレイヤーに観測可能か。
6. V1とD-022：player表示で必要な状態を識別でき、旧経路注記・弾ライフサイクル・長時間観測とsummaryが仕様どおりか。詳細な視覚表現のレビューは後続Art Directorが担当する。

## Expected output

`to: studio`の独立QA報告を作成し、outcomeをpass/fail、仕様不足ならquestionとする。検証した保存ソースID、コマンド・入力、FPS、試行数、基準ごとの判定、再現手順と証拠、未検証範囲を記録する。

通常ランの同一試行による到達・終端・部屋別時間・pause/待機を測定し、botの両FPS結果と判断ログを記録する。時間差や体験上の含意は判定と分けて後続Designerへ引き継ぐ。合格なら限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewの順にStudioがルートする。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/（保存ビルドとtests。上記コマンドで実行）
- Project: repo/manual.md
- Project: repo/public-driver.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: none（独立性のため56と実装履歴を渡さず、必要な実行情報を本Handoffへ転記）
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
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

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (2.9 s). Output:

```text
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=04fa2b1c168a
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=04fa2b1c168a
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=04fa2b1c168a
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=04fa2b1c168a
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 8, "decision_count": 145, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.39 s) | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 4.000000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 1.733333333 (exact 1.7333333333333414), shots in flight: none", "  3.17 s  dash down from short shot (hit in 0.39 s) | frame 95, grid 3.150 s, frame time 3.166667 s, player (9.866667, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none", "  1.07 s  hold off the boss's locked charge line | frame 32, grid 1.050 s, frame time 1.066667 s, player (9.866667, 1.333333), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 3.180496118 (exact 3.180496117833754), shots in flight: none", "  2.40 s  face and swing at boss | frame 72, grid 2.400 s, frame time 2.400000 s, player (9.866667, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none"], "hearts_end": 2, "hearts_lost": 0, "hearts_start": 2, "hits_by": {}, "limit": 120, "outcome": "clear", "seconds": 21.63}, "3": {"attacks": 12, "cleared": true, "dashes": 8, "decision_count": 145, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.39 s) | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.733333333 (exact 1.7333333333333414), shots in flight: none", "  3.17 s  dash down from short shot (hit in 0.39 s) | frame 95, grid 3.150 s, frame time 3.166667 s, player (9.866667, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none", "  1.07 s  hold off the boss's locked charge line | frame 32, grid 1.050 s, frame time 1.066667 s, player (9.866667, 1.333333), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 3.180496118 (exact 3.180496117833754), shots in flight: none", "  2.40 s  face and swing at boss | frame 72, grid 2.400 s, frame time 2.400000 s, player (9.866667, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none"], "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 120, "outcome": "clear", "seconds": 21.63}}, "60": {"2": {"attacks": 12, "cleared": true, "dashes": 12, "decision_count": 220, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.38 s) | frame 54, grid 0.900 s, frame time 0.900000 s, player (9.800000, 4.000000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none", "  3.15 s  dash up from short shot (hit in 0.36 s) | frame 189, grid 3.150 s, frame time 3.150000 s, player (9.800000, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none", "  1.05 s  hold off the boss's locked charge line | frame 63, grid 1.050 s, frame time 1.050000 s, player (9.800000, 1.600000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 3.000000000 (exact 3.0), shots in flight: none", "  2.40 s  face and swing at boss | frame 144, grid 2.400 s, frame time 2.400000 s, player (9.800000, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none"], "hearts_end": 2, "hearts_lost": 0, "hearts_start": 2, "hits_by": {}, "limit": 120, "outcome": "clear", "seconds": 32.87}, "3": {"attacks": 12, "cleared": true, "dashes": 12, "decision_count": 220, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.38 s) | frame 54, grid 0.900 s, frame time 0.900000 s, player (9.800000, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none", "  3.15 s  dash up from short shot (hit in 0.36 s) | frame 189, grid 3.150 s, frame time 3.150000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none", "  1.05 s  hold off the boss's locked charge line | frame 63, grid 1.050 s, frame time 1.050000 s, player (9.800000, 1.600000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 3.000000000 (exact 3.0), shots in flight: none", "  2.40 s  face and swing at boss | frame 144, grid 2.400 s, frame time 2.400000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none"], "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 120, "outcome": "clear", "seconds": 32.87}}}, "source": "04fa2b1c168a", "trial_count_per_fps_hearts": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 34, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 21.633333333333333}, "run_seconds": 86.96666666666667, "terminal_wait_seconds": 31.033333333329082, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.1}, "run_seconds": 5.1, "terminal_wait_seconds": 14.900000000000153, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 21.633333333333333}, "run_seconds": 86.96666666666667}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.12757248495472595, "source_id": "04fa2b1c168a"}, "trial_count": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 45, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333, "terminal_wait_seconds": 14.46666666666114, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333, "terminal_wait_seconds": 14.966666666666812, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 60, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3285309129860252, "source_id": "04fa2b1c168a"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "04fa2b1c168a", "trial_count_per_room_fps": 1}
........................................................................................................................................................
----------------------------------------------------------------------
Ran 152 tests in 2.855s

OK
```

### Round 2: @run/trace/boss-30 — `python3 play.py --view trace {script}`

Script:

```text
mode room
room 5
fps 30
limit 12
driver-limit 14
trace-every 0.5
control 2.2 pause
control 4.2 resume
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 30 FPS — timed inputs use room time
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 12.0, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 1, 'attempt': 1, 'room': '5', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'entry', 'details': {'hearts': 3}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 0.5, 'room_time': 0.5, 'frame': 15, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 11.500000000000002, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 1.0, 'room_time': 1.0, 'frame': 30, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 11.000000000000004, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 1.5, 'room_time': 1.5, 'frame': 45, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.500000000000005, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.0, 'room_time': 2.0, 'frame': 60, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.033333333333333, 'room_time': 2.033333333333333, 'frame': 61, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.7, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 2, 'attempt': 1, 'room': '5', 'run_time': 2.033333333333333, 'room_time': 2.033333333333333, 'frame': 61, 'kind': 'boss_warning', 'details': {'attack': 'charge', 'aim': (-1.0, 0.0)}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.2, 'room_time': 2.2, 'frame': 66, 'state': 'combat', 'paused': True, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.5333333333333333, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 3, 'attempt': 1, 'room': '5', 'run_time': 2.2, 'room_time': 2.2, 'frame': 66, 'kind': 'pause', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.2333333333333334, 'room_time': 2.2333333333333334, 'frame': 67, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.5, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 4, 'attempt': 1, 'room': '5', 'run_time': 2.2, 'room_time': 2.2, 'frame': 66, 'kind': 'resume', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.5, 'room_time': 2.5, 'frame': 75, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.2333333333333334, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.7333333333333334, 'room_time': 2.7333333333333334, 'frame': 82, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 10.000000000000007, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'active', 'phase_left': 0.3, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 5, 'attempt': 1, 'room': '5', 'run_time': 2.7333333333333334, 'room_time': 2.7333333333333334, 'frame': 82, 'kind': 'boss_active', 'details': {'attack': 'charge'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 2.933333333333333, 'room_time': 2.933333333333333, 'frame': 88, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.8, 'stun_left': 0.3, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 8.400000000000002, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'active', 'phase_left': 0.10000000000000003, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 6, 'attempt': 1, 'room': '5', 'run_time': 2.933333333333333, 'room_time': 2.933333333333333, 'frame': 88, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'hurt'}}, {'sequence': 7, 'attempt': 1, 'room': '5', 'run_time': 2.933333333333333, 'room_time': 2.933333333333333, 'frame': 88, 'kind': 'hurt', 'details': {'source': 'boss', 'hearts': 2, 'name': "boss's charge"}}, {'sequence': 8, 'attempt': 1, 'room': '5', 'run_time': 2.933333333333333, 'room_time': 2.933333333333333, 'frame': 88, 'kind': 'boss_contact', 'details': {'blocked': False}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 3.0, 'room_time': 3.0, 'frame': 90, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.7333333333333334, 'stun_left': 0.23333333333333334, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.866666666666668, 'y': 4.0, 'aim': (-1.0, 0.0), 'hp': 12, 'phase': 'active', 'phase_left': 0.033333333333333375, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 3.033333333333333, 'room_time': 3.033333333333333, 'frame': 91, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.7000000000000001, 'stun_left': 0.2, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 1.2, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 9, 'attempt': 1, 'room': '5', 'run_time': 3.033333333333333, 'room_time': 3.033333333333333, 'frame': 91, 'kind': 'boss_recovery', 'details': {'attack': 'charge'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 3.5, 'room_time': 3.5, 'frame': 105, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.2333333333333335, 'stun_left': 0.0, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 0.7333333333333328, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 3.7333333333333334, 'room_time': 3.7333333333333334, 'frame': 112, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 0.49999999999999956, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 10, 'attempt': 1, 'room': '5', 'run_time': 3.7333333333333334, 'room_time': 3.7333333333333334, 'frame': 112, 'kind': 'invulnerable', 'details': {'value': False, 'why': 'hurt timer ended'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 4.0, 'room_time': 4.0, 'frame': 120, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 0.23333333333333295, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 4.233333333333333, 'room_time': 4.233333333333333, 'frame': 127, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'short shot', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 11, 'attempt': 1, 'room': '5', 'run_time': 4.233333333333333, 'room_time': 4.233333333333333, 'frame': 127, 'kind': 'boss_pursuit', 'details': {'attack': 'short shot'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 4.266666666666667, 'room_time': 4.266666666666667, 'frame': 128, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': (1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.8, 'attack_name': 'short shot', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 12, 'attempt': 1, 'room': '5', 'run_time': 4.266666666666667, 'room_time': 4.266666666666667, 'frame': 128, 'kind': 'boss_warning', 'details': {'attack': 'short shot', 'aim': (1.0, 0.0)}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 4.5, 'room_time': 4.5, 'frame': 135, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 2, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.
[... 6512 characters cut ...]
lse, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 0.9666666666666655, 'attack_name': 'short shot', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 7.0, 'room_time': 7.0, 'frame': 210, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 1, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'recovery', 'phase_left': 0.46666666666666556, 'attack_name': 'short shot', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 7.466666666666667, 'room_time': 7.466666666666667, 'frame': 224, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 1, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'approach', 'phase_left': 0.0, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 20, 'attempt': 1, 'room': '5', 'run_time': 7.466666666666667, 'room_time': 7.466666666666667, 'frame': 224, 'kind': 'boss_pursuit', 'details': {'attack': 'charge'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 7.5, 'room_time': 7.5, 'frame': 225, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 1, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': (1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.7, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 21, 'attempt': 1, 'room': '5', 'run_time': 7.5, 'room_time': 7.5, 'frame': 225, 'kind': 'boss_warning', 'details': {'attack': 'charge', 'aim': (1.0, 0.0)}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 8.0, 'room_time': 8.0, 'frame': 240, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 1, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': (1.0, 0.0), 'hp': 12, 'phase': 'warning', 'phase_left': 0.20000000000000007, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 8.2, 'room_time': 8.2, 'frame': 246, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 1, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.600000000000001, 'y': 4.0, 'aim': (1.0, 0.0), 'hp': 12, 'phase': 'active', 'phase_left': 0.3, 'attack_name': 'charge', 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 22, 'attempt': 1, 'room': '5', 'run_time': 8.2, 'room_time': 8.2, 'frame': 246, 'kind': 'boss_active', 'details': {'attack': 'charge'}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'state': 'dead', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 0, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.8, 'stun_left': 0.3, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'boss', 'x': 7.866666666666668, 'y': 4.0, 'aim': None, 'hp': 12, 'phase': 'active', 'phase_left': 0.26666666666666666, 'attack_name': 'charge', 'struck': True, 'spent': False}], 'shots': [], 'events': [{'sequence': 23, 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'hurt'}}, {'sequence': 24, 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'kind': 'hurt', 'details': {'source': 'boss', 'hearts': 0, 'name': "boss's charge"}}, {'sequence': 25, 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'kind': 'down', 'details': {}}, {'sequence': 26, 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'kind': 'boss_contact', 'details': {'blocked': False}}, {'sequence': 27, 'attempt': 1, 'room': '5', 'run_time': 8.233333333333333, 'room_time': 8.233333333333333, 'frame': 247, 'kind': 'diagnostic_result', 'details': {'outcome': 'dead'}}]}
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 8.233333333333333, 'rooms': {'5': 8.233333333333333}, 'boss_entry_hearts': 3, 'hits': 3, 'attacks': 0, 'pauses': 1, 'pause_seconds': 2.0000000000000027, 'driver_seconds': 10.233333333333308, 'elapsed_excluding_pauses': 8.233333333333306}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': '04fa2b1c168a', 'driver_seconds': 10.233333333333333, 'processing_seconds': 0.0027434719959273934, 'execution_stop': 'terminal'}
```

### Round 2: @run/play/boss-60 — `python3 play.py --view player {script}`

Script:

```text
mode room
room 5
fps 60
limit 12
driver-limit 14
view-every 0.5
control 2.2 pause
control 4.2 resume
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room 5 run 0.000 room-time 0.000] entered room 5/5
room — room 5/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat
|                |
|                |
|                |
|                |
|        P   B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
room — room 5/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat
|                |
|                |
|                |
|                |
|        P  B    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
room — room 5/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat
|                |
|                |
|                |
|                |
|        P  B    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
room — room 5/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat
|                |
|                |
|                |
|                |
|        P B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
room — room 5/5 — hearts 3/3 — run 2.000 s — room 2.000 s — combat
|                |
|                |
|                |
|                |
|        P B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 2.017 room-time 2.017] the boss prepares a charge
room — room 5/5 — hearts 3/3 — run 2.017 s — room 2.017 s — combat
|                |
|                |
|                |
|                |
|        P~B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.700 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 2.200 room-time 2.200] paused
room — room 5/5 — hearts 3/3 — run 2.200 s — room 2.200 s — combat — paused
|                |
|                |
|                |
|                |
|        P~B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.517 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 2.200 room-time 2.200] resumed
room — room 5/5 — hearts 3/3 — run 2.217 s — room 2.217 s — combat
|                |
|                |
|                |
|                |
|        P~B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.500 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 2.717 room-time 2.717] the boss charges
room — room 5/5 — hearts 3/3 — run 2.717 s — room 2.717 s — combat
|                |
|                |
|                |
|                |
|        P B     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 2.900 room-time 2.900] YOU ARE HIT by the boss's charge — hearts 2/3
room — room 5/5 — hearts 2/3 — run 2.900 s — room 2.900 s — combat
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 3.017 room-time 3.017] the boss is recovering — safe to approach and swipe
room — room 5/5 — hearts 2/3 — run 3.017 s — room 3.017 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.200 left
room — room 5/5 — hearts 2/3 — run 3.517 s — room 3.517 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.700 left
room — room 5/5 — hearts 2/3 — run 4.017 s — room 4.017 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.200 left
[attempt 1 room 5 run 4.217 room-time 4.217] the boss resumes pursuit
room — room 5/5 — hearts 2/3 — run 4.217 s — room 4.217 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
[attempt 1 room 5 run 4.233 room-time 4.233] the boss aims a short shot
room — room 5/5 — hearts 2/3 — run 4.233 s — room 4.233 s — combat
|                |
|                |
|                |
|                |
|        P~~~    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: short shot
cue: B short shot — locked (1.0, 0.0) — 0.800 left
danger: one shot, contact radius 0.4 tile, range 3.0 tiles
room — room 5/5 — hearts 2/3 — run 4.733 s — room 4.733 s — combat
|                |
|                |
|                |
|                |
|        P~~~    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: short shot
cue: B short shot — locked (1.0, 0.0) — 0.300 left
danger: one shot, contact radius 0.4 tile, range 3.0 tiles
[attempt 1 room 5 run 5.033 room-time 5.033] the boss fires a short shot
room — room 5/5 — hearts 2/3 — run 5.033 s — room 5.033 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 1
boss B — HP 12/12 — active — next: short shot
[attempt 1 room 5 run 5.050 room-time 5.050] YOU ARE HIT by a shot from the west — hearts 1/3
room — room 5/5 — hearts 1/3 — run 5.050 s — room 5.050 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: short shot
room — room 5/5 — hearts 1/3 — run 5.550 s — room 5.550 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: short shot
[attempt 1 room 5 run 6.033 room-time 6.033] the boss is recovering — safe to approach and swipe
room — room 5/5 — hearts 1/3 — run 6.033 s — room 6.033 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: short shot
recovery: 1.400 left
room — room 5/5 — hearts 1/3 — run 6.533 s — room 6.533 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: short shot
recovery: 0.900 left
room — room 5/5 — hearts 1/3 — run 7.033 s — room 7.033 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: short shot
recovery: 0.400 left
[attempt 1 room 5 run 7.433 room-time 7.433] the boss resumes pursuit
room — room 5/5 — hearts 1/3 — run 7.433 s — room 7.433 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 7.450 room-time 7.450] the boss prepares a charge
room — room 5/5 — hearts 1/3 — run 7.450 s — room 7.450 s — combat
|                |
|                |
|                |
|                |
|        P~~     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (1.0, 0.0) — 0.700 left
danger: charge lane, radius 0.6 tile, rounded ends
room — room 5/5 — hearts 1/3 — run 7.950 s — room 7.950 s — combat
|                |
|                |
|                |
|                |
|        P~~     |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (1.0, 0.0) — 0.200 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 8.150 room-time 8.150] the boss charges
room — room 5/5 — hearts 1/3 — run 8.150 s — room 8.150 s — combat
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 8.167 room-time 8.167] YOU ARE HIT by the boss's charge — hearts 0/3
[attempt 1 room 5 run 8.167 room-time 8.167] you went down
room — room 5/5 — hearts 0/3 — run 8.167 s — room 8.167 s — dead
|                |
|                |
|                |
|                |
|        x       |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 8.166666666666666, 'rooms': {'5': 8.166666666666666}, 'boss_entry_hearts': 3, 'hits': 3, 'attacks': 0, 'pauses': 1, 'pause_seconds': 1.9999999999999978, 'driver_seconds': 10.166666666666751, 'elapsed_excluding_pauses': 8.166666666666753}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': '04fa2b1c168a', 'driver_seconds': 10.166666666666666, 'processing_seconds': 0.004392977978568524, 'execution_stop': 'terminal'}
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/58-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
