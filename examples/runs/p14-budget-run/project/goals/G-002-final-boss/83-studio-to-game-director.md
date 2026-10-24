---
kind: handoff
goal: G-002
seq: 83
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 83: studio → game-director — 残工程と残予算の不一致をOwner判断へ整える

## Task

82の残工程見積もりと残予算を照合し、費用・範囲についてOwnerが判断できるエスカレーションを準備する。既存の後続工程条件を再審議するStepではない。

## Context

Owner requestは「最後に手応えのあるボス戦がほしい」。D-025で重複工程を削減し、D-026でbudget 123を承認済み。現在87/123 operationsで残36。E1は未完了で、82は実装・測定を行わずA〜Dへの分割計画を提出した。

## Findings

82は残必須作業を22〜24 Stepと見積もる。各Step後のRouteを含め最低44〜48 operationsとなり、失敗修正・追加表示窓・本判断とOwner Resume等を含める前から残36を超える。

82の「まずAだけを開始」という推奨より先に、同報告の停止条件「残必須工程が上限内に収まらない具体的見通しが出た場合」を適用する。これはStudioによる工程数の照合であり、技術見積もりの確定やゲーム範囲の変更ではない。

E1のA〜D、E2〜E5、独立Q1〜Q6、限定Art Verify、独立Play、Designer実測後判断、Reviewは未完了。Aもまだ開いていない。必須評価を省いてGoal達成とする根拠はない。

## Decisions already made

- D-021・D-023：Studio内のテキスト検証と現実の供給上限で進める。
- D-024：歴史的一致の確認不能を現行検証・記録比較と分離する。
- D-025：必須検証と独立評価を維持し、重複工程を省く。
- D-026：budget 123。完成保証ではなく、追加継続はOwner判断。

## Constraints

StudioもGame Directorも予算を変更しない。必須検証の免除やGoal解釈の変更を既存承認に読み込まない。

存在しない環境・外部スタッフ・変更前ビルド・全文保存先を求めない。購入や外部委託は提案の前提にしない。すでに省略した重複工程を再追加しない。

まだ上限到達ではないが、費用見通しが具体化したため判断する。依存Buildは判断まで保留する。

## Open questions

- 82の必須成果を保ったまま、既存の供給上限とRole分離を守って残36以内へ収められる、根拠ある工程削減があるか。
- それが示せない場合、追加operationsでの継続と、未達を明示した打切りをどうOwnerへ提示するか。

## Expected output

原則として日本語のOwner向けEscalationを作成し、studioへ返す。追加継続と未達打切りの選択肢、推奨、各選択後の経路を示す。

追加継続案ではStepとRouteをともに数え、見積もりと失敗・表示継続の余裕を分け、完成保証ではないと明示する。追加予算はOwnerが決める。

残36以内で必須成果を維持できると判断する場合は、単なる期待ではなく、担当Role・依存・StepとRouteの総数・供給上限への適合を具体的に示してstudioへ返す。技術計画を独自に置換せず、技術判断が必要な点を明記する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Decisions: decisions/D-025-g002-minimum-remaining-scope.md
- Decisions: decisions/D-026-owner-extends-g002-budget.md
- Previous handoff: goals/G-002-final-boss/82-technical-director-to-studio.md
