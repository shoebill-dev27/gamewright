---
kind: handoff
goal: G-002
seq: 14
from: game-designer
to: studio
stage: Plan
outcome: done
---
# 14: game-designer → studio — 基準適用を確定し、実測と再判断を含むPlanへ渡す

## Task

D-019と仕様補足の適用関係を確認し、Technical DirectorのPlanを開く。実測後のDesigner再判断をReview前の経路に含める。

## Context

D-018が採択した方向に基づき、Designer権限でD-006・step44と関連基準のG-002新構成への適用変更を確定した。過去G-001の判断・結果と既存Decision本文は変更していない。

## Findings

make-decisionとwrite-design-specに従い、以下を作成・補足した。

- `decisions/D-019-g002-balance-criteria-applicability.md`：限定的な適用変更と関連基準の採否。
- `design/final-boss-and-continuous-run.md`：冒頭、§8、§10を更新。保持・適用終了・置換先、対応bot条件、実測後の再判断経路を確定。
- `design/combat.md`、`design/combat-step-44-walker-limit.md`：G-002の適用注記を追加し、旧記載から新構成の誤判定を防ぐ。

旧独立3〜5のwalker3〜7 hearts・2/3 clear、dodgerのwalker比1/2以下・3/3 clear、camperのwalker未満clearを新構成のゲートから外した。FPS別旧集計、過去数値、旧逸脱報告・再判断条件も新構成へ移さない。

第1〜4部屋、共有ルール、独立3 hearts開始、独立1〜2比較、独立1〜4のdodger FPS比較を保持する。独立3・4は各botを部屋別・30/60 FPS別に報告する。新合計下限・上限・clear数は導出しない。

基準15は独立3・4の既存規則とゼロdash時のDesigner報告を保持する。新5番は使用回数条件を終了し、B6で各攻撃への実接触、無傷、消費、dash終了後の追加被害なしを確認する。横移動の有効性と独立Playも保持する。

ボス対応dodgerの新5番FPS比較は「同じclear結果・hearts lost差1以下」を採択した。同一方針・ビルド・初期状態・limit、playerに見える情報、0.15秒反応を条件とする。独立3 hearts開始と連続ランで可能な2 hearts開始を別比較する。対応確認前の成績は合格根拠にしない。death／unfinishedを区別し、両FPSの失敗一致を攻略可能性の証拠にしない。帯内接触による差でも数値閾値超過は自動免除せずDesignerへ戻す。

§8は関連BotsTestの各assert群、CueGapTest、構成試験、共有回帰を対応付けた。旧fixtureは必須にせず、必要なら共有回帰に限定する。削除だけで完了にせず、B1〜B10・V1、R1〜R5、T1〜T4、C1〜C3、V2、独立Playと同一試行の時間計測へ接続する。

追加数値ゲートは未設定。対応botの両FPS基線、独立QA、独立Play、通常ランの到達・終端・時間実測を受け、Review前にDesignerが必要性を判断する。追加不要の場合も理由を記録する。明白な対処不能・到達不能ならPlay前にも戻す。

本Stepは文書上の適用整理であり、play／botsは実行していない。実行成功、指定sha一致、難度、体験、所要時間の新しい証拠はない。コードとテストの実装改訂も行っていない。

## Decisions already made

- D-006：過去構成の正本として保持。G-002新構成への適用はD-019で限定変更。
- D-015／D-016：承認された連続ラン、単体ボス、体験方向と範囲を保持。
- D-017：ボス・回復・境界・終端・時刻・表示の詳細契約を保持。
- D-018：旧集計を新構成評価から分離する方向。
- D-019：その適用変更、dash検証、対応bot FPS比較、実測後の再判断を確定。

## Constraints

Owner request、Interpretation、第1〜4部屋と共有ルールを維持する。新戦闘入力、ボスチェックポイント、既存部屋全面改修は追加しない。

15〜20分のVisionを維持し、時間合わせだけのHP増加・待機水増しをしない。独立部屋時間を合算して連続ラン実測と扱わない。

技術方式、実装順序、工数、実機入力経路はTechnical Directorに残す。Plan完了前にBuildを開かない。独立QA、限定Art Verify、独立Play、Reviewを維持する。Playtester資料はStudioが作成し、設計上の期待結果・Review用体験信号を渡さない。

## Open questions

1. Technical Director：指定sha `27fe16268ac8`、対象ビルド、0.4／0.6表記差と既存試験の実行基線を同定できるか。
2. Technical Director：長時間player／状態観測、pause／resume、retry、両時刻・入力、実機操作、表示と境界試験を実現・観測する方式、工数とリスクは何か。
3. Designerへの後続再判断：実測に基づき独立3・4、新5番、連続到達・回復・retryへ追加数値ゲートや調整が必要か。現時点では未判断であり、Plan開始の権限上の衝突ではない。

## Expected output

Studioは適用整理の完了を確認し、Technical Directorへ§10の依存と§8の試験対応を含むPlanを渡す。Planは対応botの確認、両FPS計測、通常ランの同一試行計測、実測後のDesigner再判断を明示する。

Planと必要判断の後、Build→独立QA→限定Art Verify→独立Play→Designerの実測後判断→Reviewへ進む。QAまたは初回基線で問題が判明した場合は前倒しで再判断する。承認超過、Owner Decision変更、範囲内で解消不能なVision不整合はStudioからGame Directorへ返す。G-002は進行中とする。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: repo/tests/test_game.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#current-state
- Project: goals/G-002-final-boss/goal.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/13-studio-to-game-designer.md
