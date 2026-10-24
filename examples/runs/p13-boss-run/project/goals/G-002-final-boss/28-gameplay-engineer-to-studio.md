---
kind: handoff
goal: G-002
seq: 28
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 28: gameplay-engineer → studio — ボス戦闘の部分実装を保存、統合Buildは未完了

## Task

部分成果を保存し、Gameplay Engineerの継続Buildへ戻す。全Build未完了のため独立QAへ投入しない。

## Context

27の継続Buildと、提示されたRound 1の失敗に対応する。D-021の開始承認は有効であり、供給・実機・費用承認を再要求しない。

## Findings

今回保存するのはボス戦闘の部分実装である。Session、公開表示、対応bot、通常ラン測定までの完成要求は未達。

### 変更

- game.py：第5部屋をB(12,4)、HP12の1体へ置換。接近、固定照準の予兆、突進／短射の交互進行、回復を追加。
- 突進は命中・保護接触・壁到達で有効時間を短縮しない。非致死swipeは予兆を変更せず、致死なら新発動を止める。
- Shotに発射元と寿命を追加。既存の5要素list fixtureは互換保持。ボス弾は寿命1秒、盤面端で消滅し、寿命到達は接触より先に判定する。
- 攻撃回復の微小な浮動小数点残値をEPS以下で0へ正規化。0.35秒経過後の攻撃受理を可能にする。
- play.py／bots.py：「grub以外はspitter」というcue参照を明示的なspitter判定へ変更。traceのボス種別分岐を追加。
- test_game.py：旧5番配置とgap試験、旧13集計をD-019に沿って移行。EDIT検索は各関数名などの周辺行を含めて一意にした。
- test_boss.py：両FPSを扱う9試験を保存。

### プレイヤー可視挙動と仕様根拠

| 挙動 | 根拠 |
|---|---|
| 第5部屋はHP12のB1体 | §2〜3、B1 |
| 固定照準の突進と短射、所定の予兆・有効時間・回復 | §3、B2〜B4 |
| 非致死swipeでは予兆が続く | §3、B8 |
| 保護接触で突進の一撃を消費 | §3、B6〜B7 |
| 回復中の4回swipe機会 | §3、B9 |

公開player表示への接続は未完成であり、内部イベント追加だけでV1を満たしたとは扱わない。

### 基準・旧assert対応

| 対象 | 保存内容 | 未完了 |
|---|---|---|
| R1、R3〜R5、C1〜C3、T4 | なし | RunSession、境界、両時刻、pause、retry、limit |
| R2／B1 | 1〜4配置保持、1番assert補完、5番置換 | 今回版の実行確認 |
| B2〜B4 | 戦闘実装と制御fixture試験 | 攻撃順反復、距離0、全軌道等の網羅 |
| B5〜B7 | 保護接触fixtureの一部 | 各攻撃の横移動・実dash接触・次攻撃、帯検証 |
| B8〜B9 | 予兆維持・回復4回・相打ち試験 | 全phase、表示との対照 |
| B10 | 共有接触判定を保持 | ボスの帯内外・上端試験 |
| T1〜T3 | 26の終端処理保持、ボス相打ち試験追加 | 最終勝利を含むSession統合 |
| V1 | traceのボス分岐のみ | player常設情報、全文言、即時描画 |
| V2 | 今回未検証 | D-021の対象外依存として保持 |
| CueGapTest | 4番、取消、cap、practice保持 | 旧5番置換先B2／B4の網羅 |
| BotsTest旧13 | 適用終了 | 独立3・4の新報告 |
| BotsTest14／15／16c | 1〜2比較、3・4dash、1〜4 FPS比較保持 | ボス対応dodgerの3／2 hearts別比較 |

旧5番比較を除外しただけでボスFPS比較を完了とはしない。

### 実行記録

提示されたRound 1は `python3 -m unittest discover -s tests`、入力script空、Exit 1、0.2秒、81 tests、1 failure／5 errors。

これは未保存提案に対する結果であり、今回保存版の合格証拠ではない。今回保存版のtests・trace・botsは未実行。成功件数、ボス攻略可能性、通常到達、所要時間を主張しない。

### 残作業と再現手順

次のBuildは逐次、以下を完了する。

1. repo/で `python3 -m unittest discover -s tests` を実行し、今回版の回帰とボス試験を確認。
2. B1〜B10の不足試験、弾ID・接触消費・消滅理由等の観測を補完。
3. RunSessionとR／T／Cを実装。
4. Plan16のmode、attempt、control、limit、driver-limit構文、player／trace、manual／READMEを完成。
5. 公開観測に基づくボス対応dodgerを追加。独立1〜4の方針は保持。
6. 同一build・初期状態・方針・limitで独立5番を開始hearts3／2別に30/60比較。独立3・4は各bot・各FPS別に報告。
7. 通常ランを正規敵撃破で実行し、同一試行の到達・終端、部屋別時間、遷移、ボス入場hearts、被弾、反撃、retry、pauseと処理実時間を記録。

測定値はまだ存在しない。独立部屋の合算やfixtureでR1を代用しない。

### Sender assessment

Round 1の属性エラーはspitter専用字段をbossへ参照した結果であり、明示種別分岐で対処した。旧5番依存のエラーはD-019に沿って移行した。

4回swipe試験失敗について、0.35秒減算後の微小残値で攻撃がrecovering扱いになる共有経路へ正規化を追加した。ただし今回版の再実行による確認は未了。

部分実装の保存であり、27が求めた全Build完成を達成していない。明白な攻略不能・到達不能を実測した証拠もない。

## Decisions already made

- D-015〜D-017：連続ラン、第5部屋単体ボス、回復、死亡優先、先頭retry。
- D-019：旧集計終了、共有回帰保持、対応bot比較、実測後Designer判断。
- D-021：現状repo/とStudio内テキスト実行を使用する。

## Constraints

第1〜4部屋と共有パラメータを保持。新戦闘入力、チェックポイント、時間合わせのHP・待機追加は禁止。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持。自己試験で代替しない。

## Open questions

新規仕様質問・開始承認待ちはない。残るのは実装・実行・測定である。

## Expected output

Studioは部分成果として保存し、統合Buildの継続を開く。全機能、必要試験、説明更新、測定が揃うまでQA投入可能としない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/27-studio-to-gameplay-engineer.md
