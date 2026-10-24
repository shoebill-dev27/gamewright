---
kind: handoff
goal: G-002
seq: 67
from: technical-director
to: studio
stage: Route
outcome: done
---
# 67: technical-director → studio — 供給上限に適合する直列検証計画

## Task

62の供給・証拠保存計画を本計画へ置き換え、試験道具対応、再測定、保持回帰、通常入力再生成、独立QAを直列にルーティングする。歴史的一致の確認不能は保持し、観察工程への技術上の進行とGoal達成判断を分離する。

## Context

60のfailは維持する。D-023は個別ファイル本文、各Stepの@need一度最大8件、@run最大3回、各実行出力最大2万字を供給条件とした。全文保存先と変更前ビルドは存在しない。

D-024は歴史比較、記録比較、現行検証を分離した。本Stepはpacket本文だけによる再計画であり、製品変更、実行、source識別の独立再算出、測定、QA判定は行っていない。技術計画skillの影響整理・依存順・リスク・試験戦略・並列可否の手順を適用した。

## Findings

### 1. 置き換える開始条件

変更前ビルド探索、全文ログ保存先の確保、全文の後続再読込みを開始条件から外す。別の実行枠も要求しない。

代わりに、各Stepは必要本文を個別Loadし、必要な証拠を2万字以内に出す試験単位を用意する。出力は原則1万2千字以内を設計目安とし、余白を失敗診断と実行器の付加情報に残す。これはゲームの受入基準ではない。

今回確認できるtests本文は4ファイルだけである。全testsのファイル名はpacketにないため、未知の名前を作らない。`repo/tests/`を@needへ再指定しない。最初のEngineer Stepで実在する全テストファイル名を列挙し、後続Loadを確定する。

### 2. 影響システムと技術方式

変更対象は原則としてbot、診断、試験、証拠出力である。ゲーム本体の規則・パラメータとplayer表示を変更する計画ではない。

- `bots.py`：ボス判断を公開情報だけの観測データへ隔離する。判断関数へGame／Enemyや任意属性転送proxyを渡さない。自己操作状態を含め、使用する全項目の公開根拠を明示する。
- ボスactive突進：warningで観測した固定経路を保持し、公開されたrecovery等の状態変化まで保守的に扱う。内部`phase_left`による残長短縮を除く。warning履歴なしでactiveから始めるfixtureは履歴不足を明示し、公開位置・方向・固定最大範囲に基づく保守的扱いを試験する。
- 全判断経路：接近、警告、active、回復、実弾、停止、反撃、dash可否、stunによるskip、部屋入場・retryの記憶初期化を監査する。問題の一分岐だけ直して全体適合としない。
- `_hurt_lines`等：ボス突進をshot診断から分ける。診断は内部状態を読んでよいが、判断へ戻さない。
- `test_split_c.py`：新botで入力を再生成する。旧の固定pause時刻・retry時刻・driver終了時刻が成立するとは仮定しない。実測されたclear区間・終端後に制御を置き、条件をassertする。
- `source_id.py`：現在の6ソースと全testsを識別する。tests追加・修正でも識別が変わるため、測定後の修正は影響範囲の再測定とQA再照合を要する。

### 3. 共通証拠契約

各証拠行または短いケースブロックに次を持たせる。

| 字段 | 内容 |
|---|---|
| identity | 基準ID、ケースID、現在source_id、bot方針版、試験関数名 |
| conditions | FPS、mode、部屋、開始hearts、位置・向き、通常状態／fixture、limit、driver-limit |
| input | 完全な短い入力、またはLoadされた生成関数と生成条件。長い通常入力は区間ごとの完全本文を直列で渡す |
| assertion | 条件、比較演算、期待仕様、実測値。成功件数だけにしない |
| observation | 対象イベント・状態の本文、時刻・frame、表示との対応 |
| scope | 全件機械検査した範囲、表示した範囲、未表示範囲、未実行条件 |
| result | 現行検証／現行内対照／記録比較／歴史確認不能を別字段にした結論 |

source_idは実行集合の識別であり、正しさや未閲覧本文の代用ではない。QAはその計算経路と実行時識別を独立確認する。

判断全件検査は、各判断に連番、公開観測、保持記憶、候補、計算根拠、選択操作を付ける。全件に対して許可字段、判断再実行一致、0.15秒間隔、禁止参照なしを検査する。表示は連番の連続区間に分け、冒頭・末尾番号、総件数、欠番・重複を示す。全判断本文を人が読んだとの主張は、全区間が後続Stepで表示された場合に限る。

診断は被弾・接触ごとに、移動前後のplayer／boss位置、固定方向、実距離、横ずれ、保護状態、接触消費前後、hurtイベントを出す。接触の直前・当該・直後フレームと保護終了・次攻撃までのassertを対応付ける。推定ETAを実接触距離と混同しない。

### 4. 直列Stepと実行配分

以下はStep種別であり、Studioが後続seqを割り当てる。各Stepの上限は3回。出力が収まらなければ対象を縮めて同Roleのpartial継続とし、切断部分を既読にしない。

| 単位 | 担当・作業 | 最大3回の配分 | 完了条件 |
|---|---|---|---|
| E0 | Engineer：実在tests台帳、基準対応、出力道具の準備 | 1: tests一覧・source識別・ケース一覧、2:短い出力自己試験、3:必要な修正確認 | 全testsを個別名で列挙。各保持／置換基準にfixture・assert・担当単位を割当。未実装ケースを明示 |
| E1 | Engineer：公開観測境界と全判断経路の対応 | 1:禁止字段アクセス・内部値変更不変、2:warning→active→recovery・距離0・壁・dash待ち・stun、3:境界／retryと既存部屋への影響 | 全判断経路が公開根拠で説明でき、内部残時間を変えても同じ公開入力なら判断不変 |
| E2 | Engineer：突進診断と不足fixture | 1:30 FPS通常被弾・保護接触・非接触、2:60 FPS同条件、3:ログ有無一致・診断誤分類・全suite | 実接触・消費・保護終了後・次攻撃が追跡可能。診断が判断・結果を変えない |
| E3a | Engineer：独立5番、開始3 hearts再測定 | 1:30 FPS、2:60 FPS、3:比較と差の制御診断 | 同一保存ソース・方針・初期状態・limitで結果と判断範囲を報告 |
| E3b | Engineer：独立5番、開始2 hearts再測定 | E3aと同じ | hearts別のFPS比較を完結。3 heartsと混ぜない |
| E4a | Engineer：独立1〜4 dodger保持 | 1:30 FPSの4部屋、2:60 FPSの4部屋、3:記録比較・FPS比較・差の診断 | 40との指定精度比較、combat14／15／16c、全条件を報告 |
| E4b | Engineer：walker／camper等保持 | 1:30 FPS、2:60 FPS、3:終了・ログ有無・brute等の回帰 | 独立1〜2のcombat14、独立3・4各bot成績、判断差の由来を報告 |
| E5a | Engineer：新通常ラン入力と30 FPS公開再生 | 1:新bot生成・入力区間出力、2:公開driver再生の状態／イベント対照、3:player表示対照 | 正規敵を実際に倒した到達、同一試行時間、pause・勝利retry・自然死亡retryを証拠化 |
| E5b | Engineer：60 FPS公開再生 | E5aと同じ | 両FPSを別々に完結。旧生成時間を期待値にしない |
| Q群 | 独立QA：下記の基準単位 | 原則1:30 FPS、2:60 FPS、3:不足条件または差の診断 | 本文・assertを独立照合し、対象基準だけ判定 |

E3の共通limitはまず現行試験の120秒とする。これは撃破秒数ゲートではない。unfinishedや比較不一致があれば理由を診断し、必要なlimit再評価をDesignerへ返す。clearを事前assertして失敗データを失わず、death／unfinishedも出力する。

各測定は最低1試行／条件、件数を明示する。決定的botの1試行を成功率と呼ばない。判断本文が長ければE3をFPS・hearts・判断連番区間ごとに追加分割する。同一入力から再実行し、対象外の行を出さないことで出力量を制限する。

E4aの時間比較はフレーム由来の未丸め時間を最も近い0.1秒へ、中間は大きい側へ丸める。現行`play_room`の小数2桁値にさらにPythonの`round`を重ねる方法は、所定の丸めを保証しないため置き換える。攻撃回数は別の現行観測として報告し、40の記録値と呼ばない。

E5で完走しなければ、それを残してDesignerへ返す。観測用fixtureや独立部屋時間の合算で通常到達を補わない。長い入力・player出力は部屋区間に分割し、全区間を直列継続する。

### 5. 独立QAの分割と判定範囲

QAはE群の自己評価を合否根拠にせず、実ソース・試験本文・自分の実行を使用する。各Q単位は別Stepにし、必要ならさらに基準単位へ分ける。

| 単位 | 基準・主な証拠 |
|---|---|
| Q0 | 全tests台帳の被覆監査、旧5番試験の保持／置換追跡、source計算、未割当assertの検出 |
| Q1 | 公開情報境界、全判断経路、診断分離、E3の4条件比較。判断区間が残れば同Role継続 |
| Q2 | B1〜B5：攻撃反復・低HP・固定照準・距離0・壁・移動・弾寿命・直交回避 |
| Q3 | B6〜B10：実接触dash、保護終了、全フェーズswipe、4反撃、帯内外・上端 |
| Q4 | R2〜R5・C1：構成、hearts1/2/3/0、全リセット、境界入力、両時刻 |
| Q5 | T1〜T4・C2〜C3：残弾、同フレーム優先、終端2秒、retry、pause各対象、limit |
| Q6 | R1・V1：新入力による通常到達とplayer／状態対照。部屋区間ごとに継続可 |
| Q7 | combat1〜11・17〜21、cap一般境界、step72 R3-1〜10保持。量に応じgrub／spitter／room3へ分割 |
| Q8 | step68・step94の現行文字列・反応・表示順・方向。歴史比較列を分離 |
| Q9 | D-022 L・S・O：注記、弾ライフサイクル、周期・summary・拒否・長時間。L／S／Oへ分割可 |
| Q10 | E4の保持記録・FPS比較、各bot報告、全Q結果の被覆統合、歴史確認不能一覧 |

O6は30／60 FPSの各1200秒を実行する。survival fixtureは観測容量の検証と明記し、通常到達には使わない。試験内で出力全体を一時捕捉して周期件数・イベント欠落・終了までの処理をassertし、表示には数え方、区間、代表本文、最終状態を出す。この方法は外部全文保存や全文閲覧を証明しない。必要な表示本文は別の短いケースで照合する。

旧未来入力破棄は、直接pending破棄の観測、または新attemptが旧入力時刻を越えた条件で確認する。141秒の既存再生だけで1100秒入力の不発を証明しない。

### 6. Load案と追加本文の配置

全E／Qに共通して個別指定する資料：

- `project.md`
- `design/final-boss-and-continuous-run.md`
- `design/g002-historical-comparison-evidence.md`
- `decisions/D-019-g002-balance-criteria-applicability.md`
- `decisions/D-021-owner-authorizes-text-build.md`
- `decisions/D-022-g002-v1-supplements.md`
- `decisions/D-023-owner-confirms-verification-supply.md`
- `decisions/D-024-g002-historical-comparison-evidence.md`
- 本Handoffと各Stepの直接前任Handoff
- 各担当Roleとそのskill

以下を単位ごとの追加Loadとする。各項目は個別ファイル指定であり、ディレクトリ・glob指定で代用しない。

| 単位 | 個別ファイル |
|---|---|
| E0 | `repo/source_id.py`, `repo/game.py`, `repo/session.py`, `repo/bots.py`, `repo/play.py`, `repo/run_driver.py`, `repo/tests/test_bots_boss.py`, `repo/tests/test_split_c.py`, `repo/tests/test_d022_observation.py`, `repo/tests/test_d022_shots_and_note.py`, `design/combat.md`, `design/combat-step68.md`, `design/combat-step72.md`, `design/combat-step94.md` |
| E1 | `repo/bots.py`, `repo/game.py`, `repo/session.py`, `repo/play.py`, `repo/run_driver.py`, `repo/source_id.py`, `repo/tests/test_bots_boss.py`, `repo/tests/test_split_c.py` |
| E2 | E1の各ファイルに加え`repo/tests/test_d022_shots_and_note.py` |
| E3a・E3b | `repo/bots.py`, `repo/game.py`, `repo/play.py`, `repo/run_driver.py`, `repo/source_id.py`, `repo/tests/test_bots_boss.py`, `repo/tests/test_split_c.py`とE1・E2で作成した試験ファイルの個別名 |
| E4a・E4b | `repo/bots.py`, `repo/game.py`, `repo/source_id.py`, `repo/tests/test_split_c.py`, `design/combat.md`とE0台帳中のbot回帰試験の個別名 |
| E5a・E5b | `repo/bots.py`, `repo/game.py`, `repo/session.py`, `repo/play.py`, `repo/run_driver.py`, `repo/source_id.py`, `repo/tests/test_split_c.py`, `repo/manual.md`, `repo/public-driver.md` |
| Q0 | `repo/source_id.py`、6ソースの各個別名、E0台帳にある全testsを分割Load |
| Q1 | E1・E2・E3の各ソース／試験個別名、対応判断区間を含むEngineer Handoff |
| Q2・Q3 | `repo/game.py`, `repo/bots.py`, `repo/play.py`, `repo/run_driver.py`、E0台帳のB対象試験個別名 |
| Q4・Q5 | `repo/game.py`, `repo/session.py`, `repo/play.py`, `repo/run_driver.py`、E0台帳の境界・終端・制御試験個別名 |
| Q6 | E5の個別ソース、`repo/tests/test_split_c.py`, `repo/manual.md`、生成入力の全区間 |
| Q7 | `design/combat.md`, `design/combat-step72.md`, `repo/game.py`, `repo/play.py`、E0台帳の共有・cap・room3試験個別名 |
| Q8 | `design/combat-step68.md`, `design/combat-step94.md`, `repo/game.py`, `repo/play.py`, `repo/run_driver.py`, `repo/manual.md`、E0台帳の文言・反応試験個別名 |
| Q9 | `repo/game.py`, `repo/session.py`, `repo/play.py`, `repo/run_driver.py`, `repo/manual.md`, `repo/tests/test_d022_observation.py`, `repo/tests/test_d022_shots_and_note.py` |
| Q10 | `repo/bots.py`, `repo/source_id.py`, `repo/tests/test_split_c.py`、bot回帰試験個別名、各QのHandoff |

未知のテスト名を含む欄は現時点ではLoad確定ではない。E0は実在一覧を必ずHandoff本文に出し、Studioが各名称を上表へ展開してからRouteする。各testsファイルを少なくとも一つのQ単位へ割り当て、複数領域なら関連単位すべてで読む。対象外ファイルも理由を記録する。

@needは各Stepの不足最大8件にのみ使う。8件を超える未読本文があれば、最初から追加の直列Stepへ割り当てる。全文が巨大な単一テストファイルなら、Engineerが意味を変えず領域別ファイルへ分け、source変更後に測定をやり直す。未読のままsuite成功で埋めない。

### 7. 記録差とリスクへの対応

独立1〜4の記録差は、FPS・開始状態・limit・方針・現在source・40のsource、未丸め値と指定丸め値、clear／損失／dash、共有関数への変更影響を併記してDesignerへ返す。比較値に合わせてbotや戦闘を調整しない。共有規則違反はQAが別件failとして扱う。

保守的なボス経路保持は成績・反撃機会を変え得る。4条件と通常ランを新しく測り、旧ボス値・旧生成時間をpass基線にしない。帯内差が原因でも比較閾値を自動免除しない。

切断、欠番、予想外の大出力は当該範囲を未確認として残し、対象を狭めて次Stepへ渡す。実行枠を使い切っただけで、入力・機能・本文が揃っている場合はpartialとする。道具が必要観測を出せない場合はEngineerへ、仕様解釈が必要ならDesignerへ返す。

すべて直列とする。bot変更が診断、入力生成、source識別、再測定へ連鎖し、共有作業領域で並列編集すると証拠対象が変わるためである。別の保存機構・外部人員・追加予算は前提にしない。

### 8. 歴史確認不能を残した工程条件

62の「全QA合格後」は、次の条件へ整理する。

1. 独立QAが今回検証可能な現行仕様・現行内対照を必要な両FPSで完了し、規則違反や供給起因の未確認を解消している。
2. 公開情報条件と4条件比較、保持回帰、新通常入力の検証が完了し、記録差があればDesignerの扱いが記録されている。
3. 歴史確認不能を独立した一覧で保持し、全基準pass・Goal達成と呼ばない。
4. Studioが観察の実施とGoal受入を区別してRouteする。

この条件なら、歴史確認不能を残したまま限定Art Verify→独立Play→実測後Designer判断の情報収集へ技術上は進める。確認不能の免除やGoal範囲変更を本計画で決めるものではない。進行にGoal再解釈が必要とStudioが判断した場合は、観察工程を省略せずGame Directorへ判断を返す。

Artによる表示変更後は該当QAを再確認してからPlayへ進む。初回測定で明白な対処不能・到達不能が見つかればPlay前にもDesignerへ返す。

最終ReviewにはL1・L4・O3、step68 V-a／V-bの歴史時点・V-c・V-eの旧結果、step94 W3／W4の旧行動列・W7等、補足仕様の未確認欄をそのまま渡す。15〜20分Visionとの差、試行件数、bot時間と人間体験の区別、難度追加ゲートのDesigner判断も添える。未解決を理由にTechnical DirectorやQAがGoalを縮小しない。

## Decisions already made

- D-019：保持回帰、公開情報限定のボス比較、開始3/2 hearts別FPS比較、実測後Designer判断。
- D-021：Studio内のテキスト・スクリプト方式。実機供給・旧指定sha照合・追加金銭は要求しない。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約。
- D-023：個別本文供給、@need一度最大8件、@run最大3回、出力最大2万字。全文保存先・変更前ビルドはない。
- D-024：歴史確認不能、40の精度での記録比較、現行検証を分離する。
- 新Decisionは作成しない。仕様変更やGoal受入判断を含まない技術再計画である。

## Constraints

60のfailを上書きしない。製品仕様、難度、戦闘数値、秒数ゲート、Goalの意味を変更しない。

未表示・切断部分は確認済みにしない。ハッシュ、summary、成功件数を必要な本文の代用にしない。存在しない全文保存・変更前ビルドを再要求しない。

独立QAは実装者の自己評価から独立させる。独立Playへ実装履歴、QA判定、期待結果、比較値、本Handoff、設計文書のReview用体験信号を渡さない。Playには公開manual、操作方法、中立な試行・記録依頼だけを渡す。

## Open questions

1. E0で列挙される全testsの実在個別名と、未被覆基準は何か。
2. 公開情報だけの判断へ対応した結果、ボス4条件と通常到達はどう変わるか。
3. 40との記録差が出た場合、条件・方針・共有処理のどこへ影響があるか。
4. 歴史確認不能が最終Goal判断を妨げる場合、Game Directorは方向・範囲をどう判断するか。

## Expected output

StudioはまずE0をEngineerへRouteし、全tests実在一覧と基準台帳を得て、以降のLoadを個別名で確定する。その後E1→E2→E3a→E3b→E4a→E4b→E5a→E5b→独立Q群を直列実施する。

各Stepは対象範囲、証拠本文、結論、残作業、未確認をHandoffに保持する。枠内で残作業だけならpartial継続し、仕様・方向判断が必要なら該当Roleへ返す。

現行検証の完了と歴史確認不能を分けて限定Art Verify、独立Play、Designer実測後判断へ進め、Game Director Reviewでは未解決事項を含むGoal判断を求める。全基準passを前提とする既存依頼文はそのまま再利用しない。

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
