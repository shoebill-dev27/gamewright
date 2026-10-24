---
kind: handoff
goal: G-002
seq: 11
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 11: studio → game-director — 旧難度基準と新構成の適用境界を判断する

## Task

D-006の旧3〜5部屋集計と、新しい第5部屋・連続ランとの整合について、方向と適用境界を判断する。Designer権限の基準変更は自ら詳細決定せず、必要なDecision変更と仕様補足をDesignerへ依頼できる形でStudioへ返す。

## Context

OwnerはD-015で連続ランと第5部屋の単体ボスを承認したが、既存Decisionを改訂していない。D-016も同じ境界を保持し、既存Decisionとの具体的な衝突がDesignで判明した場合を再検討条件としている。

DesignはD-017と仕様を確定した。D-006の集計は旧独立3部屋と各3 hearts開始を前提とするため、新構成への適用が未解決である。実装と検証はまだ行っていない。

## Findings

正本は `design/final-boss-and-continuous-run.md` §8と、前Handoff 10。

Designerの推奨は、旧第5部屋を含む集計を過去ビルドの記録として保存し、新構成の合否ゲートから外すこと。独立3・4の成績は個別に報告し、新たな合計下限などは実測後にDesignerが判断する。ボスは新仕様の攻撃・対処検証と独立Playで評価する。

代案は旧第5部屋fixtureの維持。ただし新構成の難度評価にはならず、保守が増える。いずれも未採択。D-006は部屋変更時の再計測を求めており、旧数値を自動継承できない。

仕様§8にはcombat.md15のdash使用数、16cのFPS比較など、関連する置換案もある。方向判断とDesignerの詳細基準決定を区別し、必要な後続作業を明示する。

Planはこの判断の後に開く。指定sha・ビルド表記、長時間実行、pause／retry、実機入力、工数・リスクはTechnical Directorの未解決課題であり、本Stepで技術方式を決めない。

## Decisions already made

- D-006：旧独立3〜5部屋のwalker集計基準。現時点で存続。
- D-015：連続ラン、第5部屋の単体ボス、ラン先頭からのretryをOwnerが承認。既存Decisionの変更は適切な権限で解決する。
- D-016：読み取り・位置取り・回避後の反撃を重視。既存Decisionとの衝突は再検討する。
- D-017：二攻撃、境界回復、終端・時刻・表示の詳細契約。D-006は改訂していない。

## Constraints

Owner requestとInterpretationを変更しない。第1〜4部屋と共有戦闘ルールを保持する。15〜20分のVisionを暗黙に緩和せず、時間合わせだけのHP増加は行わない。

既存Decisionは編集しない。変更が必要なら担当Roleが新しいDecisionに変更対象と適用範囲を記録する。旧テストを削除するだけで整合済みとしない。

本Stepは方向と判断権限の整理であり、詳細仕様、技術計画、QA合否、Goal達成の判定を代行しない。限定Art Verifyは経路に確定済み。

## Open questions

1. Designerの推奨する適用変更はD-015／D-016の範囲内で進められるか。方向上の制約は何か。
2. D-006と関連する置換案について、Designerが確定すべきDecision変更・仕様補足は何か。
3. Owner判断を必要とする具体的な衝突があるか。なければRole内で処理し、Ownerへ戻さない。

## Expected output

方向判断とその理由、Designerへ戻す作業の範囲、Plan開始までに残る依存を記したHandoffを `studio` 宛てに返す。担当権限の範囲で重要な判断をする場合は新しいDecisionを記録する。

DesignerのDecision変更が必要なら、変更対象・維持事項・必要な成果を具体化する。Studioが次のDesignまたはPlanを開く。Owner escalation triggerが実際に成立する場合のみ、prepare-owner-escalationで選択肢と推薦を含むbriefを作成する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#current-state
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Previous handoff: goals/G-002-final-boss/10-game-designer-to-studio.md
