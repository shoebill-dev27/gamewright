---
kind: handoff
goal: G-001
seq: 16
from: studio
to: gameplay-engineer
stage: Build material reconciliation
outcome: routed
---
# 16: studio → gameplay-engineer — 既存の模擬資料と変更記述を照合し、検証入力を整える

## Task

`15-gameplay-engineer-to-studio.md` の模擬実装変更と、既存の `sim/build-0.4.md`・`sim/repo-notes.md` を照合する。独立 QA が使える実在資料と不足を特定し、必要な補完をプロジェクトの dry-run 規約に従って具体化して Studio に返す。

## Context

G-001 はダッシュ中の被ダメージ不具合を既存仕様に従って修正する Goal。QA が AC-1〜AC-6 を作成し、technical-director が計画と D-003 を作成した。Build は Handoff 15 に変更を定義して完了したが、同 Handoff は simulator の資料生成を未実施と報告している。

現在の存在一覧には `sim/build-0.3.md`、`sim/build-0.4.md`、`sim/repo-notes.md` がある。Handoff 15 の指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在しないため、今回の Load には含めない。

## Findings

- Studio が確認できたのは Handoff 15 の内容とファイル一覧。`sim/build-0.4.md` の本文、変更反映、試行記録は未確認。
- ファイル名の違いだけでは反映失敗とも成功とも判定できない。既存資料が対象変更を含むか、明示されたビルド識別子と内容から確認する必要がある。
- Handoff 15 の期待結果、配置案、予定時刻、予定件数は観察証拠ではない。
- この Step は検証入力の照合・補完であり、独立 QA の pass / fail を出す Step ではない。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: Owner の部分的観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 無敵を発生源別に管理し、論理和で判定する。防いだ命中で保護を延長しない。

上記は既存 Handoff の要約。詳細は Load の Decision 本文に従う。

## Constraints

- 仕様、AC、承認済み計画の範囲内で作業する。ゲーム内容や技術方式を Studio の判断として追加しない。
- 既存資料が十分なら、指定ファイル名に合わせるためだけの再生成は求めない。実在する資料と対象変更の対応を報告する。
- 未生成ファイルを作成済みと記さない。観察のない条件を期待結果で埋めない。
- 実コード、実機試験、自動テストを実施したと扱わない。模擬資料による確認と実測を区別する。
- 全4環境、必要な接触・弾命中、AC と追加回帰の資料充足を確認する。無効試行や未確認条件を分離する。
- クールダウン起点、完全同時イベント、入力不能中の予約を新しく定義しない。仕様判断が必要なら game-designer、計画が成立しなければ technical-director への差し戻し事項を Studio に報告する。
- 原因説明、実装理由、自己評価は QA 向け資料から分離する。自己評価は outgoing Handoff の Sender assessment に置く。

## Open questions

1. `sim/build-0.4.md` と `sim/repo-notes.md` は Handoff 15 の変更に対応しているか。明示された識別子、反映内容、不一致は何か。
2. AC-1〜AC-6 と追加回帰について、どの環境・命中源・枝の観察が実在し、どこが不足しているか。
3. 既存クールダウン起点、命中成立、実際のイベント順序、ハート変化を確認できるか。
4. 不足は具体的な simulator 更新依頼で補えるか。それとも Role では生成できない入力や仕様・計画判断が必要か。

## Expected output

Studio 宛ての Handoff を作成し、次を含める。

- 読んだ既存資料、明示されたビルド識別子、Handoff 15 との対応と不一致。
- QA に渡せる実在ファイル・節の一覧。仕様・期待値と観察記録を分離し、原因説明や自己評価を混ぜない。
- AC・回帰ごとの資料充足表。全4環境と必要命中源・枝を区別し、観察済み、有効性不足、未確認を明示する。
- 補完が必要なら、対象、変更内容、試し方、生成すべき観察を記述する。dry-run 規約上の変更記述と simulator による反映完了を区別する。
- 解消できない場合は不足入力と理由を具体化し、必要な担当判断を報告する。同じ不足を根拠なく再依頼し続けない。

作業完了は `done`、必須入力や担当外判断で進めない場合は `question` とし、`to: studio` で返す。独立 Verify の判定は QA に残す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: sim/build-0.4.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
