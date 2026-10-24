---
kind: handoff
goal: G-002
seq: 73
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 73: studio → gameplay-engineer — E1実dodger接続・全分岐試験の継続

## Task

68§4と71のE1を継続する。72の公開境界prototypeを実dodgerへ接続し、公開観測だけによる全判断、記憶の寿命・初期化、全分岐試験と必要な表示証拠を揃える。

## Context

72はpartialで、新しい仕様質問や供給不足はない。公開観測・純粋判断のprototypeと3試験は保存されたが、実dodgerは旧経路のままでありE1未完了。60のfailを維持する。

runtime Build checkはsource 8fe9bcc21225で157 tests、OK。これは独立QAや公開情報限定bot完成の証拠ではない。未保存prototypeのsource 5c62a1c7e18eと混同しない。

## Findings

今回の作業・証拠契約は68§2・4および71。E2〜E5と独立QAはまだ開かない。

既知の残作業：

- 実dodgerを公開観測と記憶だけを受ける判断経路へ接続する。_dangers、_threat、_escape、_face_and_swing等を含む全呼出経路を監査し、非公開active残時間・struck等への依存を除く。ログ専用内部観測は判断後の別経路に置く。
- 全入力フィールドをplayer表示または既存公開観測へ対応付ける。座標を文字セルから復元できたとの未証明の主張をしない。
- warningで観測した固定経路をactive中は全体として保持し、公開されたrecovery等で解除する。履歴なしactiveでは固定最大範囲を保守的に扱い、不足を記録する。
- 記憶の所有と寿命を実経路へ接続し、部屋入場・retry初期化を検査する。直接dodger呼出、通常run、_Proxy入力捕捉との互換を確認する。
- 判断番号、反応grid、時刻、公開入力、記憶の由来、候補・除外理由、選択・実際の発行ボタンを記録する。stunによる判断省略も記録する。
- 両FPS、両攻撃の遷移、距離0・距離境界・端点、各壁、dash待ち、stun、入場・retry、履歴不足の各方向を含む全判断分岐を試験する。許可外属性を読むと失敗するfixtureと、同じ公開入力・異なる内部値での実経路の判断不変を示す。slotsだけで全経路監査済みとはしない。
- E1の状態・判断emit_rowsアダプタと窓helperの確認本文を出す。候補の途中採択だけを全候補列挙としない。既存印字の抑制でassertや検証対象を減らさない。

72で追加した完全IDは次の3件。いずれもrepo/tests/test_bots_boss.py内で、Q1を主担当、Q4にも更新本文を配布する。

- test_bots_boss.PublicBoundaryPrototypeTest.test_active_internal_values_do_not_cross_boundary
- test_bots_boss.PublicBoundaryPrototypeTest.test_warning_memory_active_and_recovery
- test_bots_boss.PublicBoundaryPrototypeTest.test_slots_only_input_and_visible_branches

71の13ファイルQA配布台帳を維持する。追加・変更試験を完全IDで追跡し、未配布を残さない。配布と基準充足は区別する。70の正本との完全対応、E4の未丸め時刻・half-up、E5公開再生、長時間観測等の残作業を消さない。

## Decisions already made

- D-019：公開情報限定、反応0.15秒、独立1〜4保持、開始3/2 hearts別FPS比較。
- D-021/D-023：Studio内テキスト検証。個別Load、@need一度最大8件、@run最大3回、各出力最大2万字。全文保存先・変更前ビルドなし。
- D-022：表示・弾・長時間観測契約を保持。
- D-024：現行検証・現行内対照・記録比較・歴史的確認不能を分離。
- 68：E1完了確認後にStudioがE2を別Handoffで開く。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、表示契約、Goal範囲を変更しない。独立1〜4の方針を保持し、共有関数への影響を報告する。

書込対象はrepo/bots.py、repo/tests/test_bots_boss.py、repo/tests/test_split_c.py、repo/tests/test_g002_evidence.py。test_split_c.pyはE1境界接続・互換・対象別出力に必要な範囲のみ。他ファイル変更が不可欠なら具体的理由と対象を返す。game.py、session.py、play.py、run_driver.pyは照合対象であり変更しない。

repo/での固定コマンドは `python3 -m unittest discover -s tests`。最大3回を公開境界不変、記憶・境界条件、suite・不足確認へ配分する。出力は概ね12000字以内を目指し、対象BEGIN/END、列定義、連番、総件数・表示件数・未表示・除外を明示する。再実行の入力・source_id・総判断数を照合し、異なる集合を継ぎ合わせない。

未表示・切断を確認済みにせず、件数やsource_idだけで必要本文を置き換えない。60のfail、歴史的確認不能を自己確認で上書きしない。

## Open questions

新しい仕様質問はない。実経路の全分岐が公開情報境界を通ること、記憶の初期化、判断ログと許可外参照禁止をどのassert・表示本文で示すか。

## Expected output

studio宛Handoffへ変更ファイル、公開フィールド対応、全呼出経路の監査範囲、完全試験IDとassert、対象別状態・判断本文、コマンド、最終source_idと識別対象を記録する。実装者の評価・理由・自試験の解釈はSender assessmentにまとめる。

全試験件数・追加ID・QA配布先、今回解消分、残作業、未表示範囲を明示する。E1完了とE2以降・独立QA完了を区別する。既知の残作業があればpartialで返し、供給条件をOwnerへ再質問しない。同じE1が3回連続partialとなった場合、StudioはTechnical Directorへ分割・再計画を戻す。

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
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/72-gameplay-engineer-to-studio.md
