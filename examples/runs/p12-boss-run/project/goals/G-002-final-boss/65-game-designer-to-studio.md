---
kind: handoff
goal: G-002
seq: 65
from: game-designer
to: studio
stage: Route
outcome: done
---
# 65: game-designer → studio — 変更前一致の記録比較と確認不能を確定

## Task

D-024と証拠適用補足を受領し、Technical Directorへ62のD-023適合再計画をルーティングする。確認不能部分を残したまま検証を進める工程と、最終判断への引継ぎを整理する。

## Context

D-023でOwnerはテキスト方式の継続を指示し、変更前ビルドは保存されていないと確定した。Designerには、変更前一致要求を記録数値との比較にするか、確認不能として扱うかが委任された。

今回はこの委任範囲だけを判断した。実装、play／bots実行、独立QA判定、実測後の難度判断は行っていない。

## Findings

新規成果物：

- `decisions/D-024-g002-historical-comparison-evidence.md`
- `design/g002-historical-comparison-evidence.md`

補足仕様の表に、従来要求、採択した扱い、出典、条件・精度、未確認範囲を記載した。

### 確定した扱い

L1の変更前出力・結果・終了時刻、O3の変更前出力、step68 V-cのbyte一致、step94 W7の変更前イベント・挙動一致は確認不能とした。L4、step68 V-a／V-b／V-e、step94 W3／W4に含まれる歴史的一致も、現在の仕様へ直接照合できる部分と分離した。

独立1〜4 dodgerは40の記録数値との比較を採択した。各FPS・部屋、3 hearts、通常初期状態、limit 60秒を揃え、clear・損失0・dash回数と小数1桁時間を比較する。時間の丸め方法も補足仕様で定義した。56の保存実行報告は後続記録として区別する。

40は既にボス対応後の保存ソース`5145454ab956`である。40も提出前一致を確認できなかったと明記しており、この記録からボス対応前の厳密な同一性は証明しない。56の`04fa2b1c168a`での152件成功も、その不足を埋めない。

R2・step72 R3-1の保持部分は元仕様の配置・パラメータへの現行照合であり、変更前実装を必要としない。step72 R3-6のgrub有無比較、combat16c、現行の注記抑制対照、既定値と明示0.5秒の対照は、現在のビルド内比較として継続できる。

### Technical Directorへの仕様上の入力

62の「変更前基線を探索・供給する」「全文原本の保存・再読込みを再開条件にする」部分はD-023へ適合させる。存在しない基線・保存先を待つ計画にはしない。

最大3回、各出力2万字の範囲で、対象を絞った証拠出力と必要な直列Stepへ再構成する。表示した証拠の範囲、集計・判定の方法、未表示部分を区別できる計画が必要である。試験構造と技術方式は本Stepでは選ばない。

ボスbotの公開情報限定対応、突進診断の訂正、開始3/2 hearts別FPS再測定、通常ラン入力の再生成は62の依存順序を保持する。対応前ボス数値と生成再生時間を新たなpass基線にしない。独立1〜4の保持比較とは分離する。

確認不能を合格・免除・Goal達成にしない。62の「全QA合格後」という工程条件は、歴史比較の確認不能を含めて再整理する必要がある。Goal再解釈や範囲変更が必要ならGame Directorへ返す。QAに直接免除を求めない。

## Decisions already made

- D-019：保持回帰、公開情報限定のボス比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- D-023：個別本文供給、@need一度最大8件、@run最大3回、出力最大2万字、全文保存先・変更前ビルドなし。
- D-024：歴史的一致の確認不能と、独立1〜4 dodgerの記録精度に限定した比較を確定。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲートを変更しない。60のQA判定を上書きしない。未確認をpassにしない。

ボスbot対応前の数値から戦闘不具合・難度不合格を断定しない。追加数値ゲートと時間Visionの判断は再測定・独立QA・独立Play後に残す。

本Handoffと補足仕様の検証結果・期待値を独立Play資料へ転記しない。

## Open questions

1. Technical Directorは、供給上限の中で基準別の証拠と独立実行をどの単位へ分割するか。
2. 歴史比較の確認不能を保持した工程条件をどう整理するか。Goalの再解釈が必要ならGame Directorへ返すこと。
3. 対応後の保持記録比較に差が出た場合、その条件と影響は何か。差が出る前の推測で仕様を変えない。

## Expected output

StudioはTechnical Directorへ、62をD-023・D-024へ適合させる再計画を依頼する。基線探索・全文保存機構の確保を開始条件から外し、対象別の本文供給、限定出力、直列分割、未確認の受渡しを具体化する。

その後、試験道具対応→再測定→独立QAへ進む条件を確定する。確認不能項目は最終Reviewにも渡す。限定Art Verify、独立Play、実測後Designer判断、Game Director Reviewを省略しない。

次の技術再計画で追加本文が必要な個別ファイル名：

- `repo/source_id.py`
- `repo/bots.py`
- `repo/run_driver.py`
- `repo/play.py`
- `repo/tests/test_bots_boss.py`
- `repo/tests/test_split_c.py`
- `repo/tests/test_d022_observation.py`
- `repo/tests/test_d022_shots_and_note.py`

この8件は62の主要所見を再計画へ結び付けるための本文であり、全QAに十分なファイル一覧ではない。後続QAの全tests本文はStudioが個別ファイル名で別途割り当てる。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/g002-historical-comparison-evidence.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/60-qa-to-studio.md
- Project: goals/G-002-final-boss/62-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/64-studio-to-game-designer.md
