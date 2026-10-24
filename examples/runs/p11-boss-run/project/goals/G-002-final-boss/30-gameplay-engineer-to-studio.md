---
kind: handoff
goal: G-002
seq: 30
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 30: gameplay-engineer → studio — Session基盤を保存、統合と測定は未完了

## Task

Session基盤と境界試験を保存する。統合Buildは未完了であり、独立QAへ渡さず、残る公開経路の実装と実行測定をGameplay Engineerへ継続ルーティングする。

## Context

Goalは既存第1〜4部屋から第5部屋の単体ボスへ進み、最終勝利・死亡・先頭retryを成立させること。29の継続Buildを受けた。D-021の開始承認は有効であり、供給・実機・費用承認の再取得は必要ない。

## Findings

### 保存成果

パケット内で「proposed in a run round; not written」とされた次の2ファイルを、今回の出力で保存する。

- `repo/session.py`：RunSession。Gameと進行を分離し、combat／room_clear／won／dead、独立pauseフラグ、部屋境界1秒、上限3の1 heart回復、両ゲーム時刻、終端retry、入力拒否、limitと戦闘結果の別記録を追加。
- `repo/tests/test_session.py`：境界fixtureの8試験。30/60 FPS、hearts1/2/3、境界での戦闘状態初期化、0 hearts死亡、dash中予約攻撃のpause保持、境界pause、retry初期化、limit同フレーム結果、非終端retry拒否を扱う。

Session実装と8試験の実行部分は、パケット内の提案と同じである。Sessionのdocstringは、driver側で必要な反応記憶初期化と試行別入力処理が未実装であることを明記した。

### プレイヤー可視挙動と根拠

公開driverへ接続したときに生じる挙動を実装前の照合対象として列挙する。今回、その公開接続は完成していない。

| 挙動 | 根拠 | 今回の範囲 |
|---|---|---|
| 生存クリアから1秒後に次部屋へ移り、1 heart回復 | 仕様§2、R3、R5 | Session内部処理とfixture |
| 入場で位置・移動・戦闘タイマーを初期化 | 仕様§2、R4 | 新規Game生成。反応記憶はdriver側未接続 |
| pause中は戦闘と境界時刻を停止 | 仕様§5、C2 | Session内部処理。外部driver時刻未接続 |
| 勝利／死亡後のretryで第1部屋へ戻る | 仕様§4、T4 | Session内部処理。試行別script未接続 |
| limitは勝敗と別の実行停止理由 | 仕様§5、C3 | 内部字段。公開表示未接続 |

新しい戦闘入力、チェックポイント、HPや待機による時間調整は追加していない。

### 提供された実行結果

コマンドはいずれも `repo/`での `python3 -m unittest discover -s tests`。

| パケットの記録 | 結果 |
|---|---|
| Round 1 | Exit 0、81 tests、0.164秒、OK |
| Round 2 | Exit 0、89 tests、0.173秒、OK |
| Round 3 | Exit 0、89 tests、0.170秒、OK |

これらは今回パケットに供給された実行記録であり、この応答内で再実行した結果ではない。Round 2・3の89件と追加8試験の件数は整合するが、ログには対象ファイル一覧やbuild識別がない。保存後の全成果に対する独立検証済みとは扱わない。

実行round残数は0。今回追加のtests・trace・bots要求は行っていない。trace・bots・通常ランの実行結果はパケットにない。

### 基準別の到達範囲と残作業

| 基準 | 保存済みの対応 | 未達 |
|---|---|---|
| R1 | なし | 正規敵撃破による同一試行1→5到達 |
| R2 | 前保存版の1〜4配置assert保持 | 独立QAでの回帰確認 |
| R3 | hearts1/2/3→2/3/3、0死亡fixture | 公開入場回復表示 |
| R4 | Game再生成とgeneration更新 | driverの反応時刻・盤面・メッセージ初期化 |
| R5、C1 | 1秒境界、ランのみ進むfixture | 期限入力破棄、入場同時刻入力、公開両時刻 |
| B1〜B10 | 前保存版のボス9試験を保持 | 28記載の攻撃順、距離0、全軌道、横移動、実dash接触、次攻撃、全phase、接触帯の不足 |
| T1〜T3 | Game終端基盤とSessionのwon/dead分岐 | 実際の勝利／死亡からのSession凍結統合試験 |
| T4 | 終端状態fixtureからretryし初期Game一致 | 実終端からのretry、旧未来入力・反応記憶破棄 |
| C2 | dash予約攻撃と境界の停止fixture | 予兆・保護中pause、独立driverからresume |
| C3 | limitと状態を別字段で保存 | 勝利／死亡同フレーム試験、公開停止理由 |
| V1 | 未接続 | 仕様§6の常設情報、全文言、即時描画、弾数 |
| V2 | D-021により今回の実機検証対象外 | 製品実機対応を検証済みとはしない |
| D-019 bot比較 | 独立1〜4の既存方針保持 | ボス対応dodger、開始3／2 hearts別FPS比較、独立3・4報告 |

T4の試験はstateをfixtureで設定している。通常ラン完走や実際の終端遷移を立証しない。

### 未完成の具体的な統合箇所

`play.py`は引き続きGameを直接生成し、RunSessionを利用していない。したがって通常のCLIから連続ラン、pause、retryを実行できない。`mode`、`attempt`、`control`、`limit`、`driver-limit`のparserとdriverを実装する必要がある。既存60秒上限も残っている。

`bots.py`はボス予兆・回復を読む専用方針がない。既存botのroom5結果をD-019の対応bot比較へ流用してはならない。manual／READMEにも新契約は未反映。

弾ID、発射・接触消費・終端消去理由、毎フレームtrace、build識別も未完成。Sessionイベントは試行・部屋・両時刻・frame・通番を持つが、これだけでPlan16の観測契約全体を満たさない。

### 次の実装・再現手順

1. 保存後に `python3 -m unittest discover -s tests` を実行し、89件の対応と失敗有無を確認する。
2. Plan16の公開構文をparserとdriverへ接続する。同時刻順序、制御先行、反応記憶初期化、境界／pause中入力破棄、試行別未来入力破棄を試験する。
3. player／traceを同じSession状態へ接続し、仕様§6の表示と全即時描画契機、毎フレーム観測、長時間limitを完成する。
4. B1〜B10、実終端からのT試験、C試験の不足を補完する。共有回帰と旧assert対応は28および仕様§8を保持する。
5. 公開観測に基づくボス対応dodgerを追加し、manual／READMEを更新する。
6. 同一build・方針・初期状態・limitで、独立5番開始3／2 heartsをそれぞれ30/60 FPS比較する。独立3・4は全bot×各FPSで条件と値を報告する。
7. 正規敵撃破による通常ランを実行する。同一試行の部屋別時間、遷移、ボス入場hearts、被弾・反撃、終端、retry、pause、処理実時間を記録する。

測定条件と値は未取得。独立部屋の時間合算や今回のfixtureを通常ラン実測へ転用しない。

### Sender assessment

統合Build完成要求は未達。今回の成果は、未保存だったSession基盤と8試験を保存対象へ明示した部分成果である。実装継続が必要であり、自己試験のgreenをQA判定へ置き換えない。

実行round枯渇は追加測定の阻害要因である。公開driver、表示、対応botの未実装は実装残作業であり、round枯渇だけを原因として説明しない。明白な攻略不能・到達不能を示す測定証拠もない。

## Decisions already made

- D-017：単体ボス、境界回復、死亡優先、先頭retry、時刻と表示契約。
- D-019：旧集計終了、共有回帰保持、対応botのhearts別FPS比較、実測後Designer判断。
- D-021：現状repo/とStudio内のテキスト実行を使用。実機・費用供給の再承認は不要。

## Constraints

第1〜4部屋と共有戦闘ルールを維持する。新戦闘入力、ボス専用チェックポイント、時間合わせだけのHP・待機、購入・外部委託・追加金銭を追加しない。

未実行を成功と扱わず、fixtureを通常到達の証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

新しい仕様質問・開始承認待ちはない。追加実行roundを持つ継続Buildで、残る実装と測定を完了する必要がある。

## Expected output

Studioは部分成果を保存し、Gameplay Engineerの統合Build継続へ戻す。公開driver、表示、対応bot、必要試験、説明更新、同一試行の実測が揃うまで独立QAへ投入しない。

次のHandoffでは変更ファイル、基準対応、実行対象、コマンドと実結果、測定条件と値、未達事項を明確に区別して報告する。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
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
- Previous handoff: goals/G-002-final-boss/29-studio-to-gameplay-engineer.md
