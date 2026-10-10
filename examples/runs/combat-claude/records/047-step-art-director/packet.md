# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/39-studio-to-art-director.md
next_seq: 40

## You may write

- goals/G-001-combat-monotony/40-art-director-to-<recipient>.md
- design/<name>
- decisions/D-010-<name>.md

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

<<<FILE goals/G-001-combat-monotony/39-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 39
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 39: studio → art-director — 模擬ビルド 0.6 の視覚レビュー(突進の予告の見た目)

## Task

`design/grub-charge-telegraph.md`(視覚仕様、D-006)に対して、模擬ビルド `sim/build-0.6.md` が書いている「プレイヤーに見えるもの」を、`visual-review` で確認する。仕様の視覚的な受け入れ基準(A 系)ごとに pass / fail / 確認不能を判定し、読みやすさと美術方針との一貫性を見る。

## Context

G-001(戦闘の単調さの改善)の Verify の視覚側。Build は、部屋の構成と進行(波)を主軸に、予告つきの Grub 突進を足す変更だった(D-002、D-003)。`qa` は規則と数値を `sim/build-0.6.md` に対して確認し、全基準 pass(模擬)だった。見た目の A 系基準は `qa` の範囲外で、今回あなたが担当する。

Owner の判断(D-008): このプロジェクトは模擬専用で、`sim/build-*.md` は変更内容の記述からシミュレーターが作った文章である。実際の画素や実時間の見え方は確認できない。判定はすべて「模擬ビルドの記述に基づく」と明記すること。

## Findings

客観的な事実だけを渡す。

- 対象は `sim/build-0.6.md`(プレイヤーが見聞きするものの記述)。最新版。
- 視覚仕様と D-006 は Load で指定する。内容はここで要約しない。仕様本文を正とする。
- `qa` の報告によれば、ビルド 0.6 の記述に「新しい音」「新しいボタン」はない。点滅は「1 秒間に 3 回を超えない(単発を除く)」と書かれている。
- 美術方針(`project.md#art-direction`): 暗い洞窟をプレイヤーのランタンが照らす。暖かい光と冷たい青黒の対比。脅威は彩度の高い橙〜赤で、暗がりの中で読めること。
- 実装の説明や自己評価は、この Handoff に含めていない。

## Decisions already made

- D-006: 突進の予告は「地面のレーン + 熾火の点灯 + 沈み込み」で示し、赤橙は害になる状態だけに使う。
- D-001: ワンボタン戦闘(新しい入力ボタンなし)。
- D-008: 判定は模擬ビルドに基づく。

## Constraints

- 戦闘の規則・数値・タイミングは変更しない。変えたい点があれば、変更せずに指摘として返す。
- 判定は模擬ビルドの記述に基づく。実機でしか確かめられない点(暗い床での読み取りやすさ、0.7 秒の予告で足りるか、実際の色の見え)は、「確認不能(実機要)」として分けて書く。記述から推測して pass にしない。
- 仕様の文面が曖昧、または不足している場合は、`art-director` の権限内で決められることは決めて D-NNN に記録する。それ以外(規則の変更を要するもの)は `outcome: question` で返す。

## Open questions

- 視覚仕様の各基準がビルドの記述に現れているか。現れていない基準は、ビルド記述の欠落か仕様側の問題かを分けて報告する。
- 赤橙が「害になる状態だけ」に使われているか(予告中・回復中・出現中の表示を含む)。
- 暗い床の上で、レーンと熾火が他の要素(Spitter の弾、他の脅威の表示)と混同されない記述になっているか。

## Expected output

- `visual-review` の報告を Findings に書く。基準ごとに引用つきで、pass / fail / 確認不能(実機要)を示す。
- `outcome` は pass / fail / question のいずれか。fail の場合は、ビルドの記述が仕様と違う点を具体的に書く(Build に戻す)。
- 宛先は `studio`(次の Play の Handoff を、実装の履歴なしで Studio が組むため)。自己評価は Sender assessment にだけ書く。
- 判定は模擬ビルドの記述に基づく旨を、Context か Constraints に明記する。

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction、design/grub-charge-telegraph.md、design/combat.md(§10 のみ)、sim/build-0.6.md
- Decisions: decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-001-one-button-combat.md
- Previous handoff: none
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
>>>END

<<<FILE design/grub-charge-telegraph.md
# Grub 突進の予告の見た目(視覚仕様、暫定)

状態: G-001 / Handoff 11 に基づく art-director の視覚仕様。色、割合、長さの新しい値はすべて暫定値(P)。実機(ゲームパッド、小さい画面、30/60 FPS)での読み取りは Play で確認するまで未確認。
戦闘の規則と数値(予告 0.7 s、突進 8.0 タイル/s・7.0 タイル、Recovery 0.8 s、出現中 0.8 s、接触の定義、怯みの規則)は `design/combat.md` と D-003〜D-005 のとおりで、この文書は変えない。決定の記録は D-006。

## 1. 意図

突進型 Grub は、「止まって、体を沈め、熾火(おきび)が灯り、足元に赤橙の帯が伸びる」ことで、害の前に突進を知らせる。帯が突進の方向と通る範囲そのものを示すので、プレイヤーは「その線から出る」か「当たる直前にダッシュで抜ける」を選べる。突進の後は、熾火が消えて沈んだ体で隙を読ませる。予告は色だけに頼らず、形(帯と矢印)・動き(沈み込み)・明るさ(熾火と帯の強さ)の組み合わせで伝える。

## 2. 共通ルール

- 見た目のタイミングはすべて、状態の経過時間の割合(経過 s / 状態の長さ)から求める。フレーム数や更新回数に結び付けない。30 FPS と 60 FPS で同じ長さに見える。これは §10 の「長さは時間で決まる」条件を満たすためである。
- 見た目の変形(拡大縮小、ずれ)は描画だけに適用する。判定の大きさと位置は変えない。
- 敵が攻撃を受けたことは、白い被弾フラッシュ(§8)だけで示す。怯みの動き(のけぞり、縮み、位置のずれ)を予告や状態の表示に使わない。
- 点滅は 1 秒に 3 回以下にする。単発のフラッシュは可。
- 脅威色(赤橙)は、「これから害になる、またはいま害になる」ことだけに使う。無害な状態(出現中、Recovery)には使わない。
- 色の指定(暫定値、P):
  - 脅威の赤橙: #FF5A1F
  - 熱い核: #FFE3B0
  - 熾火の待機色(消灯時の突進型の目印): #6B2A1A
  - Recovery の沈んだ色: 通常色に乗算 #7C8AA0 + 彩度 −40%
  - 出現中の淡い青: #8FB8E8
  - 被弾フラッシュ: #FFFFFF
  - 抜けた合図: #CFE8FF
  - 既存の Spitter の弾の色、ランタンの色との差は未確認。T0 で確認し、近ければ値だけを変える(形で区別する設計は変えない)。

## 3. 突進型の目印(常時)

- 突進型 Grub は、通常型と同じスプライトに、背中の「熾火の尾根」(暗い赤茶 #6B2A1A、点灯していない炭のような見た目)を重ねて区別する。出現中から常に見える。
- 尾根は暗い色にとどめ、通常の歩行中は脅威の赤橙を使わない。これは Windup の点灯との対比を最大にするためである。
- 尾根が「何を意味するか」は、部屋 2 で突進を見て学ぶ。目印を最初から見せることで、部屋 4、5 でどの Grub が突進するかを先に読める。
- 通常型の見た目は変えない。

## 4. 出現中(Spawning、0.8 s)

- 突進型でも通常型でも、体は半透明(不透明度 40%→100% に、時間で線形に上がる)で、足元に淡い青(#8FB8E8)の輪が出る。赤橙は使わない。
- 出現中は動かず、攻撃も通らない。Recovery(不透明、蒸気あり、§7)と、半透明と青い輪で見分ける。
- 突進型の尾根は出現中も見えるが、点灯しない。

## 5. Windup(予告、0.7 s)— 主役

### 5.1 突進の線(レーン)

- Windup の開始の最初の描画で、Grub の中心から固定した方向へ、地面に帯(レーン)を出す。方向はレーンの向きで示す。
- 長さ: 7.0 タイル、または壁まで(短い方)。壁の手前で切る。
- 幅: Grub の既存の接触判定が通る範囲と一致させる(±0.1 タイル)。実際の判定より広く描かない(広く描くと「当たらないのに避けた」になり、窓の読みを狂わせる)。
- 見た目: 赤橙(#FF5A1F)の半透明の塗りと、1 本の明るい縁取り(幅 0.06 タイル)、1 タイルおきに突進方向を指す矢印(シェブロン)。シェブロンは Windup 中は動かさない(動くと突進が始まったと誤読されるため)。
- 層: 地面の上、キャラクターと弾の下。ランタンの明暗の影響を受けず、暗い床でも読める明るさにする(自己発光)。縁取りの外側に暗い下線(幅 0.03 タイル)を引く。
- 明るさの変化: 不透明度を 35% から 100% へ、Windup の経過時間に対して線形に上げる。最初の描画から 35% で完全な形が見えている。Windup の終わりが近づくほど強くなり、突進の瞬間が近いことを示す。
- Charge に入る瞬間: 1 回だけ 100% を超える明るさ(核色 #FFE3B0 寄り)にフラッシュする。

### 5.2 体

- 体を沈める: 高さを 100%→80% に、Windup の経過時間に対して ease-in で縮める(幅は 100%→108%)。見た目だけで、判定は変えない。さらに、突進方向と逆に最大 0.15 タイル、スプライトを引く(反動)。
- 熾火の点灯: 尾根の色を待機色から赤橙へ、経過時間に対して線形に点灯させる。最後の 0.1 s は核色に寄せる。
- 目も同じ赤橙に光る。
- 歩行アニメーションは止める。止まった Grub に熾火とレーンが付いている、が合図の組み合わせ。通常の歩きとは、止まる・沈む・光る・レーンが出るの 4 点で区別できる。
- 音(予定範囲に音があれば): Windup の開始に合わせ、0.7 s で音程が上がる短い溜め音。音がなくても読める設計とする。

### 5.3 重なり

- Spitter の弾、出現中の表示、他の敵はレーンの上に描く。レーンの縁取りと矢印は、弾の下でも一部が見える。
- 同時にレーンが出るのは 1 本まで(規則どおり)。
- 倒された、またはポーズなどの場合: 倒された時点でレーンと点灯を 0.1 s 以内に消す。ポーズ中は全部の変化が止まる。

## 6. Charge

- 体を進行方向に伸ばす(進行方向 130%、横 80%)。核色の熱い芯と、赤橙の縁。
- 残像: 0.5 タイル進むごとに 1 つの残像を置き、0.2 s かけて消す(距離で置くので FPS に依存しない)。足元に土煙。
- レーン: 100% に保ち、Grub が通過した後ろ側から消していく。前方は残る。
- Charge の終わりでレーンを 0.1 s で消す。
- 接触が解決した後の「使用済み」表示(望ましい。§9 の口が使える場合): 接触が解決したら、核色を赤橙の暗い側に落とす(芯が弱まる)。Charge は続くが、その突進はもう害を与えないことを示す。「重なったのに当たらない」違和感を減らすための合図。口が使えなければ省く。
- 被弾フラッシュ(§8)は Charge 中も同じ。怯まないので、動きは止まらない。

## 7. Recovery(0.8 s)— 隙

- 突進は終わった、いまは止まっていて攻撃が通る、と読ませる。
- 熾火を消す(尾根は待機色へ 0.1 s で戻る)。目の光も消す。体全体に沈んだ色(§2)を乗せる。体は高さ 90% に沈み、足元から薄い蒸気が 0.3 s ごとに 1 つ上がる。
- 最後の 0.2 s で、体が 100% の高さに戻り、色も通常に戻る。隙が終わる合図。
- 出現中との区別: Recovery は不透明で、青い輪がなく、蒸気がある。
- 留意: 沈んだ見た目が「死にかけ」「無敵」と誤読されないか(未確認、Play で確認)。誤読された場合は、蒸気を強め、沈んだ色を弱める。
- 音(あれば): 低い息の抜ける音 1 回。

## 8. 被弾(Grub が攻撃を受けたとき)

- どの状態でも同じ。白いフラッシュ(#FFFFFF、0.1 s、時間で減衰)と小さな火花を、当たった位置に出す。
- 位置、向き、大きさ、状態の演出(レーン、点灯)は変えない。怯みに見える動きは付けない。
- HP が減ったことが分かること: 既存の敵の HP 表示があればそれを使う。なければ、HP 1 の間は体に小さな傷の重ね絵を表示する(小アセット 1 つ)。

## 9. 抜けた合図(望ましい)

- 接触の瞬間にプレイヤーが無敵で、ダメージなしに解決されたとき: プレイヤーの位置に、淡い白青(#CFE8FF)の細い輪を 0.15 s 出す。害を与えた場合の既存の被弾表現とは別の形にする。
- 被弾した場合は既存の被弾表現だけを使い、抜けた合図は出さない。
- 必要な情報: 接触の解決結果(無敵で抜けた/被弾)。D-004 の「見た目への口」にこれが含まれない場合は、この合図と §6 の使用済み表示を省く。省いても必須の予告は成立する。

## 10. 受け入れ基準

### 10.1 検証用(qa 向け、30 FPS と 60 FPS の両方)

- A1: Windup の最初の描画からレーンが出ている(不透明度 35% 以上)。予告のない Charge はない。出現直後、Recovery 後、被弾中、ポーズ復帰後を含む。
- A2: レーンの向きが、Charge の実際の進行方向と一致する(角度の差 ±3° 以内)。Windup 中にプレイヤーが動いても変わらない。
- A3: レーンの幅が接触判定の範囲と ±0.1 タイル以内で一致する。長さは 7.0 タイルまたは壁の手前まで。
- A4: レーンの不透明度が Windup の間、35%→100% に単調に上がる。30 FPS と 60 FPS で、同じ経過時間における値の差が 5% 以内。
- A5: 最も暗い床の上で、Windup の開始時点(不透明度 35%)のレーンの縁と床の明るさの比が 3:1 以上。
- A6: 沈み込み、熾火の点灯が Windup の 0.7 s の間(±1 フレーム(30 FPS 基準))に完了する。
- A7: Windup、Charge、Recovery の間に攻撃を当てても、位置、大きさ、レーン、点灯、状態の演出が変わらない。白いフラッシュと火花だけが出る。
- A8: Windup 中に倒すと、レーンと点灯が 0.1 s 以内に消える。ポーズで全部が止まり、復帰で続きから再開する。
- A9: Spitter の弾がレーンの上にあるとき、弾はレーンの上に描かれ、レーンの縁と矢印の一部が見える。
- A10: 出現中(半透明、青い輪)、Windup(レーン、熾火)、Charge(伸びた体、残像)、Recovery(沈んだ色、蒸気)、通常の歩きの 5 つの見た目が、1 枚のスクリーンショットで互いに区別できる。
- A11: 突進型の尾根が、出現中を含む全状態で見える。通常型には付かない。
- A12: 突進スイッチをオフにすると、尾根、レーン、その他の突進の演出は一切出ない(通常型と同じ見た目)。
- A13: 抜けた合図(§9)を実装した場合、無敵で抜けたときにだけ出て、被弾したときには出ない。

### 10.2 体験の観点(Play と Review 向け。Playtester の handoff には書かない)

- 突進型の Grub を初めて見たとき、「何かが来る」と分かるか。当たったとき、「予告は見えていた」と言えるか。
- 暗い部屋、小さい画面、ゲームパッドの操作中でも、レーンの向きと範囲が一瞬で読めるか。
- レーンと Spitter の弾を、形で見分けられるか(どちらも赤橙系だが、帯と小さな丸)。
- Windup 中の Grub が「まだ無害」と読めるか。近づいてよいと感じさせすぎないか。
- ダッシュで抜けたとき、「抜けた」と感じられるか。
- Recovery を「攻撃のチャンス」と読めるか。「死にかけ」や「無敵」と誤読されないか。
- 攻撃しても止まらないことが、「止められない突進」として自然に読めるか。
- 30 FPS と 60 FPS で同じに感じられるか。
- 色覚の差で、レーンの形と沈み込みだけで読めるか。

## 11. 必要な視覚要素(gameplay-engineer 向け)と見立て

優先度: 必須(M)、望ましい(S)、あれば(N)。

| # | 要素 | 優先 | 新アセット | 既存の仕組みで足りるか(T0 で確認) |
|---|---|---|---|---|
| 1 | 状態、経過割合、突進方向の取得 | M | なし | D-004 の「見た目への口」 |
| 2 | レーン(帯、縁取り、矢印) | M | 小(矢印の 1 タイル分、または手続き描画) | 地面層に半透明の矩形を、色と不透明度を指定して描けるか |
| 3 | スプライトの色変調、拡大縮小、描画ずらし | M | なし | Windup の沈み込みと Charge の伸びに必要。なければ変形なしで色と明るさだけに縮める案を下記に示す |
| 4 | 熾火の尾根の重ね絵 | M | 小(重ね絵 1 枚。向きが複数なら向きごと) | 重ね描きができなければ、体の縁の色変調で代用 |
| 5 | 被弾フラッシュ | M | なし | 既存の被弾の白フラッシュがあれば流用 |
| 6 | 出現中の半透明と青い輪 | M | 小 | 既存の出現演出があれば色を調整 |
| 7 | 残像、土煙、蒸気 | S | 小(粒子 1 種) | 既存の粒子があれば流用。なければ省いても必須は成立 |
| 8 | 傷の重ね絵(敵に HP 表示がない場合) | S | 小(1 枚) | 既存の HP 表示を確認 |
| 9 | 接触の結果(抜けた/被弾)の通知 | S | なし | 口にない場合は §6 の使用済み表示と §9 を省く |
| 10 | 音(溜め音、息の音) | N | 音 2 つ | 音が予定範囲にある場合のみ |

- 新しい大きなアセットは必要ない。小さな新規素材は、矢印 1 枚、尾根の重ね絵、必要なら傷の重ね絵と粒子 1 種で、既存の Grub のスプライトに重ねる。
- 要素 3 が使えない場合の縮小案: 変形なしで、Windup の沈み込みの代わりに尾根と目の点灯とレーンだけで予告する。Recovery は色変調と蒸気で示す。予告の成立は、色だけでなく、レーンの形と点灯の組み合わせで維持する。
- 要素 2 が難しい場合の代替案: 床の既存のタイルに色を乗せて帯を作る(粗いが成立する)。
- 費用の見立て: 要素 1〜6 は既存の仕組みの再利用が中心で、小。要素 7〜9 は T0 の結果次第で省ける。

## 12. 未確認の点と実機で確認すべき点

- レーンの赤橙と Spitter の弾の色・ランタンの光との区別(形で区別する前提)。
- 最も暗い床での 35% のレーンの読み取り(A5 の数値は目標で、実機で確認する)。
- 小さい画面とゲームパッドの操作中に、0.7 s の予告を読んでダッシュまで入力できるか。足りなければ Windup の長さは `game-designer` の判断(`design/combat.md` §7)。見た目の強調では補えない場合は、規則の問題として戻す。
- Recovery の沈んだ見た目の誤読(§7)。
- レーンの幅を接触判定に一致させたことで、プレイヤーが「かすったのに当たらない」「当たったのにかすっただけ」と感じるか。
- 抜けた合図(§9)が過剰な表示にならないか。
- 通常型と突進型の尾根の差が、小さい画面で見分けられるか。
- 技術確認(T0)で、既存のスプライトと演出の仕組みの実際の制約。仕様を満たせない要素があれば、Build から戻る。

## 13. 参照

- `design/combat.md` §10(art への条件)、§2.1、§3、§5。
- D-006(予告の見た目の割り当て)、D-003〜D-005。
- `design/combat.md` §10 からこの文書への参照は、ファイルを書き込めるロールが追記する(Handoff 12 を参照)。
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3 → G-001 仕様、暫定)

状態: G-001 / D-002 / D-003 / D-005 / D-009 に基づく仕様。**この文書の新しい数値はすべて暫定値(P)**。H1〜H4(ゲームパッドの操作感、各部屋の実時間、音と演出、敵の速度と弾速など)の実機確認後に調整する。確認前に、プレイヤー側の数値は変えない。

変更履歴: Handoff 10 / D-005 で、怯み(§2.1、§8)、接触の定義(§3.4、§3.5、V3、V4、V11)、遠い方のスロットの規則(§4.1、§4.3)、波の既定(§4.1)を明記した。数値は変えていない。
Handoff 24 / D-009 で、波 2 以降の K と T を調べ始める時点と、出現位置の待ちの敵の扱い(§4.1)を明記し、V7 を更新し、V12 を足した。§10 に `design/grub-charge-telegraph.md` への参照を足した。数値は変えていない。

## 0. 表記と共通ルール

- 長さは秒(s)、距離はタイル、速度はタイル/秒で書く。フレーム数では定義しない。
- 対応する条件は 30 FPS と 60 FPS。タイマーはゲーム内の経過時間で進める。ポーズ中は止まる。
- 30 FPS と 60 FPS で、各状態の長さの差は 30 FPS の 1 フレーム(約 0.034 s)以内にする。接触が起きるかどうかも、FPS によって変わらないこと。
- ビルドの既存値を使う項目は「既存」と書く。
- 暫定値には `(P)` を付ける。

## 1. Player kit(変更なし)

- **Attack**(ボタン1つ): 向いている方向への短い振り。1 ダメージ。回復 0.35 s。
- **Dash**: 0.25 s で 4 タイル。ダッシュ中はずっと無敵。クールダウン 0.6 s。ダッシュ中に押した攻撃は予約され、ダッシュ終了時に出る。
- **被弾**: 1 ハートのダメージ。0.3 s の硬直(入力不可)。被弾から 0.8 s 後まで無敵。

この仕様はプレイヤー側の数値を一切変えない。

## 2. 敵

| 敵 | HP | 挙動 |
|---|---|---|
| Grub(通常型) | 2 | プレイヤーへまっすぐ歩き、接触で噛む(1 ダメージ)。予告なし。 |
| Grub(突進型) | 2 | 歩いて近づき、条件がそろうと予告つきで突進する(§3)。それ以外は通常型と同じ。 |
| Spitter | 2 | 固定位置。一定間隔で、プレイヤーに向けて遅い弾を撃つ。 |

### 2.1 共通ルール

- **出現中(spawn-in)**: 敵は出現位置に 0.8 s(P)の間「出現中」で現れる。この間は行動せず、ダメージも受けず与えない。出現中だと見えることが必須(柱3)。見た目は art-director が決める。
- **弾**(Spitter):
  - 速度 4.0 タイル/s(P)。ダメージ 1 ハート(P)。
  - 撃った瞬間のプレイヤーの位置へ直進する。先読みはしない。
  - 壁で消える。敵の体は通り抜け、敵にダメージを与えない。
- **敵どうし**: 歩くときの敵どうしの押し合いは既存のまま(未定義のまま)。突進中の Grub は他の敵の体を通り抜け、ダメージを与えない。
- **敵の被ダメージと怯み(Flinch)**:
  - 既存の 0.2 s の怯み(被弾すると行動を中断して Chase に戻る)は、**Chase など通常の状態でだけ**起きる。通常型 Grub と Spitter の怯みは既存のまま変えない。
  - **突進型 Grub の Windup、Charge、Recovery の間は怯まない**。攻撃を受けてもダメージ(HP)だけ受け、状態、方向、残り時間は変わらない。ノックバックが既存にある場合も、この 3 つの状態の間は受けない(位置を動かされない)。
  - 出現中の敵は、ダメージも怯みも受けない(上の「出現中」のとおり)。出現中が終わった後は上の規則に従う。
  - HP が 0 になれば、どの状態でもその時点で倒れる。
  - 突進型 Grub が Chase 中に怯んだ場合は、Chase に戻るだけ。開始条件(§3.3)のタイマーは怯みで巻き戻さない。

### 2.2 Spitter の数値(部屋ごと、§4 の表)

- 撃つ間隔は部屋ごとに変える。出現中が終わってから最初の 1 発までは 1.0 s(P)。
- 撃ち方(直進、1 発ずつ、先読みなし)は変えない。

## 3. Grub 突進

### 3.1 意図

Grub が立ち止まって溜め、その直線上に突っ込む。プレイヤーは予告を見て「横に出る」「ダッシュの無敵で突進を抜ける」を選ぶ。抜けたあとの隙に反撃できる。害を与える前に、必ず予告が見える(柱3)。

### 3.2 状態

| 状態 | 長さ | 動き | 接触ダメージ | 怯み |
|---|---|---|---|---|
| Chase | 条件まで | 部屋の Grub 速度で歩く | あり(1 ハート) | 既存(0.2 s) |
| Windup(予告) | **0.7 s (P)** | その場で停止。突進方向を **Windup の開始時に固定** | **なし** | **なし** |
| Charge | 距離 7.0 タイルまたは壁まで | 固定した方向へ **8.0 タイル/s (P)** で直進(最大約 0.875 s) | あり(1 ハート。§3.4 の接触の定義による) | **なし** |
| Recovery(隙) | **0.8 s (P)** | その場で停止 | **なし** | **なし** |

Recovery が終わったら Chase に戻る。

### 3.3 開始条件(Chase → Windup)

次をすべて満たしたとき。

1. 出現中が終わってから 1.5 s(P)以上たっている。前回の Recovery が終わってから 2.5 s(P)以上たっている。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル(P)。
3. 部屋の突進スイッチがオンで、その Grub が突進型。
4. **別の突進型 Grub が Windup または Charge 中でない**(同時に予告できるのは 1 体まで)。

### 3.4 規則

- **方向の固定**: Windup の開始時に、そのときのプレイヤーの位置へ向く。その後プレイヤーが動いても方向は変わらない。直線上を走る範囲が「突進の線」。幅は Grub の既存の接触判定が通る範囲(新しい大きさは決めない)。
- **予告の条件**:
  - Windup の 0.7 s の間ずっと見えている。
  - これから突進すること、およびその方向がわかる。
  - 通常の Grub の歩きと見分けがつく。
  - 色だけに頼らない。音だけにも頼らない。
- **接触の定義(D-005)**: Charge 中の接触は「**1 回の突進につき、Grub の体とプレイヤーが最初に重なった瞬間に 1 回だけ解決する**」。
  - 「最初に重なった瞬間」を、この文書では**接触の瞬間**と呼ぶ。更新ごとのスイープ判定で求め、FPS によって有無が変わらない。Charge の開始時にすでに重なっている場合は、Charge の開始の瞬間を接触の瞬間とする(Windup と Recovery の間の重なりは無害で、数えない)。
  - 接触の瞬間にプレイヤーが**無敵**(ダッシュ中、被弾後の 0.8 s)なら、ダメージなし。Grub は通り抜けて走り続ける。**その突進は、その後に重なりが続いても、無敵が切れても、もうダメージを与えない**。
  - 接触の瞬間にプレイヤーが無敵でなければ、**1 ハートのダメージを 1 回だけ**与える。その突進は、その後もうダメージを与えない。
  - 1 回の突進で与えるダメージは 1 回まで。次の突進では、また最初の重なりから数える。
  - Chase 中の噛みつきは、この規則に含めない(既存のまま)。
- **終了**: 7.0 タイル進むか壁に当たったら Charge が終わり、すぐ Recovery に入る。壁に当たったときの特別な処理はない。
- **Windup 中に倒された場合**: 予告はその場で消え、同時予告の枠が空く。Charge 中に倒されたときも同じ。Windup 中の攻撃はダメージを与えるが、Windup は中断されない(怯まない、§2.1)。HP が 0 になれば倒れる。
- **ポーズ**: 状態の時間は止まる。

### 3.5 ダッシュの無敵で抜けられるか(確認)

- 止まっているプレイヤーに対して、Windup の開始時の距離が d タイルなら、接触の瞬間は Windup の開始から約 0.7 + (d − 接触までの余白)/8 s 後。余白を無視すると、おおよそ 0.7 + d/8 s。
  - d = 3 で約 1.075 s、d = 6 で約 1.45 s。
- ダッシュの無敵は 0.25 s なので、**接触の瞬間の 0.25 s 前から接触の瞬間までに、ダッシュを始めれば抜けられる**。窓の幅は 0.25 s(30 FPS で約 7〜8 フレーム)。
- 接触は最初の重なりで 1 回だけ解決する(§3.4)ので、窓は重なりの長さに削られない。ダッシュが重なりの途中で終わっても、その突進はダメージを与えない。窓の数値は変えない(0.25 s のまま)。
  - 根拠: 窓が 0.25 s あれば、読んでから押す操作として成り立つ見込みがあるため。実機で「ダッシュが使える」と感じられるかは H1 とあわせて Play で確認し、足りなければ §7 の調整項目で扱う。窓を重なりの長さ(約 0.1〜0.2 s)ぶん狭くする案 B は採らない(D-005)。
- 横方向のダッシュなら線から出るので、窓はこれより広い。
- 連続する 2 回の突進のあいだ: 次の Windup は前の Charge が終わってから始まる。次の接触は前の接触の約 1.2 s 以上あと(d = 6 の最悪の場合)。ダッシュのクールダウンが「ダッシュの終了から 0.6 s」と読んだ最悪の場合でも、前の接触から約 0.85 s 後に再使用できる。**ダッシュが間に合わない並びは作られない。**
- 歩いて線から出られるかは、プレイヤーの移動速度(未定義)に依存する。この仕様では保証しない。歩きだけで簡単に避けられ、ダッシュを使う理由が出ない場合は §7 の調整項目で調整する(C の検証)。
- 被弾直後(0.8 s 以内)にダッシュを始めた場合の窓は、この確認に含めない。欠陥 D(§8)の再現結果が出るまで、規則を書かない。

### 3.6 反撃の隙

Recovery(0.8 s)は止まっていて接触ダメージもない。攻撃の回復 0.35 s なら、隣接していれば 2 回振れる(Grub の HP 2)。怯まないので、1 回目の攻撃で Recovery が中断されることはない。ただし、攻撃の届く距離は未定義なので、2 回当てられる位置取りが実機で成立するかは Play で確認する。

## 4. 部屋の進行

### 4.1 共通ルール

- 部屋の総数は 5、各部屋の敵の数は 3〜6 体のまま(既存)。
- 波(wave):
  - 次の波は、「生きている敵が K 体以下」または「前の波の出現中が終わってから T s」の、先に起きた方で出現する。
  - 「前の波の出現中が終わってから T s」の起点は、**その波の最後の敵の出現中が終わった時点**(出現位置の待ちがあれば、その待ちが終わって出現中も終わった時点)。
  - 「生きている敵」には**出現中の敵を含める**。
  - 部屋は、すべての波が出現し、すべての敵が倒れたときに終わる。
- **次の波の条件を調べ始める時点(D-009)**:
  - 波 N の次の波(N+1)の K と T は、**波 N の全員が出現中に入った時点**から調べ始める。それより前は、K の判定も T の計測もしない。
  - 波 N に出現位置の待ち(下記)に入っている敵がいる間は、その敵は「生きている敵」に**数えない**(まだ出現していない。出現位置に敵は存在せず、攻撃も当たらない)。待ちが終わって出現中に入った敵から、数える。
  - 波 N の全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか、T s たつかの先に起きた方で出す。T の起点は上のとおり(最後の敵の出現中が終わった時点)で、変わらない。
  - 波 N に待ちの敵がいなければ、波 N の出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- 出現位置(スロット): 扉側(Door)、奥(Far)、左側面(L)、右側面(R)、奥の左隅(FL)、奥の右隅(FR)。実際の座標は部屋データ。
  - 出現の時点でプレイヤーがスロットから 4 タイル未満なら、出現を最大 2.0 s 待つ。2.0 s たったら、そのまま出現中に入る。
  - 待ちはスロットごとに別々に数える。同じ波の複数のスロットの待ちは、波の出現を決めた時点から同時に始まる。
  - 待っている間にプレイヤーが動いてスロットから 4 タイル以上になったら、そのスロットの待ちはその時点で終わり、出現中に入る(2.0 s を待ち切らない)。いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない。追加の規則は不要。
  - **出現位置にプレイヤーが重なっても、押し出さない**。出現中の 0.8 s は無害で、見えるので動ける。待ちは最大 2.0 s (上のとおり)。
- **「プレイヤーから遠い方」の規則**(部屋 3 の波 2、部屋 5 の波 2 の「FL または FR」):
  - その波の出現を決める時点(出現位置の待ちを始める前)のプレイヤーの位置から、FL と FR の各スロット座標への距離(中心間)を比べ、遠い方を選ぶ。選んだあと、待ちの間にプレイヤーが動いても選び直さない。
  - 同じ距離のときは FL を選ぶ。
  - 同じ波に FL か FR が別の敵のスロットとして指定されている場合は、この規則の対象外(固定のスロットが優先)。
- **突進スイッチ**: 部屋ごとに、突進をオンまたはオフにできる。オフのとき、突進型の Grub は同じスロットの通常型 Grub に置き換わる。敵の数、波、出現位置は変わらない。

### 4.2 進行の筋

| 部屋 | 学ぶこと | 組み合わせさせること |
|---|---|---|
| 1 | Grub が来る。振る。間合い。 | なし(基本) |
| 2 | **突進の予告を読む**。ダッシュで抜ける。 | 突進と、左右からの通常型 |
| 3 | **Spitter** の線から出続ける。止まると撃たれる。 | Spitter と Grub(突進なし) |
| 4 | 突進と弾を、同時に処理する。 | 突進 + Spitter + 通常型 |
| 5 | 全部が同時に来る。波の切り替えの判断。 | 突進 2 体(順番に来る) + Spitter 複数 |

### 4.3 部屋ごとの構成

「遠い方」は §4.1 の規則による。

| 部屋 | 波 | 構成(スロット) | 次の波の条件 | Grub 速度 | Spitter 間隔 | 突進 |
|---|---|---|---|---|---|---|
| 1 | 1 | 通常 Grub × 2(L, R) | | 2.0 | – | オフ |
| | 2 | 通常 Grub × 1(Far) | K=1, T=10 s | | | |
| 2 | 1 | **突進型 Grub × 1**(Far) | | 2.0 | – | オン |
| | 2 | 通常 Grub × 2(L, R) + 突進型 Grub × 1(Far) | K=0, T=15 s | | | |
| 3 | 1 | Spitter × 1(Far) + 通常 Grub × 1(L) | | 2.2 | 2.0 s | オフ |
| | 2 | Spitter × 1(FL または FR のうち、プレイヤーから遠い方)+ 通常 Grub × 1(R) | K=1, T=12 s | | | |
| 4 | 1 | Spitter × 1(FL)+ 突進型 Grub × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 1.8 s | オン |
| | 2 | Spitter × 1(FR)+ 突進型 Grub × 1(R) | K=1, T=12 s | | | |
| 5 | 1 | Spitter × 1(Far)+ 通常 Grub × 2(L, R) | | 2.4 | 1.6 s | オン |
| | 2 | Spitter × 1(FL または FR のうち、プレイヤーから遠い方)+ 突進型 Grub × 2(L, R) | K=1, T=12 s | | | |

「次の波の条件」の行は、その波の次の波を出す条件(波 1 の全員が出現中に入った時点から調べる、§4.1)。

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は、部屋 1: 2、2: 3、3: 3、4: 3、5: 4。

### 4.4 立って振るだけが通じなくなる理由(設計上の根拠)

- Spitter は、撃った瞬間の位置を狙う。止まっているプレイヤーには、毎回当たる(部屋 3 から)。
- 左右から同時に来る Grub は、一方向に向き直るだけでは片側を受ける(部屋 2 から)。
- 突進は、止まって見ているだけでは当たる(部屋 2、4、5)。

### 4.5 突進を外した版(部屋 2、4、5)

- 部屋 2 は、通常 Grub が 1 体、次に 3 体の部屋。部屋 1 と似るが、波と左右の挟み込みがある。この版は「案2の構成だけの効果」を見るための基準になる。
- 部屋 4 は Spitter + 通常 Grub、部屋 5 は Spitter + 通常 Grub。どれも部屋として成立する。
- 突進の効果は、突進オン/オフの比較で切り分ける。

## 5. 突進が他の脅威と同時に起きたとき(柱3)

- 同時に予告できる突進は 1 体まで。次の Windup は、前の Charge が終わってから始まる(§3.3)。
- Windup の長さは全部屋で 0.7 s に揃える。部屋ごとに変えない(読み方を一定に保つ)。
- Windup 中と Recovery 中の Grub は接触ダメージがない。「止まっている Grub は危なくない。突進に入ったら危ない」と読める。
- 弾は遅く(4.0 タイル/s)、直線で、突進の線とは別。弾が当たるタイミングは、突進の予告より遅く見える。
- 出現中(0.8 s)は、行動もダメージもない。
- 一度に見る予告は 1 つ。弾は複数ありうる。
- 突進の予告が弾で読みにくくなる場合は、§7 の順で調整する。

## 6. 検証

### 6.1 検証用(qa 向け)

各項目を 30 FPS と 60 FPS の両方で確認する。

- V1: Windup が 0.7 s(±0.034 s)。突進開始前に必ず予告が出る。予告なしの Charge はない(出現直後、Recovery 後、プレイヤーの被弾中、ポーズ復帰後を含む)。
- V2: Charge の速度が 8.0(±0.5)タイル/s。距離は 7.0 タイルまたは壁まで。方向は Windup 開始時に固定され、途中で変わらない。
- V3: 止まっているプレイヤー(d = 4)に対し、**接触の瞬間(§3.4。Grub の体との最初の重なり)の 0.25 s 前〜接触の瞬間**にダッシュを始めればダメージなし。窓から 0.05 s 外れると被弾。窓の端は FPS で 1 フレーム(30 FPS 基準)以上ずれない。ダッシュが重なりの途中で終わっても、その突進はダメージを与えない。測定は、直前 0.8 s 以内に被弾していない状態で行う(被弾直後のダッシュは欠陥 D が確認されるまで含めない)。
- V4: 接触ダメージは Chase と Charge のみ。Windup と Recovery にはない。**1 回の突進のダメージは、最初の重なりの 1 回まで**。プレイヤーが無敵のときは、ダメージなしで Grub が通り抜け、**重なりが続いても、無敵が切れても、その突進はもうダメージを与えない**。Charge の開始時にすでに重なっている場合は、開始の瞬間に 1 回解決する。次の突進では、また最初の重なりから数える。
- V5: 同時に Windup または Charge の突進型は 1 体まで。倒したら枠が空く。
- V6: 突進スイッチをオフにすると、敵の数、波、出現位置は同じで、突進が一度も起きない。
- V7: 部屋 1〜5 の波の構成、条件(K, T)、Grub 速度、Spitter 間隔が §4.3 の表と一致する。部屋 3 と 5 の波 2 の Spitter が、§4.1 の規則(出現を決める時点で遠い方、同距離は FL、待ちの間は選び直さない)で選ばれる。「T s」の起点は最後の敵の出現中の終わり、「生きている敵」には出現中の敵を含み、出現位置の待ちの敵は含まない。K と T は、前の波の全員が出現中に入った時点から調べ始める(§4.1、V12)。
- V8: 出現中が 0.8 s。この間は行動もダメージもない。出現位置にプレイヤーが重なっても押し出されず、出現中は無害。
- V9: Spitter の最初の 1 発が出現中の終了から 1.0 s、弾速 4.0 タイル/s。弾は壁で消え、敵を通り抜ける。
- V10: プレイヤー側の数値(攻撃、ダッシュ、被弾の規則)が変わっていない。
- V11: 突進型 Grub の Windup、Charge、Recovery の間に攻撃を当てると、HP は減るが、状態、方向、残り時間は変わらない(怯まない)。HP が 0 になれば、その時点で倒れる。Chase 中に攻撃を当てると 0.2 s の怯みに入り、Chase に戻る(既存)。出現中は攻撃を当ててもダメージを受けない。
- V12: 波 2 が出るタイミング(プレイヤーに見える挙動で確認する)。
  - (a) 部屋 2: プレイヤーが波 1 の突進型の出現位置(Far)から 4 タイル未満に立ち続けると、その敵は最大 2.0 s 現れない。この間、波 2 は出ない。その敵が出現中に入った時点を起点に、突進型を倒す(K=0)か、その出現中が終わってから 15 s たつかの先に起きた方で、波 2 が出る。出現中に入る前に波 2 が出ることはない。
  - (b) 部屋 1: プレイヤーが L だけ、または R だけから 4 タイル未満に立つと、そちら側の Grub は最大 2.0 s 現れず、反対側の Grub は先に出現中に入る。待つ側が出現中に入るまで、波 2 は出ない。両方が出現中に入った時点で生きている敵は 2 体(K=1 より多い)なので、1 体倒すか、最後の敵の出現中が終わってから 10 s たつかの先に起きた方で、波 2 が出る。
  - (c) 待っている間にプレイヤーが 4 タイル以上離れると、その時点で敵が出現中に入る(2.0 s を待たない)。同じ波で複数のスロットが待つ場合も、全員が出現中に入るまで波 2 は出ない。
  - (d) 待ちがない場合の波 2 のタイミングは、従来どおり(波 1 の出現を決めた時点が起点)。

### 6.2 体験の観点(Play と Review 向け)

Playtester への handoff には書かない(基準を知らせない)。

- 立って振り続けるだけでは、後半の部屋(3〜5)で被弾するか。
- 部屋ごとに、敵の出方や対応の仕方が違うと感じるか。
- 突進の予告が、害を与える前に見えて読めるか。突進に当たったとき、「予告は見えていた」と言えるか。
- ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
- ダッシュで抜けたとき、「抜けた」と感じられるか(重なったのに当たらない、あるいは抜けた直後に当たる、という違和感がないか)。
- 被弾が「自分の判断ミスのせい」と感じられるか。
- 突進中の Grub に攻撃を当てても止まらないことが、不自然に感じられないか(予告と突進が「止められない」と読めるか)。
- 30 FPS と 60 FPS で同じに感じられるか。
- 突進オンとオフを比べて、オンの方が単調さが減るか(A、C)。
- 出現位置の近くに立っていても、波 2 が理由なく早く出て敵が急に増えた、と感じないか。

## 7. 調整項目(暫定値、H1〜H4 の確認後に調整)

先に動かす順:

1. 予告が読めない場合: Windup を 0.7 → 0.9 s に伸ばす。部屋 4、5 で同時に出る数を減らす。
2. 簡単すぎる場合: 部屋 4、5 の Grub 速度、Spitter 間隔、トリガー距離。
3. 歩きだけで避けられてダッシュを使わない場合: Charge 速度(8.0 → 10.0)、Windup(0.7 → 0.55 まで)。ただし 0.5 s を下回らない。
4. ダッシュが間に合わないと感じる場合: Windup を伸ばす(項目 1)。ダッシュの窓(0.25 s)は、プレイヤー側の無敵時間そのものなので、ここでは変えない。

プレイヤー側の数値(攻撃の回復、ダッシュのクールダウンなど)は、H1 の確認後に別の判断で扱う。

## 8. 未定義のまま残す項目

- 最大ハート数: この仕様は値に依存しない。既存のビルドのまま。
- プレイヤーの移動速度、攻撃の届く距離、各敵とプレイヤーの判定の大きさ: 既存のまま。
- ダッシュのクールダウンの起点(開始か終了か): §3.5 は最悪の場合で確認済み。
- 敵どうしの歩行時の押し合い: 既存のまま、この仕様では変更しない。
- 敵の怯みとノックバック: 通常型 Grub、Spitter、突進型の Chase 中は既存のまま。突進型の Windup、Charge、Recovery は怯まない(§2.1)。
- 出現位置がプレイヤーに重なった場合: 押し出さない(§4.1)。
- 出現位置の待ちと波の条件: §4.1 で定義済み(D-009)。
- フレーム落ち(30 FPS 未満)時の挙動: サポート外。
- 欠陥 D(被弾直後のダッシュ中のダメージ)の規則: `qa` の再現結果が出てから書き足す。この仕様には含めない。V3、V4 の測定は、被弾から 0.8 s 以上たった状態で行う。
- 各部屋の実時間: H2。この仕様はラン長(15–20 分)を変えない。

## 9. 実現性の確認が要る点(technical-director 向け)

技術的な方法は決めない。次が既存のシステムで簡単にできるかを確認してほしい。

1. Grub に、歩く以外の状態(Windup、Charge、Recovery)を足せるか。接触ダメージの有効/無効を状態で切り替えられるか。
2. 突進が、速度 8.0 タイル/s、プレイヤーのダッシュ(16 タイル/s)との相対速度でも、30 FPS で接触の取りこぼしなく判定できるか。
3. 同時に予告できる突進を 1 体に制限する管理を足せるか。
4. 部屋データで、波、出現位置(スロット)、出現中(0.8 s)、Spitter 間隔、Grub 速度、部屋ごとの突進スイッチを指定できるか。
5. 既存の部屋が「3〜6 体を最初に全部出す」前提で作られていないか(波での出現に対応できるか)。
6. 敵の挙動を秒の経過時間で進めているか(フレーム数ではなく)。
7. Spitter の弾が、壁で消え、敵を通り抜ける扱いになっているか。

(1〜3 の回答は Handoff 08 にある。怯み、接触の定義、遠い方の規則は D-005 で決定済み。波の条件を調べ始める時点は D-009 で決定済み。)

## 10. art-director に渡す条件

見た目の具体案は art-director が決める。仕様として求める条件:

- **突進の予告**: Windup の 0.7 s の間ずっと見える。突進が来ることと、その方向がわかる。通常の Grub の歩きと見分けがつく。色だけに頼らない。音だけに頼らない。音を付ける場合は、Windup の開始に合わせる。
- 長さは時間(0.7 s)で決まり、30 FPS と 60 FPS で同じ長さに見える。
- Charge 中は、歩きや Windup と見分けがつく。Recovery 中は、「止まっていて攻撃が通る」とわかる。
- 突進型は Windup、Charge、Recovery の間、攻撃を受けても怯まない。攻撃が当たったことは、HP の減少が見えれば足りる(怯みの動きで示さない)。
- 突進の予告が、Spitter の弾、出現中の表示、他の敵の動きと重なっても、読める。
- 出現中(0.8 s)が、行動する敵と見分けがつく。
- 突進型の Grub が、出現時から通常型と見分けがつくかどうかは、art-director が判断する。
- 突進の予告の見た目の詳細(レーン、熾火、沈み込み、Recovery の表現など)は `design/grub-charge-telegraph.md`(D-006)にある。

## Rooms(旧記述)

旧: 5 部屋、各 3〜6 体、Grub と Spitter の混成。部屋は全敵撃破で終わる。→ §4 に置き換え。

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/build-0.6.md
# Simulated build 0.6 — what playing it looks like

A player-observable description only. Lengths are in seconds, distances in tiles, speeds in tiles per second. Everything below holds the same at 30 FPS and 60 FPS unless a difference is stated.

## Rooms and waves

- Every room sends its enemies in two waves. The first wave appears when the room starts. The second wave appears when the number of living enemies drops to the room's threshold, or when the room's timer runs out, whichever happens first.
- Enemies that are fading in count as living. Enemies still waiting to appear do not count.
- The timer starts when the last enemy of the earlier wave has finished fading in. If that enemy had to wait at its spot first, the timer starts after the wait and the fade-in.
- Each room has six spots where enemies appear: the door side, the far side (back middle), the left side, the right side, the far-left corner and the far-right corner. There is no spot in a near corner by the door. The only corners enemies appear in are the two far corners.
- Room 1: wave 1 is two ordinary Grubs, left and right. Wave 2 is one ordinary Grub at the far side. It comes when one or fewer enemies are alive, or 10 s after the last wave-1 Grub finished fading in. 3 enemies in total, at most 2 at once. No charging Grubs.
- Room 2: wave 1 is one charging Grub at the far side. Wave 2 is two ordinary Grubs (left, right) and one more charging Grub (far side). It comes when no enemy is alive, or 15 s after the wave-1 Grub finished fading in. 4 enemies in total, at most 3 at once.
- Room 3: wave 1 is a Spitter at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in whichever far corner (far-left or far-right) is farther from you at the moment the wave is triggered, and an ordinary Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 4 enemies in total, at most 3 at once. Spitters fire every 2.0 s. No charging Grubs.
- Room 4: wave 1 is a Spitter in the far-left corner, a charging Grub at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in the far-right corner and a charging Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 5 enemies in total, at most 3 at once. Spitters fire every 1.8 s.
- Room 5: wave 1 is a Spitter at the far side and two ordinary Grubs, left and right. Wave 2 is a Spitter in the farther of the far-left and far-right corners (chosen as in room 3) and two charging Grubs, left and right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 6 enemies in total, at most 4 at once. Spitters fire every 1.6 s.
- A room ends when every wave has appeared and every enemy is dead.
- The farther-corner choice (rooms 3 and 5, wave 2) is made when the wave is triggered, before any waiting, using where you stand at that moment. The far-left corner and the far-right corner are compared by distance from the center of you to the center of each spot, and the one with the greater distance gets the Spitter. If the two distances are exactly equal, the far-left corner is used. It is never a near corner, because there is none. If you move while the wave waits, the choice does not change. A corner that a room names for a specific enemy is not part of this choice.

### How fast Grubs walk

Ordinary and charging Grubs in the same room walk at the same speed:
- Room 1: 2.0
- Room 2: 2.0
- Room 3: 2.2
- Room 4: 2.2
- Room 5: 2.4

This is walking speed only. A charge always runs at 8.0. Spitters stand still.

### Standing near a spawn point

- If you are closer than 4 tiles (center to center) to the spot where an enemy would appear, that enemy does not appear yet. It appears as soon as you are 4 tiles or farther away, or after 2.0 s of waiting, whichever comes first.
- Each spot of a wave waits on its own. All spots of one wave start waiting at the same moment, when the wave is triggered. A spot that has finished waiting does not wait again if you walk back to it. You are not pushed away from a spot, and the enemy can appear on top of you.
- While some enemies of a wave are still waiting, the next wave's threshold and timer are not running. They start only once every enemy in the wave has begun fading in.
  - If one or fewer enemies are alive at that moment, the next wave comes immediately. Otherwise it comes when the count drops to the threshold, or when the timer runs out.
  - Room 1: stand near the left spot only. The right Grub appears and the second wave does not come while the left spot waits. If you kill the right Grub during the wait, then when the left Grub begins fading in only one enemy is alive, and the wave-2 Grub comes at once. If you did not kill it, the second wave comes after one is killed, or 10 s after the later one finished fading in.
  - Room 2: if the charging Grub's spot is waiting, the second wave cannot come until it begins fading in. After that it comes when the Grub is dead, or 15 s after it finished fading in. The Grub cannot be hurt during its first 0.8 s of fading in, so the earliest kill is after that.
  - Waves with no waiting spots start counting the moment they appear.

## Enemies appearing

- Every enemy fades in for 0.8 s: from 40% to full opacity, with a pale blue ring at its feet. During this time it does not move, does not attack, does not hurt you, and your swipes do nothing to it (no damage, no flinch).
- A Spitter fires its first shot 1.0 s after it finishes fading in, then at the room's interval. A Spitter shot travels at 4.0, straight at where you stood when it fired, costs 1 heart, vanishes on walls, and passes through enemies without hurting them. Spitters flinch for 0.2 s when hit, as before.

## Charging Grubs

Charging Grubs (rooms 2, 4, 5) look like ordinary Grubs with a dark ember-colored ridge on the back, visible from the moment they fade in. Ordinary Grubs have no ridge. They have 2 HP, and walk and bite like ordinary Grubs. While walking they flinch for 0.2 s when hit.

A charging Grub starts a charge only when all of the following hold:
- at least 1.5 s have passed since it finished fading in;
- at least 2.5 s have passed since its last recovery ended, that is, since it went back to walking after its last charge. The 0.8 s of recovery is not part of the 2.5 s. For example, if a charge ends at time t, the Grub stands in recovery until t+0.8, and its next wind-up can begin no earlier than t+3.3. A Grub that has never charged has no such wait;
- you are 3.0 to 6.0 tiles away (center to center);
- no other living charging Grub is currently winding up or charging.

Flinching does not reset these waits. If two charging Grubs qualify in the same moment (room 5, wave 2, left and right), one of them goes first, in a fixed but not obvious order. The other waits until the first has finished charging.

The sequence:
1. **Wind-up, 0.7 s.** The Grub stops where it stands and its walking animation stops. A red-orange lane appears on the floor from the Grub toward where you were when the wind-up began. The lane is as long as the charge will be, 7 tiles or less if a wall is in the way, and as wide as the Grub's body (within 0.1 tile). It has a bright edge, a dark underline and a chevron every tile pointing along the lane. It stays lit regardless of floor darkness. Spitter shots, fading-in enemies and other enemies are drawn on top of it. The lane fades from 35% to full brightness over the wind-up. The Grub squashes to 80% height, widens a little and leans back from the lane. The ridge and eyes warm from dark to red-orange, turning pale-yellow in the final 0.1 s. The direction is fixed; moving afterwards does not turn the lane. The Grub does no damage during the wind-up.
2. **Charge.** The Grub rushes along the lane at 8.0 for up to 7 tiles (about 0.875 s), or until it hits a wall, and stretches long and thin with a bright core and red-orange edge. The lane flashes extra bright once at the start, stays at full brightness, and disappears behind the Grub as it passes. The part in front stays until the charge ends, then everything fades out over 0.1 s. Afterimages appear every half tile and fade over 0.2 s, with dust at its feet. It passes through other enemies without hurting them. Hitting a wall has no special effect; the Grub simply stops and goes into recovery.
3. **Recovery, 0.8 s.** The Grub stands still, sunk to 90% height and tinted a dull grey-blue, fully opaque, with thin steam rising from its feet every 0.3 s. Ridge and eyes go dark within 0.1 s. It returns to normal in the last 0.2 s and goes back to walking toward you. It cannot start another wind-up for 2.5 s after this moment.

### Getting hit by a charge

- A charge can hurt you at most once. The first time the Grub's body overlaps you during a charge decides it. If it was already overlapping you as the charge began, that counts as the first moment.
  - If you are invulnerable at that moment (for example, mid-dash), you take nothing. A thin pale white-blue ring appears around you for 0.15 s, and the Grub keeps running through you. The Grub's core dims to a darker red-orange for the rest of the charge. Staying inside it afterward, or the dash ending while it still overlaps you, does not hurt you.
  - If you are not invulnerable, you lose 1 heart, with the normal hit reaction and the normal invulnerability afterward. The core dims in the same way. No ring appears.
- Overlap during the wind-up or recovery does nothing. A new charge starts the count again.
- The invulnerability check uses the state you are in at that frame. At 30 FPS the end of the dash's 0.25 s protection can differ from 60 FPS by up to one frame (about 0.034 s).

### Hitting a charging Grub

- During the wind-up, charge and recovery, your swipes lower its HP only. It does not flinch, is not pushed back, and does not change direction, speed or timing. It flashes white for 0.1 s with small sparks at the point of impact. The lane and ridge do not change.
- With 1 HP left, a small crack mark appears on its body.
- At 0 HP it dies immediately in any state. A dying winder or charger removes its lane within 0.1 s, and another charging Grub may then start its own wind-up.
- Charging Grubs that are walking, ordinary Grubs and Spitters flinch 0.2 s as before.

## Your own numbers

Nothing about you has changed:
- Your swipe does 1 damage and takes 0.35 s to recover.
- Your dash covers 4 tiles in 0.25 s, you are invulnerable for all of it, and it has a 0.6 s cooldown. A swipe pressed during a dash comes out when the dash ends.
- A hit costs 1 heart, locks your input for 0.3 s, and you are invulnerable until 0.8 s after the hit.
- Movement speed, swipe reach and your size are unchanged. No new buttons.

## Timing at 30 and 60 FPS

- Fade-in, wind-up, charge distance, recovery, the 2.5 s wait, wave timers and spawn waiting are all counted in real time. Durations at 30 FPS are within about 0.034 s of those at 60 FPS.
- Whether a charge touches you does not depend on the frame rate.
- The farther-corner choice gives the same result at 30 and 60 FPS for the same positions.
- Pausing freezes all timers and animations, including lanes, steam and rings. Resuming after a long pause does not skip ahead more than a short step (0.05 s).
- Nothing flashes more than three times per second, apart from single flashes.

## What play feels like now

- Rooms 1 and 3 behave like before but with two waves, so there is a second arrival to deal with.
- In rooms 2, 4 and 5, standing still in a corner and swiping no longer works: a lane appears, and about 0.7 s later a Grub runs the length of it. Moving off the lane or dashing through the Grub avoids damage. Swiping the Grub during the run only chips it and does not stop it.
- A single charging Grub charges again about 3.3 s or more after its previous charge ended, and later if you are out of the 3.0–6.0 range or another one is busy.
- Only one charging Grub is ever winding up or charging at a time.
- In rooms 3 and 5, the second-wave Spitter appears in the far corner that is farther from you when the wave is triggered; if you stand exactly equally far from both, it appears in the far-left corner.
- No new sounds. No new buttons.
- As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.

## Development build only

- A tester can pick room 1–5, switch charging Grubs on or off per room (off turns every charging Grub into an ordinary Grub, with no ridge, no lane and no charge; the room's counts, waves and spots stay the same), and switch between 30 and 60 FPS.
- A log lists state changes with game time, enemy and type, charge direction, contact result (unresolved, slipped through, hit), wave arrivals with spots, the distance to you when a wind-up began, and the moment all enemies of a wave have begun fading in. For the farther-corner choice, the log shows which corner was chosen: far-left or far-right.
- The log also records the time each charging Grub's recovery ended and it went back to walking, so the gap to its next wind-up can be read directly.
>>>END

<<<FILE decisions/D-006-grub-charge-telegraph-visual.md
---
kind: decision
id: D-006
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-006: 突進の予告は「地面のレーン + 熾火の点灯 + 沈み込み」で示し、赤橙は害になる状態だけに使う

## Decision

`design/grub-charge-telegraph.md` の視覚仕様の基本を、次のとおり決める。後の工程を縛るのは次の割り当て。

- **予告の主な合図**: Windup 中に、Grub の足元から固定した方向へ、地面のレーン(赤橙の半透明の帯、縁取り、突進方向の矢印)を出す。方向は、レーンの向きで示す。幅は既存の接触判定の範囲に一致させ、長さは 7.0 タイルまたは壁の手前までとする。
- **補助の合図**: 体の沈み込み、背中の尾根(熾火)の点灯、目の光。色だけに頼らず、形(レーンと矢印)、動き(沈み込み)、明るさ(点灯とレーンの強さ)を組み合わせる。音は付ける場合の補助であり、音がなくても読めるものとする。
- **色の割り当て**: 脅威の赤橙は、「これから害になる、またはいま害になる」状態(Windup のレーンと点灯、Charge)にだけ使う。出現中は淡い青、Recovery は沈んだ色と蒸気で示し、赤橙は使わない。
- **突進型の目印**: 突進型は、出現時から常に、消灯した暗い赤茶の尾根で通常型と区別する。通常型の見た目は変えない。
- **時間**: すべての見た目の変化は、状態の経過割合から求める。フレーム数に結び付けない。
- **被弾の見せ方**: 突進型への攻撃は、白いフラッシュと火花だけで示す。怯みの動き(のけぞり、位置のずれ、縮み)を予告や状態の表示に使わない。
- **Recovery**: 「止まっていて攻撃が通る」と読ませるために、熾火を消し、沈んだ色と蒸気で示し、最後の 0.2 s で通常の姿勢に戻る。
- **要素の優先度**: 必須はレーン、体の色変調と変形、尾根の重ね絵、被弾フラッシュ、出現中の表示。残像・粒子、傷の重ね絵、接触結果の合図(抜けた合図、使用済み表示)、音は、既存の仕組みで足りない場合に省いてよい。

この決定が扱わないこと: 戦闘の規則と数値(`game-designer`)。色の値は暫定値で、Spitter の弾の色との差などの確認後に値だけを調整してよい(割り当ての方針は変えない)。

## Rationale

- レーンは、方向、通る範囲、時間(明るさの上昇)を 1 つの形で伝える。柱3(害の前に見える)と、「ダッシュで抜けられると判断できる」目標に最も直接効く。
- 幅を接触判定に一致させると、見た目と判定のずれによる「避けたのに当たった」「当たらないのに避けた」を防げる。ダッシュの窓の読みを守る。
- 赤橙を害になる状態に限ると、「赤橙 = 危ない」という美術方針の読みが保たれる。Recovery と出現中を赤橙にしないことで、「無害」を同じ言語で示せる。
- 怯みの動きを使わないのは、D-005 と §10 の条件による。被弾は白いフラッシュに限り、予告の表現と混ざらないようにする。
- 既存の Grub のスプライトに重ね絵と色変調で足すので、新しい大きなアセットが要らない(小さなチームの制約)。

## Alternatives considered

- **体の色の変化だけで予告する**: アセットは最小だが、方向と範囲が分からず、色だけに頼ることになる(§10 の条件に反する)。
- **プレイヤー側の画面端の警告表示(矢印など)**: 画面の小ささと一瞬の判断に向かない。位置と範囲から目が離れる。
- **レーンを判定より少し広く描く**: 読みやすくなるが、窓の読みを狂わせる。採らない。
- **レーンのシェブロンを動かして方向を強調する**: 突進が始まったように誤読される。採らない。
- **Windup の終わりで点滅させる**: 緊迫するが、点滅の回数の制約と FPS 依存の問題がある。明るさの上昇と単発のフラッシュを採る。
- **Recovery を赤橙のままにする**: 害があるように読めて、隙にならない。採らない。
- **Recovery を特別に表示しない**: 隙が読めず、反撃の機会が減る。採らない。
- **突進型を出現中まで通常型と同じ見た目にする**: 部屋 2 を新鮮に学べるが、部屋 4、5 でどの敵が突進するか読めない。尾根の目印を採る。

## Revisit when

- Play で、レーンが暗い床、小さい画面、Spitter の弾との重なりで読めないとわかった場合。
- 実機で 0.7 s の予告が読んでダッシュするのに足りないと感じられ、見た目の強調では補えない場合(規則の問題として `game-designer` に戻す)。
- Recovery の見た目が「死にかけ」「無敵」と誤読される場合。
- T0 の調査で、必須の要素が既存の仕組みで実現できないとわかった場合。
- 別の脅威(新しい敵)を足すことになり、赤橙の割り当てを見直す必要が出た場合。
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
