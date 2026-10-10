# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-dash-damage/12-studio-to-technical-director.md
next_seq: 13

## You may write

- goals/G-001-dash-damage/13-technical-director-to-<recipient>.md
- decisions/D-003-<name>.md

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

<<<FILE goals/G-001-dash-damage/12-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 12
from: studio
to: technical-director
stage: Diagnose / Plan
outcome: routed
---
# 12: studio → technical-director — ダッシュ中被ダメージの技術調査と修正計画

## Task

QA の不具合報告と実装資料を照合し、ダッシュ中の被ダメージの原因と変更箇所を調査する。既存仕様を維持する修正計画と、Build 後に独立した QA が受け入れ条件を評価できる模擬資料の要件を作成し、Studio に返す。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」である。D-002 により Owner の部分的な観察を使って元の修正 Goal を継続している。

QA は `11-qa-to-studio.md` で、模擬ビルドの「ダッシュ途中の被ダメージ」と既存仕様の「全ダッシュ時間無敵」の不一致を確認し、不具合報告と AC-1〜AC-6 を作成した。詳細条件の独立した再現や実装原因の特定は未完了だが、追加の Owner 計測を必須とせず技術調査へ進めると報告している。

このプロジェクトには実リポジトリがなく、`sim/repo-notes.md` が実装資料に相当する。Build は gameplay-engineer が変更内容を Handoff に正確に記述し、実行環境の simulator が `sim/` に反映する方式で行う。

## Findings

以下は QA 報告の要約であり、Studio が独自に検証した結果ではない。詳細な不具合報告・比較手順・受け入れ条件は前の Handoff を参照する。

- ダッシュは 0.25 秒間すべて無敵。移動距離は 4 タイル、クールダウンは 0.6 秒。ダッシュ中の攻撃は終了時に発動する。
- 通常被弾は 1 ハート減少と 0.3 秒の入力不能を伴い、被弾後 0.8 秒まで無敵となる。
- Owner は PC・60 FPS・ゲームパッド、部屋1〜2で、Grub による被弾と硬直終了後に少し待ってダッシュすると、ダッシュ後半の別の Grub 接触で 1 ハート失うと報告した。
- 被弾から約 0.5〜0.8 秒、約 10 回中 6 回という値は体感・概数であり、計測結果ではない。Spitter 弾でも 1 回の観察があるが詳細は不明。
- 実装原因、安定再現に必要な配置・時刻、発生境界は未確認。時間条件の重なりだけから実装方式や原因を断定しない。

修正計画が満たすべき QA の受け入れ条件は次のとおり。

| ID | 検証対象 |
|---|---|
| AC-1 | 未被弾時のダッシュ中は Grub 接触・Spitter 弾命中でハートが減らない |
| AC-2 | 被弾後の入力不能終了直後に開始したダッシュ中もハートが減らない |
| AC-3 | ダッシュ途中で被弾後 0.8 秒が経過しても、ダッシュ終了前の接触・弾命中ではハートが減らない |
| AC-4 | ダッシュ終了後に被弾由来の無敵時間が残る場合、その時間内はハートが減らない |
| AC-5 | 通常時の Grub 接触で 1 ハート減少、0.3 秒入力不能、被弾後 0.8 秒まで追加被害なしを維持する |
| AC-6 | ダッシュの距離・時間・クールダウンと、ダッシュ中の攻撃入力の終了時発動を維持する |

全条件を PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せで評価する。現在はすべて未検証である。

本 Route packet には `sim/repo-notes.md`、設計・Decision 本文、technical-director の契約全文と Skill 本文がない。Studio は提供された Works from と QA 報告から必要な入力を選定したが、未提供本文との整合性は確認していない。次の Step では Load の実資料を用い、要約を資料の代用にして原因や結果を創作しない。

## Decisions already made

- `decisions/D-001-one-button-combat.md`: 攻撃・ダッシュ・ポーズ以外の入力追加には Owner 承認が必要という既存制約を守る。
- `decisions/D-002-resume-with-owner-observations.md`: Owner の部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。

Decision 本文の詳細は Load 資料で確認する。

## Constraints

- 既存仕様への修正に限定し、方向変更、新しい入力、無関係なバランス調整を行わない。
- 小規模チームのため既存システムの再利用を優先し、PC・30 / 60 FPS・キーボード・ゲームパッドを対象とする。
- この Step は技術調査・計画であり、Build や QA の合否判定を代行しない。
- 模擬資料の記述、Owner の体感、仕様から算出した検証条件、実施済みの結果を区別する。
- 入力不能中の予約入力や、ダッシュ開始・終了と命中が完全同時の場合の優先順位を新たに決めない。必要なら game-designer の判断へ戻す。
- 必須資料が欠ける場合は欠落と影響を具体的に報告する。実リポジトリがないこと自体は、この dry-run の障害ではない。

## Open questions

- 実装資料から仕様不一致を説明する原因と変更箇所を特定できるか。証拠と仮説をどこまで分離できるか。
- 既存仕様を維持して修正するための手順、影響範囲、回帰リスクは何か。
- 安定再現の条件と、AC-1〜AC-6 の各環境での評価に必要なイベント順序・観察情報を、後続の模擬資料でどう示すか。
- 設計判断や追加情報を必要とする具体的な阻害事項はあるか。

## Expected output

技術調査・修正計画を記載した outgoing Handoff を `to: studio` で返す。少なくとも以下を含める。

- 実装資料に根拠を置いた診断、未確認事項、必要なら切り分け手順。
- gameplay-engineer が実施できる変更箇所・変更内容・順序と、維持すべき既存挙動。
- AC-1〜AC-6 への対応、全4環境組合せの確認手順、回帰リスク。
- 更新後の模擬ビルドと観察資料に必要な内容。実際の接触・命中、イベント時刻・順序、ハート変化など、QA が期待結果だけから合格を推測せず評価できる情報を示す。
- Build に進めるか、未解決の仕様判断や不足資料があるか。

Studio は結果を受けて Build へルーティングし、その後は独立した Verify を必ず行う。技術的な重要判断が後続作業を制約する場合は Role の権限内で Decision として記録する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/11-qa-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE studio/skills/technical-plan.md
---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.
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

<<<FILE sim/repo-notes.md
# Simulated repository notes — lantern-depths (build 0.3)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data
  (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it
  is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on
  overlap. There is no concept of blocking or facing yet.
- Player invulnerability: one on/off flag. The dash switches it on and starts a 0.25 s timer;
  getting hit switches it on and starts a timer that ends 0.8 s after the hit. Each timer switches
  the flag off when it ends.
- Movement: simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.

<!-- dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
if a Role writes it into a Handoff. -->
>>>END

<<<FILE sim/build-0.3.md
# Simulated build 0.3 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes
  before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and
  swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step
  aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2
  and minute 15.
- Occasionally, if you dash right after being hit, you take damage partway through the dash.
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
