---
kind: handoff
goal: G-002
seq: 36
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 36: gameplay-engineer → studio — 保存本文を照合、追加契約試験と文書を出力、統合は未完了

## Task

本出力のEDITを適用し、残る観測・bot・契約試験の実装を継続する。実行枠が使える操作では保存版suite、両FPSの対応bot、正規撃破による同一試行測定を実施し、完成資料をStudioへ返す。

## Context

35は34の短射修正の保存確認と統合Build完成を要求した。今回のoperation headerもtests／trace／botsの残数0を明示している。D-021の開始承認は有効で、指定sha・実機・費用承認を再取得する必要はない。

本Stepの根拠はパケット本文である。実ファイル読取、shell実行、@runの新規実行は行っていない。ファイル変更はStudioの出力プロトコルによるEDITとして提出する。

## Findings

### 保存版と未保存提案の照合

提供された正規のrepo/game.pyには、短射生成時のborn_frame設定と、同じframeの移動・加齢を省略する処理がある。正規のtest_boss_contract.pyには34の2試験がある。したがって、パケット上では34の保存対象が存在する。

末尾の「proposed in a run round; not written」は保存版と区別した。run_driver.pyの保存版BUILDは0.6-g002-public-32であり、提案の36aへ更新されていない。提案版の追加5試験も正規テスト本文にはなかった。

### 本出力の変更

| 対象 | 内容と仕様根拠 |
|---|---|
| tests/test_boss_contract.py | 短射の次frameで3/fps移動・1/fps加齢を明示assert。B4 |
| 同上 | 未保存提案の追加5試験を今回の保存対象として提出。低HPで各攻撃3回の交互順、両攻撃の距離0照準、直交1 tile回避、全phase非致死swipe不変、致死予兆swipeによる新発動抑止。B1／B2／B5／B8 |
| manual.md | 公開run／room構文、両時刻、driver時計、pause／resume、attempt／retry、ボスと危険範囲、旧構文経路の制限を統合。旧5番spitter説明を4番へ限定 |
| README.md | Session／公開driver導線、未検証状態、現dodgerのボス非対応を明記 |
| public-driver.md | 文書統合済み範囲と未完了事項を更新 |

可視挙動の新規変更はない。試験が要求する可視挙動は仕様§3の攻撃順・照準・横移動・非中断・致死時停止で定義済みである。文書は既存実装の構文と承認仕様を説明し、経路の不足を明記する。ゲーム内容、共有パラメータ、既存1〜4番のbot方針は変更しない。

### 実行証拠と対象識別

新たに実行したコマンドはない。保存後suite、trace、botsは未実行である。

| 供給結果 | コマンド | 実結果 | 帰属 |
|---|---|---|---|
| @run-results Round 1 | python3 -m unittest discover -s tests | Exit 0、98 tests、0.184秒、OK | 対象ソース明細なし |
| Round 2 | 同上 | Exit 0、103 tests、0.191秒、OK | 未保存提案との対応未確定 |
| Round 3 | 同上 | Exit 0、103 tests、0.192秒、OK | 本出力後の結果ではない |

これらを本EDIT保存後の成功には帰属させない。34が挙げた96／102件も今回へ転用しない。

今回の対象は「35パケットの正規repo本文＋36の4ファイルEDIT」で特定する。これはソース集合の記述であり、計算済みhashではない。公開BUILD文字列だけでは戦闘修正や今回の試験変更を識別できない。次の測定では実行対象のgame.py、session.py、play.py、run_driver.py、bots.py、testsを含むソース識別を取得し、入力と結果へ付ける必要がある。識別文字列だけを変更した未保存36a提案は採用しない。

### 基準別の対応と不足

以下は試験対応であり、合格判定ではない。全項目で今回の保存後実行が必要である。

| 基準 | 対応 | 未完了 |
|---|---|---|
| R1 | mode runと正規配置入場 | 正規敵撃破による1→5連続到達、player証拠 |
| R2 | test_gameの1〜4配置assert | パラメータ・共有回帰の細目照合 |
| R3〜R5／C1 | Session回復・境界・時計、driver入力fixture | 反応記憶、入場表示と入力順序、通常ラン対照 |
| B1 | 初期状態、今回の低HP攻撃順 | 通常HP時の反復対照 |
| B2 | 予兆時間・固定方向、今回の距離0 | player表示との対照 |
| B3 | 既存突進距離・壁・全active試験 | 毎frame位置とフェーズの記録 |
| B4 | 保存済み2試験＋次frame移動・加齢assert | 部屋端、弾ID、接触／吸収／終端を含む全消去理由 |
| B5 | 今回の両攻撃の直交回避 | 公開入力列と表示の対照 |
| B6・B7 | 保護接触の一部既存fixture | 両攻撃の実dash接触、保護終了後無傷と次攻撃命中 |
| B8 | 今回の全phase非致死比較・致死予兆抑止 | 致死active等と公開文言対照 |
| B9 | 既存4回反撃fixture | 接触無害、正規試行中の実反撃記録 |
| B10 | 接触方式維持 | 両攻撃の帯内・帯外・上端と軌道記録 |
| T1〜T4 | Game終端・Session retry等 | 実勝利／死亡retry、旧未来入力・反応記憶、終端2秒統合確認 |
| C2 | dash・予約攻撃・境界pause | ボス予兆・保護途中pause、再開後対照 |
| C3 | limitと結果の別字段 | 勝利／死亡同frame limit |
| V1 | 公開player／trace、今回文書統合 | 旧構文boss表示、即時表示全契機、イベント識別・弾観測、長時間蓄積 |
| D-019 | 旧13撤去、保持比較assert | ボス対応dodger、3／2 hearts別両FPS比較、独立3・4全bot報告 |
| 共有回帰 | 既存test_game | combat1〜11・17〜21、step68、step72 R3-1〜10、step94 W1〜8の未網羅条件 |
| V2 | D-021に従い今回の実機検証対象外 | 実機対応済みとは主張しない |

旧assert移行は維持する。配置は1〜4保持・5をB1へ置換、CueGapは4と共有ケース保持・旧5をB2／B4へ置換。旧13集計は適用終了。独立1〜2比較、3・4のdash、1〜4のdodger FPS比較は保持し、新5は対応bot比較とB5／B6へ接続する。過去Decisionは変更しない。

### 測定条件と値

測定値は未取得。独立3・4の全bot×両FPS、新5番の対応dodger開始3／2 hearts別比較、通常ラン同一試行の値はない。通常ランの部屋時間、4遷移、ボス入場hearts、被弾、反撃、終端、retry、pause、processing実時間も未取得である。

現dodgerはboss専用の危険線・回復方針を持たず、その数値をD-019比較に使えない。現bots CLIは開始2 heartsを指定できない。対応実装では独立1〜4方針を保持し、公開観測だけを入力とするboss方針と開始hearts指定、clear／death／unfinishedの明示が必要である。

### 実行経路の阻害条件と解決担当

今回の@run残数0は操作ヘッダーの直接情報である。新しい@run呼出しは行わず、上限回復を仮定しなかった。供給結果はあるが保存後対象への帰属が不足している。代替shellやPython経路が利用可能との確認もない。read-only設定自体を実行不能の理由にはしていない。

Gameplay Engineer内で解消できるのはコード・試験・文書の残作業であり、本Stepでは試験と文書を進めた。実行不能はbot・観測実装の未完了理由にはならず、それらも引き続き実装が必要である。Studioは実行基盤側へ、保存後のソースと入力を対象にしたtests／trace／bots枠を割り当てる必要がある。Ownerの開始承認を再取得する作業ではない。

### 再現手順

1. 36のEDITを適用後、repo/でpython3 -m unittest discover -s testsを実行し、対象ソース識別、実件数、失敗を記録する。
2. test_boss_contract.pyの保存済み2試験と今回の5追加試験を両FPSで確認する。fixtureをR1証拠へ転用しない。
3. manualのmode room／room 5例をfps30／60、player／traceで実行し、旧構文room 5との差とV1不足を記録・修正する。
4. 公開観測のみのboss dodgerを実装し、反応0.15秒、同一方針・limit・初期位置・向きで開始3／2 heartsを別比較する。独立3・4の全bot値と保持する1〜2比較・3〜4dashを別報告する。
5. 正規敵のみを倒すmode runをまずlimit1200で測定する。同一試行のrun／room時刻、driver秒、processing秒を分離し、pause・terminal待機を戦闘時間に加えない。死亡・未完了も報告する。
6. retryとpauseを公開制御で記録し、入力・結果・ソース識別を完成資料へ結び付ける。

統合Buildは未完成で、独立QAへの投入準備は整っていない。15〜20分との整合、攻略不能・到達不能は測定なしでは判断しない。自己承認しない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。実機・指定sha・費用承認の再取得は不要。

## Constraints

第1〜4部屋と共有戦闘ルールを保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託・追加金銭を加えない。未実行を成功としない。fixtureや独立部屋時間の合算を通常ラン到達・時間の証拠にしない。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

新しい仕様質問やOwner承認待ちはない。Studioが解消すべき実行依存は保存後対象に使える@run枠である。Role内にはbot・観測・契約網羅の実装未完了が残る。今回の文書・試験提出だけで完成扱いにしない。

## Expected output

Studioは36の変更を保存し、観測・対応bot・不足試験を継続Buildへ渡す。実行枠を伴う操作でソース識別付きの保存後suite、両FPS比較、同一試行測定を取得する。完成資料を受けてStudioが独立QA投入可否を判断する。

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
- Project: repo/tests/test_boss_contract.py
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
- Previous handoff: goals/G-002-final-boss/35-studio-to-gameplay-engineer.md
