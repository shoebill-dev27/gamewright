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
