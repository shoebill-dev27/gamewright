# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-dash-damage/26-studio-to-game-director.md
next_seq: 27

## You may write

- goals/G-001-dash-damage/27-game-director-to-<recipient>.md
- decisions/D-005-<name>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-dash-damage/26-studio-to-game-director.md
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
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE goals/G-001-dash-damage/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: ダッシュ中の被ダメージに関する文書評価を完了する

## Owner request

当初の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

2026-10-11 の範囲変更：

> B。模擬専用のサンプルなので、模擬ビルド記述に基づく文書評価をこの Goal の検証とし、計測できない項目は未判定として明記したうえで Goal を閉じてください。

## Interpretation

D-004 に基づき、現資料と最新の模擬ビルド `sim/build-0.4.md`（変更識別子 `0.3-G001-15`）による文書評価を本 Goal の検証とする。確認できる文書上の整合、計測できず未判定となる項目、仕様不足、再開条件を報告し、変更後の完了条件に対する Review を経て閉じる。

全4環境の挙動実証や不具合解消の保証は完了条件としない。追加取得・計測、新規 simulator 開発、実機試験、追加実装、仕様変更、巻き戻し、無関係なバランス調整は対象外。

## Unknowns

- Observe：仕様不一致の照合と AC-1〜AC-6 の作成は完了。Owner の詳細条件の独立した試行再現とは扱わない。
- Diagnose / Plan：D-003 と模擬実装定義は存在する。25で現資料による文書評価、限界、再開条件の報告を完了した。
- Decide：Owner が D-004 で文書評価への範囲変更を決定済み。
- Design：クールダウン0.6秒の起点は未定義。今回は不足として報告し、新たな仕様判断は行わない。
- Build：模擬変更の定義は完了。追加修正は不要。
- Verify：Handoff 21 の文書評価は完了、総合結果は `question`。条件別証拠と全4環境の計測は不足したまま。D-004 に従い文書評価を今回の検証とし、実証できない項目は未判定で残す。
- Play：体験評価を求める Goal ではないため省略。
- Review：25の報告が変更後の完了条件を満たすか、game-director が判断する。
- Next：Review 後、Studio が Owner 向け Outcome を記録して閉じる。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 01-studio-to-qa.md |
| 1b | Observe | qa | reproduce-defect | done | 03-studio-to-qa.md |
| 1c | Observe | qa | reproduce-defect | done | 05-studio-to-qa.md |
| 1d | Observe | qa | reproduce-defect | done | 07-studio-to-qa.md |
| 1e | Observe | qa | reproduce-defect | done | 10-studio-to-qa.md |
| 2 | Diagnose / Plan | technical-director | technical-plan | done | 12-studio-to-technical-director.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | skipped | — |
| 4 | Design | game-designer | write-design-spec | skipped | — |
| 5 | Plan | technical-director | technical-plan | skipped | — |
| 6 | Build | gameplay-engineer | implement-change | done | 14-studio-to-gameplay-engineer.md |
| 6b | Build 資料照合・補完 | gameplay-engineer | implement-change | done | 16-studio-to-gameplay-engineer.md |
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | done | 18-studio-to-technical-director.md |
| 7 | Verify 文書評価・証拠充足性確認 | qa | verify-change | done | 20-studio-to-qa.md |
| 7a | Owner escalation 準備 | technical-director | prepare-owner-escalation | done | 22-studio-to-technical-director.md |
| 7a-owner | Decide 検証範囲変更 | owner | — | done | 23-technical-director-to-owner.md |
| 7b | Design クールダウン起点 | game-designer | write-design-spec | skipped | — |
| 7c | Verify 補完後の独立検証 | qa | verify-change | skipped | — |
| 7d | Diagnose 文書評価報告の整理 | technical-director | technical-plan | done | 24-studio-to-technical-director.md → 25-technical-director-to-studio.md |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review 変更後の完了条件 | game-director | review-outcome | open | 26-studio-to-game-director.md |
| 10 | Next | studio | — | planned | — |

done は作業終了を示し、再現成功や検証合格を意味しない。主要結果は 11（不具合報告・AC）、13（計画）、15（模擬実装定義）、17（資料照合、question）、19（条件付き再計画）、21（文書評価、question）、23（Owner escalation、D-004 により resolved）、25（文書評価報告、done）。

行 7b・7c の省略は不足の解消ではなく、D-004 による完了条件の変更による。既存 QA 判定の再採点や、同じ不足入力での QA 再依頼は行わない。

## Route changes

2026-10-10 — 02・04・06・08 の入力不足が解消せず、09 で Owner に escalation。D-002 の継続判断と補足観察を受け、11 の不具合報告・AC、13 の計画と D-003 に基づき Build へ進んだ。

2026-10-11 — 15 の模擬実装定義と17の資料照合により build-0.4 と変更識別子の対応を採用。資料不足は19で再計画し、21の独立 QA は文書評価を完了したが証拠不足により question とした。

2026-10-11 — 外部照会手段未確保のため22で brief 作成を依頼し、23を Owner に提示して blocked-on-owner とした。問い合わせ済み・モデル不存在・検証 fail とは扱っていない。

2026-10-11 — Resume：Owner の B と文書評価による完了条件を D-004 に記録し、23を resolved、Goal を active に変更。追加計測・仕様判断は省略し、24で文書評価報告を technical-director に依頼。

2026-10-11 — 25で文書評価報告が完了。予定どおり26で game-director の Review を開始する。未判定事項は承認済み範囲内の報告事項であり、新たな escalation や QA 再依頼は不要。

## Next action

game-director が `26-studio-to-game-director.md` を受け、25の報告と既存 QA 結果を D-004 の変更後の完了条件に照らして Review し、達成 verdict を Studio に返す。

Studio は達成判断を受けて Close し、文書評価の完了と挙動実証の限界を Owner 向け Outcome に明記する。追加の Owner 回答は不要。

## Outcome

25で文書評価報告を完了し、Review は未完了。Owner は D-004 により、模擬ビルド記述の文書評価を本 Goal の検証とし、計測不能項目を未判定と明記して閉じることを決定した。

報告は文書上の整合、クールダウン起点の仕様不足、全4環境の条件別証拠不足、将来の検証再開条件を記録している。従来の独立 QA 総合判定は question のままであり、不具合解消や全条件合格は実証していない。最終 Outcome は Review 後に記録する。
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/build-0.4.md
# Build 0.4 — what playing it looks like

Build identifier: 0.3-G001-15.

The following behavior applies on desktop with keyboard or gamepad, at both 30 and 60 FPS.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. Outside protected periods, you take damage if three arrive at once.
- Room 3: Spitter projectiles are slow; a single step sideways avoids them. You can walk up and defeat a Spitter with two swipes.
- Room 4–5: backing into a corner, facing the Grubs and swiping remains effective. Stepping aside avoids projectiles.
- Dashing is rarely necessary to clear rooms. Holding position and swiping remains effective throughout a run.

## Dash and damage

A dash covers four tiles over 0.25 seconds on an unobstructed straight path. Walls still stop movement. Grub contact and Spitter projectile hits cost no hearts throughout the dash, including its early and late portions.

Without protection from a dash or recent damage, either kind of hit removes one heart and prevents input for 0.3 seconds. Input then recovers, while further hits remain harmless until 0.8 seconds after the damaging hit.

Dashing as soon as input recovers does not expose you to damage during the dash. Ending that dash does not cut short the remaining protection from the earlier hit.

For example, after taking damage at 0 seconds:

- If you begin a dash around 0.70 seconds, a contact or projectile hit around 0.85 seconds costs no additional hearts while you are still dashing. A hit around 1.10 seconds removes one heart, provided you have not started another dash or taken another damaging hit.
- If you begin a dash around 0.34 seconds, a hit around 0.70 seconds costs no additional hearts even though the dash has ended. A hit around 0.95 seconds removes one heart under the same conditions.
- Without another dash, contacts around 0.15, 0.45 and 0.70 seconds cost no additional hearts. Input is unavailable during the first 0.3 seconds and available afterward.

These timings describe hits that actually connect strictly before or after the stated boundaries.

Harmless hits do not start another period of input loss or postpone when damage can occur again. Multiple harmless contacts or projectile hits have the same result. With no preceding damage, hits during a dash leave hearts unchanged, and a hit 0.40 seconds after dash start removes one heart once that dash has ended. Projectile disappearance on impact remains unchanged.

## Other controls and timing

An attack pressed during a dash waits until the dash ends, then occurs once. Dash reuse remains restricted by the existing 0.6-second cooldown. Attack, dash and pause remain the available action buttons.

At 60 FPS, 0.25 seconds spans 15 frame intervals. At 30 FPS, it falls between seven and eight frame intervals; the dash ending is visible on an updated frame rather than at a separately displayed halfway point. The exact displayed ending frame and the outcome of a hit coinciding precisely with dash start or end are not established here. The protection behavior above applies to hits clearly inside the dash or clearly within the protection following damage at either frame rate.
>>>END

<<<FILE goals/G-001-dash-damage/11-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 11
from: qa
to: studio
stage: Observe
outcome: done
---
# 11: qa → studio — ダッシュ中被ダメージの仕様不一致と修正受け入れ条件

## Task

本報告を基に、既存仕様を維持する修正の技術調査・計画へルーティングする。修正後は更新された模擬ビルドを独立した QA に渡し、下記の受け入れ条件を検証する。

## Context

G-001 は「ダッシュ中なのにダメージを受けることがある」という不具合の修正である。D-002 により Owner の部分的な観察を使って継続することが決まった。

今回は `studio/skills/reproduce-defect.md` に従い、Owner の観察、`design/combat.md`、`sim/build-0.3.md` を照合した。dry-run のためビルド実行に相当する作業は模擬資料の読解であり、新しい実測や試行は行っていない。Observe の評価完了であり、修正完了・Verify 合格ではない。

## Findings

### 不具合報告

**件名:** 被弾後のダッシュ中に再度ダメージを受けることがある。

**仕様上の期待結果:** `design/combat.md` の Player kit は、ダッシュを 0.25 秒、その全時間を無敵と定義している。先行する被弾の有無にかかわらず、ダッシュが継続している間の Grub 接触や Spitter 弾の命中によってハートが減ってはならない。被弾時は 1 ハート減少、0.3 秒の入力不能、その後は被弾から 0.8 秒まで無敵となる。

**実際の結果と根拠:**

| 根拠 | 得られた情報 | 確認の限界 |
|---|---|---|
| `sim/build-0.3.md` 末尾のプレイヤー観察 | 被弾直後にダッシュすると、ときどきダッシュ途中でダメージを受けると明記されている | 敵種、入力方式、FPS、イベント時刻、頻度は不明 |
| Owner の観察（D-002） | 部屋1〜2、PC・60 FPS・ゲームパッド。Grub に噛まれ、硬直終了後に少し待ってダッシュすると、後半で別の Grub に接触して 1 ハート減少 | 被弾から約 0.5〜0.8 秒、約 10 回中 6 回はいずれも体感・概数 |
| Owner の比較観察（D-002） | 被弾直後すぐのダッシュと未被弾時のダッシュでは発生を観察していない | 比較試行数と実際のダッシュ開始時刻が不明。非発生の保証ではない |
| Owner の追加観察（D-002） | Spitter 弾でも 1 回あった | 部屋、タイミング、先行被弾源などの詳細は不明 |

模擬資料だけからも「ダッシュ途中の被ダメージ」と「全ダッシュ時間無敵」の仕様不一致を確認できる。一方、Owner の詳細条件を独立した試行で再現したとは判断しない。最小の安定再現手順と発生境界は未確定である。

模擬資料の「被弾直後」と Owner の「硬直終了後に少し待つ」は、同じタイミングを意味するとは限らない。どちらも正確な時刻がなく、比較条件の一致や矛盾の解消まではできない。

**重大度:** プレイ体験を損なう。仕様上安全な回避行動中にハートを失い、回避の信頼性に影響する。進行不能を示す資料はない。頻度は模擬資料の「ときどき」と Owner の概数のみで、測定済みの発生率はない。

### 後続で実施する再現・比較手順

以下は検証手順であり、実施済みの結果ではない。

1. PC・60 FPS・ゲームパッドで、部屋1〜2の Grub 接触を対象にする。ダッシュが使用可能な状態とハート数を記録する。
2. Grub に噛まれて初回の 1 ハート減少を確認する。初回被弾、入力不能終了、ダッシュ入力・実際の開始、再接触、ダッシュ終了とハート変化を区別して記録する。
3. 入力可能になってから少し待ち、Owner の体感範囲である被弾後約 0.5〜0.8 秒を探索対象としてダッシュする。別の Grub とダッシュ中に接触する配置を用いる。総敵数、位置、方向、実際の開始時刻を記録する。
4. 先行被弾後の待ち時間だけを変え、入力可能になった直後にダッシュする比較を行う。入力不能中の予約操作は前提にしない。
5. 先行被弾がない状態でもダッシュ中に Grub と接触する比較を行う。
6. 命中源を Spitter 弾に変えて同じ比較を行う。先行被弾源は別途記録し、Owner の詳細条件が判明したとは扱わない。
7. 各条件を PC の 30 / 60 FPS とキーボード・ゲームパッドの全4組合せで確認する。各試行の条件・回数・発生数を残す。

比較対象でもダッシュ中の接触・命中を確認する。攻撃が届かなかった試行だけでは、無敵の検証にはならない。

### 修正の受け入れ条件

以下は `design/combat.md` に基づく。全条件を PC・30 / 60 FPS・キーボード / ゲームパッドで検証する。現時点の判定はすべて未検証。

| ID | 条件・操作 | プレイヤーから観察できる期待結果 |
|---|---|---|
| AC-1 | 被弾していない状態でダッシュし、Grub 接触／Spitter 弾命中を受ける | ダッシュ中はハートが減らない |
| AC-2 | 被弾後、0.3 秒の入力不能が終了してから直ちにダッシュし、接触／弾命中を受ける | 実際のダッシュ中はハートが減らない |
| AC-3 | 被弾後に間をおいてダッシュし、ダッシュ途中で被弾後 0.8 秒を経過する条件を作る。その経過後かつダッシュ終了前に接触／弾命中を受ける | ダッシュ後半もハートが減らない |
| AC-4 | ダッシュ終了後も被弾後 0.8 秒までの無敵時間が残る条件で、終了後かつ無敵時間内に接触／弾命中を受ける | ハートが減らない |
| AC-5 | ダッシュ中でも被弾後の無敵時間中でもない状態で Grub に接触する | 通常どおり 1 ハート減り、0.3 秒入力不能となる。その後、被弾から 0.8 秒までは追加のハート減少がない |
| AC-6 | 通常のダッシュとダッシュ中の攻撃入力を確認する | 4 タイルを 0.25 秒で移動し、クールダウン 0.6 秒を維持する。ダッシュ中の攻撃は終了時に発動する |

AC-3 の検証用設定例は「被弾後 0.7 秒にダッシュ開始、0.85 秒に命中」である。仕様上のダッシュ終了は 0.95 秒となるため、被弾由来の無敵終了後にもダッシュ中の保護を検証できる。これは仕様から算出した予定条件であり、Owner の計測値や実施結果ではない。各 FPS で実際のイベント順序を確認し、完全同時の境界は避ける。

入力不能中の予約入力、ダッシュ開始・終了と命中が完全同時の場合の優先順位は、この受け入れ条件で新たに定義しない。それらの判断が修正や検証に必要になった場合は game-designer へ戻す。

### 解消した不足と具体的な残件

**解消した事項:**

- 必須の戦闘仕様と模擬ビルド本文が揃い、期待結果と既知の仕様不一致を照合できた。
- Owner の追加観察から、優先調査条件、比較条件、環境、主な命中源を設定できた。
- 修正へ渡す不具合報告と受け入れ条件を作成できた。追加の Owner 計測を Observe 再開の必須条件とする必要はない。

**技術調査・計画に残る事項:**

- 実装原因と変更箇所は未確認。担当 Role が `sim/repo-notes.md` 等の実装資料から調査する必要がある。本 packet に同資料はなく、QA は原因や方式を断定しない。
- 安定再現に必要な配置・時刻と発生境界は未確定。技術調査と後続の模擬検証で扱い、既存資料から得られる測定値として補完しない。
- Spitter の詳細、30 FPS、キーボードは未確認。修正後の検証対象に含める。
- Verify には、変更を反映した模擬ビルドと、各受け入れ条件を評価できる観察資料が必要。資料が結果を示さない項目は合格にしない。

**ルーティング判断:** 不具合報告は修正の技術調査・計画へ渡せる。QA の追加 Observe を同じ資料で繰り返す必要はない。ただし本報告だけでは具体的な Build 変更内容は定まっていないため、Studio は担当 Role に実装資料を渡して調査・計画を進める。修正を実施した、または合格したという判断ではない。

## Decisions already made

- `decisions/D-002-resume-with-owner-observations.md`: 部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。
- 既存の入力制約: Owner 承認なく攻撃・ダッシュ・ポーズ以外の入力を追加しない。

## Constraints

- 既存仕様の不具合修正に限定し、戦闘の方向性変更や無関係なバランス調整はしない。
- Owner の体感、模擬資料の記述、今後の検証結果を区別する。
- QA は実装を変更せず、原因や修正方式を決定しない。
- 仕様未定義の境界処理が必要になった場合は game-designer に判断を返す。

## Open questions

- 技術担当は、既存の実装資料から修正箇所と変更内容を特定できるか。
- 後続の模擬ビルドで、AC-1〜AC-6 と全4環境組合せの観察結果をどのように提供するか。

現時点で Owner に追加回答を求めなければ調査へ進めない質問はない。

## Expected output

Studio が技術調査・計画へルーティングし、必要な実装資料を次の packet に含める。その後、具体的な変更内容と検証手順を備えた Build、更新済み模擬ビルドを用いる独立した Verify へ進める。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/10-studio-to-qa.md
>>>END

<<<FILE goals/G-001-dash-damage/21-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Route
outcome: question
---
# 21: qa → studio — 文書上の整合を確認、条件別証拠とクールダウン起点は未確認

## Task

全4環境・AC-1〜AC-6・必要な回帰の条件別観察を取得する経路と、クールダウン起点の原資料を確保する。取得可能な資料を揃えて独立 QA に戻す。現時点で Verify 完了・Goal 完了として扱わない。

## Context

Owner の依頼はダッシュ中の被ダメージ修正である。対象は `sim/build-0.4.md`、識別子は `0.3-G001-15`。

本 Step は `studio/skills/verify-change.md` を適用し、既存仕様、指定された AC・再現比較手順、模擬ビルドを独立に照合した。前 Handoff 19 は Constraints と Open questions のみを参照した。実装者の理由・自己評価は根拠としていない。

dry-run のビルド読解による文書評価は完了した。条件別生成観察・実測は提示されておらず、条件別試行の実施結果はない。総合 verdict は `question`。確認された不一致による `fail` ではない。

## Findings

### 証拠の採否

| 資料 | 採用する用途 | 採用しない用途 |
|---|---|---|
| `design/combat.md#player-kit` | ダッシュ全時間無敵、距離・継続、被害・入力不能・被弾後保護、予約攻撃、クールダウンの期待値 | 実施結果、クールダウン起点の確定 |
| `11-qa-to-studio.md` の受け入れ条件・再現比較手順 | 必須条件、命中の成立、有効な時間関係、全4環境の検証要件 | 記載された設定例を実測値とすること |
| `sim/build-0.4.md` | 対象ビルドの挙動記述としての文書照合 | 条件別試行記録、生成観察、発生率 |
| `sim/build-0.3.md` | 従来はダッシュ途中の被害が記述されていたことの比較 | 同一条件による修正前後試行 |
| `project.md#constraints` | dry-run、Desktop、30／60 FPS、両入力方式の対象範囲 | 全環境で検証済みという証明 |
| Handoff 20 の D-003 要約 | 発生源別保護の論理和、防いだ命中で保護を開始・延長しないという承認済み期待 | 実装適合の証拠 |

Build 0.4 の時刻例は「命中が成立し、境界の厳密な前後にある挙動」の記述として採用できる。ただし、個々の環境でその状態を生成した記録ではない。冒頭の全環境への適用宣言も条件別実施記録には代えられない。

### AC ごとの文書評価

以下の「文書整合」は条件別合格を意味しない。期待値の出典は `design/combat.md#player-kit` と `11-qa-to-studio.md#修正の受け入れ条件`。ビルド参照節は B-D＝`sim/build-0.4.md#dash-and-damage`、B-C＝同 `#other-controls-and-timing` とする。

| ID・対象 | 期待挙動 | ビルド記述と文書評価 | 条件別証拠の不足 |
|---|---|---|---|
| AC-1：未被弾、Grub／Spitter | ダッシュ中の命中でハート不変 | B-D は先行被弾なしでもダッシュ中の命中は無害と明記。文書整合 | 未被弾の初期状態、入力・受理・開始終了、両命中源の成立とハート前後値 |
| AC-2：入力回復直後、Grub／Spitter | 実際のダッシュ中はハート不変 | B-D は入力回復直後のダッシュも保護すると明記。文書整合 | 初回被害、入力不能終了と直後の受理、ダッシュ中の命中、ハート前後値 |
| AC-3：被弾保護が先に終了、Grub／Spitter | 被弾後0.8秒を過ぎてもダッシュ中はハート不変 | B-D の約0.70秒開始・約0.85秒命中が対応。文書整合 | 実際の各イベント時刻・順序、0.8秒経過後かつダッシュ終了前の命中成立 |
| AC-4：ダッシュが先に終了、Grub／Spitter | ダッシュ終了後も被弾後0.8秒までハート不変 | B-D の約0.34秒開始・約0.70秒命中が対応。文書整合 | 実際のダッシュ終了、残存保護内の命中成立、ハート前後値 |
| AC-5：無保護時のGrub接触 | 1ハート減、0.3秒入力不能、被弾後0.8秒まで追加被害なし | B-D の通常被害と約0.15／0.45／0.70秒接触例が対応。文書整合 | 初回・入力不能中・回復後の接触結果、入力不能開始終了と操作の受理、ハート前後値 |
| AC-6：通常移動・予約攻撃・再使用 | 4タイル／0.25秒、終了時に予約攻撃、0.6秒クールダウン維持 | B-D は障害物のない直線で距離・継続を明記。B-C は終了時の攻撃1回、既存0.6秒制限を明記。距離・継続・攻撃は文書整合。クールダウンは数値のみ整合 | 移動開始終了・距離、攻撃入力と発動時刻・回数、起点の定義、制限内拒否・経過後受理の記録 |

Build 0.4 に、今回の AC に反する具体的挙動は確認できなかった。AC-6 のクールダウン起点は期待値自体が不足しており、完全な文書適合を判定できない。

### 回帰の文書評価

期待値は既存戦闘仕様と D-003 要約による。各行とも条件別結果は未確認。

| 枝 | 期待挙動 | 文書上の根拠・評価 | 不足する観察 |
|---|---|---|---|
| 被弾保護が先に終了 | ダッシュ保護が残る | B-D の約0.70秒開始例。整合 | 両保護の終了順序と、その間の両命中源による命中 |
| ダッシュが先に終了 | 被弾保護が残る | B-D の約0.34秒開始例。整合 | 同上 |
| 両保護終了後 | 新しい保護がなければ通常の1ハート被害 | B-D の約1.10秒／約0.95秒命中例。整合 | 各終了順序の後で両命中源による被害と新しい保護の有無 |
| 防いだ複数命中 | 入力不能や保護を新規開始・延長しない | B-D は複数の無害な接触・弾にも同じ結果と明記。整合 | 複数命中の時刻、操作受理、当初の保護終了後の被害 |
| ダッシュ単独の複数命中と終了後 | ダッシュ中は無害、終了後に保護を持ち越さない | B-D は先行被弾なし・開始後0.40秒の被害と複数命中の挙動を記述。整合 | 未被弾状態、両命中源の複数命中、終了後の命中と被害 |
| Spitter通常被害・弾消失 | 無保護時の被害と衝突時消失を維持 | B-D は通常1ハート被害と弾消失の維持を記述。前者は文書整合、後者は維持宣言まで | 命中・被害・弾消失を結ぶ条件別観察。旧ビルドには消失の比較記録なし |

新しい入力は B-C に記述されておらず、攻撃・ダッシュ・ポーズのみという制約と整合する。部屋攻略の一般記述は無敵やクールダウンの条件別検証には用いない。

### 全4環境の判定

U＝条件別証拠不足により未判定。US＝証拠不足に加えてクールダウン起点が未定義。

| 対象 | 30 FPS・キーボード | 30 FPS・ゲームパッド | 60 FPS・キーボード | 60 FPS・ゲームパッド |
|---|---|---|---|---|
| AC-1：Grub／Spitterそれぞれ | U | U | U | U |
| AC-2：Grub／Spitterそれぞれ | U | U | U | U |
| AC-3：Grub／Spitterそれぞれ | U | U | U | U |
| AC-4：Grub／Spitterそれぞれ | U | U | U | U |
| AC-5：Grub、初回・入力不能中・回復後 | U | U | U | U |
| AC-6：移動・予約攻撃 | U | U | U | U |
| AC-6：クールダウン内／経過後 | US | US | US | US |
| 上記回帰の各枝・各命中源 | U | U | U | U |

すべてのセルで試行総数・有効数・無効数・不具合発生数は不明。ゼロ件・非発生として報告しない。先行被弾源も記録がなく、推定しない。

`11-qa-to-studio.md#後続で実施する再現・比較手順` にある、待ち時間を変えた比較、未被弾比較、命中源変更、全4環境での確認は、条件別実施記録としては未確認である。Build 0.3 と0.4の照合では「ダッシュ途中で被害」から「全時間無害」への記述変更を確認できるが、同じ配置・入力時刻での再現と修正確認にはならない。

### 仕様不足と観察不足の分離

1. **クールダウン起点：仕様不足。**  
   `design/combat.md#player-kit` の原文は “Cooldown 0.6 s.”、AC-6 は「クールダウン 0.6 秒を維持する」、B-C は “existing 0.6-second cooldown”。開始・終了・入力受理のどれを起点とするかは記載がない。これらの数値に矛盾はないが、再使用可能時刻を一意に定められない。既存の起点を定めた原資料を回復し、なければ Studio から game-designer に返す。QA は起点を決めない。

2. **30 FPS の終了表示・フレーム内順序：観察不足。**  
   B-C は0.25秒が7〜8フレーム間隔の間に位置すると説明するが、実際の終了更新フレームを示さない。この記述だけで継続時間違反とは判定できない。内部の経過時刻・状態遷移と表示更新の関係が必要。証拠取得後も期待値を定められない場合に限り、必要な仕様判断を返す。

3. **完全同時の命中優先順位・入力不能中の予約入力：今回の AC で未定義のまま。**  
   AC は完全同時の境界を避け、入力回復後の操作を確認する。これらを新規仕様として決めることは今回の開始条件ではない。検証上避けられない場合は game-designer に返す。

### 必須追加入力

| 入力 | 影響するセル・必要な理由 | 既知の取得元・取得状況 |
|---|---|---|
| 対象識別子に対応した条件別生成観察 | 全セル。環境・AC・命中源・枝ごとの独立判定に必要 | runtime の simulator が更新を担うことは project.md に記載。窓口・取得手段は不明 |
| 観察の来歴とモデル情報 | 全セル。対象変更との対応、版、初期状態、FPS・入力方式の表現範囲を判断するため | runtime 管理側が候補。提供主体・取得方法は未確認 |
| 再現・比較条件とイベント記録 | AC-1〜AC-5と回帰。配置、敵数、位置・方向、先行被弾源、命中成立、入力と受理、ダッシュ・保護・入力不能の開始終了、ハート前後値が必要 | 条件別観察資料としての提供が必要。既存資料の所在は不明 |
| 移動・予約攻撃・再使用記録 | AC-6全環境。距離・継続、攻撃発動1回、制限内拒否・経過後受理を判定するため | 同上 |
| 試行一覧と集計根拠 | 全セル。試行総数・有効数・無効数・発生数と各記録の対応、無効理由を確認するため | 同上。命中しなかった試行を無敵の成功例に数えない |
| クールダウン起点を定めた既存原資料 | AC-6の再使用判定。期待時刻を確定するため | 現 packet の combat・AC・build にはない。原資料の所在は不明。回復できなければ game-designer の判断が必要 |
| 時刻・フレーム・イベント順序の説明 | 特に30 FPSのAC-2〜AC-4・AC-6、回帰の終了順序。命中が境界の内外どちらか判定するため | runtime のモデル／観察資料が候補。未取得 |

`sim/qa-G001-15.md` は未取得という引継ぎがあるだけで、存在・内容を確認できない。必須なのは上記の内容であり、そのファイル名であることではない。未生成・未取得資料を Load に含めない。

既存の仕様文書を補完できればクールダウン起点の不足は解消し得る。Build 本文への一般的な適用宣言の追加だけでは条件別試行要件は満たせない。既存の生成記録があるなら、その来歴・条件・結果の提供で解消できる可能性があるが、存在は未確認である。

照会経路の状態は引き続き「照会手段未確保」。問い合わせ実施済み、モデル不存在、取得不可能のいずれも断定しない。新規 simulator 開発や追加 Owner 計測を要求していない。

## Decisions already made

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：元の修正 Goal を継続し、追加 Owner 計測を開始条件にしない。
- D-003：発生源別保護の論理和を維持し、防いだ命中で保護を開始・延長しない。
- 本 Step はこれらの要約を超える再解釈を行っていない。

## Constraints

- 独立 Verify は未完了。文書整合を条件別合格や Goal 完了に置き換えない。
- AC-1〜AC-6、全4環境、必要な命中源・比較・回帰を維持する。
- 期待値、挙動記述、生成観察、実測を区別する。
- 不明な試行数・発生数・時刻・ハート値を補わない。
- 既存仕様の修正範囲を守り、QA は実装変更や新規仕様決定を行わない。
- 次の QA に実装者の理由・自己評価を検証根拠として渡さない。

## Open questions

1. Studio は runtime 管理側の窓口・取得手段を確保し、必要な条件別記録の有無と提供範囲を確認できるか。
2. 取得可能なモデル・記録は、全4環境の入力受理・命中・状態遷移をどこまで表現しているか。
3. 既存クールダウン起点の原資料はどこにあるか。回復できない場合、game-designer へ判断を返せるか。

## Expected output

Studio は取得経路と必要資料の担当を具体化し、実際に取得した資料を次の packet に含める。仕様判断が必要なら該当する問いを game-designer に返す。

独立 QA は補完された資料から各セルの証拠を採否判断し、全条件を評価する。本 Step では確認された仕様不一致がないため修正差し戻しの `fail` は出さず、証拠不足と一部期待値未定義による `question` として返す。

## Load

- Project: project.md#constraints
- Project: design/combat.md
- Build: sim/build-0.4.md
- Comparison build: sim/build-0.3.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md#修正の受け入れ条件
- Exercise procedure: goals/G-001-dash-damage/11-qa-to-studio.md#後続で実施する再現・比較手順
- Previous handoff: goals/G-001-dash-damage/20-studio-to-qa.md
- Decisions: 本文の既存要約のみ。追加原文なし。
- Studio の Role・Skills と次工程の Load は Studio がルーティング時に確定する。
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-002-resume-with-owner-observations.md
---
kind: decision
id: D-002
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: Owner の補足観察を受けて修正を継続する

## Decision

Owner は `goals/G-001-dash-damage/09-studio-to-owner.md` の Option A を選択した。提供された部分的な観察を新しい入力として QA の Observe を再開し、元の修正 Goal を継続する。ゲーム仕様、実装、受け入れ条件を変更する決定ではない。

Owner の回答原文：

> A。私のプレイでの観察です(計測ではなく体感)。部屋1〜2でGrubに噛まれたあと、硬直が解けてから少し間をおいて(被弾から体感0.5〜0.8秒くらい)ダッシュすると、ダッシュの後半で別のGrubに触れてハートが1減る。被弾直後すぐにダッシュした場合と、被弾していないときのダッシュでは起きない。60 FPSのPC・ゲームパッドで10回中6回ほど。Spitterの弾でも1回あった。30 FPSでは試していない。

この回答は Owner の体感による観察であり、計測ログや独立した再現確認ではない。QA が既存仕様と照合し、確認可能な範囲と未確認事項を判断する。

## Rationale

元の依頼は不具合の修正である。発生場面、被弾後の操作、比較条件、環境、おおよその頻度という新しい情報が提供されたため、同じ資料だけの再試行を避けて調査を再開できる。

## Alternatives considered

- Option B — 現資料での調査報告への範囲縮小。Owner は修正の継続を選択した。
- Option C — 未修正のまま中止。Owner は継続を選択した。

## Revisit when

追加観察を評価しても、修正に不可欠な情報が Role の作業や既存の模擬資料から得られないと判明した場合。範囲変更、中止、または既存仕様を変更する必要が生じた場合は、適切な権限へ判断を戻す。
>>>END

<<<FILE decisions/D-003-independent-invulnerability.md
---
kind: decision
id: D-003
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-003: 無敵の終了を発生源ごとに管理する

## Decision

ダッシュ由来と被弾由来の無敵を独立して管理し、ダメージ判定時の有効な無敵を両者の論理和とする。

- ダッシュ開始はダッシュ由来の保護だけを開始し、終了はその保護だけを終了する。
- 実際に被害が成立した場合にのみ、既存の被弾処理と被弾後 0.8 秒までの保護を開始する。
- 被弾由来の保護の終了は、ダッシュ由来の保護を解除しない。
- 無敵で防いだ接触・命中によって、被弾由来のタイマーを開始・延長しない。
- 既存のタイマー機構を再利用し、共通フラグを各タイマーが直接オフにする方式を廃止する。

これは既存仕様に合わせる内部実装の判断である。ダッシュ、入力不能、攻撃予約、クールダウンの時間や起点、同時イベントの優先順位は変更しない。

## Rationale

`sim/repo-notes.md` では、二種類のタイマーが一つの無敵フラグをそれぞれオフにする。先に終了したタイマーが、まだ継続すべき別の保護を消す構造になっている。

発生源を分離すれば、被弾由来の保護がダッシュ途中で終了するケースと、ダッシュ終了後も被弾由来の保護が残るケースの両方を扱える。小規模な変更で既存システムを再利用できる。

## Alternatives considered

- **被弾タイマー終了時だけダッシュ中か確認する:** ダッシュ終了が被弾由来の保護を消す逆順の問題を残すため不採用。
- **無敵の長さを延ばす、被弾後のダッシュを制限する:** 既存のプレイヤー向け仕様を変更するため不採用。
- **単一の無敵終了時刻を最大値で更新する:** 現在の二つの固定時間でも実現可能だが、ダッシュの実際の継続状態と保護の対応、および各発生源の終了を明確に扱える独立管理を採用する。
- **汎用の参照カウント／トークン機構を導入する:** 現資料の二つの発生源に対して過大で、解除漏れなどの新たな管理負担があるため不採用。

## Revisit when

第三の無敵発生源、ダッシュの中断、状態の保存・復元など、現資料にない要件が判明した場合。ゲーム仕様の判断が必要なら game-designer に戻し、この Decision だけで挙動を追加しない。
>>>END

<<<FILE decisions/D-004-document-evaluation-scope.md
---
kind: decision
id: D-004
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-004: 模擬ビルドの文書評価を Goal の検証とする

## Decision

Owner の回答原文：

> B。模擬専用のサンプルなので、模擬ビルド記述に基づく文書評価をこの Goal の検証とし、計測できない項目は未判定として明記したうえで Goal を閉じてください。

G-001 の完了条件を、修正の条件別独立検証から、現資料と模擬ビルド記述に基づく文書評価、未判定事項、再開条件の報告へ変更する。対象は `sim/build-0.4.md`、変更識別子 `0.3-G001-15`。

追加計測や外部資料取得は今回の完了条件としない。文書評価をこの Goal の検証として扱うが、測定できない挙動は未判定とし、全4環境の実証、全条件合格、不具合解消の保証へ読み替えない。既存 QA の `question` を過去に遡って `pass` に変更しない。

報告を作成し、変更後の完了条件に対する game-director の Review を経て Studio が閉じる。Owner の選択だけでは報告作成・Review 済みとは扱わない。

D-002 の修正継続方針は、この Goal の完了条件について本 Decision により変更する。D-001 の入力制約、D-003 の発生源別保護、ゲーム仕様と既存の模擬変更は維持する。新規 simulator 開発、実機試験、追加実装、巻き戻しは承認しない。

## Rationale

模擬専用サンプルという用途に合わせ、Owner が文書評価による完了を明示的に選択した。測定不能な項目を未判定として残すことで、報告の完了と挙動の実証を区別する。

## Alternatives considered

- A：アクセス・資料を手配して元の独立検証を継続する。今回は追加取得を完了条件としない選択となった。
- B の報告のみへの縮小：採用し、Owner の条件により文書評価を本 Goal の検証と位置づける。
- C：未検証のまま中止する。Owner は文書評価を経た完了を求めており、中止は選択していない。

## Revisit when

実際の不具合解消や全4環境での動作保証が必要になったとき、または条件別証拠・モデルへのアクセスが得られて未判定項目の検証を再開するとき。Studio を通じて範囲、対象ビルド、仕様、必要入力を再確認する。
>>>END

<<<FILE goals/G-001-dash-damage/25-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 25
from: technical-director
to: studio
stage: Route
outcome: done
---
# 25: technical-director → studio — 文書評価報告を完了し、変更後の完了条件の Review へ渡す

## Task

本報告を、D-004 による変更後の完了条件に対する game-director の Review へ渡してください。Review 後、Studio がその結果に基づいて Close を行ってください。

## Context

G-001 はダッシュ中の被ダメージを既存仕様に合わせる修正として開始した。条件別証拠の取得経路が確保できず、独立 QA の Handoff 21 は文書評価完了・総合判定 `question` を報告した。

Owner は D-004 で、模擬ビルド記述に基づく文書評価を本 Goal の検証とし、計測できない項目を未判定として報告したうえで閉じる方針を承認した。本 Step はその報告作成を完了したものであり、条件別試行の実施、QA 判定の変更、Goal 達成の自己承認ではない。

## Findings

### 1. 対象と参照資料

評価対象は **`sim/build-0.4.md`、変更識別子 `0.3-G001-15`**。`sim/repo-notes.md` の Implemented change identifier と Current build description が一致している。旧 build-0.3 を今回の評価対象とはしない。

| 参照資料 | 本報告での用途と限界 |
|---|---|
| `project.md#constraints` | dry-run、Desktop、30／60 FPS、キーボード／ゲームパッド、既存システム再利用と入力制約。実機や条件別試行の証拠ではない |
| `design/combat.md` の Player kit | ダッシュ、被害、入力不能、被弾後保護、予約攻撃、クールダウンの仕様 |
| `11-qa-to-studio.md` の受け入れ条件・再現比較手順 | AC-1〜AC-6、命中成立、比較条件、全4環境の要求。設定例は実施結果ではない |
| `sim/build-0.4.md` | 現在の模擬挙動を仕様と照合する主資料。条件別生成観察・計測ログではない |
| `sim/repo-notes.md` | 対象変更の識別、D-003 との技術的整合、提供情報の限界。実装説明を独立した挙動実証には用いない |
| `19-technical-director-to-studio.md` | 回帰の枝、必要証拠、将来の取得・検証経路。記載の計画を実行済みとは扱わない |
| `21-qa-to-studio.md` | 既存の独立 QA による文書評価、証拠不足、総合 `question` の記録 |
| D-001〜D-004 | 入力制約、継続判断、発生源別保護、今回の完了条件 |
| `23-technical-director-to-owner.md`、`24-studio-to-technical-director.md` | Owner の選択、照会状況、今回の報告範囲と後続工程 |

上記の提供原文を照合した。旧ビルド原文は本 packet にないため、修正前の挙動は Handoff 11・21 と D-002 の記録としてのみ参照する。同一条件での修正前後比較を実施したとは判断しない。

以下で「文書整合」は仕様と模擬挙動の記述が対応することを示し、条件別合格を意味しない。B-D は `sim/build-0.4.md` の「Dash and damage」、B-C は「Other controls and timing」を指す。

### 2. AC-1〜AC-6 の文書評価

期待値の出典は `design/combat.md` の Player kit と Handoff 11「修正の受け入れ条件」。

| AC・対象 | 文書上の評価と根拠 | 未判定事項 |
|---|---|---|
| AC-1：未被弾でのダッシュ、Grub／Spitter | 文書整合。B-D は両命中源についてダッシュ前半・後半を含む全時間の無被害と、先行被弾なしのハート不変を記述 | 未被弾の初期状態、入力受理、実際の開始・終了、各命中源の前半・後半の命中成立、ハート前後値 |
| AC-2：入力回復直後のダッシュ、Grub／Spitter | 文書整合。B-D は入力回復直後にダッシュしてもダッシュ中に被害を受けないと明記 | 初回被害、0.3秒の入力不能終了、最初の入力可能機会での操作・受理、ダッシュ中の命中とハート前後値 |
| AC-3：被弾保護がダッシュ途中で先に終了、Grub／Spitter | 文書整合。B-D の被弾後約0.70秒開始・約0.85秒命中の例は、被弾後0.8秒を過ぎてもダッシュが保護する記述 | 実際の時刻・フレーム順序、被弾保護終了より後かつダッシュ終了より前の命中成立と無被害 |
| AC-4：ダッシュ終了後に被弾保護が残る、Grub／Spitter | 文書整合。B-D の約0.34秒開始・約0.70秒命中の例は、ダッシュ終了が残存する被弾保護を切らない記述 | 実際のダッシュ終了、残存保護内の命中成立、ハート前後値 |
| AC-5：無保護時の Grub 接触 | 文書整合。B-D は1ハート減少、0.3秒入力不能、被弾後0.8秒までの保護を記述。約0.15／0.45／0.70秒の接触例も対応 | 初回・入力不能中・回復後の各接触、入力不能の開始・終了、回復後の入力受理、ハート前後値 |
| AC-6：距離・継続・予約攻撃 | 文書整合。B-D は障害物のない直線で4タイル／0.25秒、B-C はダッシュ中の攻撃入力が終了時に1回発動すると記述 | 移動端点・距離・継続時間、実際の終了フレーム、攻撃入力と発動時刻・回数 |
| AC-6：クールダウン | 0.6秒という数値は整合。B-C は既存の0.6秒制限を維持すると記述。ただし起点未定義のため完全な文書適合は未判定 | 起点の仕様、再使用可能時刻、制限内の拒否・経過後の受理。仕様不足と観察不足の両方がある |

Build 0.4 の記述に、これらの AC に反する具体的挙動は確認できなかった。ただし、時刻例は境界の厳密な前後に成立する命中の説明であり、測定されたイベント列ではない。

### 3. 必要な回帰の文書評価

期待値は既存戦闘仕様と D-003、枝の対応は Handoff 19・21 に基づく。各行の条件別結果は未判定。

| 回帰対象 | 文書上の評価と根拠 | 未判定事項 |
|---|---|---|
| 回帰1：被弾保護が先に終了し、ダッシュ保護が残る | 整合。B-D の約0.70秒開始・約0.85秒無被害、約1.10秒通常被害の例が対応 | Grub／Spitter それぞれの終了順序、残存保護中の命中、両保護終了後に新しい保護がない状態での通常被害 |
| 回帰2：ダッシュが先に終了し、被弾保護が残る | 整合。B-D の約0.34秒開始・約0.70秒無被害、約0.95秒通常被害の例が対応 | 両命中源について、ダッシュ終了後の残存保護と両保護終了後の通常被害 |
| 回帰3：防いだ複数命中が入力不能・保護を開始または延長しない | 整合。B-D は無害な命中が入力不能を再開せず、次に被害が可能となる時刻も遅らせず、複数の接触・弾でも同じと明記 | 両終了順序 × 両命中源について、異なるフレームで2命中以上、入力受理、元の期限、期限後の被害を結ぶ記録 |
| 回帰4：ダッシュ単独の複数命中と終了後 | 整合。B-D は先行被弾なしのダッシュ中無被害、複数命中でも同じ挙動、ダッシュ開始後0.40秒の通常被害を記述 | 未被弾状態、両命中源それぞれの複数命中、終了時刻、保護を持ち越さないことを示す終了後の被害 |
| Spitter の通常被害と弾消失 | B-D の無保護時1ハート被害は整合。衝突時の弾消失は維持宣言まで確認 | 命中・通常被害・弾消失の条件別記録。弾消失の修正前後比較 |
| 入力・移動等の維持 | B-C の攻撃・ダッシュ・ポーズは D-001 と整合。B-D は壁で移動が止まると記述。repo-notes は敵 AI、Flinch、移動、攻撃ダメージ・硬直の維持を宣言 | 各維持事項の独立した回帰記録。維持宣言だけから動作保証はできない |

技術記述として、repo-notes の「Player invulnerability」「Contact and projectile damage」は D-003 と整合する。保護を発生源別に保持し、論理和を共通被害入口で評価し、各終了処理が自身の保護だけを解除する。防いだ命中はハート、入力不能、被弾保護と期限を変更しない。この対応は実装説明の文書照合であり、独立 QA の証拠を追加するものではない。

### 4. 全4環境の証拠不足

U＝条件別証拠不足による未判定。US＝証拠不足に加え、クールダウン起点の仕様不足。

| 対象 | 30 FPS・キーボード | 30 FPS・ゲームパッド | 60 FPS・キーボード | 60 FPS・ゲームパッド |
|---|---|---|---|---|
| AC-1〜AC-4：各 AC、Grub／Spitter の各枝 | U | U | U | U |
| AC-5：Grub の初回・入力不能中・回復後 | U | U | U | U |
| AC-6：距離・継続・予約攻撃 | U | U | U | U |
| AC-6：クールダウン内／経過後 | US | US | US | US |
| 回帰1〜4：各終了順序・各命中源 | U | U | U | U |
| Spitter 通常被害・弾消失、その他の維持事項 | U | U | U | U |

Build 0.4 冒頭は全4環境への適用を宣言しているが、環境ごとの実施記録ではない。repo-notes「Limits of available implementation detail」も、時刻例が測定ログではなく、配置・衝突・初期ハート・試行総数を再構成できないと明記している。

すべてのセルで試行総数、有効数、無効数、不具合発生数は不明。ゼロ件や非発生には置き換えない。先行被弾源も推定しない。待ち時間変更、未被弾比較、命中源変更を含む Handoff 11 の比較手順について、条件別実施記録はない。

D-002 の60 FPS・ゲームパッドでの観察は修正前の体感による報告であり、最新ビルドの当該環境を実証する資料にはならない。

### 5. 仕様不足と観察証拠不足

**クールダウン0.6秒の起点は仕様不足。**  
combat は「Cooldown 0.6 s.」、AC-6 は0.6秒の維持、B-C は既存制限の維持までを定める。repo-notes も起点を開始または終了と特定できないと明記する。入力受理・ダッシュ開始・ダッシュ終了のどれから数えるかを現資料では確定できない。これは再使用の計測ログがないこととは別の不足である。技術側では決めず、将来必要なら既存原資料の回復、回復できなければ game-designer の仕様判断へ渡す。

**30 FPS の終了フレームと更新順序は観察・実装詳細の不足。**  
B-C は0.25秒が30 FPSで7〜8フレーム間隔の間、60 FPSで15フレーム間隔に相当すると説明するが、実際の終了表示フレームは確定していない。repo-notes もタイマー更新順序と最終区間の移動積分を未提示としている。これだけで継続時間違反とは判定せず、独自の丸め規則・許容差も設けない。将来、詳細が得られても期待値が定まらない場合に必要な仕様判断へ進む。

**完全同時の命中優先順位・入力不能中の予約入力は今回の AC で新たに定義しない。**  
Handoff 11 は完全同時境界を避け、入力回復後の操作を対象にしている。将来の検証で回避不能な場合のみ game-designer に返す。保存・復元、ダッシュ中断など未定義の挙動も本報告で追加しない。

### 6. 既存 QA 判定と今回の完了範囲

Handoff 21 の総合判定は **`question` のまま**。文書評価は完了しているが、条件別証拠と一部期待値が不足している。具体的な仕様不一致による `fail` ではなく、D-004 によって過去の判定が `pass` に変わることもない。

本 Step では、D-004 が求める文書評価、未判定事項、仕様不足、再開条件の報告を作成した。追加取得・問い合わせ・試行生成・計測・実機試験・実装・巻き戻しは実施していない。技術上の新たな選択もなく、D-005 は作成しない。

外部窓口については、Handoff 23・24 の記録どおり**照会手段未確保、問い合わせ未実施**。モデル不存在や永久に取得不能とは確認されていない。同じ不足を理由に今回の作業を再計測や QA 再依頼へ戻す必要はない。

### 7. 将来、独立した挙動検証を再開する条件

以下は将来の再開条件であり、今回の Review・Close の追加前提ではない。

1. **範囲と対象を再確認する。**  
   実際の不具合解消や全4環境での保証が必要になった場合、または条件別証拠・モデルへのアクセスが得られた場合、Studio を通じて必要な独立検証の範囲、対象ビルドと変更識別子、仕様・AC を確認する。新規 simulator 開発や実機試験は D-004 の承認範囲外として別途判断する。

2. **取得経路と資料の来歴を確保する。**  
   runtime 管理側などへの実際の照会経路、既存モデル・記録の有無、版・出典・対象変更との対応、FPS・入力方式の表現範囲を確認する。期待値の文章の再出力を試行結果として採用しない。

3. **期待値の不足を解消する。**  
   クールダウン起点の既存原資料を回復し、回復できなければ game-designer が判断する。30 FPS の更新順序等は資料を先に確認し、必要になった仕様判断だけを返す。

4. **条件別記録を揃える。**  
   全4環境・AC・各命中源・回帰の各枝に対し、配置と衝突条件、初期状態、先行被弾源、予定時刻と実際の時刻、フレームと処理順序、入力と受理、ダッシュ・保護・入力不能の遷移、命中成立、ハート前後値、移動、攻撃、再使用を記録する。試行一覧、無効理由、総数・有効数・無効数・発生数を対応づける。必要試行数や許容差は原資料の確認なしに定めない。

5. **独立 QA が証拠を評価する。**  
   命中不成立や必要順序の不成立を成功例に数えず、取得できた枝だけを評価する。部分結果を全環境へ一般化しない。資料取得→期待値・条件確定→記録生成→独立評価の依存順序を守る。

今回はコード変更がなく、並列実装は行わない。将来も、証拠生成の前提が未確定な段階で独立したログ生成を並列依頼しない。

### 8. Owner 向け結果文

対象の模擬ビルド `sim/build-0.4.md`（`0.3-G001-15`）の文書評価を完了しました。ダッシュ中の保護、被弾後の保護、通常被害、移動と予約攻撃は既存仕様と文書上整合しています。クールダウンは0.6秒という数値のみ確認でき、起点は未定義です。全4環境の条件別挙動と回帰は証拠不足により未判定であり、不具合解消や全条件合格は実証していません。既存 QA の `question` を維持し、D-004 に沿った報告を game-director の Review に渡します。

## Decisions already made

- [D-001](../../decisions/D-001-one-button-combat.md)：Owner 承認なしに戦闘入力を追加しない。
- [D-002](../../decisions/D-002-resume-with-owner-observations.md)：部分的な Owner 観察を受けて修正を継続した。今回の完了条件は D-004 により変更。
- [D-003](../../decisions/D-003-independent-invulnerability.md)：保護を発生源別に管理し、論理和で判定する。防いだ命中で保護を開始・延長しない。
- [D-004](../../decisions/D-004-document-evaluation-scope.md)：文書評価を本 Goal の検証とし、未判定事項と再開条件を報告して Review 後に閉じる。

## Constraints

- 文書整合、条件別実証、Goal の達成 verdict を区別する。
- QA の過去の `question` を変更せず、全条件合格や不具合解消を保証しない。
- 仕様、AC、試行数、クールダウン起点を補作しない。
- 追加取得・計測・開発・実装・巻き戻しを今回の完了条件に戻さない。
- 本報告は technical-director の報告作成完了であり、Review・Close は未実施。

## Open questions

- game-director：本報告は D-004 の変更後の完了条件を満たすか。

挙動の未判定事項と仕様不足は Findings に記録済み。今回、Owner に追加回答を求める質問はない。

## Expected output

Studio は本報告を game-director の Review へ route する。game-director は D-004 の変更後の完了条件に対して達成 verdict を返す。その結果に基づき Studio が Close を行い、文書評価による完了と未実証事項を終了記録に保持する。

## Load

- Report: goals/G-001-dash-damage/25-technical-director-to-studio.md
- Project: project.md#constraints
- Specification: design/combat.md
- Build: sim/build-0.4.md
- Technical reference: sim/repo-notes.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md
- Supporting plan: goals/G-001-dash-damage/19-technical-director-to-studio.md
- Existing QA assessment: goals/G-001-dash-damage/21-qa-to-studio.md
- Resolved escalation: goals/G-001-dash-damage/23-technical-director-to-owner.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Decisions: decisions/D-004-document-evaluation-scope.md
- Previous handoff: goals/G-001-dash-damage/24-studio-to-technical-director.md
- Routing note: Studio が Review の Role・Skill を指定する。未取得のモデル・条件別観察資料は Load に含めない。
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
