# Studio operation packet

operation: Step
goal: G-002
role: game-designer
incoming_handoff: goals/G-002-final-boss/64-studio-to-game-designer.md
next_seq: 65
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-final-boss/65-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-024-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-002-final-boss/64-studio-to-game-designer.md
---
kind: handoff
goal: G-002
seq: 64
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 64: studio → game-designer — 変更前一致基準の証拠と扱いを確定する

## Task

変更前ビルドが存在しない条件で、変更前との一致を求める基準を個別に整理する。Ownerの指定に従い、記録数値との比較にするか、確認不能として扱うかを決め、後続の技術再計画と独立QAが使える基準を示す。

## Context

G-002は、既存第1〜4部屋から最終単体ボスへ進む連続ランを、repo/のテキスト方式で成立させるGoalである。Build後のQAでは検証資料・実行・ログ不足が二度報告され、Technical Directorが62で試験道具と証拠構成の計画を提出した。

Ownerは63に案Aと回答し、D-023で供給条件を確定した。変更前ビルドは保存されておらず、その供給を待つ計画は採れない。Ownerは変更前一致基準の扱いをDesignerに委ねた。今回はその判断を先行させる。実測後の難度・追加数値ゲート判断は別の予定Stepとして残る。

## Findings

- 現行buildはrepo/。操作packetの識別値はd86d55d41027。D-021により旧指定sha照合は要件ではない。
- 56のBuild報告には通常ラン勝利時間30 FPS 86.967 s／60 FPS 103.533 s、保存ソース04fa2b1c168aの全suite152件OKがある。これらは独立QAの合格でも変更前同一性の証明でもない。
- 60のQA結果、62の計画、正本仕様と関連Decisionから、L1/O3を含む該当基準を特定すること。数値の意味、測定条件、精度を本文で確認してから比較可能性を判断する。
- ボスbotの非公開active残時間の参照について対応計画がある。対応前の比較値を新たな合格根拠にしない。製品戦闘の不具合や難度不合格と同一視しない。

## Decisions already made

- D-021：テキストビルドとStudio内の別Stepによる独立検証で進める。
- D-019：旧集計の適用関係と代替評価を定める。具体的内容は本文を参照する。
- D-022：V1補足を定める。具体的内容は本文を参照する。
- D-023：案Aを選択。変更前一致基準を記録数値との比較にするか確認不能として扱うかはDesignerが決める。

## Constraints

- 製品仕様、戦闘パラメータ、難度、秒数ゲートを供給不足だけを理由に変更しない。
- 記録数値との一致から、保存されていない変更前実装との厳密な同一性を主張しない。
- 確認不能は合格・免除・Goal達成と区別する。Goalの再解釈や範囲縮小が必要なら、権限を越えて決定せず手戻り理由を示す。
- Loadは個別ファイル本文が届く。ディレクトリ指定はファイル名だけ。追加本文は@need一度、最大8ファイルまで。
- @runはStepあたり最大3回。出力は先頭と末尾を含む最大2万字で、全文保存先も別実行枠もない。必要なら検証対象を絞った出力を使う。
- 実機、gamepad、外部配員、追加金銭、存在しない変更前ビルドを要求しない。
- 実装やQA判定は今回行わない。

## Open questions

- 変更前一致を要求する基準はどれか。それぞれどの記録を使えるか。
- 記録比較が成立するものの測定条件、精度、比較方法、証明できる範囲は何か。
- 確認不能の項目を、後続QAと最終Reviewへどう明示して渡すか。

## Expected output

重要な判断を新規Decisionに記録し、必要なら正本仕様の該当箇所を更新する。各基準について、従来要求、採用する扱い、根拠資料、比較条件と精度、未確認として残る点を表で示す。

結果Handoffはto: studioとする。Technical Directorが62をD-023へ適合させるために必要な仕様上の入力と、追加で必要な個別ファイル名を明示する。QAへ直接免除を依頼しない。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/60-qa-to-studio.md
- Project: goals/G-002-final-boss/62-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Previous handoff: goals/G-002-final-boss/63-studio-to-owner.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
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

<<<FILE design/final-boss-and-continuous-run.md
# G-002 最終ボスと連続ラン仕様

Status: Designと基準適用整理を確定。§11でV1補足3件（旧経路のボス表示、弾ID・消滅理由、長時間観測）を確定（D-022）。未実装・未検証。詳細契約はD-017、D-018に基づく旧基準の適用変更はD-019に記録する。

本書は新しい連続ラン、第5部屋、ラン境界・終端についての追加仕様。第1〜4部屋の構成、部屋内の既存敵・プレイヤー戦闘規則は既存仕様が正本である。G-002新構成への基準適用はD-019と本書§8が正本。過去G-001の判断・結果と既存Decision本文は変更しない。

## 1. 体験意図

道中で覚えた固定照準と回避を使い、ボスの次の攻撃を見て、避けた後にも攻撃できる場所を選ぶ。遠くへ逃げる安全と、近くに残って反撃する利益を区別し、通常敵との混戦とは異なる一対一の山場を作る。

## 2. ランと入場

通常ランは第1部屋から始まり、1→2→3→4→5の順に進む。第5部屋はボス1体のみ。通常敵、増援、第6部屋、ボス用チェックポイントはない。

各戦闘フレームの勝敗解決後、生存して全敵撃破なら第1〜4部屋は部屋クリアとなる。クリア表示を1.0秒間出してから次部屋へ自動遷移する。この間に戦闘は進まず、操作も受け付けない。次部屋の開始表示を出した後、次の戦闘フレームから動く。第5部屋の全敵撃破は部屋遷移を起こさず最終勝利となる。

通常ランの初期状態は第1部屋、3/3 hearts、位置(8,4)、右向き、停止。敵は各部屋の正規初期配置から始まる。

### 境界での継承

| 状態 | 第1〜4部屋クリア後の処理 |
|---|---|
| hearts | 生存者に1 heart回復、上限3。0から回復しない |
| 回復の時点 | 次部屋入場時に1回だけ。クリア表示中の再適用なし |
| 位置・向き | (8,4)、右向きへ戻す |
| 移動・ダッシュ | 停止。ダッシュ中なら終了させる |
| 攻撃回復、ダッシュ待ち時間 | 0へ戻す |
| hit-stun、被弾保護 | 0へ戻す |
| 予約攻撃 | 破棄 |
| 敵、予兆、弾、攻撃の接触消費状態 | 旧部屋分を破棄し、次部屋を新規開始 |
| 保持入力 | 破棄。実機入力では離して再入力するまで再発火させない |
| 反応ルールの定義・順序 | 同じラン内で継承 |
| 反応ルールの最終実行時刻、直前の盤面・メッセージ記憶 | 入場時に初期化。新部屋の表示から判断する |
| 未来の時刻指定入力 | ラン時刻に従い保持。境界中に期限が来た戦闘入力は破棄し、後からまとめて実行しない |

3 heartsでクリアすれば3、2なら3、1なら2で次へ進む。第4部屋も同じ扱いなのでボスには2または3 heartsで入る。消耗を完全には消さず、最低2回の被弾余地を確保する。部屋内回復、回復アイテム、任意回復は追加しない。

「3 hearts per room」は独立部屋試験の開始条件として保持する。通常ランの継承は本書の新契約であり、既存部屋内ルールの変更ではない。

## 3. ボス「洞窟の番人」

盤面印は`B`。初期位置(12,4)、HP12。プレイヤーへの接触そのものではダメージを与えず、攻撃の有効期間だけ危害がある。全フェーズで既存の正面スワイプが届けば1ダメージを受ける。装甲、無敵フェーズ、HPによる加速・形態変化はない。

攻撃は「突進」「短射」の2種類。順序は突進→短射→突進…で固定し、HPや距離で飛ばさない。初回入場時は突進を準備する。

各攻撃の前は接近状態となり、速度1.0 tile/sでプレイヤーへ歩く。距離2.0 tiles以下になったフレームで停止し、その攻撃の予兆を始める。予兆以降、回復終了まで追尾・再照準しない。回復終了後に次の攻撃の接近へ移る。距離0での照準は右(+x)に固定する。

### 攻撃定義

| 項目 | 突進 | 短射 |
|---|---|---|
| 予兆 | 0.7秒 | 0.8秒 |
| 照準 | 予兆開始時のプレイヤー位置への単位方向に固定 | 同左 |
| 予兆中の移動 | なし | なし |
| 発動 | 8.0 tiles/sで0.3秒、最大2.4 tiles移動 | 固定方向へ弾1個を発射 |
| 危険範囲 | 移動中のボス中心から半径0.6 tile | 弾中心から半径0.4 tile |
| 弾 | なし | 3.0 tiles/s、寿命1.0秒、最大移動3.0 tiles |
| ダメージ | 1 heart、1突進につき最大1回 | 1 heart、1弾につき最大1回 |
| 有効期間後 | 1.2秒の回復 | 発射から1.0秒の有効期間後、1.4秒の回復 |
| 回復中 | 停止、無害、スワイプ可能 | 同左。回復開始時には当該弾が存在しない |

短射は弾が早く消費されても発射から1.0秒待って回復へ入る。命中・吸収によって次の予兆が早まらない。寿命到達フレームは弾を失効させ、その弾の接触を新たに判定しない。

突進は部屋端でクランプするが、壁到達や接触によって有効期間・回復開始を早めない。通常命中、保護中接触とも突進の一撃を消費し、移動自体は継続する。

短射の弾は部屋端、寿命、最初の接触で消える。短射の有効期間にボス本体からの接触ダメージはない。ボスの弾は同時に最大1個であり、スピッターのcap／cue gap調停には参加しない。

### 中断と反撃

非致死スワイプはどのフェーズも中断・遅延・延長しない。HPは通常どおり減る。予兆中には`the boss takes the swipe; the warning continues`を出す。致死スワイプなら直ちに予兆と攻撃主体を失効させ、フレーム末の勝敗解決へ進む。

回復中は接触しても無害で、プレイヤーの攻撃回復0.35秒は変更しない。回復開始から届く位置にいれば、突進回復では時刻0、0.35、0.70、1.05秒の4回、短射回復では少なくとも同じ4回の攻撃開始が可能。これは理論上の機会数で、実測の撃破時間ではない。

突進には横移動またはダッシュ、短射には射線からの横移動、ダッシュ吸収、射程外への退避が使える。後退だけで避けた場合は回復中に距離を戻す必要がある。横へ避けて近くに残れば反撃しやすい。2種類とも予兆中の連打で止められない。

### 共有戦闘との関係

攻撃1ダメージ、射程1.5 tiles、回復0.35秒、ダッシュ4 tiles／0.25秒・待ち時間0.6秒、ダッシュ中の予約攻撃、被弾stun0.3秒・被弾後0.8秒までの保護は保持する。

D-005の結果規則をボスにも明示適用する。保護中の弾接触は弾消費、保護中の突進接触はその突進の一撃消費。保護終了後に持ち越しダメージを起こさない。

接触は移動後のフレームごとの距離判定、`distance <= reach`とする。本仕様は、既存と同じ速度・接触半径の突進と弾に限り、D-002／D-003と同じ帯を明示採択する。

- 弾：横ずれ0.39以下は命中、0.40超は非命中。
- 突進：横ずれ0.57以下は命中、0.60超は非命中。
- その間は上端を含み、30/60 FPSで命中差を許容する。
- 許容は命中／消費の有無だけ。照準、フェーズ、表示、時間の違いを免責しない。
- 新形状・別速度への包括的な拡張ではない。帯外差または突進帯0.03 tile超の所見はDesignerへ戻す。

## 4. フレーム内勝敗と終端

同一戦闘フレームでは、受理済みのプレイヤー行動と、まだ有効な危害による結果を解決した後、次の優先順位で終端を一度だけ決定する。

1. heartsが0なら死亡。
2. 生存して第5部屋のボスHPが0なら最終勝利。
3. 生存して第1〜4部屋の全敵HPが0なら部屋クリア。
4. それ以外は戦闘継続。

同一フレームに致死スワイプと既発射弾による致死被弾が成立した場合は死亡。スワイプで攻撃主体を倒したなら、その主体から新しい突進接触や発射は生じない。既発射弾はフレーム末の結果確定までは独立した危害として扱う。

部屋クリア・最終勝利・死亡の確定時に、残弾と予兆を全消去する。以後の表示時間中にダメージ、移動、予約攻撃、回復待ち時間、敵行動を進めない。死亡したまま次部屋へ進まず、勝利後の残弾死もない。確定後の勝敗変更と重複イベントは禁止する。

### 再挑戦

最終勝利・死亡の画面で`retry`を受け付ける。戦闘中と部屋クリア表示中のretryは無効。retryは終端メニュー操作であり、新しい戦闘入力ではない。

再挑戦は第1部屋、3 hearts、通常ラン初期状態へ戻る。ボスHP・順序、敵、弾、タイマー、予約・保持入力、勝敗、両ゲーム時刻、反応記憶を初期化する。FPSと反応ルール定義は同じセッション設定として保持する。旧試行の未来の時刻入力は破棄し、再挑戦の入力列を新試行用として明示して渡す。旧時刻入力を自動再生しない。

同一プロセス内のretryと、通常ランを新規起動した場合の初期戦闘状態は一致する。独立第5部屋試験の再実行は診断経路に留まり、通常ランのチェックポイントとして表示しない。

## 5. 時刻、入力、ポーズ、実行上限

- 部屋時刻は入場時0。戦闘中だけ進む。
- ラン時刻は第1部屋開始時0。戦闘と1.0秒の部屋間表示中に進む。ポーズ・死亡・勝利画面中は停止する。
- 各イベントは試行番号、部屋番号、ラン時刻、部屋時刻を区別して観測できること。
- 通常ランの時刻指定戦闘入力はラン時刻基準。独立部屋試験は部屋時刻基準。モードを冒頭に表示し、同じ入力列の基準を途中で変えない。
- 同じ時刻の入力は記載順。時刻入力を処理してから反応ルールを上から評価する。反応は既存のルールごとの0.15秒制限を保持する。
- 入場時刻と一致する時刻入力は、入場初期化と開始表示の後に受理する。クリア確定フレームでまだ受理していない戦闘入力を次部屋へ持ち越さない。
- ポーズは戦闘・部屋間表示を凍結する。時刻、フェーズ、弾、ダッシュ、保護、入力待ち時間、反応評価も進めない。
- ポーズ突入時に保持移動を解除する。予約済み攻撃は凍結して保持し、再開後のダッシュ終了時に通常どおり実行する。ポーズ中の戦闘入力は破棄する。
- 再開はゲーム時刻に依存しない制御操作で可能とする。スクリプト経路にも有限時間で再開を検証する手段が必要。具体構文はPlanで定め、停止したゲーム時刻にresumeを予約するだけの方式にはしない。
- 検証実行のlimit到達は`time limit — run unfinished`。勝利・死亡・部屋クリアと異なる終了理由とし、limitそのものを敗北にしない。
- limitと戦闘結果が同じ最終フレームなら、そのフレームの死亡／勝利／クリアを先に解決し、実行停止理由も別に記録する。

現行のpause、retry、連続モード、実機入力層、長時間player／trace経路は存在すると仮定しない。上記は新設要求である。Desktopキーボード／ゲームパッドの同等操作を要求として保持し、実装・検証経路と費用をPlanへ渡す。

## 6. player viewの情報契約

数値座標を内部確認専用にせず、テキストだけで危険を識別できること。

常設表示：

- `run — room n/5 — hearts h/3`と両ゲーム時刻。
- ボス部屋では`boss B — HP n/12 — <approach|warning|active|recovery>`。
- 次攻撃名は、その攻撃の接近開始時から`next: charge`または`next: short shot`として表示する。
- 既存のプレイヤー、敵、弾の印は保持し、ボスだけ`B`を追加する。

予兆開始時に即時描画し、全予兆中に`cue: B <charge|short shot> — locked <direction> — <seconds> left`を出す。

- 突進：固定した2.4-tile経路を`~`で示し、`danger: charge lane, radius 0.6 tile, rounded ends`を併記する。
- 短射：固定した3.0-tile射程を`~`で示し、`danger: one shot, contact radius 0.4 tile, range 3.0 tiles`を併記する。
- 文字セルの線は正確な連続座標の境界そのものではないことをmanualで説明する。方向と射程・接触幅の数値を省略しない。
- 発動で予兆線を外し、短射の実弾を`*`で描く。敵印と重なって隠れる弾も、活動中の弾数を表示して存在が消えたように見せない。

メッセージ：

| 契機 | 文字列 |
|---|---|
| 突進予兆 | `the boss prepares a charge` |
| 短射予兆 | `the boss aims a short shot` |
| 発動 | `the boss charges` / `the boss fires a short shot` |
| 回復開始 | `the boss is recovering — safe to approach and swipe` |
| 回復中 | `recovery: <seconds> left` |
| 回復終了 | `the boss resumes pursuit` |
| 突進被弾 | `YOU ARE HIT by the boss's charge`＋既存hearts suffix |
| 短射被弾 | 既存`YOU ARE HIT by a shot from the <direction>`＋suffix |
| 部屋クリア | `room n cleared — next room n+1` |
| 入場回復 | `recovered 1 heart`または`hearts already full` |
| 最終勝利 | `run won — boss defeated — retry: start from room 1` |
| 死亡 | `you went down — run lost — retry: start from room 1` |
| 再挑戦 | `new attempt — room 1/5` |

半秒ごとの定期表示に加え、予兆、発動、回復開始・終了、HP変化、被弾、部屋クリア、入場、勝敗、retry、pause／resumeで即時描画する。同時刻の複数変化は順序を保って1画面へまとめてよいが、メッセージを欠落させない。

既存敵の`rears back`、`takes aim`、`YOU ARE HIT by`のprefixとstep94の文言・方向規則を保持する。ボス予兆は既存敵の文字列に偽装しない。ボス対応の反応ルール／botsは、プレイヤーに見えるボス印・状態・攻撃名を根拠に追加する。

Art Directorによる限定Verifyを推奨する。対象はテキストの2攻撃の区別、予兆と実弾の区別、回復と次攻撃、重なり、勝敗・retryの識別。成果はplayer viewの具体的な読みにくさと文言・表示配置の修正案。グラフィカル素材制作や戦闘ルール決定は依頼しない。

## 7. 独立QAの受け入れ基準

以下を30 FPSと60 FPSで別々に判定する。時間許容は各実行の1フレーム以内、位置は仕様上の値とそのフレームの移動量を照合する。接触帯以外の結果差を、時間許容だけで免責しない。

player表示と同一ビルドの状態観測を対照する。試験用状態設定は独立した境界再現に使ってよいが、通常ランの連続到達の証拠にはしない。

| ID | 条件と合格条件 | 必要な観測 |
|---|---|---|
| R1 | 新規通常ランで1→2→3→4→5へ生存到達。各正規敵を実際に倒し、第5部屋はB1体だけ | 入場・撃破・クリア列、状態とplayer表示 |
| R2 | 第1〜4部屋の構成・配置・既存パラメータが元仕様と一致 | 部屋データと回帰試験 |
| R3 | 境界直前hearts1/2/3から次入場2/3/3。0なら死亡し遷移しない | 境界前後のhearts、回復イベント |
| R4 | ダッシュ、保護、予約攻撃、弾、保持移動、反応記憶を残した境界で、§2の各リセットが成立 | 境界前後全状態、次部屋最初の行動 |
| R5 | 部屋クリアから1.0秒後に次入場。表示中の戦闘入力は持ち越されず、入場同時刻入力は新部屋へ1回だけ適用 | 両時刻、入力処理列 |
| B1 | Bは(12,4)、HP12、攻撃順が突進→短射で反復。HP6以下でも変わらない | 初期状態、少なくとも各3回の予兆 |
| B2 | 予兆の途中にプレイヤーが移動しても照準不変。距離0では右。発動まで突進0.7秒／短射0.8秒 | cueと方向、発動時刻 |
| B3 | 開けた位置で突進2.4 tiles／0.3秒。壁ではクランプし、回復開始時刻は変化しない | 毎フレーム位置・フェーズ |
| B4 | 短射は1弾、速度3.0、寿命1.0秒。未接触・通常命中・吸収の各場合で回復開始は発射1.0秒後 | 発射、弾消滅理由、回復開始 |
| B5 | 開けた位置で、予兆開始から0.4秒以内に射線と直交して1 tile移動を完了すると各攻撃を無傷で避ける | 操作列、固定方向、hearts |
| B6 | 各攻撃へのダッシュ接触で無傷。ダッシュ終了後も同じ攻撃からダメージなし | 接触時の保護、消費、以後のhurt |
| B7 | 被弾保護が攻撃途中で切れる設定でも、既に接触した突進／弾から追加ダメージなし。次攻撃は通常命中 | 消費状態と各hurt |
| B8 | 非致死スワイプは全フェーズでHPだけ1減り、時刻・照準・状態不変。予兆中は継続文言。致死なら新発動なし | スワイプ前後状態と表示 |
| B9 | 回復中に接触しても無傷。開始から射程内・正面なら少なくとも4回の攻撃が成立。回復時間1.2／1.4秒 | 攻撃・HP・フェーズ時刻 |
| B10 | 接触帯の内側・外側・上端を各攻撃で確認。帯外は両FPSで同じ結果、帯内だけ許容差 | 実軌道の横ずれと接触距離 |
| T1 | 最後の敵撃破後に残弾を残す。クリア確定後は弾消去、追撃死なし、操作拒否 | 終端前後とその後2秒の状態 |
| T2 | ボス致死スワイプと既発射弾の致死接触を同フレームで成立させると死亡のみ。生存なら勝利のみ | 同フレーム結果、終端イベント数 |
| T3 | 勝利／死亡後に2秒分stepと戦闘入力を与えても戦闘状態・ゲーム時刻不変 | 終端状態比較 |
| T4 | 勝利と死亡の各々からretryし、初期状態が新規通常ランと一致。旧未来入力・予約攻撃・メッセージは再発しない | 試行番号、初期状態、入力列 |
| C1 | 部屋時刻は毎入場0、ラン時刻は連続。境界1秒はランだけ進む | 両時刻の列 |
| C2 | 予兆・ダッシュ・保護・部屋間表示の各途中でpause。外部経過2秒を挟んでも各残時間不変、再開後に通常継続 | pause前後とresume後状態 |
| C3 | 戦闘中のlimit到達はunfinishedで勝敗なし。勝利／死亡同フレームではその結果が記録される | 終了理由と勝敗の別字段 |
| V1 | §6の各表示がplayer viewだけで読め、変化フレームに出る。短射の予兆と実弾、回復終了を取り違える文字列なし | player出力と状態の照合 |
| V2 | キーボード／ゲームパッドで移動・攻撃・ダッシュ・pause・終端retryが同じ状態遷移を生む | 実機経路の同等操作記録 |

V2をheadless scriptのみで合格にしない。実機入力経路が未実装なら未検証／依存として明記する。

共有回帰はcombat.md基準1〜11、17〜21、step68のvariant文字列・runner kill解釈、step72 R3-1〜R3-10、step94 W1〜W8を対象にする。第5部屋固有部分と既存の既知ギャップは§8に従う。既存テストのgreenだけで新しい連続ランを合格にしない。

## 8. 旧基準とDecisionの対応

D-019で以下を確定する。「保持」は該当する独立部屋／共有挙動で保持する意味であり、通常ランのhearts合計へ置き換えない。「適用終了」はG-002新構成に限る。旧Decision本文と過去G-001の判断・結果は保存する。

| 出典・対象 | 扱い | 置換先・理由 |
|---|---|---|
| combat.md Rooms、12、test_rooms_match_the_spec | 第1〜4部屋保持、第5部屋置換 | 旧5番ブルート位置のassertをB(12,4)、HP12、1体の確認へ置換。R2／B1。単体ボスへの構成変更による |
| step72 R3-1の「rooms 1,2,4,5 unchanged」 | 第5部屋だけ適用終了 | 新5番はB1。他のR3-1〜R3-10と第1〜4部屋は保持 |
| combat.md1〜10、19〜21、D-001／D-004／D-005 | 保持 | 既存敵・プレイヤーの共有回帰。ボスの明示適用は§3、B5〜B9 |
| combat.md11／18、step46、CueGapTest | 第4部屋と共有試験保持、旧5番依存を置換 | 4番の初射・実部屋gap・強制同時射撃・cap遅延等を保持。5番の旧spitter試験はB2／B4へ。ボスはspitter gap調停に参加しない |
| D-002／D-003、combat.md17／16e | 保持＋ボスへ明示適用 | §3／B10。帯内の命中差だけを許容し、時刻・表示・フェーズは免責しない |
| D-006、step44の13a／13b | 新構成への適用終了 | walker独立3〜5合計3〜7 hearts、2/3 clear、構造上限7を新ボス・連続ランへ移さない。独立3・4の部屋別報告、ボス対処試験、独立Playへ接続 |
| step44の13c | 新構成への適用終了 | dodgerのwalker比1/2以下・3/3 clearを終了。母集団変更のため。新しい比率・clear数は未設定 |
| step44の13d | 新構成への適用終了 | camperのclear数がwalker未満という旧比較を終了。独立3・4の両者成績は引き続き報告 |
| step44の13e／13f、Reporting rule、Revisit、What QA re-verifies | 旧集計部分の適用終了 | 旧FPS別集計、旧逸脱報告・再計測手順、過去実測値を新構成のゲートにしない。両FPS別の新報告と下記再判断へ。過去記録は保持 |
| combat.md14、step44の14保持注記 | 保持 | 独立1〜2、各FPS別にwalker合計1以上、dodger合計1以下・両方clear。walkerのclear義務なし。brute対応方針も保持 |
| combat.md15、step44の15保持注記 | 独立3・4保持、5番置換 | 3・4は各FPSでdodger dash1回以上。0ならDesigner報告、使用を強制する変更はしない。5番は両攻撃の実接触を伴うB6で有効性を確認。B5と独立Playも保持 |
| combat.md16a／16b | 適用対象を更新 | 保持した共有基準と14／15を両FPSで確認。終了した13の旧集計を16b経由で復活させない。新仕様§7も両FPSで確認 |
| combat.md16c、BotsTest.test_dodger_agrees_at_30_and_60_fps | 独立1〜4保持、5番置換 | 新5番はボス対応dodgerで同じclear結果・hearts lost差1以下を採択。下記条件を必須とし、難度評価の代用にしない |
| combat.md16d／16e | 保持 | walker成績の一致は要求しない。bot時刻感度と規則違反を区別し、共有ルールの差は免責しない |
| BotsTest.test_walker_meets_criteria_13_and_14_at_each_rate | 一部保持・置換 | 旧13のwalker下限・clear数・dodger比率と3/3・camper比較を新構成から外す。14の1〜2 assert、15の3・4確認を保持。独立3・4報告と新5番比較・対処試験を追加する |
| その他BotsTest | 保持＋対応確認 | bot終了、ログ有無の結果一致、ログ観測、walker比較距離、brute wind-upへswipeしない試験を保持。新ボス対応とログの観測範囲を確認 |
| D-007、step46、SpitterTestのroom3 | 保持 | 一般上限は最大5。静止12秒最大3の試験だけでcap遅延の一般境界を合格にしない。player印＋直近spitによる観測法も保持 |
| step59→step68／D-011 | 保持 | step68が正本。runner通常HPはcancelではなくkill。variant文字列も保持 |
| step94、D-013／D-014 | 保持、一部経路置換 | 既存文字列・方向・prefixとW1〜W8を保持。W2の旧5番実spitter経路は4番とpracticeへ、新5番はボス短射の表示確認へ |
| D-013／D-014のG-001既知ギャップ・合格判断 | 保持 | 過去判断を変更せず、新機能への検証免除に拡張しない |
| 旧終端記述、manual、04の静的所見 | 新契約へ接続 | §4、T1〜T4。現行実装が満たすとの証拠ではない |

旧第5部屋fixtureの維持は必須ではない。使用するなら旧構成と明示した共有回帰に限り、新5番・連続ランの難度や合格を示すものにしない。テストの削除だけで完了とせず、上表の保持部分と置換先を追跡可能にする。具体的な試験構造はPlanに残す。

### ボスのFPS比較条件

同一ビルド、同一方針のボス対応dodger、同一初期位置・向き・戦闘状態、同一ゲーム時間limitで独立5番を30/60 FPS比較する。3 hearts開始と、連続ランで可能な2 hearts開始を別々に比較し、各対で同じclear結果・hearts lost差1以下を要求する。

対応botはplayer viewのB、攻撃名、固定方向・危険範囲、予兆、回復、実弾に基づき、反応間隔0.15秒で回避と反撃を選ぶ。未表示の将来状態を利用せず、非致死swipeで予兆を止める方針を使わない。両FPSで同一方針を使い、対応根拠と実際の判断ログをQAが確認する。独立1〜4の方針を変更する場合は影響を明示して回帰する。対応前の旧bot成績は比較の合格根拠にしない。

clear／death／unfinishedを区別する。一方のみunfinishedなら比較未完了として原因とlimitを再評価する。両方死亡またはunfinishedで数値が一致しても、攻略可能性の証拠にはしない。秒数差の追加閾値は設けず、各フェーズ時間はB1〜B10で検証する。

数値差は判断時刻・位置・照準・接触距離・消費・被弾のログで診断する。帯内接触差はB10の許容対象だが、比較閾値超過を自動免除しない。Designerへ戻して比較条件または基準の再判断を記録する。帯外の同条件差、時間・表示・フェーズの規則違反はQAの不合格対象とする。walker／camperには新たなFPS成績一致条件を置かない。

### 新評価への接続と実測後の判断

難度評価を未実施のまま基準整理だけで合格にしない。

- 独立3・4：各bot・各FPSで開始hearts、clear／death／unfinished、終了時heartsと損失、秒数、被弾源、攻撃・dash回数、limit、方針・ビルド識別を報告する。失敗や差があれば判断ログを添える。新しい合計数値ゲートは現時点で設けない。
- 独立5番：上記の3／2 hearts別FPS比較と、B1〜B10・V1で二攻撃の読み取り、横移動、dash、消費、反撃機会を確認する。独立Playで最終戦の体験を観察する。bot成績だけで手応えを合格にしない。
- 通常ラン：R1〜R5で正規敵を倒した連続到達、T1〜T4で終端とretry、C1〜C3で時刻・pause・limit、V2で実機入力を確認する。状態設定した境界試験は連続到達の代用にしない。
- 時間・到達体験：§9に従い同一試行のラン時刻、pauseを分けた実経過、部屋別時間、遷移、ボス入場hearts、被弾・反撃・再挑戦回数を記録する。完走と死亡・未完了を分け、試行数を明記する。独立部屋時間の合算は禁止する。

Planは、対応botと観測経路の整備後に両FPSの基線を測り、独立QA・独立Play後、Review前にDesignerへ返す経路を含める。初回基線で明白な対処不能や到達不能が見つかればPlay前にも返す。

Designerが実測後に判断する項目は、独立3・4のbot間比較に数値ゲートが必要か、新5番のhearts別clear・被害・反撃機会に追加ゲートが必要か、連続到達と回復・retry負担に調整が必要かである。報告された試行条件・件数と独立Playを根拠に、新Decisionと仕様更新、または追加不要の理由を記録する。今ここで成功率や秒数の閾値を推定しない。

Studioは未判断項目をReview前に再ルーティングし、適用整理完了と難度・体験の検証済みを区別する。15〜20分と整合しない場合は差と原因を報告し、HPや待機だけで合わせない。承認範囲内で解消できないVision不整合、承認超過の費用・リスク、Owner Decision変更はGame Directorへ戻す。独立QA、限定Art Verify、独立Play、Reviewは省略しない。Playtester資料に本節の期待結果や§9のReview用体験信号を転記しない。

### 仕様とテストの相違

- SpitterTestのroom3試験は、その静止プレイヤーの12秒実行で最大3をassertしている。D-007はcap遅延条件で最大5を許容する。特定入力で3以下という試験と一般上限5は必ずしも矛盾しないが、この試験だけではD-007の一般境界を検証できない。条件付きの確認として保持し、cap遅延の別試験を必要とする。
- BotsTestのコメントは旧上限6を説明し、上限assertを持たない。過去構成の正本はstep44／D-006の3〜7である。新構成での下限・clear数・関連比較の適用終了と置換先はD-019および上表で確定した。テスト実装の改訂は未実施。
- combat.mdの旧13の6という記載よりstep44が優先する。step72内の旧限界への言及も現行合否値ではない。
- D-007の11.7秒表記よりstep46のstep54補足が印刷画面による算定時刻を具体化する。旧Decision本文は編集しない。
- 04が指摘する残弾・終端のコード差は未実行。新契約を実装済みや現行不具合確認済みと扱わない。

## 9. 体験評価と時間

本Stepではplay／botsを実行していない。戦闘時間、連続到達率、実行成功、指定sha一致を示す数値はない。

HP12は既存スワイプ12回であり、理論上の4回反撃を3回成立させれば倒せる値として選ぶ。実際の反撃回数は接近と向き直しで減る。秒数の目標に合わせた値ではない。初期調整の判断は「2種類を学び、複数回の反撃へ戻れるか」で行い、秒数だけを理由に増やさない。

ボス単体の秒数ゲートは設けない。連続ラン15〜20分のVisionは保持し、実測が外れたら差を報告する。範囲内の調整で整合しない場合はGame Director経由でOwnerへ戻す。

計測は同一試行で第1部屋開始から勝敗確定までのラン時刻と、pauseを分けた実経過、各部屋時間、遷移時間、ボス初入場hearts、被弾・反撃回数、再挑戦回数を記録する。終端後表示時間は戦闘時間へ加えない。独立部屋bots時間の合算を連続ラン実測として扱わない。

Review用の体験信号。PlaytesterへのHandoffには転記しない。

- 予兆から、突進と短射のどちらかを説明できる。
- 回避後に攻撃する場所を選び、単に遠ざかり続ける以外の行動が見られる。
- 被弾理由を固定射線・突進・タイミングに結び付けられる。
- ボスを通常部屋とは異なる山場と述べ、同じ回答を長時間繰り返す戦闘と述べない。
- 道中の消耗と入場回復を理解し、ボスで試す余地があったと説明する。
- 死亡後に最初から戻ることと、再挑戦方法を迷わず認識できる。

これらが成立しない場合は読みやすさ→反撃位置と時間→継承・回復の順でDesignerへ戻す。攻撃追加や新フェーズは自動採択しない。

## 10. Planへ渡す依存

1. 指定sha `27fe16268ac8`との一致、実行対象、project.mdの0.4と他資料の0.6の差を同定する。
2. D-019と§8の確定した基準対応を試験計画へ反映する。旧集計の新構成への適用は終了した。独立3・4の両FPS別報告、ボス対応dodgerの条件確認・比較、実測後のDesigner再判断を計画へ含める。適用整理を難度検証済みと扱わない。
3. 単体敵の攻撃切替、進行、終端優先順位、入力・時刻・retryを実現・観測する方式と費用を評価する。
4. 現行60秒上限を超える連続player／traceと同一試行の計測経路を用意する。必要長は実行結果とVisionの双方から評価する。
5. pause／resume、終端retry、モードと時刻基準、再試行用入力列の具体的な公開構文を確定しmanualへ反映する。
6. ボス対応botsを試験道具として明示する。対応前の成績を難度判断へ使わない。
7. Desktop実機入力の現状・対応範囲・独立検証経路を提示する。headlessビルドで実機対応済みと扱わない。
8. player表示、重なり、イベント発火の実現性とArt Directorの限定Verifyを計画する。
9. 通常到達の長時間証拠と、同時勝敗等の制御された境界試験を両方可能にする。
10. 承認された案Aを超える費用・リスクがあればBuild前に具体的影響をStudioへ返す。

実装順序、コード構造、人日見積もりは本仕様では決めない。独立QA、独立Play、Reviewを省略しない。

## 11. V1補足の確定（D-022）

Engineer handoff 46の3件への回答。D-017の契約、第1〜4部屋、共有戦闘規則、入力、HP、時間は変更しない。以下はいずれも30 FPSと60 FPSで別々に判定する。

### 11.1 旧経路（run指令なしのスクリプト）のボス表示

**採択：現行のmanualの注記を受け入れる。** §6の完全な表示契約が適用される経路は公開ドライバ（`mode run`、`mode room`）である。旧経路は旧来の独立部屋診断として60秒上限と`Player.describe`を保持し、旧経路へボス部屋を公開ドライバへ委譲する変更はしない（旧60秒挙動を変えるためD-017／D-021の範囲外）。

ただし、旧経路で`room 5`を選んだ場合に、完全な表示と誤認させないため次を必須とする。

- player viewの先頭（最初の盤面描画の前）に1行だけ出す：`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`
- この行は表示のみ。ゲーム状態、イベント、時刻、結果、上限を変えない。旧経路の第1〜4部屋とtrace viewには追加しない。

受け入れ基準：
- L1：旧経路`room 5`の同一スクリプトを30／60 FPSで実行し、注記行を除く出力とゲーム結果・終了時刻が変更前と一致する。60秒上限も不変。
- L2：旧経路`room 1`〜`4`と`room empty`の出力に注記行が出ない。
- L3：同じ入力列に`mode room`と`room 5`を足すと、§6の常設表示とボスメッセージが出る（V1）。
- L4：manualの旧経路注記は上記の一致を保つ。

### 11.2 弾IDと消滅理由

**要求範囲：trace view（開発者状態）と公開ドライバのイベントログ。player viewには新しい文言を足さない。** 理由：ボスの弾は同時最大1個で、player viewは既に`*`、活動中の弾数、被弾・吸収の既存メッセージを持つ。IDの露出は読み取りの助けにならない。旧経路は対象外。

- ID：`S<n>`。試行ごとに`S1`から作成順で連番、再利用しない。retryで`S1`へ戻る。ボスの弾とスピッターの弾で同じ連番を共有する。
- 発射イベントに`id`と`source`（`boss`またはスピッター識別）を含める。
- 消滅は弾1個につきちょうど1回の`shot_removed`で、`id`、`source`、`reason`、ラン時刻、部屋時刻を持つ。`reason`は次の5種のみ：
  - `lifetime`：寿命到達
  - `edge`：部屋端
  - `hit`：ダメージを与えた接触
  - `absorbed`：ダッシュまたは被弾保護による接触消費（ダメージなし）
  - `cleared`：部屋クリア・勝利・死亡確定による全消去
- 既存の`lifetime`／`edge`ログに`hit`、`absorbed`、`cleared`を追加する。接触消費は現在ログされていないため追加が必要。
- 弾が消えたフレームに、その`id`は活動中の弾数から外れる。同一フレームの発射と消滅の順序を保つ。

受け入れ基準：
- S1：B4の短射を未接触、通常命中、ダッシュ吸収、保護中接触の各場合で実行し、各弾が発射1回・消滅1回、理由がそれぞれ`lifetime`（または`edge`）、`hit`、`absorbed`、`absorbed`である。
- S2：どの場合も回復開始は発射の1.0秒後（B4）で、消滅理由に依存しない。
- S3：終端確定時に残る弾は`cleared`で1回ずつ消え、その後に`hit`が出ない（T1）。
- S4：retry後の最初の弾は`S1`。旧試行の`shot_removed`は再発しない。
- S5：player viewの出力にID文字列（`S<n>`）が現れず、既存のメッセージ文言が変更されない（V1、step94の文言保持）。

### 11.3 長時間観測

**必要な出力形と量の上限：既存の既定を保ったまま、周期出力の間隔を指定でき、最後に要約を出す。**

- `view-every <seconds>`：player viewの周期描画間隔（既定0.5、許容0.5〜60）。イベント契機の描画（§6）は間引かない。
- `trace-every <seconds>`：trace viewの周期状態行（`trace-every frame`も従来どおり許容）。イベント行は常に出す。
- `trace-every frame`は出力量の上限を設けない。使用者の選択として許容する。
- 出力間隔の指定はゲーム結果・時刻・イベント列に影響しない。
- 実行の最後に1ブロックの要約を常に出す（player／trace共通）：終了理由（clear／death／unfinished）、試行数、各試行のラン時刻、各部屋の部屋時間、ボス初入場hearts、被弾数、攻撃数、ポーズ時間を除く経過とドライバ時間、processing_seconds。
- 出力量の上限：周期行は`ceil(limit / 間隔) + 1`行以下。それ以外の行はイベント数に比例するだけで、時間に比例する出力を増やさない。

受け入れ基準：
- O1：`limit 1200`、`view-every 10`、`trace-every 5`の通常ランで、player周期描画は121以下、trace周期行は241以下。
- O2：同じスクリプトで`view-every`を0.5、10に変えても、イベントメッセージの列と最終結果が一致する。
- O3：指定なしの出力は変更前と同じ（周期0.5秒）。
- O4：要約ブロックが、勝利・死亡・limit到達（unfinished）の各終了で1回ずつ出て、数値が状態観測と一致する。
- O5：範囲外（0.5未満、60超、数値以外）の指定は実行前に拒否し、理由を出す。
- O6：20分（`limit 1200`）の通常ランを30／60 FPSで実行でき、出力は途中で切れない。

具体的な構文は上記名称を既定とするが、manualへの反映はEngineerが行う。
>>>END

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 94 (wording only, no rule or number changed):** the hit message for a shot now names the side the shot came from (`YOU ARE HIT by a shot from the <direction>`), and a swipe that damages a grub already in its lunge shows `the <variant>'s lunge had already started, the swipe was too late to stop it`. Exact formats and acceptance criteria W1–W8 are in `design/combat-step94.md`, which governs these two messages.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

## G-002 applicability

D-019 and `design/final-boss-and-continuous-run.md` §8 govern application to the new room 5 and continuous run. Historical G-001 rulings and results below remain records of that configuration. Rooms 1–4 and shared combat rules remain in force. Independent room tests start with 3 hearts; continuous-run inheritance follows the G-002 specification.

For the new configuration, criterion 13's old rooms 3–5 aggregates and walker/dodger/camper comparisons cease to apply. Criterion 14 remains. Criterion 15 remains for independent rooms 3–4, including reporting zero dash use to the designer; new room 5 uses actual dash-contact checks for both boss attacks. Criterion 16c remains for independent rooms 1–4; boss-adapted dodger comparisons use the conditions in §8. Criterion 16b does not restore retired criterion 13 aggregates. The old room-5 contents and spitter-specific checks are replaced as mapped in §8. These changes establish applicability, not verified difficulty or experience.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 56
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 56: gameplay-engineer → studio — Split C delivery and independent-verification guide

## Task

Inspect the appended saved-source Build check before routing independent QA. Preserve the measurement evidence for subsequent limited Art Verify, fresh Play, Designer judgment and Game Director Review.

## Context

55 requested public-driver normal-run pause/retry measurements, retained independent dodger regressions and actual boss decision-log inspection. D-022 was previously executed at source `120ca2671495` with 149 tests.

## Findings

### Delivery and evidence provenance

Delivered `repo/tests/test_split_c.py`, README status updates and public-driver reproduction instructions. No combat, room data, bot policy, HP, input syntax or difficulty parameter changes are submitted. Player-observable behavior remains the approved D-017/D-022 behavior; this change adds engineering coverage and documentation.

The supplied run results contain two proposal executions:

- Round 1: source `187d2b2be59b`, 152 tests, one failure: the public replay's first attempt died rather than cleared. Its failed integration result is not completion evidence.
- Round 2: source `eff43c2d918c`, 152 tests, all successful in 2.886 seconds. The measurements below belong to that executed proposal.
- The final files written here are identified by the runtime's appended `## Build check`. Do not assign `eff43c2d918c` to these saved files without the appended source identification. The saved-source suite includes all three Split C tests and prints its actual source IDs and measurements. If that execution fails, return the concrete failure to engineering before QA.

### Reproduction

From `repo`, generate each FPS script separately:

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
python3 play.py --view trace run30.txt
python3 play.py --view player run60.txt
```

Both generated scripts support both views. Generation records the existing dodger's button presses through `_Proxy.press`; replay passes the resulting text through `play.read_script` and the public driver. No live bot, state injection, raised hearts or automatic enemy defeats occur during replay. The observer in the integration test reads paused state only.

Settings: build `0.6-g002-public-32`, dodger boss policy v1, reaction interval 0.15 seconds, ordinary initial position/facing and 3 hearts, game limit 1200 seconds per attempt, driver limit 141 seconds. Each FPS execution contains three attempts; reported trial count is one per FPS.

The first clear display pauses at driver time 7–9 seconds at 30 FPS or 10–12 at 60 FPS. Retry controls occur at driver times 120 and 140. Attempt 2 explicitly receives `0 stop`; attempt 3 receives `0 move up`, `0.1 stop`, `0.1 attack`. Attempt 1 also contains an old future `1100 dash left`.

### Public integration measurements

All times below are seconds, rounded to three decimals. Elapsed excludes pause but includes terminal waiting.

| FPS | Attempt | Outcome | Visited rooms | Run time | Driver time | Elapsed | Pause count/time | Terminal wait |
|---|---|---|---|---:|---:|---:|---|---:|
| 30 | 1 | clear | 1–5 | 86.967 | 120.000 | 118.000 | 1 / 2.000 | 31.033 |
| 60 | 1 | clear | 1–5 | 103.533 | 120.000 | 118.000 | 1 / 2.000 | 14.467 |
| 30 | 2 | death | 1 | 5.100 | 20.000 | 20.000 | 0 / 0 | 14.900 |
| 60 | 2 | death | 1 | 5.033 | 20.000 | 20.000 | 0 / 0 | 14.967 |
| 30 | 3 | unfinished | 1 | 1.000 | 1.000 | 1.000 | 0 / 0 | 0 |
| 60 | 3 | unfinished | 1 | 1.000 | 1.000 | 1.000 | 0 / 0 | 0 |

Execution ends at the driver limit, independently of the final unfinished combat outcome. Two retries occur per execution: victory→attempt 2 and death→attempt 3. Retry counts before attempts are 0, 1 and 2.

| FPS | Attempt-1 room times, rooms 1 / 2 / 3 / 4 / 5 | Transitions |
|---|---|---|
| 30 | 6.633 / 20.733 / 15.633 / 18.333 / 21.633 | four × 1.000 |
| 60 | 9.617 / 25.067 / 15.017 / 16.967 / 32.867 | four × 1.000 |

Attempt 1 at either FPS: first boss entry 3 hearts, zero hurts and no hurt sources, 41 successful attack starts, 12 boss hits. Dashes: 34 at 30 FPS and 45 at 60 FPS.

Attempt 2 at either FPS: three hurts, all source `grub`, hearts 2→1→0; zero attacks, boss hits or dashes; no boss entry or transitions. Room-1 time equals the attempt run time.

Attempt 3 at either FPS: zero hurts, one attack start, zero boss hits/dashes, no boss entry or transitions. It remains in room 1 with 3 hearts.

Total simulated driver duration is 141 seconds at each FPS. Measured processing time for the whole three-attempt execution was 0.129023 seconds at 30 FPS and 0.327988 seconds at 60 FPS. Per-attempt processing times are unavailable; these figures are headless processing, not human play time.

These are same-attempt session clocks, not sums of independent-room measurements.

### Pause, retry and input evidence

During the finite two-second pause, every sampled tuple of run time, room time, combat frame, clear-display frame count and session state is identical. The state is `room_clear`. All four transition durations remain exactly one run second; paused driver time does not enter either game clock.

After each retry, the observed entry is room 1, run time 0, room time 0 and 3 hearts. Subsequent attempt-specific inputs execute. No dash event occurs in attempts 2 or 3.

The `1100 dash left` sentinel is beyond this integration run's subsequent attempt durations; its nonappearance alone is not a complete pending-input-discard proof. `DriverDiscardTest.test_old_future_timed_input_is_discarded_on_retry` supplies the complementary controlled public-parser check. Fresh complete combat-state equality from both terminal outcomes is covered by session and boss-contract tests. Warning, protection, dash/queued-attack and boundary freeze cases remain in their dedicated contract tests.

### Retained independent rooms 1–4

One trial per room/FPS, ordinary 3 hearts, limit 60 seconds, unchanged dodger. Every result is clear with end hearts 3, loss 0 and no hurt sources.

| FPS | Room | Seconds | Attacks | Dashes |
|---|---|---:|---:|---:|
| 30 | 1 | 6.63 | 6 | 3 |
| 30 | 2 | 20.73 | 8 | 10 |
| 30 | 3 | 15.63 | 8 | 6 |
| 30 | 4 | 18.33 | 7 | 7 |
| 60 | 1 | 9.62 | 6 | 5 |
| 60 | 2 | 25.07 | 8 | 14 |
| 60 | 3 | 15.02 | 8 | 6 |
| 60 | 4 | 16.97 | 7 | 8 |

The retained regression test fixes clear outcome, zero loss, attack and dash counts, and times at the historical one-decimal precision. It also retains D-019's separate cross-FPS requirement: same clear result and per-room hearts-lost difference at most one. Rooms 3 and 4 each use at least one dash.

All historical times/dashes from 40 match at its reported precision. This establishes a new executable regression reference; it does not establish exact unrounded historical identity or equality with the unavailable pre-boss bot policy. Existing criterion-14 walker/dodger coverage is retained. No retired rooms-3–5 aggregate gate is restored.

### Boss logs and FPS comparison

Independent room 5, limit 120 seconds, one trial for each FPS/start-hearts pair:

| FPS | Start hearts | Outcome | Seconds | Loss | Attacks | Dashes | Decision lines |
|---|---:|---|---:|---:|---:|---:|---:|
| 30 | 3 | clear | 21.63 | 0 | 12 | 8 | 145 |
| 30 | 2 | clear | 21.63 | 0 | 12 | 8 | 145 |
| 60 | 3 | clear | 32.87 | 0 | 12 | 12 | 220 |
| 60 | 2 | clear | 32.87 | 0 | 12 | 12 | 220 |

Each hearts-matched pair has the same clear outcome and zero loss difference. Actual log samples show:

- Both FPS: approach from (8,4) toward B at (12,4), then hold on the charge warning and dash up at 0.900 seconds.
- At that dash, player x is 9.866667 at 30 FPS and 9.800000 at 60 FPS; reported charge ETA is 0.39 versus 0.38 seconds.
- The first short-shot dodge is down at 3.166667 seconds at 30 FPS and up at 3.150000 seconds at 60 FPS. The respective player positions are (9.866667,3.6) and (9.8,3.6).
- Both logs show holding off the locked attack line and returning to face/swipe at 2.400 seconds. Shot positions and velocities appear after emission.

Complete logs can be reproduced with `python3 bots.py SCRIPT`, using:

```text
bots dodger
rooms 5
fps 30
hearts 3,2
limit 120
log on
```

Repeat with `fps 60`.

#### Sender assessment

Engineering assessment, to strip before independent QA/Play: source inspection supports the approved observable-information policy: the boss branches use displayed B position, phase, attack name, locked direction/countdown and visible projectiles. Logs support avoidance followed by return to attack; samples alone do not prove the absence of every hidden-state dependency.

The first short-shot escape already differs between FPS, alongside different sampled positions and decision times. Later paths therefore cannot be treated as identical-input geometry probes. The measured historical boss difference remains approximately 11.24 seconds and four dashes; no new timing threshold is proposed and no contact-band explanation is asserted. Dedicated phase/contact contract tests, rather than bot duration, establish mechanics.

Round 2's successful proposal evidence supports completion, but only the appended saved-source check establishes this delivery's execution result. The earlier failed replay is explicitly preserved above; its precise cause is not established by the supplied results.

Normal bot completion remains 86.967/103.533 seconds, approximately 1.5–1.7 minutes, substantially below the 15–20-minute Vision. Pause and terminal waiting must not inflate combat duration. No HP increases, waiting or difficulty gates were added. Bot victory is neither difficulty acceptance nor evidence of the human experience.

### Independent QA acceptance and exercise guide

1. Run `python3 -m unittest discover -s tests` on saved sources and record the printed source ID. Independently generate and execute both public scripts in player and trace views.
2. Check R1/C1: actual regular-enemy defeats and entries 1→5, B alone in room 5, room clocks resetting, four one-second transitions, and first boss-entry hearts.
3. Check C2/T4: finite pause freezes both clocks and clear countdown; victory and natural death each accept retry into fresh room 1. Compare complete fresh state and exercise pending old inputs using the dedicated controlled discard test.
4. Check per-attempt summaries against event logs, including attack/boss-hit/dash/hurt counts, pause accounting, terminal waiting and final driver-limit outcome.
5. Independently exercise retained criteria 14/15/16c and boss comparisons at 3 and 2 starting hearts. Inspect full boss decision logs against visible information. Use B1–B10/T1–T4/C1–C3 and D-022 tests as reproducible controlled fixtures, not normal reachability substitutes.
6. Check V1 in player output and D-022 lifecycle/observation behavior against trace. V2 real keyboard/gamepad operation remains unverified under D-021.

No independent QA, Art Verify, Play or experience verdict is claimed. No engineering implementation work remains conditional on a green appended Build check; a saved-source failure must be corrected before routing.

## Decisions already made

- D-017: boss, progression, terminal priority, pause/retry and clocks.
- D-019: retained independent regressions, FPS comparisons and later Designer judgment.
- D-021: Studio text/script execution; no real-device provision or extra expenditure.
- D-022: public observation controls, summaries and shot lifecycle metadata.

## Constraints

Preserve rooms 1–4, shared combat and existing independent-room bot policy. Keep both FPS separate. Do not substitute controlled fixtures or independent-room time sums for normal reachability. Do not force duration with HP or waiting. No purchases or outsourcing. Strip engineering assessment and design-side experience expectations before Play routing.

## Open questions

None requiring specification clarification. Saved-source execution status is supplied by the appended Build check.

## Expected output

Studio checks the appended full-suite result and executed source ID. If green, route independent QA with the exercise guide and saved files, followed by limited Art Verify and fresh Play. Route the measurements and independent findings to Designer for D-019 judgment before Game Director Review, preserving the Vision-duration discrepancy. If the saved-source check fails, return the failure to gameplay-engineer.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.0 s).

```text
2-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.33148257399443537, "source_id": "04fa2b1c168a"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "04fa2b1c168a", "trial_count_per_room_fps": 1}
........................................................................................................................................................
----------------------------------------------------------------------
Ran 152 tests in 2.903s

OK
```

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/session.py
- Project: repo/game.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_boss_contract_details.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Project: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/54-gameplay-engineer-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/55-studio-to-gameplay-engineer.md
>>>END

<<<FILE goals/G-002-final-boss/60-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 60
from: qa
to: studio
stage: Verify
outcome: fail
---
# 60: qa → studio — ソース照合の追加所見と独立検証の供給不足

## Task

不足しているテスト本文・省略されていないログ・追加実行枠を供給し、独立QAを継続する。ボスbotの観測情報条件について、以下のソース所見を確認して検証経路を整理する。

## Context

59の依頼に従い、packet内の仕様、保存ソース本文、今回の収録実行結果を独立に照合した。実装者の自己評価は根拠にしていない。

今回も実行枠は0回である。Loadに指定されたrepo/tests/の本文はpacketに含まれていない。追加実行、ファイルからのsource_id再算出、完全ログの保存は実施できていない。収録結果の再評価だけで独立検証完了とはしない。

## Findings

### 総合判定

**fail：全基準の独立検証は未完了。加えて、ボスbotの条件付きFPS比較にはソース上の不適合所見がある。**

152 tests成功は今回の収録でも確認できる。ただしテスト本文がないため、条件・操作・assertを基準へ対応付けられない。未確認項目をsuite成功でpassにしていない。

### 識別と証拠の所在

- 保存ソース本文のBUILD：`0.6-g002-public-32`。
- 今回の全収録出力のsource_id：`04fa2b1c168a`。
- 保存ファイルからの独立ハッシュ再算出：未実施。本文と収録出力が同一ソース集合であることは未確定。
- 完全ログ：packetには供給されていない。Round 2 traceとRound 3 botsは明示的に中段が切断されている。

使用した実行証拠は今回の`@run-results`である。

| 参照 | コマンド・入力 | 観測範囲 |
|---|---|---|
| Round 1 tests | `python3 -m unittest discover -s tests` | 152 tests、Exit 0、2.886秒。本文・個別assertなし |
| Round 2 boss-zero-30/60 | `python3 play.py --view trace SCRIPT` | 両FPS。距離0開始、直交移動、driver時刻0.4〜2.4のpause。中段省略 |
| Round 3 retained-and-boss-30/60 | `python3 bots.py SCRIPT` | camper/walker/dodger、rooms 1-5、limit 120、hearts 3,2、log on。中段省略 |
| Round 3 boss-zero-player-60 | `python3 play.py --view player SCRIPT` | 60 FPSの上記距離0診断、view-every 10。表示全文あり |

入力列は各参照のScript欄にある。今回新たに実行したコマンドはない。

### 追加所見：D-019のボスbot観測条件

`repo/bots.py::_dangers`のactive charge分岐は、次の内部値を使う。

```python
e.phase_left * LUNGE_SPEED + 0.6
```

これを危険経路の残長として`_threat`へ渡し、`ahead > length`なら危険候補から外す。したがって、この値は単なるログではなく、回避・停止・その後の行動選択に影響する。

一方、`repo/run_driver.py::Output.emit`のplayer viewは、active中の残時間を表示していない。残時間を表示するのはwarningとrecoveryだけである。botも、表示済み発動時刻を記憶して残時間を算出する経路ではなく、内部`phase_left`を直接読む。

D-019項目6および仕様§8の「player viewで読める情報」「未表示の将来状態を使わない」という比較条件に対し、この判断経路は適合を確認できない。**現状のボスbot比較を条件付きpassにはできない。** 全判断経路を見たとの主張もできないが、この分岐だけで公開情報限定の条件には具体的な問題が残る。

これはゲーム戦闘結果の再現済み不具合とは区別する。対応は試験道具の情報取得経路を整理し、両FPS・開始hearts 3/2を再測定すること。秒数や難度の調整要求ではない。

また、`_hurt_lines`はboss被弾をshot側の診断分岐へ送り、収録にも`source boss`と`shot position not found (fired in this frame)`が併記される。被弾イベントのsourceは読めるが、この補助文から突進の接触位置を証明できない。

### ソースから確認できた事項

- `game.py::ROOMS`の第1〜4部屋は保持仕様の構成・位置・順序と一致する。第5部屋はboss (12,4)だけ。GRUBSと共有定数も提示仕様の値と一致する。
- 境界は`session.py::_enter`で新しいGameを生成する。heartsは入場時に`min(3, old_hearts + 1)`となる。反応記憶の初期化は`run_driver.py::drive`のgeneration変更時に実装されている。
- 同フレームの結果判定は`Game.step`で敵、既発射弾、結果の順。`_resolve_result`は死亡優先で残弾と照準を消す。
- retry時のpending破棄処理は`drive`に存在する。ただし処理の存在と、要求された独立実行証拠は別である。
- D-022の旧room 5注記はlegacy playerだけに置かれ、manualも一致する。
- 公開driverのinterval検証、shot ID採番、消滅理由、summaryの実装経路は読める。ただし全条件の実行確認は未完了。

### 基準別・FPS別判定

「未確認」は部分証拠があっても基準全体を合格にできない場合を含む。

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| R1 | 未確認 | 未確認 | SPLIT_C_PUBLICは通常入力再生の完走を支持。正規敵全撃破・全入場を両viewで対照する完全ログがない |
| R2 | pass（静的） | pass（静的） | ROOMS、GRUBS、共有定数を仕様と照合。FPSによるデータ分岐なし。挙動回帰の判定は下段に分離 |
| R3 | 未確認 | 未確認 | 1/2/3/0 heartsの境界実行なし |
| R4 | 未確認 | 未確認 | 新Game生成と反応初期化は確認。残存全状態を置いた境界前後assertなし |
| R5 | 未確認 | 未確認 | 構造化結果の遷移は各1秒。境界入力破棄・入場同時刻1回適用の独立証拠なし |
| B1 | 未確認 | 未確認 | 初期値・固定交互順はソースにある。各3回・低HPを満たす観測なし |
| B2 | 未確認 | 未確認 | 距離0 charge右固定と移動後の固定方向は収録で確認。short shot距離0など全条件は不足 |
| B3 | 未確認 | 未確認 | ソースは速度8、active 0.3、壁クランプ。毎フレーム位置・壁比較が不足 |
| B4 | 未確認 | 未確認 | 発射速度3・寿命1の実装。60 FPS playerは発射3.633→回復4.633を確認。全消費条件不足 |
| B5 | 未確認 | 未確認 | chargeの直交回避は部分確認。30 FPSは量子化で1.0667 tiles、60 FPSは1 tile。両攻撃の指定条件は不足 |
| B6 | 未確認 | 未確認 | botのdash件数は接触消費の証明にならない |
| B7 | 未確認 | 未確認 | 保護終了を攻撃途中に置く条件と次攻撃の通常命中が未観測 |
| B8 | 未確認 | 未確認 | 全フェーズのswipe前後比較・致死時新発動なしの実行不足 |
| B9 | 未確認 | 未確認 | 60 FPS playerで回復1.2/1.4秒。開始から4回攻撃のassertなし |
| B10 | 未確認 | 未確認 | 帯内外・上端の実軌道と接触距離なし |
| T1 | 未確認 | 未確認 | 残弾を持つ終端とその後2秒比較なし |
| T2 | 未確認 | 未確認 | 同フレーム致死swipe＋致死既発射弾のfixtureなし |
| T3 | 未確認 | 未確認 | 終端待機の集計はあるが、入力を伴う全状態比較なし |
| T4 | 未確認 | 未確認 | 勝利／死亡retry集計あり。完全初期状態比較・旧入力時刻を越える生存試験なし |
| C1 | 未確認 | 未確認 | 同一試行の時間集計は整合。全入場時刻0の完全列なし |
| C2 | 未確認 | 未確認 | warning中pauseは部分確認。dash・保護・clear表示等の全対象比較不足 |
| C3 | 未確認 | 未確認 | driver-limitとoutcomeの分離は観測。game limit同フレーム優先fixture不足 |
| V1 | 未確認 | 未確認 | 60 FPS診断表示は二攻撃・HP・回復・実弾数を確認。通常run終端・retryを含む両FPS対照不足 |
| V2 | 対象外 | 対象外 | D-021の今回範囲。実機対応済みとは判定しない |

Round 2の距離0 chargeは、30 FPSでwarning 0.033333、60 FPSで0.016667、aim (1,0)。60 FPS playerでは発動0.716667、回復1.016667、追跡再開2.216667を確認する。charge回避後にshort shotで被弾しており、試行全体の無傷を示さない。

### D-019保持回帰とbot測定

| 対象 | 30 FPS | 60 FPS | 判定 |
|---|---|---|---|
| combat14 walker側 | room 1で損失3 | room 1で損失3 | 損失下限1は既に充足。ただし独立1〜2の全成績表は省略部分にあり供給不足 |
| combat14 dodger側 | rooms 1/2 clear、損失0/0 | rooms 1/2 clear、損失0/0 | 収録数値上pass |
| combat15 rooms 3/4 | dash 6/7 | dash 6/8 | 収録数値上pass |
| combat16c rooms 1〜4 | 全clear、損失0 | 全clear、損失0 | 収録数値上pass |
| 新boss比較、開始3/2 | 両方clear、損失0 | 両方clear、損失0 | 数値条件は充足。観測情報条件は上記所見によりfail |
| 共有combat1〜11、17〜21 | 未確認 | 未確認 | 個別テスト本文・assert対応なし |
| step68保持部分 | 未確認 | 未確認 | 文字列定義はソース一致。全実行・旧出力比較不足 |
| step72 R3-1〜10保持部分 | 未確認 | 未確認 | R3-1の配置は静的一致。他の条件・assert不足 |
| step94 W1〜8保持部分 | 未確認 | 未確認 | 方向算出・文言はソース一致。W1〜6全ケース・旧出力比較不足 |

独立3/4のcamperは、開始3 hearts、limit 120、同一初期位置・向き。

| FPS・部屋 | 結果 | 終了hearts／損失 | 秒 | 被弾源 | 攻撃／dash |
|---|---|---|---:|---|---|
| 30・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 30・4 | death | 0／3 | 6.73 | shot 3 | 1／0 |
| 60・3 | death | 0／3 | 6.30 | shot 3 | 0／0 |
| 60・4 | death | 0／3 | 6.75 | shot 3 | 1／0 |

独立3/4のwalker成績と判断ログ全文は今回も省略されている。数値を推定しない。camperの行動分岐はソースで読めるが、判断文言をnoteへ記録していないため、実行ログには主に被弾・stunが残る。

cap遅延の一般上限5は、通常静止試験の最大3やsuite greenからは合格にできない。旧第5部屋依存の試験がどこで置換されたかも、tests本文なしでは追跡できない。

### D-022

| 基準 | 30 FPS | 60 FPS | 根拠・不足 |
|---|---|---|---|
| L1 | 未確認 | 未確認 | 注記以外の変更前出力一致・60秒上限実行比較なし |
| L2 | 未確認 | 未確認 | ソースの表示条件は一致。各旧部屋出力未収録 |
| L3 | 未確認 | 未確認 | 指定された同一入力のmode room＋room 5比較なし |
| L4 | pass（文書） | pass（文書） | manualと旧経路注記条件が一致 |
| S1 | 未確認 | 未確認 | 正常命中の発射／消滅抜粋あり。未接触・dash・保護の全列不足 |
| S2 | 未確認 | 未確認 | hit時の1秒維持は部分確認。他の理由不足 |
| S3 | 未確認 | 未確認 | 残弾終端のcleared全列なし |
| S4 | 未確認 | 未確認 | retry後S1と旧removed再発なしの列なし |
| S5 | 未確認 | 未確認 | 60 FPS player診断にID露出なし。全条件・両FPS不足 |
| O1 | 未確認 | 未確認 | 収録カウンタは121/241で上限内。数え方を含むテスト本文なし |
| O2 | 未確認 | 未確認 | 間隔0.5/10のイベント・結果比較なし |
| O3 | 未確認 | 未確認 | 既定実装値は確認。変更前出力比較なし |
| O4 | 未確認 | 未確認 | deathと構造化3 attemptsのsummaryは整合。全終了条件の状態対照不足 |
| O5 | 未確認 | 未確認 | parserの範囲検証は確認。拒否実行出力なし |
| O6 | 未確認 | 未確認 | suiteは1200秒完了を報告。全出力とテスト本文がなく切断なしを独立確認できない |

### 同一試行の時間と後続判断

通常入力再生attempt 1の収録値は次のとおり。独立部屋の時間合算ではない。

| 項目 | 30 FPS | 60 FPS |
|---|---:|---:|
| ラン時刻 | 86.966667秒 | 103.533333秒 |
| 部屋1/2/3/4/5 | 6.633333 / 20.733333 / 15.633333 / 18.333333 / 21.633333秒 | 9.616667 / 25.066667 / 15.016667 / 16.966667 / 32.866667秒 |
| 遷移 | 4回、各1秒 | 4回、各1秒 |
| pause | 2秒 | 2秒 |
| driver経過 | 120秒 | 120秒 |
| 終端待機 | 31.033333秒 | 14.466667秒 |
| boss入場hearts／hurt | 3／0 | 3／0 |
| 攻撃／boss命中／dash | 41／12／34 | 41／12／45 |

部屋時間＋遷移はラン時刻、ラン時刻＋pause＋終端待機はdriver経過に一致する。retryは勝利後と死亡後の2回。attempt 2は自然死亡、attempt 3はunfinishedである。

15〜20分Visionとの差はDesignerへ保持する。人間の体験時間と同一視せず、新たな秒数ゲートは設けない。

### 具体的な供給不足

59が要求する追加実行に対して、packetは最初から0 roundsである。また以下が欠けている。

1. `repo/tests/*.py`全本文。個別テストの条件・assert・対応IDを読むために必要。
2. Round 2/3の省略されていないログと、公開連続入力再生の両FPS・両view完全出力。
3. 保存ソース識別を独立算出し、不足fixtureと公開再生を実行できる枠。
4. L1/O3等の変更前比較に使える基線出力、または比較可能な保存ソース。
5. 完全ログと検証入力を永続参照できる供給経路。今回の許可書込先はhandoff一件だけである。

これは実機ホストやgamepad供給の要求ではない。明確な基準未定義を示す所見もない。今回をpartialとしない理由は、継続に必要な入力・実行枠が具体的に欠けているためである。

## Decisions already made

- D-017：二攻撃、境界、終端、pause・retry・時刻の契約を保持。
- D-019：旧集計を終了し、保持回帰・条件付きbot比較・実測後Designer判断を要求。
- D-021：今回の対象はテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。

## Constraints

- 製品コード・仕様は変更していない。
- 未確認をpassにしない。静的確認、収録実行、fixture、生成入力再生、bot、独立Playを区別する。
- ボスbotの比較条件の所見を、戦闘難度やゲーム本体の再現済み不具合へ拡張しない。
- 新たな難度・秒数ゲートを置かない。
- QA結果・期待値・Review用体験信号を独立Play資料へ転記しない。

## Open questions

1. tests本文、完全ログ、追加実行枠を次の独立QAへ供給できるか。
2. ボスbotのactive残時間参照を、公開情報だけに基づく試験道具としてどう扱うか。整理後の両FPS・hearts 3/2再測定が必要。
3. 変更前一致を要求するL1/O3等について、比較基線を供給できるか。

## Expected output

Studioは供給不足を解消して独立QAを再ルートする。ボスbot所見は試験道具の担当へ渡し、公開情報限定条件を満たす具体的な経路と再測定証拠を用意する。

次のQAは保存source_idを独立算出し、tests本文のassertを基準に対応付け、不足条件を両FPSで実行する。旧未来入力破棄は新attemptが旧入力時刻を越える条件、または破棄列の直接観測で証明する。

全基準合格後に限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewへ進める。本Stepでは合格ルートへ進めない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/tests/*.py（次Stepでは本文を必ず供給）
- Project: 今回の@run-results、および省略のないログ・入力・基線比較資料
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/59-studio-to-qa.md
>>>END

<<<FILE goals/G-002-final-boss/62-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 62
from: technical-director
to: studio
stage: Route
outcome: question
---
# 62: technical-director → studio — 検証供給の復旧と試験道具対応の計画

## Task

下記のOwner宛Escalation案を提示し、検証資料・実行・完全証拠の供給条件を調整する。回答後は供給確認、Engineerの試験道具対応、再測定、独立QAの順で進める。

## Context

58・60は独立検証未完了を報告し、59で要求した入力・実行・完全ログの供給が60でも不足した。同じ資料だけで第三のQAを開かない。

D-021によるテキスト・スクリプト方式とStudio内検証の承認は維持する。今回必要なのは承認の取り直しではなく、その実行経路と証拠参照を利用可能にする調整である。

## Findings

### このStepで確認した範囲

packetのソース本文・テスト4ファイル・仕様・報告を静的に照合した。製品コード、bot、仕様は変更していない。tests・traceは実行しておらず、保存ファイルからのsource_id再算出、保存基線の探索、完全ログの永続化も未実施である。

本packetではtests・traceに最大3 roundsが明示され、以前不足していたテスト本文の一部も供給された。この改善を60の「0枠」の継続と混同しない。一方、次のQAにも実行枠が付くこと、全tests本文、完全ログの保存先・再閲覧手段、変更前基線の存在は確認できない。以前0枠になった生成・配布機構の根本原因はpacketからは特定できない。

収録出力のsource_id `04fa2b1c168a`とBUILD `0.6-g002-public-32`は60の報告値であり、現在の保存repo/と一致するとの独立確認ではない。

### 技術所見

1. `bots.py::_dangers`のactive chargeは内部`phase_left`から危険経路残長を計算し、`_threat`の候補除外へ使う。`Output.emit`のplayer viewにはactive残時間がない。表示済み情報を記憶・計算する経路も当該分岐にはないため、D-019項目6の公開情報条件に不適合な判断依存がある。現状のボス比較値をpass根拠にはしない。
2. `_hurt_lines`はsourceがbossの場合もshot側へ入り、突進接触の位置・距離・消費を証明できない。被弾源イベントと補助文を分けて扱う。
3. `test_split_c.py`はボス判断ログ全文を結果に残さず、サンプルへ縮約する。完全ログの別保存が必要である。同ファイルの公開再生入力は現在のbotから生成されるため、bot修正後は入力生成と通常ラン測定も更新対象になる。
4. `test_legacy_note_only_changes_leading_line`は同じ現行実装の注記抑制との比較である。`test_default_player_cadence_is_explicit_half_second`も現行の既定値と明示値の比較であり、いずれも変更前基線との一致を単独では証明しない。
5. 長時間試験はheartsを変更した観測用fixtureである。長時間出力の検証と、正規敵を倒した通常連続到達の証拠を分離する。

これらは試験道具・証拠の問題であり、ゲーム本体の戦闘不具合、対処不能、難度不合格を意味しない。

### 影響システムと順序

並列Stepは開かない。試験道具の変更が入力生成・測定・証拠識別へ連鎖するため、次の順序で固定する。

1. **Studio／Owner：供給条件の確認。** 次の担当Stepに全必要本文、独立実行枠、入力・完全出力を書ける許可先、後続packetから参照可能な経路を具体的に割り当てる。Loadへのパス記載だけで本文供給済みと扱わない。全件を一packetへ収められなければ、依存を明記した直列分割にする。
2. **Engineer：証拠台帳と基線調査。** 使用ソース集合を保存し、`source_id.py`の対象全ファイルとtestsを列挙して識別する。変更前保存ソース・出力が供給された場合は由来、入力、FPS、比較可能範囲を確認する。存在しなければL1/O3等を未確認としてStudioへ返す。要件変更の要否はDesignerへ、Goal範囲の判断はGame Director経由でOwnerへ戻す。
3. **Engineer：ボス判断経路の限定。** ボス判断用に公開情報だけの観測データを作り、判断処理へ内部Game／Enemyを渡さない。warningの固定方向・範囲と、発動時の公開イベントから観測済みの経路を保持し、active中はその全経路を保守的に危険候補とする。内部残時間による残長短縮は使わない。recovery等の公開状態変化で解除する。warningを観測せずactiveから開始する診断では、現在の公開情報から固定最大範囲を保守的に扱い、履歴不足を記録する。プレイヤー表示の追加は不要とする。公開契約変更が必要と判明した場合だけDesignerへ返す。
4. **Engineer：診断ログと試験。** 意思決定入力・計算根拠・候補・選択行動を全判断について記録する。接触診断は判断用データから分離し、boss突進のフレーム前後位置、固定方向、距離、保護、接触消費、被弾を記録する。既存イベントで不足する場合は試験用観測で補い、推定値を実接触値と表記しない。
5. **Engineer：再測定。** 同一保存ソース・同一方針・初期位置／向き／状態・limitで、独立5番を30/60 FPS、開始3/2 heartsの4条件で実行する。全判断ログ、終了理由、hearts、被弾源、攻撃・dash、時間を保存する。数値が閾値を超えた場合は診断後Designerへ返し、自動免除しない。
6. **Engineer：保持回帰と公開再生。** 独立1〜4は既存方針を保持する。共有関数に変更が及べば変更前後の行動列・結果と全保持基準を確認する。独立1〜2のcombat14、3・4の各bot成績・dash、独立1〜4のFPS比較、終了・ログ有無一致・brute対応を追跡する。新botで通常ラン入力を再生成し、両FPS・両viewの公開再生と同一試行時間を再取得する。
7. **独立QA：基準ごとの検証。** 実装者の自己評価を根拠にせず、保存識別を再算出し、全testsの条件・assert・基準IDを照合する。不足fixture、公開再生、共有回帰、D-022を両FPSで独立実行する。
8. **全QA合格後：** 限定Art Verify→独立Play→Designer実測後判断→Game Director Review。Artの表示変更があれば該当QAを再確認してからPlayへ進む。初回再測定で明白な対処不能・到達不能が判明した場合はPlay前にもDesignerへ戻す。

### 試験と証拠保存

Engineerが通常Roleの成果として作るもの：

- 基準ID／FPS→ソース・テスト名・条件・assert・入力・完全ログ参照の対応表。
- 公開情報が同じで内部active残時間だけ異なる場合に、ボス判断が変わらない試験。公開データに存在しない属性を読めない境界も確認する。
- warning→active→recovery、距離0、壁、dash待ち、stun、room境界・retryの判断記憶初期化を確認する試験。
- boss突進の通常被弾・保護接触・非接触で、診断がshotとして誤記されず、接触位置と消費を追えるログ。
- 新attemptが旧未来入力時刻を越える試験、またはpending破棄列の直接観測。
- 共有combat、step68／72／94、cap遅延上限、旧5番からの置換先の追跡表。

保存方式は供給側が許可する実パスを確定してから使用する。実行ごとに、完全入力、コマンド、作業ディレクトリ、FPS、開始条件、limit、ソース識別、終了コード、stdout／stderr全文を保存する。台帳にはファイルのハッシュ・バイト数・行数と分割順を記録し、summaryや抜粋だけで全文を代用しない。

大きい出力は完全原本を保持して連番分割し、後続Stepへ必要部分を全文供給する。ハッシュは同一性確認に使い、閲覧可能性の代用にはしない。保存・再読込みの小規模確認に成功するまで、長大な再測定を始めない。

### リスクと対策

- 保守的な危険経路保持でbot成績・反撃機会が変わる：実測を更新し、ゲームのHP・時間・表示をbotに合わせて変えない。
- 共有判断処理への影響：ボス専用境界を優先し、独立1〜4の変更範囲と回帰結果を明記する。
- source_idはtests変更でも変わる：測定前にソースを固定し、異なる識別の結果を混ぜない。
- 完全ログの再切断：原本保存と再閲覧を先に確認し、収録不能なら直列分割して未確認を残す。
- 変更前資料の不在：現行greenや同一コード内比較で埋めず、該当基準を未確認として判断先へ返す。
- 約87／104秒という既報と15〜20分Visionの差：人間の所要時間と同一視せず、再測定と独立Play後にDesignerへ渡す。新たな秒数ゲートを設けない。

### 独立QAの再開条件

次の全項目をStudioが確認してから、60の未確認表を添えて再開する。

- 全必要ソース・全tests・仕様本文が実際に閲覧できる。
- QA自身が必要な追加実行を行える枠とコマンドが割り当てられている。
- 入力・完全ログの書込先と後続参照経路が確認されている。
- ボス公開情報対応と4条件の再測定資料が揃い、独立1〜4への影響が追跡できる。
- 変更前比較資料が供給されているか、不在と判断待ちの基準が明示されている。

基線不在でも他項目の検証は進められるが、L1/O3等を含む全基準passは保留する。枠を使い切り、入力・機能の不足なく残作業だけがある場合は、完了条件を示して直列の継続Stepへ渡す。

### Owner宛Escalation案（Studio Routeで提示する）

---
kind: escalation
goal: G-002
seq: 62
from: technical-director
to: owner
status: open
decision: none
---

# 62: Owner decision needed — 承認済み検証の供給をどう整えるか

#### Question

G-002について、承認済みのテキスト方式を維持して全資料・独立実行枠・完全ログの保存参照経路を調整する案A、検証可能な範囲へGoalを狭める案B、供給が整うまで停止する案Cのどれを選びますか。

#### Why this needs the Owner

58・60で同じ供給不足が二度報告されたことが、再び同じQA依頼を出さずEscalationする手続上の理由です。修正後に同じ受入基準が二度失敗した事例ではありません。

Roleが解消できない具体的な障害は、担当Stepに付与される実行枠、packetへの全必要本文の収録、許可書込先、完全ログを後続Stepへ届ける参照経路を、このTechnical Director Stepから設定できないことです。以前のQAでは実行枠0、tests本文不足、ログ切断が報告されました。今回のStepには最大3 roundsと一部tests本文があり改善していますが、次のQAで必要機能が揃うとの確認はありません。0枠の根本原因と保存基線の所在も不明です。

D-021が再検討条件とする「通常のStudio Stepでは実行できない具体的な障害」に関する調整です。bot修正、試験作成、基準対応表、ログ生成は通常Roleの仕事として計画済みであり、Ownerへ技術方式の選択は求めません。実機、gamepad、外部配員、追加金銭、旧指定sha照合も求めません。

#### Options

**案A — D-021を維持して供給条件を整える（推奨）**

全必要ソース・tests本文、担当Step内の追加実行枠、完全入力・stdout／stderrを書ける場所、後続Stepが全文を参照できる経路を調整します。一度に収まらなければ直列Stepに分割します。L1/O3等の変更前保存ソース・出力は、所在と提供可否を回答対象に含めます。

失う検証範囲は予定しません。ただし基線がなければ該当基準は未確認として残り、別途判断が必要です。費用は通常Step内で、追加金銭は使いません。リスクは供給機構の制約が残ることで、実現性はまだ確認できていません。計画・資料分割は変更可能です。

選択後：Studioが供給担当・具体的経路・利用可能な枠を確定し、小規模な保存／再閲覧確認→Engineerの試験道具対応→再測定→独立QAへ進みます。

**案B — 今回のGoalを検証できる範囲へ狭める**

利用可能な本文、実行枠、保存参照経路を明示したうえで、Game DirectorとDesignerが検証可能な成果へGoal・該当基準を再定義します。最低限、残す成果の入力と証拠を保存・再閲覧できる供給が必要です。

変更前基線が得られなければL1/O3等の変更前一致を、独立実行・全証拠が得られなければ該当する全基準検証と体験判断を、今回の完了範囲から外す可能性があります。具体的な除外一覧は再計画で確定します。従来G-002全体の合格は主張できません。通常Step内で調整できますが、後日の再検証と判断のやり直しがリスクです。未検証の記録を保持すれば範囲の再拡大は可能です。

選択後：Studio→Game Director→Designerによる範囲・Decision整理→Technical Director再計画。QAへ基準免除を直接依頼しません。

**案C — 供給が整うまで停止する**

新たな実行・保存機能の即時供給は求めず、現状の資料と未確認一覧を維持します。今回失うのは残りの検証を進める機会で、基準自体は維持します。追加金銭は不要ですが、Goal達成時期は未定となります。供給再開条件を満たせば再開可能です。

選択後：StudioがOwner待ちとして停止を管理し、資料・実行・保存参照経路が確認できた時点でTechnical Directorへ戻します。

#### Studio recommendation

案Aを推奨します。D-021の承認を維持し、ゲーム仕様やGoalを狭める前に、承認済みの検証経路を実際に供給できるか確認するためです。これはTechnical Directorの提案であり、Ownerの決定済み事項ではありません。

#### Reasoning

今回のpacketには実行枠と一部tests本文があり、供給改善の兆候があります。しかし次のQAの枠、全文収録、永続参照は未確認なので、復旧可能とは断定しません。

供給機構が完全証拠の保存・再読込みや必要な独立実行を提供できないと確認された場合は、案BまたはCへ推奨を見直します。変更前基線だけが存在しない場合は、その基準に限定した再判断を先に検討します。

回答待ちの間に通常Roleが進められるのは、既供給本文に基づく基準対応表と試験道具修正briefの準備です。新規の並列Stepは開かず、第三のQA再依頼や合格後の工程へは進めません。

#### Owner decision required

A／B／Cと条件を回答してください。Aの場合は、全本文・実行枠・完全ログ保存参照経路を誰がどう調整するか、および変更前資料の提供可否を指定してください。現時点で不明な項目は、確認担当と確認方法の指定で構いません。

## Decisions already made

- D-019：公開情報限定のボスbot、開始3/2 hearts別FPS比較、独立1〜4保持回帰、実測後Designer判断を維持。
- D-021：テキスト・スクリプト方式とStudio内独立QA・Playを承認。実機供給・旧指定sha照合・追加金銭は要求しない。
- 仕様§11／D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- 本Stepは新Decisionを採択せず、上記の技術計画と未決Escalation案を返す。

## Constraints

- QAのfailと未確認を上書きしない。実行・保存・基線探索を実施済みと扱わない。
- 製品コード・bot・仕様は変更しない。後続Engineerで試験道具を対応する。
- プレイヤー向け契約変更はDesigner、Goal範囲変更はGame Director経由で判断する。
- 新たな難度・時間ゲートを設けず、変更前比較を現行suite成功で代用しない。
- QA用資料と独立Play資料を分ける。Playへ期待結果、QA判定、実装履歴、Review用体験信号を渡さない。
- Ownerへの実際の提示とGoalのblocked-on-ownerへの変更はStudio Routeが行う。

## Open questions

1. 次のEngineer・QA Stepへ全必要本文、実行枠、完全ログの保存参照経路を具体的に供給できるか。
2. 以前のQAで0枠・本文未収録・出力切断となった配布上の原因と、再発防止を確認する担当は誰か。
3. L1/O3等に比較可能な変更前ソース・完全出力は存在するか。不在なら該当基準の扱いをDesignerへどう戻すか。
4. Ownerは案A／B／Cのどれを選ぶか。

## Expected output

Studioは本Handoff内のEscalation案をOwnerへ提示し、供給障害に対する選択と条件を記録する。回答前に同じQA依頼を繰り返さない。

案Aなら具体的な供給確認を先に行い、本計画をEngineerの試験道具対応briefへ落とす。再測定と独立QAの再開条件を満たしてから検証を再ルートする。全QA合格後の限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewを保持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/escalation.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/61-studio-to-technical-director.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting report: goals/G-002-final-boss/58-qa-to-studio.md
- Supporting request: goals/G-002-final-boss/59-studio-to-qa.md
>>>END

<<<FILE decisions/D-019-g002-balance-criteria-applicability.md
---
kind: decision
id: D-019
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-019: G-002新構成における旧集計の適用終了と代替評価

## Decision

D-018の方向に基づき、D-006、正本step44、combat.mdの関連基準の適用を次のとおり変更する。本DecisionはG-002の新第5部屋と連続ランに限定した適用変更であり、D-006本文、過去G-001の判断・結果、旧構成に対する基準は変更しない。

1. 新構成には、step44基準13a〜dのwalker独立3〜5合計3〜7 hearts・2/3 clear、dodgerのwalker比1/2以下・3/3 clear、camperのwalker未満clearを適用しない。13eの旧集計に関するFPS別判定と、13fの過去実測値も新構成の合否根拠にしない。旧集計の逸脱に関する再判断条件は新構成へ移植しない。
2. 第1〜4部屋の構成、共有戦闘ルール、独立部屋の3 hearts開始を保持する。combat.md14の独立1〜2比較は30/60 FPSそれぞれで保持する。独立3・4はwalker／dodger／camperの部屋別・FPS別成績を報告し、新たな合計下限・上限・clear数・bot間比率を旧値から算出しない。
3. combat.md15は独立3・4で保持する。各FPSでdodgerのdash1回以上を確認し、0回ならDesignerへ報告する既存規則も保持する。使用を強制するためcapやgapを変更しない。新5番は使用回数条件を終了し、仕様B6の実接触による無傷・攻撃消費・終了後の追加被害なしを、突進と短射それぞれ、両FPSで検証する。B5の横移動も保持し、dash必須戦にはしない。
4. combat.md16cと対応BotsTestの独立1〜4のdodger比較は保持する。新5番にも「同じclear結果、hearts lost差1以下」を採択する。ただし下記の対応条件を満たすボス対応dodgerによる独立試験に限る。これはFPS比較であり、ボスの難度や到達可能性の合格基準ではない。
5. 新5番比較は、同一ビルド・同一bot方針・同一初期状態・同一ゲーム時間limitを使う。独立標準開始は3 heartsとし、連続ランで生じる2 hearts開始も別対として試験する。開始heartsを混ぜて比較しない。両FPSで終了理由をclear／death／unfinishedとして区別し、一方のみunfinishedの場合は比較を未完了として再調査する。両方unfinishedでも攻略の証拠にはならない。
6. ボス対応dodgerはplayer viewで読めるB、攻撃名、予兆の固定方向・範囲、回復、実弾を根拠に行動する。未表示の将来状態を使わず、非致死スワイプによる中断を前提にせず、回避後の反撃へ戻る。反応間隔0.15秒と方針を両FPSで共通にする。対応確認前の数値は診断資料に留め、比較をpassにしない。独立1〜4の既存方針は保持し、変更が必要なら影響と回帰を明示する。
7. FPS比較の不一致はログと制御入力で原因を分ける。帯内接触だけによる命中差にはD-017の許容を適用するが、bot比較の閾値を自動的に緩和しない。閾値超過はDesignerへ戻す。帯外の同条件差、フェーズ・表示・時間の不一致はQAが規則違反として扱う。walker／camperに新たな成績一致条件は設けず、bot時刻感度を共有規則の違反の免責にしない。
8. 旧第5部屋fixtureは必須にしない。残す場合は共有回帰専用と明示する。新評価は仕様B1〜B10・V1、通常ランR1〜R5・T1〜T4・C1〜C3・V2、独立Play、同一試行の連続ラン時間計測へ接続する。

追加の難度数値ゲートの要否は、対応botの両FPS成績とログ、独立QA、独立Play、連続到達・終端・時間の実測後にDesignerが判断する。StudioはReview前にその再判断を必ずルーティングする。追加不要の場合も理由を記録し、未判断のままGoal達成へ進めない。詳細は仕様§8による。

## Rationale

旧基準は旧第5部屋を含む独立3部屋と各3 hearts開始に依存する。単体ボスと回復付き連続ランでは、集計の母集団と開始条件が変わり、旧数値から難度を推定できない。

dashの価値は実接触に対する有効性と独立Playで評価できる。使用回数を強制すると、有効な横移動を不当に罰する。

ボス対応dodgerの数値比較はFPSによる大きな挙動差を検出する補助ゲートとして採る。両FPSで死亡する同一結果も通り得るため、攻略可能性や体験の代用にはしない。

## Alternatives considered

- 旧集計を新5番または連続ランへ継承する：開始条件と敵構成が異なるため不採択。
- 独立3・4へ比例配分した新数値を置く：実測上の根拠がないため不採択。
- 新5番でもdash1回以上を強制する：対処の有効性と使用頻度を混同するため不採択。
- ボスのFPS比較を設けない：共有規則試験だけでは対応botの戦闘全体の差を見落とすため不採択。
- 旧fixtureを必須維持する：新構成の難度証拠にならず、必須成果にはしない。

## Revisit when

対応botのFPS比較が閾値を超える、対処が有効でも反撃へ戻れない、道中で到達が妨げられる、回復やretryが学習を妨げる場合。

追加数値ゲートの判断に必要な実測が揃った場合。15〜20分との不整合を承認範囲内で解消できない場合、または承認を超える費用・リスクが判明した場合は、StudioからGame Directorへ戻す。

本Decisionは適用整理の完了を示す。実行成功、指定sha一致、難度、体験、所要時間の検証済みを示さない。
>>>END

<<<FILE decisions/D-021-owner-authorizes-text-build.md
---
kind: decision
id: D-021
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-20
supersedes: D-020
---
# D-021: テキストビルドとStudio内検証でBuildへ進む

## Decision

Ownerは22の案Aを選択し、供給・検証・予算の回答権限者をすべてOwnerとした。実機ホスト・実gamepad・外部配員を今回の開始条件から除き、既存のテキスト表示とスクリプト実行によるBuildを承認した。

Ownerの回答全文：

> 案A。回答の権限者はすべて Owner（私）で、ここで回答します。(1) 実行経路: project.md の build: と run_tests / run_play / run_trace / run_bots がそのまま実行経路です。gameplay-engineer と qa は Step の中で @run を使い、サンドボックスでテスト・プレイ・トレース・ボットを実行できます（G-001 と同じ）。基線は repo/ の現状で、指定 sha の確認は不要です。project.md の「build 0.4」は古い記述で、repo/ が正です。(2) 実機・gamepad・デスクトップの表示環境はなく、用意もしません。Constraints の「Desktop, keyboard and gamepad」は製品の対象環境で、今回の検証環境の要求ではありません。検証は G-001 と同じく、テキスト表示のビルドとスクリプト実行で行います。(3) 独立した QA と Play は、Studio の qa と playtester の Step が担います。外部の配員はありません。(4) 費用: 購入・外部委託・追加の金銭は一切ありません。予算は Studio の通常の Step の範囲で、人日の見積もりは不要です。以上で D-020 の条件は満たされたものとして、Build へ進んでください。

実行基線は作業開始時のrepo/とし、指定shaとの照合は要求しない。project.mdのbuild 0.4表記は基線の根拠にしない。購入・外部委託・追加金銭支出は認めない。人日見積もりや外部検証枠の取得を開始条件にしない。

D-020に代わる開始条件として本Decisionを適用する。D-020に由来する実機ホスト、実gamepad、外部配員、費用見積もり取得の要求は後続計画より本Decisionを優先する。D-015〜D-019のゲーム体験、共有戦闘回帰、30/60 FPS、実測後Designer判断は維持する。独立QA・限定Art Verify・独立PlayはStudio内の別Stepで行う。

これはOwnerによる開始許可と検証範囲の変更であり、実行成功、受け入れ基準合格、体験Goal達成の証拠ではない。

## Rationale

Owner自身から不足していた供給・実行経路・予算方針への回答があり、今回の検証をG-001と同じテキストビルド方式に限定した。Studioが同じ供給確認を繰り返す必要はなく、既存仕様・計画に基づくBuildへ進める。

## Alternatives considered

- 実機ホストと実gamepadを用意する：Ownerが用意しないと明示したため採らない。
- 見積もり・調達条件を取得する案B：追加金銭を使わず通常Step内で進めるため採らない。
- 条件整備まで停止する案C：OwnerがBuild開始を明示したため採らない。

## Revisit when

通常のStudio Stepでは実行できない具体的な障害、追加支出の必要性、またはテキスト方式では仕様の意味を定められない矛盾が判明したとき。製品の実機対応を検証する別のGoalを開始するとき。
>>>END

<<<FILE decisions/D-022-g002-v1-supplements.md
---
kind: decision
id: D-022
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-022: V1補足の確定（旧経路表示、弾ID・消滅理由、長時間観測）

## Decision

詳細は`design/final-boss-and-continuous-run.md`§11。D-017の契約、第1〜4部屋、共有戦闘規則は変更しない。

1. 旧経路のボス表示：現行manualの注記を受け入れる。§6の完全表示は公開ドライバの経路に適用し、旧経路を委譲しない（旧60秒挙動を保つ）。旧経路`room 5`のplayer viewだけに誤認防止の注記1行を先頭に出す。
2. 弾IDと消滅理由：trace viewと公開ドライバのイベントログに限り要求する。ID `S<n>`、消滅は弾1個につき1回、理由は`lifetime`／`edge`／`hit`／`absorbed`／`cleared`。player viewの文言は変更しない。
3. 長時間観測：`view-every`と`trace-every <seconds>`で周期出力の間隔を指定でき、既定は変更しない。終了時に要約を出す。周期出力の行数に上限を置く。間隔指定は結果に影響しない。

## Rationale

最小の変更でD-017とG-002の検証要求を満たす。旧経路を変えるとD-017／D-021で承認した範囲外の挙動変更になる。ボスの弾は最大1個で、player viewでは数と既存メッセージで足りるため、IDは検証用のtraceに限る。20分の実行では0.5秒周期の描画が大量になるため、間隔指定で量を制限する。

## Alternatives considered

- 旧経路にも完全なボス表示を出す：旧60秒挙動とPlayer.describeを変えるため不採択。
- 注記なしで現状維持：旧経路でボス部屋を見た利用者が表示の欠落を契約違反と誤認するため不採択。
- player viewにIDと消滅文言を出す：読み取りを増やさず、既存文言の保持（step94）を乱すため不採択。
- 長時間は`trace-every frame`のみ：20分では出力が膨大で検証に使えないため不採択。

## Revisit when

旧経路でボスを観測する利用が多く、注記では不足とわかった場合。独立QAでIDや消滅理由の不足が出た場合。20分実行で周期間隔の指定だけでは出力が扱えない場合。
>>>END

<<<FILE decisions/D-023-owner-confirms-verification-supply.md
---
kind: decision
id: D-023
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-023: 実際の供給上限に合わせてテキスト検証を継続する

## Decision

Ownerは63の案Aを選び、D-021を維持して進めると決定した。ただし、利用可能な供給は以下に限られる。

- Loadに個別指定したファイルは本文が届く。ディレクトリ指定では中のファイル名だけが届く。
- Stepは@needを一度、最大8ファイルまで使用できる。
- @runは1 Stepにつき最大3回。別の実行枠はない。
- 実行結果は先頭と末尾を含む最大2万字。全文保存先はない。長い出力は確認対象の行を出すスクリプトで絞る。
- 変更前ビルドは保存されていない。変更前一致の基準について、記録数値との比較にするか、確認不能として扱うかはGame Designerが決める。

案Aに記載された全文保存・再閲覧機構の新設は実行条件としない。利用可能な出力から何を検証できるかは各担当Roleが判断し、未確認を合格として扱わない。製品仕様、難度、秒数ゲート、Goal達成の判断を本Decisionで変更しない。

Ownerの原文：

> 案A。供給の事実を答えます。(1) 本文: Load に書いたファイルは本文が届きます。ディレクトリ（repo/ など）を書くと本文は届かず、中のファイル名だけが届きます。足りない本文は、Step が @need で 1 回、8 ファイルまで追加で求められます。Route は、検証に要るテストなどのファイルを 1 つずつ Load に書いてください。(2) 実行: 1 回の Step で @run を 3 回まで使えます。別の実行の枠はありません。(3) ログ: 実行結果は先頭と末尾を含む 2 万字までで、全文の保存先はありません。長い出力は、確かめたい行だけを出すスクリプトで絞ってください。(4) 変更前のビルドは保存されていません。変更前との一致を求める基準は、記録にある数値と比べるか、確かめられないものとして扱うかを Designer が決めてください。以上の範囲で、D-021 のまま進めてください。

## Rationale

Ownerが利用可能な供給条件を確定した。存在しない実行枠、保存機構、変更前ビルドを待つ反復を止め、本文の個別指定、出力の絞り込み、必要な直列分割で進める。変更前一致の扱いは、指定された仕様責任者の判断を先行させる。

## Alternatives considered

- 案BのGoal縮小：Ownerは選択していない。検証未完了を理由にStudioが範囲や基準を免除しない。
- 案Cの停止：Ownerは継続を指示した。
- 全文保存先や変更前ビルドの供給を再要求する：確定した供給事実と合わないため採らない。

## Revisit when

担当Roleが、出力の絞り込みや直列分割でも必要な判断を成立させられない具体的な理由を示した場合。または供給条件が変わった場合。変更前一致の個別基準の扱いは、まずGame Designerが判断する。
>>>END

<<<FILE goals/G-002-final-boss/63-studio-to-owner.md
---
kind: escalation
goal: G-002
seq: 63
from: studio
to: owner
status: resolved
decision: D-023
---
# 63: Owner decision needed — 承認済み検証の供給をどう整えるか

## Question

承認済みのテキスト方式で検証供給を整える案A、Goalを検証可能な範囲へ狭める案B、供給が整うまで停止する案Cのどれを選びますか。

## Why this needs the Owner

58・60で同じ検証入力・実行・完全ログの不足が二度報告されたため、Studioの反復制限に従い、第三の同じQA依頼を出さずOwnerへ戻します。製品の同じ受入基準が修正後に二度失敗した事例ではありません。

Technical Directorが62で準備したbriefに基づく提示です。Roleからは、後続Stepの実行枠、packetへの全必要本文収録、許可書込先、完全ログを後続Stepへ届ける経路を設定できません。このRouteでも供給条件は確定していません。

62のStepには最大3 roundsと一部tests本文が供給され、以前から改善しています。ただし、後続QAでも必要な機能が揃うこと、完全証拠の保存・再閲覧、変更前基線の所在は未確認です。

D-021の承認を取り直す依頼ではありません。実機、gamepad、外部配員、追加金銭、旧指定sha照合も求めません。bot修正、試験作成、証拠台帳、再測定は通常Roleの仕事として計画済みです。

## Options

### Option A — D-021を維持して供給条件を整える（推奨）

全必要ソース・tests・仕様本文、担当Stepの独立実行枠、完全入力・stdout／stderrの保存先、後続Stepから全文を閲覧できる経路を調整します。一度に収まらなければ、依存を明記した直列Stepへ分割します。変更前保存ソース・出力の所在と提供可否も確認します。

検証範囲は維持します。通常Step内で進め、追加金銭は使いません。供給機構が必要な機能を提供できるかは未確認で、調整・分割は変更可能です。変更前基線が存在しない場合は該当基準を未確認として残し、別途判断へ戻します。

If chosen: Studioが調整担当・経路・実行枠を確認し、小規模な保存／再閲覧確認→Engineerの証拠台帳・基線調査→公開情報だけを使うボス判断と診断ログの修正→30/60 FPS・開始3/2 heartsの再測定と保持回帰→独立QAへ進みます。全QA合格後、限定Art Verify→独立Play→Designer実測後判断→Game Director Reviewとします。

### Option B — 今回のGoalを検証可能な範囲へ狭める

利用できる資料・実行・保存参照の条件を明示し、Game DirectorとDesignerが成果と基準を再整理します。残す範囲にも、入力と証拠を保存・再閲覧できる供給が必要です。

変更前基線がなければL1/O3等の変更前一致を、独立実行・完全証拠が得られなければ該当検証や体験判断を、今回の完了範囲から外す可能性があります。具体的な除外一覧は後続判断で確定し、従来のG-002全体の合格は主張しません。通常Step内で調整しますが、後日の再検証が必要になる可能性があります。未確認記録を保持し、範囲の再拡大は可能です。

If chosen: Game Director→Designerで範囲・基準・Decisionを整理し、Technical Directorが再計画します。QAへ直接基準免除を依頼しません。

### Option C — 供給が整うまで停止する

現在の資料と未確認一覧を維持し、新たな供給の即時調整を求めず停止します。基準は維持し、追加金銭は不要です。達成時期は未定となりますが、供給確認後に再開できます。

If chosen: Studioが停止と再開条件を記録し、資料・実行・完全ログ保存参照経路が確認できた時点でTechnical Directorへ戻します。

## Studio recommendation

案Aを推奨します。D-021の承認を維持し、Goalを狭める前に承認済みの検証経路を供給できるか確認するためです。

## Reasoning

62では供給改善が報告されており、復旧を検討する根拠があります。ただし、実行・保存・再閲覧や基線探索は行われておらず、復旧可能とは断定しません。必要な機能を提供できないと確認された場合は、案BまたはCへ推奨を見直します。変更前基線だけが不在なら、その基準に限定した再判断を先に検討します。

ボスbotが非公開のactive残時間を判断に使う所見は、62の技術計画に従って対応します。現状の比較値を合格根拠にせず、再測定します。これはゲーム本体の戦闘不具合や難度不合格の判断ではありません。新しい難度・秒数ゲートも設けません。

技術計画と再開条件の詳細は、goals/G-002-final-boss/62-technical-director-to-studio.mdに保持しています。

## Meanwhile

新規Stepは開きません。第三のQA依頼、限定Art Verify、独立Play、実測後Designer判断、Reviewは回答待ちです。

## Owner decision required

A／B／Cと条件を回答してください。

Aの場合は、全本文・実行枠・完全ログ保存参照経路を誰がどう調整するか、および変更前資料の提供可否を指定してください。不明な項目は、確認担当と確認方法の指定で構いません。回答後のResumeでOwner Decisionを記録して再ルートします。

---

**Owner response (2026-10-23):** 案A。供給の事実を答えます。(1) 本文: Load に書いたファイルは本文が届きます。ディレクトリ（repo/ など）を書くと本文は届かず、中のファイル名だけが届きます。足りない本文は、Step が @need で 1 回、8 ファイルまで追加で求められます。Route は、検証に要るテストなどのファイルを 1 つずつ Load に書いてください。(2) 実行: 1 回の Step で @run を 3 回まで使えます。別の実行の枠はありません。(3) ログ: 実行結果は先頭と末尾を含む 2 万字までで、全文の保存先はありません。長い出力は、確かめたい行だけを出すスクリプトで絞ってください。(4) 変更前のビルドは保存されていません。変更前との一致を求める基準は、記録にある数値と比べるか、確かめられないものとして扱うかを Designer が決めてください。以上の範囲で、D-021 のまま進めてください。
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

- Write the outgoing Handoff as goals/G-002-final-boss/65-game-designer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
