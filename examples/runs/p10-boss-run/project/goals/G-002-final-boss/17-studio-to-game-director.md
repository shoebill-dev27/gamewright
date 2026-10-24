---
kind: handoff
goal: G-002
seq: 17
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 17: studio → game-director — 実機ホスト・費用・開始条件の承認範囲判断

## Task

16の技術計画が示すdesktop実機ホスト追加、暫定費用、環境依存をD-015／D-016の承認範囲と照合し、次に解決すべき判断と調査条件を確定する。Owner権限の問題が具体化した場合は、実装前に回答できるEscalationを作成する。

## Context

Ownerは連続ラン、第5部屋の単体ボス、ラン先頭からの再挑戦を承認した。詳細仕様と旧基準の適用整理はD-017／D-019で確定している。

Technical Directorは16で技術計画を提出したが、実行基線、回帰正本、実機ホスト・検証環境・費用が未確認のためoutcome: questionとしてBuild開始を保留した。Studioは提出Stepを完了として記録したが、計画の開始条件を充足済みとは扱っていない。

## Findings

16の診断と選択肢の要点：

- 現行資料はheadlessの入力script経路を示す。Technical Directorの静的所見ではkeyboard／gamepad実機経路がなく、仕様V2を満たすには薄いdesktop入力・表示ホストの新設が必要。
- 技術候補は共通Sessionへactionを渡す最小ホスト。具体ライブラリ、対象OS、機器、依存導入、独立実機検証の供給は未確定。技術方式の選択はTechnical Directorの権限に残す。
- Build準備から統合まで暫定11.5〜20人日。その内訳に実機ホスト2〜4人日を含む。独立QA 2〜3人日、限定Art確認0.5〜1人日、独立Play 1〜2人日は別枠。Designer実測後判断と修正・再検証は別途。
- 予算上限は提示されておらず、見積もりだけでは承認超過も承認内も確定できない。
- 指定sha・Python実行基線・版表記の差は未確認。欠けた回帰正本はプロジェクトのファイル一覧に存在するため、次のPlan補完のLoadへ追加できる。未読を資料不存在とは扱わない。
- StudioはBuildを開いていない。QA、限定Art、独立Play、Designer実測後判断、Reviewは維持する。

判断経路として比較するもの：

1. 承認範囲内であり追加調査が可能なら、その根拠と限界を記録し、Technical DirectorのPlan補完へ戻す。実行基線・環境・費用の確認前に無条件のBuild許可を出さない。
2. 承認を超える費用・リスク、またはRoleでは供給できない機器・環境が必要と判明した場合は、OwnerへのEscalationを作る。必要な供給物・承認内容と、供給／調査継続、範囲変更、停止の現実的な選択肢を示す。
3. 判断材料が足りない場合は、Technical Directorが取得できる証拠とOwnerしか供給できない情報を分け、限定調査へ返す。根拠不足だけでV2やGoalを緩和しない。

これらは判断経路であり、Studioによるゲーム内容・技術方式・費用承認の決定ではない。

## Decisions already made

- D-015：連続ラン、第5部屋単体ボス、先頭retryをOwnerが承認。承認案を超える範囲・費用・リスクは実装前にOwnerへ戻す。
- D-016：読み取りと回避後の反撃を中心とする方向、既存部屋・共有規則の維持、既存システムの再利用を優先。
- D-017：詳細契約。実機入力と長時間検証の不足をPlanの依存として扱う。
- D-019：旧集計の適用整理とReview前のDesigner実測後判断。難度検証済みを意味しない。

## Constraints

- Owner requestとInterpretationを変更しない。範囲変更が必要ならOwnerへ戻す。
- headlessや模擬入力だけでV2を合格扱いしない。実機検証を任意課題へ落とさない。
- 未確認の予算、OS、機器、依存導入権限、実行成功を推定しない。
- Game Directorは技術方式や詳細仕様を変更しない。必要な調査・再設計は担当Roleへ返す。
- 過去Decisionは編集しない。新たに将来の作業を拘束する判断は新Decisionとして記録する。
- 本StepはDecideであり、Buildや検証を代行しない。

## Open questions

1. 最小desktopホストの新設は、D-015が承認した案Aの実現に含まれるか。費用・リスクについて現時点で何を判断でき、何が未確認か。
2. 実行基線と実機環境について、Roleによる調査で解決できる事項と、Ownerからの情報・機器供給が必要な事項は何か。
3. OwnerへのEscalationを今作れるだけの具体的な根拠があるか。なければ、次のPlan補完で取得する最小の証拠と返却条件は何か。

## Expected output

権限内で判断できる場合は、必要なDecisionとStudio宛てHandoffを作る。承認範囲の根拠、残る依存、次のPlan補完の入力・完了条件、Build保留解除条件を明記する。

Owner escalation triggerが成立する場合は、prepare-owner-escalationに従い、日本語のEscalationをOwner宛てに作成する。質問を一つに絞り、具体的な必要物・費用の幅・未確定部分、選択肢と各ルート、推奨を含める。

後続はPlan補完→Build→独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを基本とする。実測で明白な対処不能・到達不能が出た場合のDesignerへの前倒し返却を保持する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Template: studio/templates/decision.md
- Template: studio/templates/handoff.md
- Template: studio/templates/escalation.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/16-technical-director-to-studio.md
