---
kind: handoff
goal: G-002
seq: 32
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 32: gameplay-engineer → studio — 公開Session経路を保存、統合検証と測定は未完了

## Task

公開Session driverと接続変更を保存し、Gameplay Engineerの継続Buildへ戻す。全成果の実行確認、対応bot、通常ラン測定が揃うまで独立QAへ投入しない。

## Context

31はSession基盤を公開parser・driver・player／traceへ接続し、対応botと不足試験、説明、同一試行実測まで完成する要求である。D-021の開始許可は有効。今回のパケットでは実行round残数が0であり、供給済み結果以外の実行証拠は取得していない。

## Findings

### 今回の変更ファイル

- `repo/run_driver.py`：新規保存。Plan16のmode、attempt、control、limit、driver-limit、trace-everyを解析し、RunSessionまたは独立診断RoomSessionへ接続する。停止しないdriver時刻、制御先行、同時刻記載順、試行別入力、入場時反応記憶初期化を実装する。
- `repo/play.py`：新構文の公開dispatchとボス予兆経路の描画を追加。旧構文は既存経路を保持する。
- `repo/game.py`：hurtイベントへ既存の被弾名を追加し、新driverでも短射・spitterの方向文言を保持する。
- `repo/tests/test_run_driver.py`：7試験を新規保存。実行していない。
- `repo/public-driver.md`：新構文、時計、再現例、表示範囲、未完成事項を記載。

パケットで「proposed … not written」とされた全文は保存済み成果と扱わず、今回出力したファイル／編集だけを保存対象とする。提案版の9試験をそのまま採用したという報告ではない。

### 実装前に照合した可視挙動

| 挙動 | 正本 |
|---|---|
| 通常ランは第1部屋から開始、診断setupとの併用を拒否 | 仕様§2、Plan16公開構文 |
| driver時計でpause／resume／retryを制御 | 仕様§4〜5、Plan16 |
| 同時刻は記載順、制御→時刻入力→反応 | 仕様§5、Plan16 |
| 境界・pause中の期限入力を破棄 | 仕様§2、§5 |
| 入場で反応時刻・盤面・メッセージ記憶を初期化 | 仕様§2 |
| 両時計、ボスHP・攻撃名・予兆寸法・回復・活動弾数を表示 | 仕様§6 |
| 長時間limitを勝敗と別に報告 | 仕様§5、C3 |

新しい戦闘入力、ボスcheckpoint、時間合わせのHP・待機は追加していない。

### 基準対応と未達

| 対象 | 今回の対応 | 残作業 |
|---|---|---|
| R1 | 通常ラン公開起動経路 | 正規撃破による1→5到達の実行証拠 |
| R2・共有回帰 | 第1〜4部屋と既存パラメータを変更しない | 全保存版suite実行、保持基準の不足追跡 |
| R3〜R5、C1 | Session接続、境界入力試験、入場時反応記憶初期化 | 実行確認、反応記憶の専用試験、公開表示対照 |
| B1〜B10 | ボス予兆線と表示を公開経路へ接続 | 30の残作業表にある全不足試験と実行 |
| T1〜T4 | 終端待機とdriver制御retry、旧試行未来入力の除外処理 | 実勝利・実死亡からのretry、凍結、反応記憶破棄の試験 |
| C2 | driver時刻resume、pause中入力破棄の試験 | 予兆・保護・境界を含む実行確認。headless時計を実時間2秒と呼ばない |
| C3 | limitとoutcomeを別字段に表示 | 勝利・死亡同フレームlimitの統合試験 |
| V1 | 公開player情報・メッセージ・即時表示、毎tick trace選択 | 全契機対照、弾ID、全消去理由、イベントbuild字段、長時間メモリ評価 |
| D-019 | 独立1〜4の既存bot方針を維持 | ボス対応dodger、開始3／2 hearts別FPS比較、独立3・4全bot報告 |
| 文書 | public-driver.mdを追加 | manual／READMEへの統合更新 |
| V2 | D-021の今回対象外 | 実機対応検証済みとはしない |

旧assertの保持／終了／置換は仕様§8、Plan16・20、30を維持する。旧13集計を復活させず、独立1〜2比較、3・4のdash、独立1〜4のFPS比較を保持する。今回botsおよび既存assertの追加変更はない。

### 実行対象・コマンド・実結果

パケット供給の@run-results：

| Round | コマンド | 供給結果 |
|---|---|---|
| 1 | `python3 -m unittest discover -s tests` | Exit 0、89 tests、0.169秒、OK |
| 2 | 同上 | Exit 0、95 tests、0.188秒、OK |
| 3 | 同上 | Exit 0、98 tests、0.192秒、OK |

今回出力版は実行していない。上記98件へ今回7試験を加えて成功件数を推定・認定しない。trace、bots、通常ランの実結果は供給されていない。build識別は今回の公開driverで`0.6-g002-public-32`とするが、供給済み結果をこの識別へ帰属させない。

### 再現手順

次の継続Buildでは保存後の`repo/`を対象に実行する。

1. `python3 -m unittest discover -s tests`で既存試験と新7試験を確認する。
2. `public-driver.md`のpause例をscriptへ保存し、`python3 play.py --view player SCRIPT`と`python3 play.py --view trace SCRIPT`を実行する。両FPSで制御時刻、拒否入力、凍結時計を対照する。
3. 同文書の独立5番例を両FPSで実行し、warning／active／recoveryと予兆線、活動弾数を対照する。
4. 実終端retry・旧未来入力破棄、反応記憶、limit同フレーム結果の不足試験を追加する。
5. ボス対応dodgerを公開観測に基づいて実装し、独立5番開始3／2 heartsを同一limit・同一方針で比較する。独立3・4は全bot×両FPSを報告する。
6. 正規敵撃破による同一試行の通常ランを記録する。部屋別時間、1秒遷移、ボス入場hearts、被弾、回復中反撃、終端、retry、pause、処理実時間を対応付ける。

### 測定条件と値

新測定値なし。独立部屋合算、境界fixture、供給されたsuite処理時間を通常ラン時間へ転用しない。明白な攻略不能・到達不能を示す測定証拠もない。

### Sender assessment

31の統合Build完成要求は未達である。今回は未保存提案を含むパケットから、公開driver接続を具体的な保存成果へ進めた部分成果である。

実行round枯渇は保存後検証・測定の阻害要因である。対応bot、受け入れ試験の不足、観測・文書の未完成は実装残作業であり、round枯渇だけが未完了原因ではない。自己承認および独立QAへの投入要求は行わない。

既存scriptを旧経路へ残すため、新表示契約は新構文経路に限定されている。全経路の契約整理、短射の発射フレームと寿命・回復時刻の対照、イベント蓄積の長時間評価を継続Buildで確認する必要がある。

## Decisions already made

- D-017：二攻撃ボス、境界回復、死亡優先、先頭retry、両時計・表示契約。
- D-019：旧集計の適用終了、共有回帰保持、対応botのhearts別FPS比較、実測後Designer判断。
- D-021：現状repo/とStudio内テキスト実行で進める。実機・sha・費用承認を再取得しない。

## Constraints

第1〜4部屋と共有戦闘規則を保持する。新戦闘入力、ボスcheckpoint、時間合わせのHP・待機、購入・外部委託・追加金銭を追加しない。

未実行を成功と扱わず、fixtureを通常到達証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

新しい仕様質問・開始承認待ちはない。保存後検証と比較・通常ラン測定を実施できる実行roundが必要である。実装残作業は本Findingsの基準表に残す。

## Expected output

Studioは今回の部分成果を保存し、実行可能な継続BuildをGameplay Engineerへルーティングする。全保存版の試験、観測不足、ボス対応bot、文書統合、同一試行実測を完成してstudioへ返す。全成果が揃うまで独立QAへ投入しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_run_driver.py
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
- Previous handoff: goals/G-002-final-boss/31-studio-to-gameplay-engineer.md
