---
kind: handoff
goal: G-002
seq: 69
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 69: studio → gameplay-engineer — E0試験棚卸しと証拠出力整備

## Task

68のE0のみを実施する。全テストの実在ファイル名・discoverされた全テストID・基準との対応と未対応を棚卸しし、供給上限内で対象別の証拠を出せる試験道具を整える。

## Context

Goalは連続ランの最後に手応えのあるボス戦を成立させること。60のQAは証拠・供給不足等でfailであり、第三の同条件QAを開く前に試験道具と証拠を整える。

68が62の実行計画を置換した。今回はE0だけを行い、公開情報botの変更、接触診断の対応、成績再測定、通常ラン入力再生成は後続Stepへ残す。

## Findings

68の§2・3が今回の出力契約と作業計画である。§4〜10は後続作業の依存関係を示す。

プロジェクト一覧には次のテストファイルがある。実行時の棚卸しで実在性と追加・欠落を確認すること。この一覧だけで網羅済みとしない。

- repo/tests/test_boss.py
- repo/tests/test_boss_contract.py
- repo/tests/test_boss_contract_details.py
- repo/tests/test_bots_boss.py
- repo/tests/test_d022_observation.py
- repo/tests/test_d022_shots_and_note.py
- repo/tests/test_game.py
- repo/tests/test_play_run_controls.py
- repo/tests/test_run_driver.py
- repo/tests/test_session.py
- repo/tests/test_split_c.py
- repo/tests/test_terminal.py

新規証拠出力ファイルの提案はrepo/tests/test_g002_evidence.py。まだ存在するとは扱わない。

## Decisions already made

- D-019：保持回帰、公開情報限定ボス比較、開始3/2 hearts別FPS比較、実測後Designer判断を維持。
- D-021：repo/のテキスト・スクリプトとStudio内独立検証で進める。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約。
- D-023：個別Load、@needは一度最大8件、@runは最大3回、各出力最大2万字。全文保存先・変更前ビルドは存在しない。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離。確認不能をpassや免除にしない。
- 技術計画は68を使用する。今回は新しい仕様・方向の判断を行わない。

## Constraints

製品仕様・戦闘パラメータ・難度・秒数ゲート・Goal範囲を変更しない。E0では製品ソースと既存bot方針を変更しない。

書込対象はrepo/tests/test_g002_evidence.py。棚卸し・対象別証拠出力に必要な試験道具をここへまとめる。他ファイルの変更が不可欠なら理由と具体的な対象をStudioへ返す。

固定実行コマンドはrepo/での `python3 -m unittest discover -s tests`。trace枠で任意Pythonを動かす前提を置かない。最大3回で、棚卸し・通常suite・道具の確認を配分する。

出力は対象開始・終了、列定義、連番、総件数・表示件数・除外対象を明示し、概ね1万2千字以内を目指す。切断・未表示を確認済みにしない。成功件数やsource_idだけで必要本文を置き換えない。

未供給のテスト本文を読んだものとして対応付けない。必要なら個別パスで@needを使い、それでも残る既知の範囲はpartialとして直列継続する。ディレクトリを@needへ指定しない。

## Open questions

- 実在する全テストファイルとdiscoverされた全IDは何か。
- 各基準をどの試験がどのassert・観測で扱い、どこが未対応または本文未確認か。
- 旧第5部屋依存試験の保持部分とD-019による置換先は何か。
- 後続E1〜E5・Q1〜Q6に必要な対象別出力をどう選び、欠落を検知するか。

## Expected output

結果を`studio`宛Handoffとして返す。次を含める。

1. 実在する全テストファイル・全テストIDの連番付き棚卸し、総件数と未表示範囲。
2. 基準ID→試験ID→assert・観測対象の暫定対応表。本文未確認・未対応、旧5番依存と置換先を分ける。
3. 変更ファイル、証拠出力の選択方法と再現手順、実行コマンド、実行時source_idと識別対象ファイル一覧。
4. 通常suite結果と道具の確認証拠。実装者の確認であり独立QAではないと明記する。
5. E1に必要な個別Load候補と、QA全試験配布台帳に使えるQ1〜Q6別の割当案。未割当・追加試験を明示する。
6. 残作業と不足。既知の作業が残るだけならpartialとし、何も新たに不足していない作業をOwnerへ戻さない。

E0完了後の次工程はE1。今回は着手しない。Studioが棚卸しを確認し、次のHandoffと後続QAの個別Loadを確定する。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/source_id.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/bots.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/68-technical-director-to-studio.md
