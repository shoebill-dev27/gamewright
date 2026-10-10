---
kind: handoff
goal: G-001
seq: 11
from: studio
to: art-director
stage: Design
outcome: routed
---
# 11: studio → art-director — Grub 突進の予告(Windup)の見た目を仕様化する

## Task

`design/combat.md` §10 の条件に従い、予告つき Grub 突進の「見た目」を仕様にする。見た目は、Windup 中の予告、突進方向の示し方、Charge 中、Recovery 中の読み取りやすさを含む。プレイヤーが突進を「害の前の合図」として見分けられ、ダッシュで抜けられると判断できることを目標にする。成果は player-observable な受け入れ基準を持つ視覚仕様にする。

## Context

Goal G-001「戦闘の単調さの改善」。Decide の D-002 により、主軸は部屋の構成と進行とし、敵の挙動の追加は予告つき Grub 突進の 1 つに限った。戦闘仕様は `design/combat.md` に書かれ、技術確認(D-004)と仕様の食い違いの解消(D-005)は終わっている。残る Build の前提は、この見た目の仕様と、本 Handoff と独立した作業である。突進の予告の見た目は戦闘仕様の範囲外で、`art-director` の判断に委ねられている。

## Findings

視覚仕様に影響する、確定済みの仕様上の事実(出典は `design/combat.md` と Decisions。数値と正確な文面は文書で確認すること):

- 突進型 Grub は Windup(予告)、Charge、Recovery の順に動く。Windup 中は無害で、突進の方向は予告の間に固定される(D-003)。
- 突進は同時に 1 体だけ。見た目の状況は「同時に複数の予告が重なる」ものにならない(D-003、D-004)。
- 突進型 Grub は Spawning、Windup、Charge、Recovery の間は怯まない(D-005)。したがって、被弾時の怯みの動きを予告や状態の表示に使ってはならない。§10 にも同趣旨の条件がある。
- 接触の判定は突進ごとに最初の重なりで 1 回だけ解決する(D-005)。プレイヤーが避けられたと分かる見た目と、当たったと分かる見た目を区別できることが望ましい。
- 技術側は、状態に応じた見た目を差し込む口を用意する方針(D-004、「見た目への口」)。見た目は状態遷移に結び付ける前提で考えてよい。
- 技術確認のために、Build の最初の作業 T0 で、既存のスプライトや演出の仕組みを調べる。既存の仕組みで実現できない見た目を仕様にした場合、Build で技術側から戻る可能性がある。

プロジェクトの美術方針(`project.md#art-direction`):暗い洞窟をプレイヤーのランタンが照らし、暖色の光と冷たい青黒の対比で見せる。脅威は彩度の高いオレンジ/赤で、暗闇の中でも読み取れるようにする。ビジョンの柱 3「Readable threats」(脅威は害の前に必ず見える)を守る。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。新しい入力は足さない。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進のみ。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-004: 技術方針(スイープ判定、状態の追加、見た目への口)。
- D-005: 突進型は Windup、Charge、Recovery で怯まない。接触は突進ごとに最初の重なりで 1 回だけ解決する。

## Constraints

- 戦闘の規則(予告の長さ、ダッシュの窓、判定、数値)は変えない。見た目のために規則や数値の変更が必要と判断したら、決めずに `outcome: question` で返す。規則は `game-designer`、方向やスコープは `game-director` の判断になる。
- 30 FPS と 60 FPS の両方で同じように読み取れること(`project.md#constraints`)。
- 小さなチームで、既存システムを再利用する変更を優先する。新しい大きなアセットが必要な案は、代替案と費用の見立てを添える。
- 新しい入力ボタンは足さない。
- プレイヤーはゲームパッド主体の、回避と間合いに慣れたアクション好き(`project.md#player-profile`)。画面の小ささや一瞬の判断を想定する。
- 見た目の仕様は体験を保証しない。実機での読み取りやすさは Play で確認される。仕様には未確認の点を書いておくこと。

## Open questions

- 予告の合図は、色、形、光、動き、効果音(音が予定範囲にあれば)のどれを主に使うか。美術方針の枠内で決める。
- 突進の方向を、予告のどの要素で示すか。
- Recovery 中を、無防備である(攻撃のチャンス)と読み取らせる見た目にするか。するなら、どう仕様に書くか。
- 別の敵(Spitter など)の脅威色と区別できるか。

## Expected output

- 視覚仕様(player-observable な受け入れ基準を含む)を、Project 内の設計文書として書く。置き場は `design/` 内に新しい文書を作るのを基本にし(例: `design/grub-charge-telegraph.md`)、`design/combat.md` §10 から参照する。書き込みできる範囲は、その実行の Packet が決める。
- 決めたことのうち、後の工程を縛るもの(例: 予告の色の割り当て)は Decision として記録する(`make-decision`)。
- 結果は `studio` 宛ての Handoff で返す。`to: studio`。Build で `gameplay-engineer` が必要とする視覚要素の一覧、既存の仕組みで足りるかについての見立て、実機で確認すべき点を含める。

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md(§10 の art への条件を必ず。突進の状態は §3 も)、project.md#art-direction、project.md#constraints、project.md#player-profile
- Decisions: decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-005-flinch-contact-and-far-slot-rules.md
- Previous handoff: none(受け手に渡すのは設計文書と Decisions。`game-designer` の Sender assessment は渡さない)
