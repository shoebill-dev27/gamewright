---
kind: handoff
goal: G-002
seq: 15
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 15: studio → technical-director — 確定仕様・基準移行・実測の技術計画

## Task

承認済みの連続ランと最終ボス仕様を、実装・試験・観測が可能な技術計画にする。仕様§8の試験対応と§10の依存、D-019の適用条件、実測後のDesigner再判断を含め、工数・リスクと実装開始を妨げる未決事項をStudioへ返す。

## Context

Ownerは「最後に手応えのあるボス戦がほしい」と依頼し、D-015で第1〜4部屋の連続ラン、第5部屋の単体ボス、勝敗とラン先頭からの再挑戦を承認した。詳細仕様はD-017、旧集計との整合方向はD-018、適用変更と代替評価はD-019で確定した。Design補足が完了したためPlanを開く。ゲーム変更はまだ行われていない。

## Findings

14は文書上の適用整理を報告している。旧独立3〜5のwalker合計、dodgerとの比率・clear数、camper比較とその旧報告条件を新構成のゲートから外し、第1〜4部屋と共有ルールの回帰を保持した。

独立3・4はbot別・部屋別・30/60 FPS別に報告し、新しい合計閾値は導出しない。ボスのdashは使用回数ではなくB6の接触・無傷・消費・終了後被害で検証する。対応dodgerの新5番FPS比較は同じclear結果・hearts lost差1以下とし、独立3 hearts開始と連続ランで可能な2 hearts開始を別比較する。詳細条件と試験対応の正本はD-019と仕様§8である。

追加数値ゲートは未設定。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、DesignerがReview前に必要性を判断する。追加不要でも理由を記録する。

指定shaとの一致、実行成功、難度、所要時間の新しい証拠はない。現在ビルドは `repo/`、指定shaは `27fe16268ac8`。project.mdの0.4表記と既存資料の0.6表記の関係も未確認。

## Decisions already made

- D-001：戦闘入力はattackとdash。
- D-015：連続ランと第5部屋の単体ボスをOwnerが承認。
- D-016：読み取り・位置取り・回避後の反撃を中心とする体験方向。
- D-017：ボス、回復、継承、境界、終端、時刻・表示の詳細契約。
- D-018：旧第5部屋依存の集計を新構成評価から分離。
- D-019：旧基準の限定的な適用変更、保持する回帰、dash検証、対応bot FPS比較、実測後判断。過去Decision本文・G-001の結果は保持。

## Constraints

- 第1〜4部屋の構成と共有戦闘ルールを維持する。新戦闘入力、ボスチェックポイント、既存部屋全面改修を追加しない。
- 30/60 FPS、desktop、keyboard・gamepadの制約を扱う。実機入力経路を確認できない場合は、観測可能な範囲と不足を明記する。
- 15〜20分のVisionを維持する。時間合わせだけのHP増加・待機水増しを計画しない。独立部屋時間の合算を連続ラン実測に代用しない。
- 設計の数値・振る舞いはDesignerの権限。曖昧さや実現困難な仕様は具体的な質問として返す。
- 旧fixtureの保持は必須ではないが、assert削除だけで移行完了にしない。仕様の代替試験・共有回帰へ接続する。
- Plan完了前にBuildを開始しない。承認を超える規模・費用・リスクやOwner Decision変更が必要なら実装前に返す。
- 後続はBuild→独立QA→限定Art Verify→独立Play→Designer実測後判断→Review。明白な対処不能・到達不能はPlay前にもDesignerへ返す。

## Open questions

1. 指定sha、対象ビルド、表記差、既存試験の実行基線を同定できるか。
2. 進行、攻撃切替、表示、HP・回復、終端・retry、pause/resume、両時刻・入力をどの構造と順序で実装・観測するか。共有コードへの影響と工数・リスクは何か。
3. player viewと状態観測、長時間スクリプト、境界試験、実機入力経路をどう扱うか。
4. 対応botの情報・反応・方針をどう確認し、同一ビルド・初期状態・limitで両FPSを比較するか。deathとunfinishedをどう分けるか。
5. 通常ランの同一試行計測と独立QA・Playの証拠を、いつDesignerへ戻せるか。

## Expected output

技術計画と実行基線の確認結果を、次のHandoffで `to: studio` として返す。計画には以下を含める。

- 実装順序、依存、変更対象、工数・リスク、仕様質問と実行制限。
- 仕様B1〜B10・V1、R1〜R5、T1〜T4、C1〜C3、V2、共有回帰と旧assert群の移行対応。
- 対応botの確認、独立3・4の部屋別報告、新5番の開始HP別・両FPS比較、通常ランの同一試行計測。
- 独立QA、限定Art確認、独立Playへ渡せる実行・観測方法。
- Designerの実測後判断に必要な証拠と返却時点。閾値超過や失敗一致を自動合格にしない経路。
- Buildを開けるか、先にDesign・Decideへ戻す必要があるかの明示。

実行できなかった項目は未確認として理由と次の確認方法を記録し、成功を推定しない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: goals/G-002-final-boss/04-technical-director-to-studio.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Build: repo/
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/14-game-designer-to-studio.md
