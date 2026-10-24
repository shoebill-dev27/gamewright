# Studio operation packet

operation: Step
goal: G-002
role: game-director
incoming_handoff: goals/G-002-final-boss/05-studio-to-game-director.md
next_seq: 6
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-002-final-boss/06-game-director-to-<recipient>.md
- decisions/D-015-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-002-final-boss/05-studio-to-game-director.md
---
kind: handoff
goal: G-002
seq: 5
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 05: studio → game-director — 最終戦の配置と実装範囲を判断する

## Task

初回Designの候補とTechnical Directorの調査から、ボスの配置、既存第5部屋の扱い、今回の終端・再挑戦の範囲を判断する。Goalの意味を変える、または作業規模を大きく変える必要がある場合は、採択する前にOwner向けEscalationを作成する。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。現Interpretationは「ランの最後」に位置取り、攻撃・ダッシュのタイミング、敵への対応を通じた手応えを持つ戦闘を求める。

初回Designは配置を独断で選ばずquestionを返し、その後Technical Directorが提供コードを静的調査した。配置・攻撃・終端について新しいDecisionはまだない。Studioは内容の採択を行っていない。

## Findings

判断の根拠は02と04。詳細はLoadに含める。

- A：第5部屋を単体ボスに置換。部屋数を増やさず単独評価しやすいが、既存混成戦と第5部屋固有の基準の扱いを決める必要がある。Game Designerの第一候補であり、未承認。
- B：第5部屋の後に追加。既存構成を保持できるが、部屋の追加だけでは前の部屋から到達する経路はできない。
- C：第5部屋の混成戦に同居。複数脅威の調停と回避可能性、表示の組合せ検証が増える。Game Designerは初手として推奨していない。
- 提供コードの実行経路は個別部屋選択方式で、連続ラン・状態継承・最終勝利・専用リトライはない。同じコマンドの再実行は新しい部屋セッションになる。
- 選択可能なボス部屋だけでは「ランの最後に到達する」という現Interpretationを実証できない。連続ランを含める場合、A/B/Cいずれでも進行・継承・終端・再挑戦・時刻と入力の契約が新設となる。
- 死亡・クリア後も表示用の時間中に弾などが進む可能性が静的に指摘されている。勝敗の優先順位、残弾、終端後の操作は後続仕様で明確化する必要がある。既存不具合のQA判定ではない。
- 単体敵の複数攻撃切替は未実装。既存戦闘の基盤は再利用可能だが、敵更新・表示・イベント・botsの前提をまたぐ変更になる。設計後のPlanを予定する。
- player/traceには60秒上限がある。15〜20分はVision上の目標であり、現行ランの実測ではない。独立部屋のbots時間の合算をラン実測として扱えない。
- 攻撃種、固定方向、危険範囲、回復状態、HPの表示に不足がある。ゲームルール確定後、Art Directorへの限定的な表現仕様依頼が必要か判断材料を残す。

04は提供ファイルの静的所見である。指定sha `27fe16268ac8` と実ファイルの一致、テスト、player/trace、botsは未確認・未実行。資料はbuild 0.6、project.mdのCurrent stateは0.4という差がある。実行・計測を伴う事実として採択しない。

## Decisions already made

- D-001：攻撃とダッシュが基本。追加の戦闘入力はOwner承認が必要。
- 既存接触端の例外、非中断、cue gap、無敵接触消費の制約は02・04に整理されている。今回それらを変更する承認はない。
- G-002の配置、攻撃構成、終端・再挑戦範囲のDecisionは未作成。

## Constraints

- project.mdのVisionとConstraints、goal.mdのOwner requestとInterpretationを維持する。
- Goalの再解釈や大幅な範囲変更をRole内の採択で済ませない。該当時はOwnerへ戻す。
- 権限内の配置・優先度の判断を、選択肢があるという理由だけでOwnerへ戻さない。
- 詳細な攻撃ルール・数値はGame Designer、技術方式はTechnical Directorの責任に残す。
- ボスに不要な既存部屋の全面改修、新規入力、グラフィカルな実装を前提にしない。
- 静的調査をQA合格、体験評価、戦闘時間の実測として扱わない。

## Open questions

1. A/B/Cのどれを採るか。既存第5部屋と固有基準をどの範囲で保持・置換するか。
2. 現Interpretationを維持して必要となる到達経路・最終勝利・再挑戦の範囲は何か。それはGoalが含意する範囲内か。
3. 選択可能なボス部屋に限定する場合、Goalの再解釈を要するか。連続ランを新設する場合、大幅な規模変更としてOwner判断が必要か。
4. 時間配分の判断に実測が必須か。未実測のまま定められる方向上の限界と、後続で集めるべき証拠は何か。
5. 診断が判断に不足するなら、どの具体的な追加情報が必要か。

## Expected output

権限内で決められる場合、配置・既存第5部屋・到達経路・終端と再挑戦の範囲、採択理由と代替案、後続設計の限界をDecisionとして記録し、結果をStudio宛Handoffで返す。詳細仕様や技術方式は決めず、Game Designerが仕様化できる方向を示す。

Owner escalationの条件に当たる場合は、prepare-owner-escalationに従い、日本語のEscalationを作成する。必要な判断を一問にまとめ、選択肢、規模・体験への影響、推奨、各選択後のルートを記す。Owner判断前に方向を確定しない。

判断材料が不足する場合は、必要な情報と理由を特定してStudioへ返す。今回は実装・QA・Goal達成判定を行わない。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-002-final-boss/04-technical-director-to-studio.md
- Supporting handoff: goals/G-002-final-boss/02-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots
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

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE goals/G-002-final-boss/goal.md
---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-20
---
# G-002: 最後に手応えのあるボス戦

## Owner request

> 最後に手応えのあるボス戦がほしい

## Interpretation

ランの最後に、プレイヤーが位置取り、攻撃とダッシュのタイミング、敵の挙動への対応を通じて手応えを感じられるボス戦がある。短いランと、被害を受ける前に脅威を読み取れる体験を維持する。

具体的なボスの仕組み、配置、難度、数値基準は担当Roleが定める。新しい入力ボタン、ゲームの基本コンセプト変更、ボス戦に必要のない既存部屋の全面改修は対象外。ラン構成や作業規模を大きく変える必要が生じた場合はOwnerに判断を戻す。

## Unknowns

- Observe：既存の不具合報告ではないため skipped。技術調査は静的確認のみであり、実行による裏付けは未実施。
- Diagnose：done。提供コードでは個別部屋のセッションのみで、連続ラン・部屋間継承・最終勝利・専用リトライはない。指定shaとの一致、実行時の終端挙動、戦闘時間は未確認。調査の制限は04に記録。
- Decide：open。配置A/B/C、既存第5部屋の扱い、終端・再挑戦の範囲をGame Directorが判断する。選択可能なボス部屋だけでは現Interpretationの達成を実証できず、連続ラン新設は配置変更とは別の規模となる。Goalの再解釈や大幅な範囲変更が必要ならOwnerへ戻す。
- Design：方向確定後、攻撃構成、予兆と対処、時間配分、勝敗・残弾・終端後操作・再挑戦、受け入れ基準を仕様化するため planned。
- Plan：planned。技術調査で、単体敵の複数攻撃切替、表示、終端の契約と共有コードへの影響が判明したため、確定仕様に基づく実装計画が必要。
- Build：仕様と計画の確定後にゲーム変更が必要なので planned。
- Verify：Build後の独立確認は planned。30/60 FPSと共有戦闘ルールの回帰を含む。Art Directorの表現確認は、攻撃・表示仕様で依存が確定するまで tentative。
- Play：最終戦の手応えを独立したプレイヤー観察で評価するため planned。実装内容や期待結果は渡さない。
- Review：体験Goalの達成判断が必要なので planned。
- Next：結果と残課題をOwnerへ返すため planned。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md → 結果: 02-game-designer-to-studio.md |
| 2 | Diagnose | technical-director | technical-plan | done | 03-studio-to-technical-director.md → 結果: 04-technical-director-to-studio.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | open | 05-studio-to-game-director.md |
| 4 | Design | game-designer | write-design-spec | planned | — |
| 5 | Plan | technical-director | technical-plan | planned | — |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | tentative | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

原則として逐次実行する。Game Directorの方向判断後にDesign、Planへ進む。Owner判断が必要になった場合は依存する後続Stepを停止する。Art DirectorのVerifyが必要になった場合は、同じビルドに対するQAのVerifyと独立に並行できる。

## Route changes

Technical Directorの静的調査を完了し、予定どおりGame Directorの配置・範囲判断を開く。連続ラン不在と実行未確認を明示し、Goal再解釈・大幅な範囲変更はOwner判断へ戻す。攻撃切替・表示・終端の複数システムへの影響から、設計後のPlanをplannedに確定した。

## Next action

Game Directorが `05-studio-to-game-director.md` から配置・既存第5部屋・終端と再挑戦の範囲を判断する。権限内ならDecisionとStudio宛Handoffを、Owner判断が必要ならEscalationを作成する。次の操作はこのDecide Step。

## Outcome

未完了。初回Designと技術的な静的調査を完了した。配置・範囲の決定、仕様確定、実装、検証、体験評価は未実施。技術調査は実行成功やQA合格を示さない。
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

<<<FILE goals/G-002-final-boss/04-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 4
from: technical-director
to: studio
stage: Diagnose
outcome: done
---
# 04: technical-director → studio — 個別部屋の終端とボス実現範囲の静的調査

## Task

調査結果をGame Directorへ渡し、ボスの配置A/B/C、既存第5部屋の扱い、今回実装する終端・再挑戦の範囲を判断できるようにする。判断後、Game Designerへ仕様化を戻す。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。初回DesignのA/B/Cは未承認であり、今回は技術的な診断のみを行った。

提供された `repo/game.py`、`repo/play.py`、`repo/bots.py`、テストおよび資料を静的に確認した。コード・仕様・Decisionは変更していない。実行結果によるQA判定、配置選択、Goal達成判定は行っていない。

## Findings

### 1. 調査の証拠と実行上の制限

対象として指定されたshaは `27fe16268ac8`。このStepで読めた証拠はパケット内のファイル本文であり、実ファイルとshaの一致は検証していない。README、manual、コードの表示はbuild 0.6で一致する。`project.md` のCurrent stateの0.4とは異なる。

実行ツールの探索を試みたが、`code-mode host is disabled` が返り、シェル実行手段を取得できなかった。したがって、以下のコマンドはすべて未実行であり、テスト件数・成功・戦闘時間の実測値は報告できない。

| 確認予定コマンド（作業ディレクトリ `repo/`） | 状態 |
|---|---|
| `python3 -m unittest discover -s tests` | 未実行 |
| `python3 play.py --view player {script}` | 未実行 |
| `python3 play.py --view trace {script}` | 未実行 |
| `python3 bots.py {script}` | 未実行 |

再現確認には、指定shaの実行可能な `repo/`、Python 3、スクリプトを渡せる実行環境が必要。以下はすべて「提供コードから確認した挙動」であり、観測した実行結果ではない。

### 2. 現行の入場・終端・再挑戦

| 項目 | 提供コードで確認した実装と根拠 |
|---|---|
| 入場 | `play.read_script()` が一つのroom値を読み、`play.play()` が一つの `Game` を生成する。room行を複数書いても順番の指定にはならず、後の値が上書きする |
| 選択範囲 | `game.ROOMS` は1〜5とempty。ボス定義・ボス部屋はない |
| 開始状態 | `Game.__init__()` で座標(8,4)、右向き、移動なし、3 hearts、各種タイマー0、キュー攻撃なし、弾なし、イベントなし、`cleared=False`。選択部屋の敵を新規生成する |
| クリア | `Game.step()` で敵リストが空でなく、全敵のHPが0以下なら `cleared=True` と `cleared` イベント。プレイヤー表示は `room cleared` |
| 死亡 | `_hurt()` でheartsが0になると `down` イベント。表示は `you went down`、盤面のプレイヤー印は `x` |
| セッション終了 | `play.play()` はクリアまたは死亡を認識してから最大1秒継続する。ただし指定endまたは60秒上限が先ならそこで終了。最後は時間・hearts・残敵数を表示する |
| 次の部屋・最終勝利 | 提供された実行経路には存在しない。第5部屋だけの勝利表示もなく、全5部屋共通の部屋クリアで終わる |
| 再挑戦 | 専用入力、再開地点、同一セッション内のリトライ処理はない。同じコマンドを再実行すると新しい `Game` が作られ、上記開始状態から始まる |
| 状態継承 | 部屋間遷移自体がなく、継承処理もない。botsも各部屋で新しい `Game` を生成する |
| ポーズ・入力機器 | `Game.press()` とplayの受理入力はmove/stop/attack/dash。pauseや実機キーボード・ゲームパッドの入力層は、提供ビルドにはない |

従って、提供された現在のビルドは個別部屋のセッション方式である。botsの1〜5実行も、独立した部屋を順に試験する処理であり、連続ランではない。この結論の範囲は提供されたファイルに限る。

**終端には注意点がある。** 資料の「死亡・クリア時はすべて停止」とコードは完全には一致しない。`_update_enemies()` は死亡時には戻るが、クリアを停止条件にしていない。`step()` 全体と `_update_shots()` も終端で停止しないため、終了後の表示用1秒間もタイマーや弾は進む。最後の敵を倒しても弾が残れば、その後に被弾・死亡する可能性をコード上は排除できない。また `press()` は死亡を拒否するが、クリアを拒否しない。勝敗の優先順位と終端後の操作・残弾処理は、新しい終端仕様で明記し、実行確認する必要がある。現段階で既存ビルドの不具合判定はしない。

emptyは敵0体のままでは自動クリアしない。時間上限の検証には使えるが、通常部屋のクリア確認の代用にはならない。

### 3. 「最後」の到達範囲による費用差

**選択可能な最終部屋としてのボス戦**であれば、ボス挙動、部屋データ、テキスト表示、スクリプト選択と検証の追加が中心となる。部屋数を増やす案でも、選択肢を増やすだけなら連続ランの実装は必要ない。ただし、それだけでは「ランの最後に到達した」というGoal解釈を実証できない。

**連続ランから最終勝利まで**を対象にする場合は、現行の部屋戦闘に加えて次が新設となる。

- 部屋順序と進行状態、次部屋へ移る条件・時点。
- hearts、位置、向き、タイマー、弾、入力・反応ルールのリセット／継承契約。
- 部屋クリアとラン勝利の区別、死亡と勝利が近接した場合の優先順位。
- 死亡後の再開地点と再挑戦手段。
- 部屋内時刻とラン時刻、スクリプト入力の時刻基準、長時間実行と集計。
- 部屋境界・最終勝利・再試行を独立確認するテスト経路。

これはA/B/Cのどれでも別途必要であり、Bだけの費用ではない。現行コードには基盤がないため、配置変更だけと同等の規模には扱えない。大幅な範囲変更に当たるかはGame Directorが判断し、必要ならOwnerへ戻す材料になる。

### 4. 配置候補別の変更範囲とリスク

攻撃構成が未確定なので、人日・絶対的な工数は見積もれない。以下は共通のボス実装に対する相対的な影響である。

| 候補 | 影響するシステム | 固有のリスク・検証 |
|---|---|---|
| A：第5部屋を単体ボスへ置換 | `ROOMS["5"]`、敵更新・攻撃判定、表示、manual、botsと部屋別テスト | 旧混成戦を失う。部屋5の構成、cue gap、既存bots集計条件のどこを置換・維持するか仕様が必要。第4部屋からの難度接続を別途評価する |
| B：第5部屋の後に追加 | 新しい部屋キー、選択説明、テスト対象、botsの部屋指定・既定対象 | 既存1〜5の構成を保持しやすい。ただし部屋を追加するだけでは「後に進む」経路はできない。連続ランを求めるなら前節の新設が必要 |
| C：第5部屋に同居 | 第5部屋データ、ボスと既存敵の更新・予兆調停、表示、bots・複合戦検証 | 最も組合せ検証が増える。グラブの同時予兆抑制、スピッターのcue gap・弾数上限と、ボス攻撃の関係を明示する必要がある。単体で回避できても混成時の回避可能性は保証されない |

第5部屋のスピッター挙動は、`ROOM_SPIT_STAGGER` と `GAP_ROOMS` が文字列の部屋番号に結び付いている。Aで敵を取り除けばその戦闘では使われなくなるが、設定を残す／変更する判断とテストの扱いは必要。Bの新しい部屋にはcue gapが自動適用されない。Cでもボス攻撃は既存スピッターの調停に自動参加しない。

既存テストには第5部屋のブルート位置、部屋4〜5のgap、1〜5のdodger比較、3〜5合計のバランス条件がある。A/Cでは旧第5部屋を含む合計をそのまま新ボスの受け入れ基準に使えない。Bでもbotsの既定対象は `ROOMS` から作られるため、新部屋追加で出力対象が変わる。旧部屋の回帰と新ボスの評価を明示して扱う必要がある。

### 5. ボス挙動・表示の再利用範囲

**再利用できる基盤**

- 秒単位の固定フレーム更新、30/60 FPS指定、移動・部屋端のクランプ。
- プレイヤーの攻撃、ダッシュ、被弾保護、キュー攻撃。
- 敵HP減少と全敵撃破判定。
- グラブの固定照準、予兆・突進・回復・中断可否の考え方。
- スピッターの固定照準、予兆後の弾生成、弾の接触消費。
- イベント、盤面の印、警告メッセージ、`cue:`行、traceという表示の入口。

**現状のままでは不足するもの**

単体敵の複数攻撃切替は未実装。`Enemy` はグラブ系かスピッターのどちらかで、各更新処理も分岐する。グラブのパラメータ追加だけでは、突進と射撃を切り替えるボスにはならない。

新種を追加する場合、`Enemy` の検証だけでなく、`is_grub`、敵更新、`mark`、`_line_cells()`、`cue_lines()`、trace、botsの脅威認識を確認する必要がある。現行には「グラブ以外はスピッター」という前提があるため、未知のkindを受理するだけでは安全に拡張できない。

HPは内部とtraceには存在するが、player viewには数値表示がない。回復状態もplayer viewでは明示されず、盤面で停止すること以外に識別情報が乏しい。ボス用の攻撃名、予兆と危険範囲、回復開始・終了、HPの表示は追加対象となる。現行の半秒ごとの定期描画に加えて、必要な状態変化で描画を発火する条件も必要。

Art Directorへ限定して依頼する場合の具体的な不足は次のとおり。

- ボスと攻撃種を区別できる印・メッセージ・`cue:`の表現。
- 狙いの固定方向と危険範囲を読める表示。新形状では既存の細い `~` 線だけで足りるか。
- 安全な攻撃機会としての回復状態と、その終了の識別。
- HP表示と、同居案で印や予兆線が重なる場合の読みやすさ。

攻撃順・危険範囲・回復時間などのルールは先にGame Designerが定める。Art Directorへゲームルールの決定を移さない。グラフィカルな実装は前提としない。

### 6. 60秒上限と計測

`play.MAX_SECONDS=60.0` は反応ルールの有無によらず、player/trace両方の `play.play()` に適用される。明示的な `end 120` でも60秒に丸められる。

反応ルールなしの既定終了は、入力ありなら最終入力時刻+3秒、入力なしなら5秒。反応ルールありなら既定60秒。いずれも終端後の表示時間はこの上限を超えない。

一方、`Game` 自体には60秒上限がない。`bots.play_room()` は指定limitまで動作し、botsのlimitは既定60秒だが上限への丸めはない。したがって、60秒超の内部シミュレーションは可能だが、現行play経路ではその全期間のplayer/trace検証ができない。ボス時間が上限に近い場合も、時間切れを勝利・死亡と区別する必要がある。時間切れの専用イベント・メッセージは現状ない。

時間設計後、必要ならplayの実行上限と終了理由表示を変更し、独立検証にも同じ長さを提供する。上限を外すだけでは連続ランは実装されない。

計測可能なのはシミュレーション上の秒数である。botsはクリア・死亡・limit到達時点を返し、playは終了時刻、traceはイベント時刻を示す。playの終了時刻には最大1秒の終端後表示が含まれるため、戦闘時間には `cleared` / `down` の時刻を使う。

15〜20分の目標との比較には、連続ランの契約、移動・部屋間時間、再挑戦の扱い、人間の入力判断と習熟を含む観察が不足している。独立した5部屋のbots時間を足しても、現行ランの実測にはならない。今回は時間数値を実測していない。

### 7. 次の調査・実装計画への依存と検証方針

方向判断前に必要な追加実行は、実行環境が得られれば次の順で行える。

1. 指定shaを確認し、既存unittestを実行する。
2. 30/60 FPSそれぞれで、第5部屋の死亡と再実行、practiceの全敵撃破をplayer/traceで対照する。
3. 空のpracticeに `end 120` を指定し、player/traceの60秒終了を確認する。反応ルールの有無も比較する。
4. 第5部屋クリアはbotsで確認し、必要ならその判断記録からplay用入力を作成して表示を確認する。
5. 最後の敵撃破時の残弾と、終端後の操作・被弾を確認する。

これは追加のQA合否判定ではなく、静的所見を実行で裏付けるための調査である。

仕様確定後の自動検証は、攻撃切替、固定照準、予兆時間、回復、安全性、中断、無敵接触、終端・再試行を30/60 FPSで対象にする。共有コードの変更に応じて既存攻撃・敵の回帰を行う。新しい攻撃形状にD-002/D-003の接触端例外は自動適用しない。

QAは同じビルドのplayer/traceで表示と内部状態を照合し、手応え・理解・所要時間は後続Play/Reviewが判断する。既存botsはボスの新攻撃を読む実装ではないため、未対応の成績を人間の難度評価に流用しない。

今回の調査と配置判断は逐次でよく、並行コード作業は行わない。後続実装の分割は仕様と敵更新・表示間の契約が定まってから判断する。現状で並行実装を始めると、kind・phase・イベント形式の共有箇所で衝突する。

## Decisions already made

- D-001：追加の戦闘入力にはOwner承認が必要。今回の調査では追加入力を提案・採択していない。
- D-002/D-003：既存の弾・突進の接触端例外。新形状への適用は別途明示が必要。
- D-004：ブルートの非中断と部屋4〜5のスピッターcue gap。
- D-005：無敵接触時の弾消費・突進の一撃消費。
- G-002の配置・攻撃・終端範囲に新規Decisionはない。D-015は作成していない。

## Constraints

- この結果は提供コードの静的調査。実行成功、sha一致、QA合格を示さない。
- A/B/C、既存第5部屋の存廃、今回の到達範囲はGame Directorの判断に残す。
- 新しい入力を追加せず、30/60 FPSと既存のプレイヤー戦闘ルールを維持する。
- ボスに不要な既存部屋の全面改修を含めない。
- player向け表示はテキストビルドで成立させる。
- 15〜20分はVision上の目標であり、現在のラン実測値ではない。
- 秘密情報・個人情報を後続資料に含めない。

## Open questions

1. A/B/Cのどれを採るか。第5部屋の旧構成と固有基準をどう扱うか。
2. 今回は選択可能な最終部屋までか、連続ラン・最終勝利・再挑戦までか。前者ならGoal解釈に残る不足をどう扱うか。
3. 連続ランを含める場合、その新設規模をOwnerへ戻す必要があるか。
4. 勝利・死亡・残弾・終端後操作の優先順位と再挑戦地点をどう定めるか。
5. ボスの攻撃構成・時間をどう定め、60秒超のplayer/trace検証を必要とするか。
6. 上記の表示不足について、Game Designerの仕様後にArt Directorへ限定した表現仕様を依頼するか。

## Expected output

Studioは本結果と初回DesignのA/B/CをGame Directorへ渡し、配置、既存第5部屋、今回の終端・再挑戦範囲を判断するStepへルーティングする。大幅な範囲変更ならOwnerへの判断材料を用意する。

判断後、Game Designerへ採択範囲と静的確認事項・実行未確認事項を渡し、ボスと終端の受け入れ基準を仕様化する。実装計画はその後に必要性を判断する。本報告を確定仕様やQA合格として扱わない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-002-final-boss/03-studio-to-technical-director.md
- Supporting handoff: goals/G-002-final-boss/02-game-designer-to-studio.md
>>>END

<<<FILE goals/G-002-final-boss/02-game-designer-to-studio.md
---
kind: handoff
goal: G-002
seq: 2
from: game-designer
to: studio
stage: Design
outcome: question
---
# 02: game-designer → studio — 最終戦の組み込み方とラン終端の確認を先行する

## Task

Game Directorへ、既存の第5部屋をボス戦へ置き換えるか、第5部屋の後にボス戦を追加するかの方向判断をルーティングする。併せてTechnical Directorへ、現行のラン終端・部屋間遷移・再挑戦の実態と、候補の実現範囲の確認を依頼する。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。今回のDesignでは、提供された戦闘仕様、プレイヤー向けマニュアル、README、D-001〜D-005を照合した。

戦闘の既存ルールは確認できた。一方、提供資料が説明する実行単位は個別の部屋であり、連続したランの終端は確定できない。最終戦の配置と規模を独断で選ばず、方向判断と不足情報をStudioへ返す。実装、QA判定、Goal達成判定は行っていない。

## Findings

### 確認できた事実と限界

- `design/combat.md`では5部屋が定義され、各部屋は全敵撃破で終了する。第5部屋は通常グラブ2体、ブルート1体、スピッター2体の混成戦である。
- マニュアルは`room 1`〜`room 5`を選択して遊ぶ方式を説明している。反応ルールを使うセッションは部屋クリアまたは死亡で終了し、最大60秒。これは実行セッションの上限であり、15〜20分の連続ランが存在しないという証拠ではない。
- 提供資料には、部屋クリア後の自動遷移、最終勝利表示、死亡後の再開地点、部屋間での状態継承の具体的な説明がない。
- プレイヤーは部屋ごとに3 heartsと規定されている。ただし、実際の部屋間遷移での回復・リセット処理は未確認。
- 提供された敵定義にボスは記載されていない。ビルド内のボス不在を確認したものではない。
- `project.md`のCurrent stateはbuild 0.4の記述だが、戦闘仕様・manual・READMEはbuild 0.6を説明している。今回の戦闘ルールの比較には後者を用いた。
- このStepではplay/botsを実行していない。既存部屋のプレイやバランス集計だけでは、資料にない連続ランの終端と再挑戦の契約は確定できない。

### 体験上の設計課題

通常グラブは予兆中の攻撃で中断でき、ブルートは横移動またはダッシュで避けて回復中に攻撃する。スピッターは固定された射線から移動して逃れる。最終戦には、この既習の読み取りを使いつつ、「次の危険に備えて位置を選び、回避後に攻撃へ戻る」判断を継続して求めたい。

単にブルートのHPを増やすだけでは、既存の回答を長く繰り返す戦闘になる懸念がある。攻撃機会を失う位置取りと、回避後に攻撃できる位置取りを区別する構成を、方向確定後の仕様候補とする。具体的な攻撃構成・数値はまだ採択していない。

### 実質的な選択肢

| 選択肢 | 利点 | 代償・未確認事項 |
|---|---|---|
| A：第5部屋を単体ボス戦へ置換 | 部屋数を増やさず、最後の戦闘を明確にできる。既存の予兆・突進・回復・ダメージ規則の再利用を優先できる | 現行第5部屋の混成戦を失う。第4部屋からの難度接続と、第5部屋に限定された既存受け入れ基準の扱いを決める必要がある |
| B：第5部屋の後にボス戦を追加 | 既存5部屋を残し、既習内容の後に独立した最終戦を置ける | 部屋追加、終端変更、状態継承、総所要時間への影響がある。15〜20分の目標に収まるかは現状資料では判断できない |
| C：第5部屋の混成戦にボスを同居 | 既存の複数脅威を最終戦に残せる | ボスと既存敵の予兆・射線・回避経路の競合が増える。読みやすさの検証と調整範囲が広がる |

**推奨はAを第一候補として方向判断すること。** 小規模チームと既存システム再利用の制約に合い、最終戦固有の判断を単独で検証しやすい。ただし、第5部屋の役割を変更する選択なので、このStepでは確定しない。Cは最初の候補としては推奨しない。

### 判断の担当範囲

- Game Director：最終戦の配置、既存第5部屋の存廃、今回の到達範囲と優先度。新たなOwner確認が必要かも判定する。
- Owner：追加の戦闘入力を必要とする案、または既存の基本方針を変える案。今回の推奨案は入力追加を必要としないため、その理由だけでOwner承認を求める必要はない。
- Game Designer：承認された配置と範囲の中で、攻撃順序、予兆、対処、攻撃機会、HP、時間、境界条件、観測可能な受け入れ基準を決める。
- Technical Director：現行終端の確認、実現可能性と費用、技術方式。既存の敵が同じ部屋にいることと、単体の敵が複数の攻撃を使えることは別であり、後者の再利用可能性は未確認。
- Art Director：テキストで危険と攻撃機会を区別できない場合の表現仕様。グラフィカルな実装を前提にしない。

### 後続仕様・検証への引き継ぎ

方向確定後の仕様には、入場条件と開始状態、戦闘の全状態と遷移、攻撃ごとの予兆・固定照準・危険範囲・回避手段・回復時間、勝利・死亡・再挑戦、ポーズと同時イベントを明記する。既存の攻撃・ダッシュ・被弾保護は原則維持する。

QA向けには、30/60 FPSそれぞれで、予兆から最初の危害までの時間、固定された狙い、回避可能性、回復中の安全性、攻撃による中断の可否、無敵接触後の遅延ダメージ不在、終端と再試行の状態リセットを検証できる条件を作る。時間の許容差は既存同様に±1フレームを基本とし、接触端の例外はD-002/D-003の適用対象を明示する。新たな攻撃形状へ例外を自動拡張しない。

回帰確認は、プレイヤーの攻撃・ダッシュ・被弾保護と、共有挙動に影響する既存敵の予兆・中断・接触消費・射撃間隔に限定して必要範囲を指定する。Aを採択した場合、旧第5部屋の構成とその部屋固有の基準は新仕様で置換範囲を明記し、旧第5部屋のクリアを新ボスの合格条件に流用しない。既存部屋の全面再調整は含めない。

体験評価では、予兆から次の対処を選べるか、回避後に攻撃へ戻れるか、被弾理由を説明できるか、最終戦を既存部屋と異なる山場として受け取るかを後のPlay/Reviewへ残す。これらの評価意図はPlaytester向けHandoffへそのまま転記しない。

## Decisions already made

- D-001：攻撃とダッシュを基本とし、追加の戦闘入力にはOwner承認が必要。
- D-002/D-003：既存の弾・突進の接触は移動後のフレーム単位の距離判定。指定された接触端の帯だけに30/60 FPS間の命中差を認める。
- D-004：ブルートは予兆中の非致死攻撃で中断しない。第4〜5部屋のスピッターには0.6秒のcue gapがある。
- D-005：無敵中に接触した弾は消費され、突進の一撃は使用済みとなる。保護終了後の持ち越しダメージを生まない。
- G-002の配置・ボス構成・難度について、新規Decisionは作成していない。上記の選択肢と推奨は未承認である。

## Constraints

- 新規入力を追加しない。キーボードとゲームパッド、30/60 FPSに対応する。
- 脅威は危害の前に読み取れること。既存の接触・保護規則を難度のために暗黙変更しない。
- 短時間ランの目標は15〜20分。現行の所要時間は未計測であり、ボスの時間配分を推測で確定しない。
- 小規模チームとして既存システムの再利用を優先するが、技術方式はこのRoleで決めない。
- ボスに不要な既存部屋の全面改修や、過去Goalの履歴調査は範囲に加えない。
- プレイヤー向け情報は現在のテキスト表示で成立させる。現行表示は盤面の印、警告時の描画、メッセージ、`cue:`行を持つ。
- QAの合否と体験Goalの達成は後続Roleが判断する。

## Open questions

1. Game Director：A/B/Cのどれを採用するか。既存第5部屋の置換を今回の範囲としてよいか。
2. Technical Director：現行ビルドは個別部屋のセッションのみか、連続ランを持つか。クリア・死亡・再開時に何が表示され、どこへ戻り、何がリセットされるか。
3. Game Director：連続ランが未実装だった場合、今回の到達点は「最後の部屋として選択可能なボス戦」か、「連続ランと最終勝利まで」か。前者を採る場合、Goalの最終評価に残る不足を明示する必要がある。
4. Technical Director：単体ボスの攻撃切替、識別可能な表示、状態・残HPの提示を既存基盤でどこまで実現できるか。60秒の実行上限は検証可能な戦闘時間にどの制約を与えるか。
5. Game Director：既存ランの実測がない段階で、最終戦の時間配分を何に基づいて決めるか。
6. 表現上の依存：攻撃の種類、予兆の固定方向、回復開始を既存のテキスト表示で区別できるか。難しい場合はArt Directorへ限定した表現仕様を依頼する。

## Expected output

Studioは配置・範囲の方向判断をGame Directorへ、終端と実現範囲の確認をTechnical Directorへルーティングする。必要な参照ファイルだけで回答できるよう、それぞれのLoadを整える。

判断後、Game Designerへ、採択した配置、今回実装する終端・再挑戦の範囲、確認済みの現行挙動、技術・表示上の制約を渡す。Game Designerはその範囲内で、実装と独立検証に使える最終戦仕様および必要なDecisionを作成し、Studioへ返す。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/combat.md
- Project: repo/manual.md
- Project: repo/README.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-002-final-boss/01-studio-to-game-designer.md
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

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/06-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
