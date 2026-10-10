---
kind: handoff
goal: G-001
seq: 6
from: game-designer
to: studio
stage: Route
outcome: done
---
# 06: game-designer → studio — 部屋の構成と進行、予告つき Grub 突進の仕様ができた。技術確認と見た目の条件を回す

## Task

`design/combat.md` の仕様(D-002 に沿った 5 部屋の構成と進行、予告つき Grub 突進)を受け取り、次の宛先を決める。実装の前に `technical-director`(実現性)と `art-director`(予告の見た目)に回し、そのあと実装、`qa`、Play に進む。

## Context

Goal G-001 の依頼は「戦闘が単調なので改善したい」。`game-director` が D-002 で方向(案2を主、案1は予告つき Grub 突進の 1 つのみ)を決め、仕様化(`write-design-spec`)が回ってきた。この handoff はその結果。

## Findings

**書いたもの**

- `design/combat.md` を更新。プレイヤー側の数値は変えていない。内容は次のとおり。
  - §2〜3: 敵の共通規則(出現中 0.8 s、弾の扱い)と Grub 突進の状態・数値・規則・ダッシュで抜けられるかの確認。
  - §4: 5 部屋の進行の筋、波の規則、部屋ごとの構成表、突進を外した版。
  - §5: 突進が他の脅威と重なったときの読みやすさの規則。
  - §6: 検証(qa 向け V1〜V10、体験の観点)。
  - §7: 調整項目。§8: 未定義のまま残す項目。§9: 技術確認。§10: art への条件。
- `decisions/D-003-grub-charge-and-room-rules.md`: 突進の規則(同時 1 体、方向固定、予告中は無害、Windup は全部屋で同じ、部屋ごとのスイッチ)を記録。

**主な数値(すべて暫定値)**

- 突進: Windup 0.7 s、Charge 8.0 タイル/s で最大 7.0 タイル、Recovery 0.8 s。再突進の間隔は 2.5 s。
- 突進は部屋 2、4、5 に入れる。部屋 1 と 3 には入れない。
- Grub 速度は部屋 1〜5 で 2.0 / 2.0 / 2.2 / 2.2 / 2.4 タイル/s。
- Spitter 間隔は部屋 3〜5 で 2.0 / 1.8 / 1.6 s。弾速 4.0 タイル/s(全部屋)。
- 敵の合計は 3 / 4 / 4 / 5 / 6 体。既存の「3〜6 体」の範囲内。

**Open questions への回答**

1. 5 部屋の進行の筋: 基本 → 突進を読む → Spitter → 突進と弾の組み合わせ → 全部入り(§4.2)。
2. 突進は部屋 2、4、5。突進スイッチをオフにすると、同じ数・同じ位置の通常 Grub に置き換わり、どの部屋も成立する(§4.5)。
3. 予告 0.7 s、突進 8.0 タイル/s・7.0 タイル、隙 0.8 s。ダッシュの無敵(0.25 s)で抜けられる。接触の 0.25 s 前から接触の瞬間までにダッシュを始めればよい。連続する突進でも、ダッシュのクールダウンが間に合う並びだけが作られる(§3.5)。歩いて避けられるかはプレイヤーの移動速度(未定義)に依存し、保証しない。
4. 同時に予告できる突進は 1 体まで。Windup は全部屋で 0.7 s。予告中の Grub は無害。弾は遅い(§5)。読めるかは実機で確認する必要がある。
5. 実現性の確認が要る点は §9、art に渡す条件は §10。
6. 検証の観点は §6。診断の 6 項目を引き継いだ。

**routing の依頼**

- `technical-director`: `design/combat.md` §9 の確認事項(状態の追加、判定の取りこぼし、波の出現、部屋データ、時間の進め方)。実装の前に回す。
- `art-director`: §10 の条件(予告の見た目と音、Charge、Recovery、出現中の見分け方)。技術確認と並行してよい。
- 欠陥 D は別の流れ(2b)。`qa` の再現結果が出てから、設計書に書き足す。この仕様に含まれていない。
- Playtester に渡す handoff には、仕様の数値や §6.2 の体験の観点を書かないこと。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つのみ。
- D-003(今回): 突進の規則と部屋の突進スイッチ(game-designer の権限内)。

## Constraints

- D-001、D-002 の範囲内。新しい敵の種類、Spitter の撃ち方の変化、プレイヤー側の数値やキットの変更、部屋数、ラン長は変えていない。
- 時間はすべて秒。30 FPS と 60 FPS で同じ長さ。
- 技術的な方法と見た目の具体案は決めていない。

## Open questions

方向や優先度に関わる選択は出ていない。次は他の Role の判断を待つ。

- 技術確認で、波の出現や状態の追加が既存のシステムで大きな費用になる場合は、仕様を変えるか `game-director` に回す。
- 予告が弾や他の敵と重なって読めない場合は、Play の後で §7 の順に調整する。

## Expected output

- Studio が `technical-director` と `art-director` に回す。結果を受けて、必要なら仕様を修正する(`game-designer`)。
- そのあと、実装 → `qa`(§6.1 の V1〜V10、30 FPS と 60 FPS) → Play(H1〜H4 の実機確認を含む) → Review。
- 突進オンとオフの比較は、Play で行う。

## Sender assessment

- 確信度: 構成と進行は中〜高。突進の効果と、予告の読みやすさ(特に部屋 4、5 の重なり)は、実機で見るまで中程度。
- 数値(Windup 0.7 s、Charge 8.0、Recovery 0.8 など)は、反応時間と性質の推定で置いた暫定値。H1〜H4 の確認前なので、固定しない。
- 歩きだけで避けられる場合、ダッシュを使う理由が出ない可能性がある(C)。その場合の調整は §7 に書いた。
- Windup 中の攻撃で突進を無効にする対処が簡単すぎる可能性がある。Play で見る。
- Owner のエスカレーションは不要(D-001 も柱1の解釈も変えていない)。

## Load

- Role: none(Studio の routing)
- Skills: none
- Project: design/combat.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/05-game-director-to-game-designer.md
