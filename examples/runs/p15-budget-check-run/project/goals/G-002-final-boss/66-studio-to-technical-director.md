---
kind: handoff
goal: G-002
seq: 66
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 66: studio → technical-director — 検証計画を供給上限と証拠区分へ適合

## Task

62の技術計画をD-023・D-024へ適合させ、試験道具対応、再測定、独立QAを実行可能な直列Stepへ分割する。歴史的一致の確認不能を保持したまま、後続工程へ進む条件と判断先を明示する。

## Context

60のQAはfailであり、同じ入力・実行・証拠不足のまま第三のQAを開かない。OwnerはD-023で利用可能な供給条件を確定し、その範囲で継続を指示した。65でDesignerがD-024と証拠適用補足を納品したため、予定どおり技術再計画へ進む。

今回の担当は再計画である。製品変更、再測定結果、独立QAの合否を先取りしない。

## Findings

62の技術所見と依存順序を出発点とする。ただし、変更前基線の探索・供給、完全ログの保存・再読込みの確保を開始条件にする部分は置き換える。

D-023の供給は以下に限る。

- Loadに個別指定したファイルは本文が届く。ディレクトリ指定はファイル名だけ。
- 各Stepの@needは一度、最大8ファイル。
- 各Stepの@runは最大3回。別の実行枠はない。
- 実行出力は先頭・末尾を含む最大2万字。全文保存先はない。
- 変更前ビルドは存在しない。

D-024により、以下を分離する。

- L1・O3・step68 V-c・step94 W7等の歴史的一致は確認不能。現行suite成功や同一現行ビルド内の対照で埋めない。
- 独立1〜4 dodgerは40の記録との比較。各FPS・部屋、開始3 hearts、通常初期状態、limit 60秒を揃える。clear、損失0、dash数、小数1桁へ所定の方法で丸めた時間を比較する。補足仕様の表を正本とする。
- 40は既にボス対応後のsource 5145454ab956の記録であり、ボス対応前の厳密一致を証明しない。56は別の後続記録として扱う。
- 現行仕様照合、現行内対照、保持共有基準、FPS比較は継続する。

62の公開情報限定ボス判断境界、突進接触診断の訂正、開始3/2 hearts×30/60 FPSの再測定、独立1〜4保持比較、新botによる通常ラン入力再生成の依存関係を維持する。対応前ボス値と生成再生時間を新たなpass基線にしない。

## Decisions already made

- D-019：保持回帰、公開情報限定ボス比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト方式で進める。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- D-023：実際の本文・実行・出力上限に適合させ、存在しない保存機構や変更前ビルドを待たない。
- D-024：歴史的一致の確認不能、記録精度に限定した比較、現行検証を分離する。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goalの解釈を変更しない。60のfailを上書きせず、確認不能をpass・免除・適用終了にしない。

未表示・切断部分は確認済みにしない。ハッシュ、summary、成功件数だけで必要な証拠本文を代用しない。一方、出力全文の永続保存を再び要求せず、検証対象を絞る出力と直列分割で構成する。

限定Art Verify、独立Play、実測後Designer判断、Game Director Reviewを維持する。独立Playへ実装履歴、QA判定、期待結果、本補足の比較値を渡さない。

## Open questions

1. どの基準をどのStepで扱い、各Stepの本文・最大3回の実行・出力上限をどう割り当てるか。
2. 全判断を対象とする公開情報条件の検証と突進接触診断を、表示範囲・集計方法・未表示範囲が明確な証拠へどう構成するか。
3. 歴史的一致の確認不能を残す場合、62の「全QA合格後」をどの工程条件へ整理するか。技術上の進行可否とGoal達成判断を分離し、方向・範囲の判断が必要ならGame Directorへ返すこと。
4. 記録比較に差が出た場合、条件と共有処理への影響をどう整理してDesignerへ返すか。

## Expected output

Studio宛のHandoffに、62を置き換える適合計画をまとめる。

- 影響システム、順序、各Stepの完了条件、リスクと対策、逐次実行の理由。
- 各Engineer・QA Stepが必要とするファイルを個別名で列挙したLoad案。追加本文が必要なら、各Stepの@need上限を踏まえて配置する。
- 基準ID・FPS・初期条件・入力・source識別・試験assert・出力対象・結論・未確認を対応付ける証拠構成。
- 各Stepの最大3回の実行配分と、出力切断を避ける対象別出力。残作業だけならpartialで直列継続できる単位。
- 公開情報bot対応→診断・試験→4条件再測定→保持回帰・通常ラン再生成→独立QAの順序と受渡し。
- 歴史的確認不能を含むQA結果から、限定Art Verify以降へ進む条件。未解決事項を最終Reviewへ残し、必要な権限判断は適切なRoleへ返す。

後続QAは実装者の自己評価から独立させ、全tests本文を必要な検証単位へ個別に割り当てる。今回の8つのコード・テスト本文だけで全QA資料が揃ったとは扱わない。

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
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/65-game-designer-to-studio.md
