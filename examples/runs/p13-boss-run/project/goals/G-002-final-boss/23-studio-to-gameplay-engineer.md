---
kind: handoff
goal: G-002
seq: 23
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 23: studio → gameplay-engineer — テキストビルドで連続ランと最終ボスを実装する

## Task

承認された最終ボス・連続ラン仕様と既存技術計画に従い、repo/へ実装する。D-021を優先し、現状repo/の実行基線を取得してから変更・試験を行い、結果をstudioへ返す。

## Context

OwnerのGoalは「最後に手応えのあるボス戦がほしい」。DesignとPlan補完は完了したが、実行・実機供給・費用条件が未確定としてBuildを保留していた。22へのOwner回答により、今回の実装・検証方式は既存のテキストビルドとスクリプト実行に確定し、Build開始が承認された。

## Findings

Ownerが指定した実行経路はproject.mdのbuildとrun_tests／run_play／run_trace／run_bots。Gameplay EngineerとQAはStep内の@runを使用できるとの回答がある。

repo/で実行するコマンド：

- `python3 -m unittest discover -s tests`
- `python3 play.py --view player {script}`
- `python3 play.py --view trace {script}`
- `python3 bots.py {script}`

スクリプト形式と利用可能な操作はrepo/manual.mdを読むこと。作業開始時のrepo/を基線とし、指定sha照合は不要。project.mdのbuild 0.4記述は古く、repo/が正本である。Studioは本Resumeで実行しておらず、合格結果はない。

計画正本は16と20、仕様正本はdesign/final-boss-and-continuous-run.md。計画中の実機ホスト追加、実gamepad、外部検証枠、金銭・人日見積もりの取得条件はD-021により今回適用しない。その他の適用可能な計画と回帰対応を用いる。技術方式の実質的な再設計が必要ならTechnical Directorへ、仕様の意味が未確定ならDesignerへ手渡し、推測で仕様を変えない。

## Decisions already made

- D-015：連続ラン・部屋間継承・終端・先頭retryと第5部屋単体ボスを範囲に含める。
- D-016：読み取り・位置取り・回避後の反撃を中心とする体験方向。
- D-017：二攻撃のボスと1 heart回復を伴う連続ランの契約。
- D-018・D-019：旧第5部屋依存の集計と新構成の評価を分離し、保持回帰と代替評価を定める。
- D-021：D-020を置き換えるOwner判断。現状repo/と既存@run経路でBuildを開始。実機・実gamepad・外部配員・指定sha確認・人日見積もりは不要。追加金銭支出は認めない。

## Constraints

- 第1〜4部屋の構成と既存共有戦闘ルールを維持する。新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修を行わない。
- テキストplayer viewとスクリプト実行を今回の実装・検証対象とする。実機ホストを追加しない。
- 30/60 FPS、仕様の受け入れ基準、保持する共有戦闘回帰を維持する。
- 通常Studio Step内で進め、購入・外部委託・追加金銭支出・外部連絡を行わない。
- 15〜20分を満たすためだけの敵HP増加をしない。
- 独立QA、限定Art Verify、独立Play、Designer実測後判断、Reviewを省略しない。
- 未実行・未確認事項を成功と記録しない。Ownerの実行経路指定は実行結果ではない。

## Open questions

- 現状repo/の実行基線、適用可能な回帰試験と両FPSでの結果。
- 連続到達・継承・ボス二攻撃・勝敗・先頭retryの実装と、仕様基準への対応。
- 対応bot、通常ランの到達・終端・所要時間を同一試行で記録する経路。
- D-021適用後も具体的な仕様矛盾や技術上の不成立が残るか。残る場合は根拠と該当箇所を報告する。

## Expected output

実装、必要な試験・プレイヤー向け説明、およびstudio宛ての結果Handoffを作成する。変更内容、実行基線、実行コマンドと結果、30/60 FPSの試験対応、未解決事項、独立検証用の再現手順を記録する。

実装者自身の評価・原因推定・確信度は`## Sender assessment`にまとめ、QAへ渡す検証手順・事実と分ける。QAの合否やGoal達成を代行しない。仕様不明ならDesigner、計画不成立ならTechnical Directorへの差し戻し理由を記し、studioへ返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#art-direction
- Project: repo/
- Project: repo/manual.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-cues-visual-spec.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step59.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/22-game-director-to-owner.md
