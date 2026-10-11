---
kind: handoff
goal: G-001
seq: 26
from: studio
to: game-director
stage: Review
outcome: routed
---
# 26: studio → game-director — 文書評価が変更後の完了条件を満たすか判断する

## Task

Handoff 25 の報告を D-004 の変更後の完了条件に照らして Review し、G-001 の達成 verdict を Studio に返してください。文書評価による完了と、実際の挙動・不具合解消の実証を区別して判断してください。

## Context

当初の Goal はダッシュ中の被ダメージ修正だった。模擬変更後の独立 QA は文書評価を完了したが、条件別証拠と一部期待値の不足により総合判定を `question` とした。

Owner は D-004 で、模擬ビルド記述に基づく文書評価を今回の検証とし、計測不能項目を未判定として明記して閉じることを承認した。technical-director は25で文書評価、未判定事項、仕様不足、再開条件の報告を完了した。Studio は予定された Review を開始する。

## Findings

- 対象は最新の `sim/build-0.4.md`、変更識別子 `0.3-G001-15`。project.md の Current state に残る build-0.3 は履歴として扱う。
- 25は AC-1〜AC-6 と回帰の文書照合を整理した。ダッシュ保護、被弾後保護、通常被害、移動、予約攻撃は文書上整合すると報告している。
- クールダウンは0.6秒の数値のみ確認でき、起点の仕様は不足している。
- 全4環境の条件別挙動・回帰は未判定。適用宣言や時刻例を計測記録と扱わず、試行数・発生数も不明としている。
- 21の独立 QA 総合判定は `question` のまま。25は再検証や QA 判定の変更ではない。
- 25は将来の取得経路確保、期待値補完、条件別記録、独立 QA の再開条件を記載している。これらは今回の Close の追加前提ではない。
- 外部照会は手段未確保・問い合わせ未実施。モデル不存在や永久的な取得不能とは確認されていない。

これらは報告内容の要約であり、Studio による Goal 達成判断ではない。

## Decisions already made

- `decisions/D-001-one-button-combat.md`：Owner 承認なしに戦闘入力を追加しない。
- `decisions/D-002-resume-with-owner-observations.md`：部分的な Owner 観察を受けて修正を継続した。今回の完了条件は D-004 により変更済み。
- `decisions/D-003-independent-invulnerability.md`：保護を発生源別に管理し、論理和で判定する。防いだ命中で保護を開始・延長しない。
- `decisions/D-004-document-evaluation-scope.md`：文書評価を本 Goal の検証とし、未判定事項と再開条件を報告して Review 後に閉じる。

## Constraints

- D-004 の完了条件を適用し、当初の全条件実証を完了要件に戻さない。
- QA の pass/fail を再採点せず、既存の `question` を保持する。
- 追加取得・計測、新規 simulator 開発、実機試験、追加実装、仕様変更、巻き戻しは今回の範囲外。
- クールダウン起点、試行数、丸め規則、許容差を補作しない。
- 今回は体験 Goal ではなく、Play は省略済み。プレイ観察の新規取得を Review の前提にしない。
- 残る仕様不足・証拠不足と将来の再開条件を終了記録に残す。将来の課題は新規 Goal 候補とし、今回の範囲を拡張しない。
- Owner 向け結果文は日本語で記す。

## Open questions

- 25の報告は、D-004 が求める文書評価、未判定事項の明記、再開条件の報告を満たすか。
- Close の終了記録に残す結果・限界・将来の課題は何か。

## Expected output

Studio 宛ての Review Handoff を作成し、`outcome: goal-met` または `goal-not-met` とする。

判断の根拠を D-004 の完了条件に対応づけ、Owner 向け結果文と将来の課題を記す。`goal-met` の場合も、文書評価の完了であり、不具合解消や全4環境の合格を実証したものではないこと、21の `question` が維持されることを明記する。

`goal-not-met` の場合は、変更後の完了条件に対して不足する報告箇所と必要な補完を具体的に示す。承認済みの未判定事項そのものを、追加計測が必要な理由に置き換えない。Studio が結果を受けて次の Route または Close を行う。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Goal: goals/G-001-dash-damage/goal.md
- Project: project.md#vision
- Project: project.md#constraints
- Specification: design/combat.md
- Build: sim/build-0.4.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md
- Existing QA assessment: goals/G-001-dash-damage/21-qa-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Decisions: decisions/D-004-document-evaluation-scope.md
- Previous handoff: goals/G-001-dash-damage/25-technical-director-to-studio.md
