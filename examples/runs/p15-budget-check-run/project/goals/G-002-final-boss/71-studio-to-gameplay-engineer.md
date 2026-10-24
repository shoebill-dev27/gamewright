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
