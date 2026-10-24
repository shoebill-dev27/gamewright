---
kind: handoff
goal: G-002
seq: 75
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 75: studio → gameplay-engineer — E1接続と公開再生差の診断を継続

## Task

68§4・71・73のE1を継続する。公開境界を実dodgerへ接続し、既存suite互換、記憶の寿命・初期化、全分岐監査、対象別判断本文を整える。未保存接続案で発生した公開再生の被弾差を診断し、既存assertを弱めない。

## Context

74はE1 partial。E1の連続partialは72・74の2回である。70はE0棚卸しであり同じE1の回数には含めない。新しい入力不足・仕様質問はなく、同Roleで継続する。次もE1 partialならStudioはTechnical Directorへ分割・再計画を戻す。

60のfailを維持する。E2以降と独立QAは今回開かない。

## Findings

保存済み集合はsource b0770a4180c9、runtimeで159 tests OK。実dodgerは未接続であり、公開情報条件の完成を示さない。

74の保存変更はescape候補列挙と限定adapter監査。次の2IDをQ1主担当・Q4にも配布する。

- test_bots_boss.PublicBoundaryAuditTest.test_all_escape_candidates_are_enumerated
- test_bots_boss.PublicBoundaryAuditTest.test_adapter_rejects_forbidden_attribute_reads

72のPublicBoundaryPrototypeTestの3IDも同じ配布先で保持する。71の13ファイル配布台帳を維持し、追加試験を完全IDで追跡する。

未保存接続案source eddd95dd5926／189dbf689d7eは不採用。いずれもtest_split_c.SplitCTest.test_public_normal_pause_victory_retry_death_retryでfirst["hits"]の期待0に対し1だった。切断された出力を補完したり、両集合を接合したりしない。保存済み集合を出発点とし、必要な変更は供給された現行本文から実施する。

今回の未完了事項：

1. 実dodger、直接呼出、_Proxy、通常runを公開観測と記憶だけによる判断経路へ接続する。共有補助関数から未表示値へ戻る経路も監査する。
2. warning履歴の所有・寿命、active中の保守的な全経路保持、履歴なしactiveの最大範囲、recovery解除、入場・retry初期化を実経路で試験する。
3. 両FPS・両攻撃で距離0・境界・端点・全壁・dash待ち・stun・履歴不足各方向を検査する。同じ公開入力で内部値だけを変えた判断不変と許可外参照禁止を示す。
4. 判断番号、grid、時刻、公開入力、記憶由来、候補・除外、選択、実発行ボタン、stun省略を短い列で記録する。限定adapter試験を全実経路監査へ読み替えない。
5. 状態・判断emit_rowsアダプタと、窓helperの確認本文を外側へ出す。全件評価と表示範囲を区別する。
6. 接続時の公開再生被弾差を、生成入力・再生入力・接触条件で診断する。診断用内部観測を判断へ戻さない。E5の本測定・再生成を先取りせず、E1互換確認として対象を限定する。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較。
- D-021・D-023：Studio内テキスト検証、個別Load、@need一度最大8件、@run最大3回、各出力最大2万字。全文保存先・変更前ビルドなし。
- D-022：表示・弾・長時間観測契約を保持。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離。
- 68：E1完了確認後にE2を別Handoffで開く。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、表示契約、Goal範囲を変更しない。独立1〜4方針を保持する。

書込対象はrepo/bots.py、repo/tests/test_bots_boss.py、repo/tests/test_split_c.py、repo/tests/test_g002_evidence.py。test_split_c.pyはE1接続・互換・対象別出力に必要な範囲のみ。既存assert・対象集合を削除、緩和して成功させない。他ファイル変更が不可欠なら対象と理由を返す。

固定コマンドはrepo/で `python3 -m unittest discover -s tests`。最大3回以内。出力は概ね12000字以内を目指し、BEGIN/END、列定義、連番、総件数・表示件数・未表示・除外を明示する。再実行の入力・source_id・総判断数を照合し、異なる集合を接合しない。

60のfail、未表示・切断、歴史的確認不能を自己確認で上書きしない。source_idと件数で必要な本文を代替しない。

## Open questions

新しい仕様・Owner供給質問はない。公開再生被弾差の原因、実経路監査・記憶・全分岐・判断本文が既知の残作業である。原因が仕様の曖昧さや計画不成立に当たる場合は、権限を越えて決めず具体的に返す。

## Expected output

studio宛Handoffに変更ファイル、公開フィールド対応、全呼出経路の監査範囲、完全試験IDとassert、被弾差診断、状態・判断本文、実行条件、コマンド、source_idと識別対象、未表示範囲を記録する。自己評価・理由はSender assessmentへまとめる。

13ファイル配布台帳と追加5IDを保持し、新規ID・変更件数・配布先を追記する。70の後続残作業を消さない。E1完了、E2以降、独立QA、Goal達成を区別する。

既知の残作業はpartialで返す。その場合はE1連続partial 3回目としてTechnical Directorへ分割・再計画を戻す材料として、完了部分、依存関係、未成立条件、次の実装単位を明示する。Ownerへ同じ供給質問を戻さない。

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
- Supporting handoff: goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/74-gameplay-engineer-to-studio.md
