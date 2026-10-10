# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-combat-monotony/19-studio-to-technical-director.md
next_seq: 20

## You may write

- goals/G-001-combat-monotony/20-technical-director-to-<recipient>.md
- decisions/D-008-<name>.md

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

<<<FILE goals/G-001-combat-monotony/19-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 19
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 19: studio → technical-director — コードにアクセスできない Build をどう進めるか(D-007 の 7)。Owner への確認が要るかの判断と、要るなら Escalation の作成

## Task

Build がゲームのコードを読み書きできないと報告して返ってきた。D-007 の 7 に従い、この状況での進め方を判断すること。Owner の判断(リポジトリの提供、または範囲・リスクの受け入れ)が要ると判断したら、`prepare-owner-escalation` で Escalation を作ること。

## Context

G-001(戦闘の単調さの改善)は、D-002 の方向(部屋の構成と進行を主軸、併用は予告つき Grub 突進の1つ)で、Design まで完了している。Build の1回目(Handoff 14)は、T0 を実施できず実装に入らなかった。そこで 6a で D-007 を作り、T0 を「前提の台帳」(7 項目)に置き換え、コードを全く読めない場合は再試行せず返す条件(D-007 の 7)を定めた。Build の再開(Handoff 17)は、その条件に該当して `outcome: question` で返ってきた(Handoff 18)。

## Findings

Handoff 18 の客観的な内容:

- Build の実行環境に渡されたのは packet の入力ファイルだけで、ゲームのソースコード、ビルド、テストの実行手段、リポジトリはなかった。コードやテストを変更する経路もなかった。
- `project.md` は `repository: none`(サンプルのドライランで、ビルドは `sim/build-*.md` で模擬)としている。`sim/repo-notes.md` と `sim/build-0.3.md` はコードの代わりの模擬の記述であり、台帳の項目をこれらで「確認した」とは扱えない。
- 台帳 7 項目はすべて未確認:
  1. 部屋データ、スポナー、波
  2. 部屋のコードと敵のコントローラの分離(T2 と T3 は既定どおり直列)
  3. 接触の判定形状、レーン幅の元の値
  4. Spitter の弾の衝突処理
  5. 視覚の仕組み(要素 2〜10)
  6. 接触結果の通知
  7. 敵の挙動が経過時間で進むか(`sim/repo-notes.md` に「可変 delta」とあるが、コードでの確認はない)
- 実装、テスト、状態ログ、30/60 FPS の切り替え、ビルドノートは何も作られていない。QA と `art-director` の Verify に渡せるものはない。
- 仕様、D-001〜D-007、視覚仕様を読み合わせた範囲で、新しい矛盾や欠落は報告されていない(文書上の確認のみ)。
- Handoff 18 が挙げた選択肢:
  - (a) 実際のリポジトリとビルド・テスト手段を Build が使えるようにする。
  - (b) 模擬であることを前提に、Build の範囲を確認し直す(例: 実装ではなく実装計画のレビューまで)。
- (a) が満たされた場合の再開順序は Handoff 17 の台帳のとおり(部屋のタスク冒頭で 1・2、状態追加の冒頭で 7、突進の冒頭で 3・6、弾の処理を読んだ時点で 4、見た目の冒頭で 5)。

## Decisions already made

- D-001〜D-006: 変更しない。
- D-004: 技術方針(共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)。
- D-007: T0 を前提の台帳に置き換えた。7 は、読める・書けるコードが全くない場合は再試行せず返す条件。今回これに該当した。

## Constraints

- 新しい入力ボタンは足さない(D-001)。ビジョンの柱とランの長さは変えない。
- 30 FPS と 60 FPS の両方で正しく動くこと。小さなチームで既存の仕組みを再利用すること。
- Owner 向けの Escalation は `owner_language`(日本語)で書く。
- 判断の材料にする事実は、上の Findings と `project.md`、`sim/repo-notes.md` に限る。確認していない前提を、確認済みとして扱わない。

## Open questions

1. この状況は、Owner の判断を要するか。Escalation の条件のうち、スコープ・費用・リスクの大幅な変化に当たるか(コードのない環境で Build を進めること、または Build の範囲を模擬に合わせて縮めること)。当たらないと判断する場合は、その理由と、Build の再開の仕方を示すこと。
2. Owner の判断が要る場合、選択肢は (a)(b) で足りるか。他に妥当な選択肢(例: 実装の代わりに、実装計画と受け入れ基準の確定までを成果とするなど)があれば加える。各選択肢で Goal の成功条件(実際に遊んで単調でなくなったかを確かめる)がどう変わるか、Play と Review がどこまで可能かを書くこと。
3. 範囲を縮める選択肢では、Verify・Play・Review のどれが成立しなくなるかを明示すること。

## Expected output

次のどちらか。

- Owner の判断が要る場合: Escalation(`studio/templates/escalation.md`、`goals/G-001-combat-monotony/20-technical-director-to-owner.md`、`to: owner`、`status: open`)。選択肢ごとに「選んだ場合の次の経路」と推奨を書く。Studio が Goal を `blocked-on-owner` にしてOwner に返す。
- 不要と判断した場合: `to: studio` の Handoff(`20-technical-director-to-studio.md`)に、理由と Build の再開の条件、または Build の範囲変更の内容を書く。必要なら Decision を記録する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md, studio/skills/prepare-owner-escalation.md, studio/skills/make-decision.md
- Project: project.md#constraints, project.md#current-state, sim/repo-notes.md, studio/templates/escalation.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-007-build-without-code-access-assumption-register.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md
- Previous handoff: goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
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

<<<FILE decisions/D-004-technical-approach-grub-charge-and-waves.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-004: 突進と波の技術方針 — 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ

## Decision

`design/combat.md` を実現する技術方針を次のとおり決める。仕様の内容(数値、規則)は変えない。

- **状態の追加**: 突進は共通の敵コントローラに Spawning、Windup、Charge、Recovery を足して実現する。突進型は `grub_charger`(Grub のデータ + 突進の数値)とし、別のコントローラや別クラスは作らない。
- **時間**: 状態のタイマーはゲーム内の経過時間(delta)で進める。delta は 1 更新あたり 0.05 s を上限にする。状態が切り替わるときは余りを次の状態に持ち越す。ポーズ復帰の最初の更新も同じ上限を通す。
- **突進の接触**: Charge 中は、Grub とプレイヤーの相対運動をスイープ判定する(判定形状が円でない場合は相対移動 0.25 タイル以下に分割)。接触の解決は 1 つの関数にまとめ、プレイヤーの無敵は問い合わせ関数を通して読む。無敵の実装自体は変えない。
- **同時 1 体**: 保存する状態は作らない。Windup に入る瞬間に、生きている他の突進型が Windup または Charge にいるかを調べる。
- **突進スイッチ**: スポナーが生成時に `grub_charger` を `grub` に置き換える 1 か所で実現する。
- **部屋データ**: 部屋ごとの数値、スロット、波(スポーン一覧と K/T)を宣言的に持たせる。出現中、最初の 1 発、出現位置の待ちは全部屋共通の定数にする。
- **見た目への口**: 敵の状態、状態の経過割合、突進の方向を、見た目側が読める形で出す。
- **開発用補助**: 部屋選択、スイッチ、30/60 FPS の切り替え、状態ログは開発ビルド限定にする。

仕様と既存実装の食い違い 2 点(Flinch、接触の定義)は、この決定では決めない。計画は仕様の文面どおりに組み、`game-designer` の確認を待つ。

## Rationale

- 共通コントローラは種別ごとの違いをデータと小さなルーチンで持つ構造のため、状態の追加が既存の枠に収まる(小さなチーム、再利用)。
- 突進は 30 FPS で約 0.27 タイル/更新、向かい合うダッシュとの相対で約 0.8 タイル/更新動く。判定形状が仕様にも未定義のため、離散判定は取りこぼしの可能性を排除できない。スイープなら形状の大きさに依存しない。
- 同時 1 体を導出で判定すれば、倒された、部屋が終わった、といった経路での解放漏れが起きない。敵は最大 4 体なので費用も無視できる。
- スイッチをスポナーの 1 か所に置くと、「敵の数、波、位置は同じで突進だけ消える」(V6)が構造で保証される。
- 無敵を問い合わせ関数の裏に置くと、欠陥 D の修正がこの作業と独立する。

## Alternatives considered

- **離散の重なり判定のまま、判定を大きくする**: 形状を変えると仕様の判定の範囲(既存の接触判定)から外れ、窓も変わる。
- **シミュレーション全体を固定時間刻みにする**: 取りこぼしと時間の誤差は消えるが、既存の操作感に触れる範囲が大きく、この Goal の費用を超える。
- **同時 1 体を保存したトークンで管理**: 解放漏れ(Windup 中の撃破、部屋終了、ポーズ)の経路が増える。
- **各コントローラに突進スイッチのフラグを持たせる**: 置き換えの場所が敵ごとに散り、V6 の保証が弱い。
- **突進用に別の敵コントローラを作る**: Chase や Flinch、出現中の処理が二重になる。

## Revisit when

- T0 の調査で、部屋のコードと敵のコントローラが強く結合していた、または部屋の終了条件が広く参照されていた場合(T3 の大きさと並列化を見直す)。
- 接触の判定形状が、スイープまたは分割で扱いにくい形だった場合。
- 欠陥 D の修正が、無敵の問い合わせ関数の前提(1 つの真偽で答える)を変える場合。
- 30 FPS 未満のサポートが必要になった場合(delta の上限を見直す)。
>>>END

<<<FILE decisions/D-007-build-without-code-access-assumption-register.md
---
kind: decision
id: D-007
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-007: コードを読めない状況では、T0 を「前提の台帳」に置き換え、前提ごとに検出点と戻し先を決めて Build を進める

## Decision

D-004 の技術方針(状態の追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)は変えない。D-004 の「T0 で確認する前提」の扱いだけを次のとおり改める。

1. **T0 の扱い**: T0 を、着手前に済ませる独立した調査工程としては扱わない。未確認の 7 項目は「前提の台帳」(Handoff 16 の Findings)に載せ、各項目を、それに最初に依存するタスクの冒頭で確認する(プローブ)。確認できた事実は Build の Handoff に書く。
2. **前提が崩れたときの戻し先**: 崩れた時点で、そのタスクを止めて返す。分類は次のとおり。
   - (i) D-004 の範囲内の局所的な修正で済む: Build が直して進め、Handoff に記録する。
   - (ii) 仕様の変更が要る: `game-designer` へ。
   - (iii) 技術方針の変更が要る(D-004 の「Revisit when」に該当する場合を含む): `technical-director` へ。
   - (iv) 必須の視覚要素が実現できない: `art-director` へ(Studio 経由)。
3. **推測の封じ込め**: 未確認の前提に依存するコードは、1 か所の継ぎ目(関数または定数)の後ろに置く。前提が外れたときの修正を局所にするため。
4. **報告の規則**: Build は、実行できなかった確認を「通った」と書かない。確認できたこと、できなかったこと、その理由を分けて書く。
5. **無敵の問い合わせ関数**: 署名(1 つの真偽で答える)は変えない。無敵フラグを書くタイマーのコードには、この Build では触れない(欠陥 D は別扱い)。
6. **接触結果の通知**: D-004 の「見た目への口」に、突進ごとの接触結果(未解決 / 抜けた / 被弾)を加える。接触を解決する 1 つの関数が決めた値を、その突進の間だけ保持する。突進の開始時に未解決へ戻す。
7. **打ち切りの条件**: Build が、読める・書けるコードが全くないために、台帳のプローブもコード変更もできないと再び報告した場合、それは前提のリスクではなく入力の欠落である。この場合は Build を再試行せず、`technical-director` に返し、Owner へのエスカレーション(リポジトリの提供、または模擬の範囲の確認)を用意する。

この決定が扱わないこと: 戦闘の規則・数値、D-001〜D-006 の内容。欠陥 D の原因と修正。

## Rationale

- D-004 の方針は、`sim/repo-notes.md` の確認済みの 7 つの事実と矛盾しない。確認できた事実(共通コントローラ、状態遷移、可変 delta、1 つの無敵フラグ)が方針の骨格を支えている。崩れると方針が変わるものは、未確認の項目のうち、部屋の終了条件の結合の強さと判定形状の 2 点で、どちらも実装の入口で見える。
- 同じ入力を与えれば T0 の結果は変わらない。事前に別の調査をしても情報は増えない。実装の入口で確かめれば、確認とコード変更を同じ場所で行える。
- 継ぎ目を 1 か所にすると、前提が外れても、書き直しの範囲が 1 か所で済む。
- 接触の解決はすでに 1 つの関数にまとめる方針(D-004)なので、結果を保持する費用は小さい。仕様と D-006 は、この通知を「望ましい(S)」とし、省いてよいとしている。
- 打ち切りの条件を先に決めておくと、コードが全くない状態でのやり直しを繰り返さずに済む。

## Alternatives considered

- **(b) 仮定で埋めた計画に作り直し、対象を縮める**: 仮定が正しいかどうかは実装の入口でしか分からない。先に縮めると、不要な縮小で仕様の効果(波、予告)を落とすおそれがある。採らない。縮小は、前提が実際に崩れた箇所に限る。
- **(c) 今すぐ Owner に確認する**: このサンプルは `repository: none` で、ビルドを `sim/` で模擬する設計である。Build が何も作れないと分かる前にエスカレーションするのは早い。ただし、7 の条件に当たった時点で行う。
- **T0 を台帳なしで保留する**: 崩れたときの戻し先がなく、Build がまた止まる。採らない。

## Revisit when

- Build が、台帳の項目 1(部屋)または項目 3(判定形状)で D-004 の「Revisit when」に該当する事実を見つけた場合。
- Build が、実行できる確認がほとんどなく、報告が「未確認」ばかりになる場合(7 の条件)。
- 欠陥 D の修正が、問い合わせ関数の前提を変える場合(D-004 と同じ)。
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

<<<FILE goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 18: gameplay-engineer → studio — コードを読み書きできないため、実装も台帳のプローブもできなかった(D-007 の 7、§8 に従い再試行せず返す)

## Task

Studio は、D-007 の 7 に従ってこの Build を再試行せず、`technical-director` に回し、Owner へのエスカレーションを用意すること。エスカレーションの内容は、リポジトリの提供、または模擬の範囲の確認。

## Context

Handoff 17 は、Build の再開にあたり、最初に「実際にコードを読み書きできるか」を報告するよう求めていた。この Step で次を確認した。

- 実行環境に渡されたのは、この packet の入力ファイルだけ。ゲームのソースコード、ビルド、テストの実行手段、リポジトリはない。
- 書けるのは `goals/G-001-combat-monotony/18-gameplay-engineer-to-<recipient>.md` の 1 ファイルだけ。コードやテストを変更する経路はない。
- `sim/repo-notes.md` と `sim/build-0.3.md` は、コードの代わりの模擬の記述で、コード自体ではない。台帳の項目をこれらで「確認した」とは扱えない。

この状態は D-007 の 7(読める・書けるコードが全くないため、台帳のプローブもコード変更もできない)に該当する。そのため再試行せず、`outcome: question` で返す。

## Findings

### 1. 確認できたこと

- コードを読み書きできないこと。上の Context のとおり。
- 仕様、決定(D-001〜D-007)、視覚仕様は読んだ。コードに頼らずに分かる範囲では、これらの間に新しい矛盾や欠落は見つけていない。ただしこれは文書を読んだだけの結果で、実装の確認ではない。

### 2. 確認できなかったこと(すべて、コードにアクセスできないため)

| # | 項目 | 結果 | 分類 | 理由・備考 |
|---|---|---|---|---|
| 1 | 部屋データ、スポナー、波 | 未確認 | なし | 部屋の終了条件の参照箇所と、敵の生成の結合の強さを見るコードがない。 |
| 2 | 部屋のコードと敵のコントローラの分離 | 未確認 | なし | 同じファイルや関数を変更するか見られない。T2 と T3 は既定どおり直列とするしかない。 |
| 3 | 接触の判定形状、レーン幅の元の値 | 未確認 | なし | 判定形状と、接触判定の大きさが 1 つに定まるかが不明。 |
| 4 | Spitter の弾 | 未確認 | なし | 弾の衝突処理を読めない。 |
| 5 | 視覚の仕組み(要素 2〜10) | 未確認 | なし | §4 の段階はどれも判定できない。使った段階は「なし」(何も実装していない)。 |
| 6 | 接触結果の通知 | 未確認 | なし | 接触を解決する関数を作っていない。省くかどうかの判断もできない。 |
| 7 | 敵の挙動が経過時間で進むか | 未確認 | なし | `sim/repo-notes.md` に「可変 delta」とあるが、これは模擬の記述で、コードでは確認していない。 |

- 実装、テスト、開発ビルド限定の状態ログ、30/60 FPS の切り替え、ビルドの手順とビルドノートは、いずれも作っていない。
- 何も実行していないので、「通った」と言える確認は 1 つもない。

### 3. QA へ渡せるもの

なし。変更がないので、`qa` と `art-director` の Verify に回すものはない。

### 4. 次に必要なこと

D-007 の 7 のとおり。

1. Studio は、この Build を再試行せず `technical-director` に返す。
2. `technical-director` は、Owner へのエスカレーションを用意する。選択肢は次の 2 つ。
   - (a) 実際のリポジトリとビルド・テストの手段を、Build が使えるようにする。
   - (b) このプロジェクトが模擬(`repository: none`)であることを前提に、Build の範囲を確認し直す。たとえば、実装ではなく実装計画のレビューまでを範囲とする。
3. (a) が満たされたら、Build は Handoff 17 の台帳のとおり再開できる。そのときの順序は次のとおり。
   - 台帳 1、2 を部屋のタスクの冒頭で確認する。
   - 台帳 7 を状態追加のタスクの冒頭で確認する。
   - 台帳 3、6 を突進のタスクの冒頭で確認する。
   - 台帳 4 を弾の処理を読んだ時点で確認する。
   - 台帳 5 を見た目のタスクの冒頭で確認する。

## Decisions already made

- D-001〜D-006: 変更しない。
- D-007: 台帳の方針と打ち切りの条件。今回は 7 の条件に該当した。

## Constraints

- 仕様、数値、D-001〜D-006 は変えていない。
- 無敵のタイマーのコードには触れていない(そもそもコードに触れていない)。
- 実行できなかった確認を「通った」とは書いていない。
- 仕様の曖昧さ・矛盾・欠落は見つけていない。したがって `game-designer` に回すものはない。

## Open questions

1. Owner または `technical-director` へ: Build がコードを読み書きできる環境(リポジトリとビルド・テスト手段)を提供するか。提供しない場合は、Build の範囲を模擬に合わせて確認し直すか。

## Expected output

`technical-director` が、D-007 の 7 に従って Owner へのエスカレーションを用意する。Build の再開は、その結果を待つ。Studio は、この Handoff を `technical-director` に回すときに、`qa` や `art-director` へ並列で渡さない。

## Sender assessment

- この Step は、コードの読み書きができるかを最初に報告する、という Handoff 17 の指示に従った。結論は「できない」。
- Handoff 16 の技術確認の内容は、この packet にない。Handoff 17 の Findings と D-007 のみに基づいて書いた。
- 推測のコードや、確認していない前提に基づく計画の「実装済み」扱いは、書いていない。文書だけで進められる部分(仕様の読み合わせ)は済ませたが、新しい矛盾は見つからなかった。
- 確信度: コードにアクセスできないという点については高い。台帳 7 項目の実際の結果については、情報がなく、評価できない。

## Load

- Role: studio/roles/technical-director.md
- Skills: none
- Project: project.md#constraints, sim/repo-notes.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-007-build-without-code-access-assumption-register.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
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
