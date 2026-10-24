# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/20-studio-to-qa.md
next_seq: 21

## You may write

- goals/G-001-dash-damage/21-qa-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/20-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 20
from: studio
to: qa
stage: Verify
outcome: routed
---
# 20: studio → qa — 模擬ビルドの文書評価と検証証拠の十分性を判断する

## Task

既存仕様・受け入れ条件と模擬ビルドを独立に照合し、文書から評価できる範囲と条件別検証に不足する証拠を判断する。評価結果と次に必要な入力を Studio に返す。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」である。戦闘の方向性変更、新しい入力、無関係なバランス調整は対象外。

本作は dry-run であり、「ビルドを実行する」とは `sim/build-*.md` を読むことである。対象は `sim/build-0.4.md`。Studio が採用した対象変更識別子は `0.3-G001-15` である。対応は検証対象の識別情報であり、合格の根拠ではない。

Build は変更記述による模擬実装として完了している。独立 Verify は未完了である。

## Findings

### 利用可能な資料

- `design/combat.md`：既存の戦闘仕様。
- `11-qa-to-studio.md` の指定節：AC-1〜AC-6 と再現・比較手順。
- `sim/build-0.4.md`：今回評価する模擬ビルド。
- `sim/build-0.3.md`：従来ビルドの記述。比較用であり、条件別試行記録とは扱わない。
- `project.md#constraints`：dry-run、対象入力方式、30／60 FPS の制約。

Studio は本 Route でこれらの原文を独自に照合していない。内容と採用可能性は QA が確認する。

### 取得状況と証拠の限界

本 packet には runtime 管理側の照会窓口、モデル取得手段、条件別生成観察がない。照会経路の状態は「照会手段未確保」。問い合わせを実施した、モデルが存在しない、または取得が不可能と確定したという意味ではない。

`sim/qa-G001-15.md` は存在一覧になく、未取得である。モデルの版・来歴、配置・衝突条件、初期状態、フレーム内の処理順序、入力方式の表現範囲も未確認。

以下は前段から引き継ぐ不足候補であり、QA 判定ではない。AC の意味・数値・有効試行条件は原文を優先する。

| 対象 | 確認が必要な証拠 |
|---|---|
| AC-1〜AC-4 | Grub／Spitter 別の命中成立、入力と受理、保護とダッシュの時刻関係、ハート前後値 |
| AC-5 | 初回・入力不能中・回復後の接触と被害、入力不能の開始終了、操作の受理 |
| AC-6 | 移動距離・継続、予約攻撃1回、クールダウン内／経過後の入力受理 |
| 回帰 | 両保護の終了順序、両保護終了後の通常被害、防いだ複数命中による保護延長の有無、ダッシュ単独の複数命中と終了後の被害 |
| 全対象 | 30／60 FPS × キーボード／ゲームパッドの4環境別の根拠、試行総数・有効数・無効数・発生数と出典 |

クールダウン起点は未解決として報告されている。既存仕様に記載があるか確認し、不足・矛盾があればその箇所を示す。QA が新規仕様を決める必要はない。

## Decisions already made

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：Owner の補足観察を受けて元の修正 Goal を継続する。追加の Owner 計測を開始条件にしない。
- D-003：発生源別保護の論理和、防いだ命中で保護を開始・延長しないという承認済み方針。実装がこれを満たすという証拠ではない。

この Step では Decision の再解釈を行わない。上記要約と仕様・AC の不整合で評価できない場合は Studio に返す。

## Constraints

- QA の独立性を守り、新しい実行コンテキストで開始する。
- 実装理由、原因説明、実装者の自己評価を根拠にしない。
- 前 Handoff 19 は Load で指定した2節のみ読む。全文を読み込まない。
- AC-1〜AC-6、全4環境、必要な命中源と回帰を維持する。文書評価への限定を要件緩和と扱わない。
- 仕様上の期待値、ビルドの挙動記述、生成観察、実測を区別する。
- 挙動記述や全環境への適用宣言を条件別試行の実施記録と扱わない。
- 未提示の試行数、発生数、時刻、ハート値を作らない。不明をゼロに変換しない。
- 証拠不足と、確認された仕様不一致を区別する。
- 実装変更、新規 simulator の開発、試行条件の創作はこの Step に含めない。
- 証拠採否と合否は QA が判断する。Studio や前段の計画は verdict を指定しない。

## Open questions

1. 文書上でどの AC・回帰をどの範囲まで評価できるか。根拠資料のどの記述を採用できるか。
2. 従来の条件別試行要件に対し、現資料は十分か。不十分なら、環境・命中源・枝ごとに何が欠けるか。
3. クールダウン起点などの期待挙動に不足や矛盾があるか。証拠不足とは分けて報告できるか。
4. Verify を完了するために必須の追加入力は何か。既存資料の補完で解消可能なものと、取得元・取得方法が不明なものはどれか。

## Expected output

Studio 宛ての Handoff に、以下をまとめる。

- AC・回帰・対象環境ごとの、期待挙動、参照資料、評価結果、証拠の限界。
- 文書上の適合・不適合と、未確認の条件別試行の区別。
- 確認した不一致があれば、その再現または照合手順と受け入れ条件。
- 必須追加入力の具体名、影響するセル、必要な理由、既知の取得元。取得元が不明なら不明と記す。
- 仕様判断が必要なら、該当する原文と未定義・矛盾する問い。
- 独立 Verify の完了可否と、その根拠。

証拠不足で verdict を出せない場合は `outcome: question` とし、判断可能な範囲と不足を明記する。確認した不一致による `fail` と区別する。QA は次工程を実施せず、結果を Studio に返す。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/combat.md
- Build: sim/build-0.4.md
- Comparison build: sim/build-0.3.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md#修正の受け入れ条件
- Exercise procedure: goals/G-001-dash-damage/11-qa-to-studio.md#後続で実施する再現・比較手順
- Previous handoff: goals/G-001-dash-damage/19-technical-director-to-studio.md#constraints
- Previous handoff: goals/G-001-dash-damage/19-technical-director-to-studio.md#open-questions
- Decisions: 原文の追加 Load なし。上記要約を超える解釈が必要なら Studio に返す。
- Independence: 指定節だけを読み、前 Handoff 全文や実装者の説明・自己評価を追加取得しない。節が見つからない場合は資料不足として報告する。
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
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

<<<FILE goals/G-001-dash-damage/11-qa-to-studio.md#
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

<<<FILE goals/G-001-dash-damage/11-qa-to-studio.md#
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

<<<FILE goals/G-001-dash-damage/19-technical-director-to-studio.md#constraints
## Constraints

- 仕様・AC・全4環境・必要な命中源と枝を維持する。
- 模擬挙動の記述、生成観察、実測、期待値を区別する。
- 未提示の試行数・発生数をゼロに変換しない。
- 未取得モデル、処理順序、初期状態、既存起点を創作しない。
- 追加実装・条件別試行の実施・QA 判定・Goal 完了は本 Step に含めない。
- 未生成資料を Load に入れない。
>>>END

<<<FILE goals/G-001-dash-damage/19-technical-director-to-studio.md#open-questions
## Open questions

1. runtime 管理側の照会窓口・手段は何か。既存モデル・記録のどの部分を取得できるか。
2. モデルは条件別の状態遷移と命中を生成できるか。入力方式とFPSをどこまで表現するか。
3. クールダウン起点とフレーム順序を既存原資料から回復できるか。
4. 原文を回復した試行要件に対し、独立 QA が採用できる証拠はどこまでか。
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
