# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/05-game-director-to-game-designer.md
next_seq: 6

## You may write

- goals/G-001-combat-monotony/06-game-designer-to-<recipient>.md
- design/<name>
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

<<<FILE goals/G-001-combat-monotony/05-game-director-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 5
from: game-director
to: game-designer
stage: Design
outcome: done
---
# 05: game-director → game-designer — D-002 の方向に沿った、部屋の構成と進行・予告つき Grub 突進の仕様化

## Task

D-002 で決めた方向に沿って、`write-design-spec` で戦闘の仕様を書く。内容は (1) 5部屋の構成と進行(波、出現位置、部屋ごとの段階的な上昇)と、(2) 予告つき Grub 突進の挙動と予告。数値は暫定値として明記し、実機の確認で調整できる形にする。

## Context

Goal G-001 の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。
プレイテスターの観察(問題 A〜C)から、あなたが診断(`04-game-designer-to-game-director.md`)と3つの選択肢を出した。それを受けて `game-director` が方向を決め、`decisions/D-002-combat-direction-rooms-and-grub-charge.md` に記録した。

## Findings

**決めた方向(詳細は D-002):**
- 主軸は案2。既存の敵2種のまま、部屋ごとに出し方と強さが変わる構成と進行を作る。
- 併用は案1のうち、予告つき Grub 突進の1つだけ。新しい敵の種類は作らない。
- 突進は部屋ごとに配置を外せる形にする。案2の構成だけの効果と、突進を足した効果を切り分けて見られるようにするため。

**回答(あなたの Open questions への回答):**
1. 方向: 上のとおり。案2を先に、案1は Grub 突進の1つのみ。
2. 見た目の作業: 突進の予告の見た目(溜めの動き、色、効果音)が必要。仕様では、予告に求める条件(害を与える前に見える、長さ、30/60 FPS で同じ長さ)を定義する。見た目の具体案は `art-director` が決めるので、仕様に見た目の制作指示は書かない。仕様が書けたら、Studio が `art-director` に回す。
3. 実現可能性: 突進の挙動追加と波の出現が、既存の敵と部屋のシステムでどこまで簡単かは未確認。仕様の中で「実現性の確認が要る点」を分けて書き、Studio が実装前に `technical-director` に回す。技術的な方法はあなたが決めない。
4. 実機の確認: H1〜H4 は、次の Play で実機確認する。この仕様の数値は暫定値として、確認後の調整を前提に書く。確認前にプレイヤー側の数値は変えない。
5. 欠陥 D: 2b として G-001 に含める(Studio 注の route のまま)。ただし、今回の仕様には含めない。`qa` の再現結果が出てから、ダッシュと被弾後の無敵の規則を設計書に書き足す。

## Decisions already made

- D-001: 戦闘は攻撃ボタン1つとダッシュのみ。新しい入力ボタンは Owner の承認なしには追加できない。
- D-002: 主軸は部屋の構成と進行(案2)。併用は予告つき Grub 突進の1つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は今回は扱わない。

## Constraints

- D-001 と D-002 の範囲内。ビジョンの柱(ワンボタン戦闘、短いラン、読める脅威)を保つ。
- 突進は、害を与える前に必ず見える予告を持つ(柱3)。予告なしの突進は不可。
- 時間はすべて秒で定義する。30 FPS と 60 FPS の両方で、予告の長さや回避のしやすさが同じになること。
- 既存の敵と部屋のシステムの再利用を優先する。
- 範囲外: 部屋数(5)とラン長(15–20分)の変更、戦闘以外のシステム、Spitter の変更、新しい敵の種類、プレイヤー側の数値やキットの変更、欠陥 D の規則。
- 設計書に未記載の項目(最大ハート数、敵の速度、弾速と弾のダメージ、敵の出現位置、弾が壁や他の敵に当たる扱い)は、今回の仕様に必要な範囲で定義する。必要でないものは「未定義のまま」と明記する。
- 仕様の数値は暫定値であることを明記し、H1〜H4 の確認後に調整する前提を書く。

## Open questions

仕様の中で次を答えること(決めるのはあなたの権限内。方向や優先度に関わる選択が出た場合は `game-director` に戻す)。

1. 各部屋で、何を学ばせ、何を組み合わせさせるか(5部屋の進行の筋)。
2. どの部屋に、どの波・配置・数値で、Grub 突進を入れるか。突進を外した版でも部屋が成立するか。
3. 突進の予告の長さ、突進の速さと距離、突進後の隙を、秒とタイルで暫定値として定義する。ダッシュの無敵(0.25秒)で抜けられる設計かどうかを確認する。
4. 突進の予告が、他の敵や弾と同時に起きたときも読めるか(柱3)。
5. 実現性の確認が要る点と、`art-director` に渡す条件は何か。
6. 検証の観点を、プレイヤーが観察できる形で書くこと(次の「Expected output」参照)。

## Expected output

- `design/combat.md` の更新を含む仕様(`write-design-spec`)。部屋の構成と進行、Grub 突進、暫定値の明示、未定義のまま残す項目の記録を含む。
- 仕様の後に、検証の観点(Play や Review で、プレイヤーが観察できる形)を書く。診断の観点を引き継ぐこと:
  - 立って振り続けるだけでは、後半の部屋で被弾するか。
  - 部屋ごとに、敵の出方や対応の仕方が違うと感じるか。
  - 突進の予告が、害を与える前に見えて読めるか。
  - ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
  - 被弾が「自分の判断ミスのせい」と感じられるか。
  - 30 FPS と 60 FPS で同じに感じられるか。
- 次の宛先は Studio による routing(Handoff は `to: studio`)。実現性の確認(`technical-director`)と予告の見た目(`art-director`)を回したあと、実装、qa、Play に進む。

## Sender assessment

- 確信度: 方向は中〜高。診断の主因(P1、P2)が設計書と観察で一致しているため。突進が A と C にどこまで効くかは、実機で見るまで中程度。
- 実機の確認(H1〜H4)が未済のため、数値は暫定。プレイヤー側の数値を触らないのは、原因の切り分けを保つため。
- D-001 の変更も、柱1の解釈の変更も伴わないので、Owner のエスカレーションは書いていない。キット変更(案3の踏み込み)は選んでいない。
- 欠陥 D は G-001 に残るが、この仕様とは別の流れ。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#current-state, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
- Also: goals/G-001-combat-monotony/02-playtester-to-studio.md(元のプレイテスト観察。問題 A〜C の根拠として参照する)
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
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

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
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

<<<FILE decisions/D-002-combat-direction-rooms-and-grub-charge.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: 戦闘の単調さへの対応は「部屋の構成と進行」を主軸にし、敵の挙動追加は予告つき Grub 突進の1つに限る

## Decision

G-001 の方向を次のとおり決める。

**主軸: 案2(部屋の構成と進行を作る)**
- 既存の2種類の敵(Grub、Spitter)のまま、部屋ごとに出し方と強さが変わる構成を定義する。
- 時間差で出る波、出現位置の指定、部屋ごとの敵数と数値の段階的な上昇を含む。
- 5部屋の構成で、序盤は基本を覚え、後半は組み合わせの判断が必要になる進行にする。

**併用: 案1のうち「予告つき Grub 突進」の1つだけ**
- Grub に、立ち止まって短く溜めてから直線上に素早く突っ込む型を追加する。既存の Grub の枠組みに挙動を足す形で、新しい敵の種類は作らない。
- 予告は、害を与える前に見えること(柱3)を必須条件にする。予告の長さは秒で定義し、30 FPS と 60 FPS で同じ長さに感じられること。
- 突進を、ダッシュの無敵で抜ける使い道を生む手段として位置づける。

**優先度:** 部屋の構成と進行(案2)が先。Grub の突進は同じ仕様の中で定義するが、実装と検証は案2の構成と合わせて行い、効果を切り分けて見られるようにする。突進を部屋に配置するかどうかは、部屋ごとに外せる形にする。

**この決定が扱わないこと(スコープ外):**
- Spitter の撃ち方の変化、新しい敵の種類は、今回は作らない。案2と突進の結果を見てから、別の判断として扱う。
- 案3のプレイヤー側の数値調整(攻撃回復、被弾後の無敵、ダッシュのクールダウンなど)は、今回は行わない。実機の感触(H1)の確認後に再検討する。
- 案3のキット変更(ダッシュに攻めの使い道を与える、など)は選ばない。ダッシュの役割を変え、柱1の解釈に触れるため、必要になった場合は別途 Owner への Escalation を検討する。今回は不要。
- D-001 の変更、新しい入力ボタン、ラン長(15–20分)、部屋数(5)の変更は行わない。Owner のエスカレーションは不要(トリガーに該当しない)。
- 欠陥 D(被弾直後のダッシュ中のダメージ)は、2b として G-001 に含めるが、この決定の対象外。`qa` の再現結果が出てから、期待される挙動を設計書に書き足す。

## Rationale

- 診断の主因は P1(敵の挙動が単調)と P2(部屋に進行がない)で、設計書と観察が一致している。
- P2 は案2が低コストで戻しやすく、既存システムの再利用という制約に合う。
- P1 を根本から解くのは案1だが、全面的に進めると実装と見た目の作業が大きい。小さなチームの制約を考えると、効果が最も直接的な Grub 突進の1つに絞るのが妥当。突進は C(ダッシュの使い道がない)にも直接効く。
- 案2だけでは数値が上がるだけで「速くなっただけ」になるおそれがある。突進を併用することで、型そのものを変える要素を確保する。
- 案3は、実機の感触が未確認のまま数値を触ることになり、敵が変わらないと不快な縛りに感じられるおそれがある。主案にしない。
- 診断の B3 と C2 は推定にとどまる。確認が取れるまで、プレイヤー側の変更は避ける。

## Alternatives considered

- **案1を全面的に進める(Spitter の変化も含む):** A の根本には最も強く効くが、予告の演出と実装の量が増える。まず小さく試して効果を見る方が、リスクが低い。
- **案2のみ:** 最も安いが、P1 が残り、A の根本が解けない可能性がある。
- **案3を主にする:** 実機の確認がなく、A への効果が小さい。キット変更は柱1の解釈に触れる。
- **Owner にエスカレーションする:** D-001 の枠内で、ビジョンの柱も変えないため、game-director の権限内。

## Revisit when

- 次の Play で、立って振るだけでは後半の部屋で通用しなくなったが、まだ型が単調と感じられる場合(Spitter の変化や敵の追加を検討)。
- 実機の確認で、H1〜H4(操作感、実時間、演出、数値)が単調さの主因だと分かった場合(案3の数値調整を再検討)。
- 突進の予告が柱3を満たせない、または Grub 突進の追加費用が見込みを大きく超えた場合。
- 深みが敵と位置取りだけでは足りないと分かった場合(D-001 の「Revisit when」に該当。その場合は Owner に Escalation する)。
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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: studio
stage: Route
outcome: done
---
# 02: playtester → studio — ビルド 0.3 の戦闘体験の観察報告

## Task

ビルド 0.3 を全5部屋通してプレイした観察報告を渡す。次の宛先(体験の問題は `game-designer`、不具合は `qa`)の判断は Studio が行う。

## Context

Goal G-001 の Observe ステップ。ビルド 0.3 を、戦闘に注目して、アクション志向・短く濃い走りを好み、ゲームパッドで遊ぶプレイヤーとして遊んだ。内部実装や設計意図は読んでおらず、推測もしていない。

## Findings

### 観察方法

- ドライランのため、実機の操作は行っていない。`sim/build-0.3.md`(プレイヤーに見える挙動の記述)を読むことを「ビルドを実行する」ことの代わりとした。
- 以下は、その記述から読み取れるプレイヤー視点の体験だけを書いている。
- 観察できなかったこと:
  - ゲームパッドでの操作感(入力の反応、スティックの感触)。
  - 音、演出、画面の見た目。
  - 各部屋にかかる実時間。
  - 記述にない敵の種類や挙動。
- 感じたことの記述は、この記述から推定した体験であり、実際に操作した感覚の記録ではない。

### セッション概要

全5部屋を通して遊んだ。

- 部屋1〜2: Grub が近づいてくる。
- 部屋3: Spitter が登場する。
- 部屋4〜5: 混成の部屋。

どの部屋でも、同じやり方で突破できた。

### 具体的な場面

1. **部屋1〜2(Grub)**
   - その場に立って攻撃ボタンを押すだけで、Grub は2振りで倒れる。近づかれる前に片付く。
   - ダメージを受けるのは3体が同時に来たときだけ。
   - 感じたこと: 「立って振っていれば終わる」。位置取りも回避も必要なく、緊張はほぼなかった。

2. **部屋3(Spitter)**
   - 弾は遅く、横に1歩動けば避けられる。
   - 近づいて2回振れば倒せる。
   - 感じたこと: 避けること自体は成立しているが、1歩動くだけの簡単な作業で、危うさや駆け引きはなかった。

3. **部屋4〜5(混成)**
   - 角に下がり、Grub に向き直って振る。弾は横にずれて避ける。この型がそのまま通用した。
   - 感じたこと: 敵の組み合わせが変わっても、やることは部屋1〜3と変わらない。新しい判断を求められなかった。

4. **ダッシュ**
   - ほとんど必要にならなかった。使うのは部屋を早く横切るときくらい。
   - 感じたこと: 「ダッシュを戦闘で使う理由がない」。ダッシュや位置取りに慣れたプレイヤーには、持ち味を使う場面がなかった。

5. **全体の流れ**
   - どの部屋も「位置を決めて、空になるまで振る」で終わる。
   - 感じたこと: 「2分目も15分目も同じ」。進んでも変化や盛り上がりを感じなかった。

6. **ダッシュ中のダメージ(不具合の疑い)**
   - 被弾した直後にダッシュすると、ダッシュの途中でダメージを受けることがあった。毎回ではなく、時々。
   - 感じたこと: ダッシュで逃げたのに当たるのは納得しづらい。ただし戦闘でダッシュを使う機会が少ないので、遭遇頻度は低い。

### 問題点と影響度

| # | 問題 | 影響度 | 根拠 |
|---|------|--------|------|
| A | 戦闘が毎部屋同じ型(立つ→振る→避ける)で、プレイが進んでも変化しない | **大** | 全5部屋、最初から最後まで同じやり方が通用し、「2分目も15分目も同じ」と感じた |
| B | 緊張感がほとんどない。被弾は3体同時のときだけ、弾も1歩で避けられる | **大** | 短く濃い走りを求めるプレイヤーには、危機感や手応えが足りない |
| C | ダッシュが戦闘で使われず、回避や位置取りの腕前が活きない | **中〜大** | ダッシュは部屋の移動にしか使わなかった |
| D | 被弾直後のダッシュ中にダメージを受けることがある | **小〜中** | 時々起きる。理不尽に感じる。頻度は低い |

### 良かった点

- 観察できた範囲では、攻撃の結果は分かりやすかった(2振りで倒れる)。操作の理解に迷いはなかった。
- Spitter の弾が遅く、避けられることは読み取れた。避ける動作自体は成立している。

### プレイヤーとしての疑問

- 「ダッシュは何のためにあるのか」。戦闘で使う場面がなかった。
- 「部屋が進んでも敵の脅威が変わらないのはなぜか」。

## Decisions already made

None

## Constraints

- 観察は `sim/build-0.3.md` の記述に基づく。ゲームパッド操作感や実時間は未確認。
- 原因の推測や、コードレベルの修正案は書いていない。

## Open questions

- 宛先の判断は Studio に委ねる。
  - A〜C は体験の問題なので `game-designer` が妥当。
  - D は不具合の疑いなので `qa` が妥当。

## Expected output

Studio が Route で宛先を確認する。体験の問題(A〜C)は `game-designer`、不具合の疑い(D)は `qa` に回す想定。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.3.md
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
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
