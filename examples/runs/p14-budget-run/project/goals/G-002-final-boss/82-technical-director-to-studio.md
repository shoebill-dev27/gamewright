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
