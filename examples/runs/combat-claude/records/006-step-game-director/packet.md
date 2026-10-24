# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
next_seq: 5

## You may write

- goals/G-001-combat-monotony/05-game-director-to-<recipient>.md
- decisions/D-002-<name>.md

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

<<<FILE goals/G-001-combat-monotony/04-game-designer-to-game-director.md
---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 04: game-designer → game-director — ビルド 0.3 の戦闘が単調な原因の診断と、D-001 の枠内の選択肢

## Task

下の診断と3つの選択肢を見て、G-001 の方向・優先度・スコープを決める。どの案(または組み合わせ)を進めるか、新しい敵や見た目の作業をどこまで許すかを決めること。仕様や数値の最終決定は、方向が決まってからの `write-design-spec` で行う。

## Context

Goal G-001 の Owner の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。
Observe で、プレイテスターがビルド 0.3 を全5部屋通してプレイした(`02-playtester-to-studio.md`)。体験の問題 A〜C が `game-designer` に回り、これが最初の Diagnose。
観察はドライランで、`sim/build-0.3.md` の記述から推定した体験。ゲームパッドの操作感、音、演出、各部屋の実時間は未確認。このため、それらに依存する原因は仮説として分けて書く。

## Findings

### 1. 診断: 症状と原因

根拠は `design/combat.md` の記述(以下「設計書」)と、プレイテスターの観察(以下「観察」)。

**共通の原因(A・B・C のすべてに効いている)**

- **P1. 敵の挙動が各1種類で、プレイヤーに別の答えを求めない。**
  - Grub は「まっすぐ歩いて接触で噛む。予告なし」(設計書)。Spitter は「その場に固定で、2秒ごとに遅い弾を撃つ」(設計書)。
  - どちらも「向き直って振る」「横に1歩ずれる」で足りる。観察の部屋4〜5の型と一致する。
  - 敵が2種類でそれぞれ挙動が単純なので、混成にしても足し算にしかならず、組み合わせの判断が生まれない。
- **P2. 部屋の構成に進行がない。**
  - 設計書は「5部屋、各3〜6体、Grub と Spitter の混成」としか定義していない。敵の強さ、出現の仕方、配置が部屋ごとに変わる記述がない。
  - これが「2分目も15分目も同じ」(A)と「部屋が進んでも脅威が変わらない」(疑問)の直接の原因と考えられる。

**A. 毎部屋同じ型で変化しない**

- 主因は P1 と P2。
- 補助的な要因として、プレイヤー側の選択肢が攻撃とダッシュだけ(D-001)なので、敵が型を変えない限り、型は変わらない。

**B. 緊張感がほとんどない**

- **B1. Grub の脅威が低い。**
  - HP2、攻撃1ダメージ、回復0.35秒。Grub は一直線に来るので、その場で振れば接触前に倒せる(観察:「近づかれる前に片付く」)。
  - 被弾は3体が同時に来たときだけ、という観察と整合する。
- **B2. Spitter の脅威が低い。**
  - 弾が遅く、固定のリズム(2秒ごと)で、狙いが単純。横に1歩ずれれば避けられる(観察)。
  - 読める脅威(柱3)としては成立しているが、避けるのに技量が要らない。
- **B3. 被弾の罰が軽い(推定)。**
  - 被弾後は0.3秒の硬直のあと、被弾から0.8秒は無敵(設計書)。
  - 最大ハート数、弾のダメージ量などは設計書に未記載で、被弾の重さは断定できない。観察でも被弾は少なかった。

**C. ダッシュが戦闘で使われない**

- **C1. ダッシュを必要とする脅威がない。**
  - ダッシュは4タイル・0.25秒の全区間無敵で、クールダウン0.6秒(設計書)。性能は十分に強い。
  - 歩くだけで足りる敵(P1、B1、B2)しかいないため、使う理由がない。性能の問題ではなく、需要の問題と見る。
- **C2. ダッシュに「攻めの使い道」がない。**
  - 設計書では、ダッシュは移動と無敵のみ。攻撃はダッシュ中に予約されて終了後に出る。位置取りで敵を崩す動機がない(推定)。

**確認が必要な仮説(観察が届いていない部分)**

- H1. ゲームパッドでの実際の入力感。攻撃の回復0.35秒とダッシュのクールダウンが、実機で「軽すぎる」か「普通」か。
- H2. 各部屋の実時間。5部屋で15〜20分に届くか、テンポが単調さを悪化させているか。
- H3. 音と演出が単調さを強めている、または緩和している可能性。
- H4. 敵の移動速度、弾速、配置の具体値。設計書にない。観察は「遅い」「簡単」と述べているが、数値の根拠はない。

### 2. 設計書の未定義事項(記録)

被弾後のダッシュ(欠陥 D)に関わる事実として、設計書は次のことを定義していない。

- 被弾の硬直(0.3秒)中にダッシュ入力を受け付けるか。
- 被弾後の無敵(0.8秒)とダッシュの無敵(0.25秒)が重なったときの扱い。
- 無敵の終了時刻と、ダッシュの途中で被弾が成立する条件。
- ダッシュのクールダウン中に被弾した場合の挙動。

設計書の文面どおりなら、ダッシュ中は常に無敵で、被弾から0.8秒も無敵なので、「ダッシュ途中のダメージ」は期待される挙動にならない。だから、この観察は不具合の疑いで、設計の抜けではなく実装の問題かもしれない。ただし、上の抜けが原因である可能性も残る。再現と原因の特定は `qa` の仕事で、ここでは扱わない。`qa` の結果次第で、期待される挙動を設計書に書き足す必要がある。

その他、設計書に未記載で、次の仕様化で必要になる項目: 最大ハート数、敵の速度、弾速と弾のダメージ、敵の出現位置、弾が壁や他の敵に当たる扱い。

### 3. 選択肢(すべて D-001 の枠内。新しい入力ボタンは不要)

**案1: 敵の挙動を増やす(予告つきの突進と、Spitter の撃ち方の変化)**

- 変更内容:
  - Grub に、予告つきの突進を持つ型を追加する。例えば、立ち止まって短く溜めたあと、直線上に素早く突っ込む。
  - Spitter に撃ち方の変化を追加する。例えば、3連射や、プレイヤーの進行方向を狙う弾。
  - 既存の敵の枠組みに挙動を足す形が基本で、新しい敵の種類は作らない。
- 効く症状: A(型を壊す)、B(駆け引きが生まれる)、C(突進をダッシュの無敵で抜ける、という使い道ができる)。
- コスト: 中。既存の敵の仕組みを再利用できるが、新しい挙動の実装と調整が要る。予告の見た目(溜めの動き、色、効果音)が必要になる。
- リスク: 予告が読めないと、柱3(害を与える前に見える)に反する。予告の長さと見た目の調整が必要。
- 戻しやすさ: 高。敵の型ごとに部屋への配置を外せば元に戻る。
- ビジョンとの適合: 高。深みを敵の挙動から生む、というD-001の趣旨そのもの。

**案2: 部屋の構成と進行を作る(既存の敵のまま、出し方と強さを変える)**

- 変更内容:
  - 時間差で敵を出す波、出現位置の指定(Spitter が通り道を撃ち抜く位置、Grub が背後から来る位置など)、部屋ごとの数と数値の上昇(Grub の速度、Spitter の発射間隔)を定義する。
  - 最初は敵の種類は2つのまま。
- 効く症状: A(部屋ごとに状況が変わる)、B(圧が上がる)、C(同時に複数の脅威が来るので、ダッシュで抜ける場面ができる)。
- コスト: 低。既存の敵とシステムだけで、主にデータと配置の変更。
- リスク: 数値を上げるだけだと、型は同じまま「速くなっただけ」になり得る。A の根本(P1)は解けない可能性がある。
- 戻しやすさ: 非常に高い。
- ビジョンとの適合: 高。ただし、効果は構成の作り込み次第。

**案3: プレイヤー側の数値を締める(「立って振る」が通らないようにする)**

- 変更内容:
  - 攻撃の回復を長くする、被弾後の無敵を短くする、Grub の体力を増やす、ダッシュのクールダウンを変える、などの調整。
  - さらに踏み込む場合は「ダッシュに攻めの使い道を与える」(例えば、ダッシュで敵を通り抜けると一瞬スタンさせる)という、キットの変更もあり得る。これは入力を増やさないので D-001 の範囲内だが、ダッシュの役割を変える点で、ワンボタン戦闘(柱1)の解釈に触れる。選ぶ場合は方向の判断が必要。
- 効く症状: B(罰が重くなる)、C(ダッシュが必要になる)。A への効果は小さい。
- コスト: 低(数値のみの調整)。キット変更を含めると中。
- リスク: 実機の感触(H1)が未確認のまま数値を触ることになる。敵が変わらないので、不快な縛りに感じられるおそれがある。30 FPS と 60 FPS の両方で、フレーム数ではなく秒で定義する必要がある。
- 戻しやすさ: 数値は高い。キット変更は中。
- ビジョンとの適合: 数値調整は適合。キット変更は柱1の解釈の確認が要る。

### 4. 推奨(根拠: 設計書と観察。実機の確認は未済)

**案2を先に行い、案1のうち「予告つきの Grub の突進」だけを同時に試す、という段階的な進め方を推奨する。**

- 理由:
  - 主因 P1(敵が単調)を解くのは案1だけ。しかし、新しい挙動は予告の見た目も含めて費用がかかる。
  - 案2は低コストで戻しやすく、P2(進行がない)を解く。
  - 案1の最小の一つ(Grub の突進)を足すと、C(ダッシュの使い道)に直接効く。Spitter の変化や新しい敵の種類は、結果を見てから決められる。
- 案3は、実機の感触を確認してから判断する。今は主案にしない。
- 反対の見方: 案1を全面的に進めれば、A の根本には強く効く。ただし、見た目の作業(予告の演出)と実装の量が増える。これはスコープの判断になる。

### 5. 検証すべき観点(後で Play や Review で、プレイヤーが観察できる形)

- 立ち止まって振り続けるだけでは、後半の部屋で被弾するか。
- 部屋ごとに、敵の出方や対応の仕方が違うと感じるか(「2分目と15分目が同じ」でなくなるか)。
- 突進の予告が、害を与える前に見えて読めるか(柱3)。
- ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
- 被弾が「自分の判断ミスのせい」と感じられるか(理不尽でないか)。
- 30 FPS と 60 FPS で、予告の長さや回避のしやすさが同じに感じられるか。

## Decisions already made

- D-001: 戦闘は攻撃ボタン1つとダッシュのみ。新しい入力ボタンは Owner の承認なしには追加できない。上の3案はいずれもこの範囲内で、D-001 の変更は不要。

## Constraints

- D-001 の枠内。ビジョンの柱(ワンボタン戦闘、短いラン、読める脅威)を保つ。
- 既存のシステムの再利用を優先する(小さなチーム)。
- 30 FPS と 60 FPS の両方で正しく動くこと。時間は秒で定義する。
- 範囲外: 戦闘以外のシステム、ラン長、ビジョンの柱の変更。
- 数値と仕様の最終決定は、方向が決まった後の仕様化で行う。

## Open questions

`game-director` に決めてほしいこと:

1. **方向の選択**: 案1(敵の挙動)、案2(部屋の構成)、案3(数値)のどれを主にするか。または推奨の段階的な組み合わせでよいか。これは優先度とスコープの本当の選択で、選び方によって作業量と見た目の作業が変わる。
2. **見た目の作業**: 案1は、予告の見た目(溜めの動き、効果音)が必要になる。`art-director` を巻き込むか。巻き込む場合、いつ。
3. **実現可能性**: 案1の敵の挙動追加と、案2の波の出現が、既存の敵と部屋のシステムでどこまで簡単にできるか分からない。`technical-director` に確認するか。
4. **実機の確認**: H1〜H4(操作感、実時間、演出、数値)を、次の Play で実機確認するのか。確認してから数値を決めるのか。
5. **欠陥 D**: `qa` の再現結果が出たら、ダッシュと被弾後の無敵の規則を設計書に書き足す。この件を G-001 に含めるか、別扱いにするか。(Studio 注: 現在の route では 2b として G-001 に含め、`qa` の再現を別途行う。扱いを変える場合は Decide で指示すること。)

## Expected output

`game-director` が、案(または組み合わせ)、優先度、スコープを決める。その結果を決定として記録し(`make-decision`)、`game-designer` に仕様化(`write-design-spec`)を渡す。必要なら `art-director` と `technical-director` に確認を回す。D-001 の変更は必要ないので、Owner のエスカレーションは不要と見ている。ただし案3のキット変更(ダッシュに攻めの使い道を与える)を選ぶ場合や、柱1の解釈が変わると判断する場合は、`prepare-owner-escalation` で Owner への Escalation を書くこと。

## Sender assessment

- 確信度: P1 と P2 が主因という診断は、設計書の記述と観察が一致しているので、中〜高。B3(被弾の罰の軽さ)と C2(ダッシュの攻めの使い道がない)は、設計書の未定義部分が多く、推定にとどまる。
- 観察はドライランで、感触に関わる原因(H1〜H4)は未確認。数値を決める前に、実機の確認が望ましい。
- 欠陥 D は、設計書の文面と矛盾する観察なので、実装の問題の可能性が高いと見るが、断定せず `qa` に任せる。
- 決定ファイル(`decisions/D-002-...`)は書いていない。方向を決めるのは `game-director` で、この段階で設計上の重要な決定は行っていないため。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#constraints, project.md#current-state, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/03-studio-to-game-designer.md
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

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
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
>>>END

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.
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

<<<FILE goals/G-001-combat-monotony/03-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 3
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 03: studio → game-designer — ビルド 0.3 の戦闘が単調に感じられる原因の診断

## Task

プレイテスターが報告した体験の問題(A〜C)の原因を、デザインの言葉で診断し、D-001 の枠内で取れる解決策の選択肢を示す。解決策は決めず、選択肢と各案の影響を出す。

## Context

Goal G-001 の Owner の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。
Observe の段階で、プレイテスターがビルド 0.3 を全5部屋通してプレイし、観察報告(`goals/G-001-combat-monotony/02-playtester-to-studio.md`)を出した。原因の特定はまだで、これが最初の Diagnose になる。

## Findings

プレイテスターの観察(プレイヤー視点の体験のみ。実装や設計意図は読まずに書かれている)。

観察の制約: ドライランのため `sim/build-0.3.md` の記述から推定した体験であり、ゲームパッドの操作感、音、演出、各部屋の実時間は確認されていない。

体験の問題:

- **A. 戦闘が毎部屋同じ型で、進んでも変化しない(影響度 大)**
  - 全5部屋、最初から最後まで「位置を決めて、空になるまで振る」が通用した。プレイテスターは「2分目も15分目も同じ」と感じた。
  - 部屋4〜5の混成でも、角に下がり、Grub に向き直って振り、弾は横にずれる、という同じ型が通った。新しい判断は求められなかった。
- **B. 緊張感がほとんどない(影響度 大)**
  - 部屋1〜2: Grub はその場で攻撃ボタンを押すだけで2振りで倒れる。ダメージを受けるのは3体が同時に来たときだけ。「立って振っていれば終わる」と感じた。
  - 部屋3: Spitter の弾は遅く、横に1歩動けば避けられる。近づいて2回振れば倒せる。避けること自体は成立しているが、危うさや駆け引きはなかった。
- **C. ダッシュが戦闘で使われず、回避や位置取りの腕前が活きない(影響度 中〜大)**
  - ダッシュは部屋を早く横切るときにしか使わなかった。「ダッシュを戦闘で使う理由がない」。
  - プレイヤーとしての疑問: 「ダッシュは何のためにあるのか」「部屋が進んでも敵の脅威が変わらないのはなぜか」。

良かった点: 攻撃の結果は分かりやすく(2振りで倒れる)、操作の理解に迷いはなかった。Spitter の弾が遅く、避けられることは読み取れた。

別ルートで扱う件: 被弾直後にダッシュすると、ダッシュの途中でダメージを受けることが時々ある(問題 D、不具合の疑い)。`qa` が別に再現するので、この診断では原因や修正を扱わない。

## Decisions already made

- D-001: 戦闘は攻撃ボタン1つとダッシュのみ。新しい入力ボタンは Owner の承認なしには追加できない。深みは位置取り・タイミング・敵の挙動から生む。

## Constraints

- D-001 の枠内(攻撃とダッシュだけ、新ボタンなし)。枠を超える案が必要な場合は、その案を選択肢に含めるのではなく「D-001 の変更が必要」と明記して `game-director` に渡す(Owner のエスカレーション対象になる可能性がある)。
- ビジョンの柱: ワンボタン戦闘、短いラン(15–20分)、読める脅威(脅威は害を与える前に見える)。
- 小さなチームのため、既存のシステムを再利用する案を優先する。
- 30 FPS と 60 FPS の両方で正しく動く必要がある。
- 範囲外: 戦闘以外のシステム、ラン長、ビジョンの柱の変更。
- 観察の制約(上記)により、操作感や実時間に依存する原因は、確認が必要な仮説として区別して書く。

## Open questions

- A〜C の原因は何か。敵の種類・挙動、部屋の構成と進行、ダメージや無敵の数値、プレイヤーキットの幅などのうち、何が支配的か。複数の原因が重なっている場合は、それぞれの寄与を分けて示す。
- 診断の選択肢が、方向・優先度・スコープの本当の選択になるか。なる場合は、どの選択か。
- 選択肢のどれかが D-001 の変更や新ボタンを必要とするか。
- 設計文書(`design/combat.md`)が、被弾後のダッシュ中の無敵などの規則を未定義のままにしていると気づいた場合は、その事実を記録する。それは欠陥 D の期待される挙動に関わるが、D の再現は `qa` が行う。

## Expected output

- 診断と選択肢を、このステップの出力 Handoff の Findings に書く(`diagnose-experience`)。
  - 原因の診断: A〜C ごとに、設計文書に基づく原因と、根拠(設計文書のどこか、観察のどの部分か)を示す。確認できていない仮説は分けて書く。
  - 選択肢: D-001 の枠内の案を、プレイヤーの体験への効果、コスト(既存システムの再利用度)、リスク、元に戻しやすさとともに示す。推奨があれば理由とともに書く。
  - 検証すべき観点(後で Play や Review で確認できる、プレイヤーが観察できる形のもの)。
- 宛先は `game-director`(Decide)。選択肢が方向・優先度・スコープの選択であるか、D-001 の変更に触れる場合はその旨を明記する。診断の結果、`game-director` の判断が不要と判断した場合は、`studio` 宛てにして理由を書く。
- ゲームの仕様や数値の最終決定はまだ行わない(選択肢の段階)。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-studio.md
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
