---
kind: handoff
goal: G-001
seq: 21
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 21: studio → gameplay-engineer — 変更内容を正確に書く(模擬ビルドの元になる Build)

## Task

承認済みの仕様と計画に従い、`sim/repo-notes.md` をこのプロジェクトのコードとして扱って、ゲームに加える変更内容を Handoff に正確に書く。変更内容を正確に書いた時点で、この Build は完了する(D-008)。

## Context

G-001「戦闘が単調なので改善したい」。方向は D-002(部屋の構成と進行が主軸、予告つき Grub 突進を併用)で、仕様は `design/combat.md`(D-003、D-005)と `design/grub-charge-telegraph.md`(D-006)、技術方針は D-004 と D-007 で決まっている。以前の Build は実コードがなく 2 回 `question` で返った(Handoff 14、18)。Owner は Escalation 20 に Option C で回答した(D-008): `sim/repo-notes.md` をコードとして扱い、模擬ビルドは変更内容から、ランタイムのシミュレーターが作る。以後の Verify・Play・Review は模擬ビルドに基づく。

## Findings

- 入力の欠落は解消した。`sim/repo-notes.md` は読める入力として Load にある。D-007 の 7(コードが読めない場合に返す)は今回は適用しない。
- 台帳 7 項目(Handoff 17、D-007)は `sim/repo-notes.md` と `sim/build-0.3.md` に照らして確認する。記述が答える項目は、答えの引用つきで「確認(模擬のコード)」と書く。記述が答えない項目は「模擬上の前提」と書き、その前提を変更内容に明記する。実際のコードで確認済みとは書かない。
- 範囲: D-002/D-003 の部屋の構成と進行(波、突進スイッチ)、予告つき Grub 突進、D-006 の視覚要素、D-004 の接触結果の通知(視覚仕様の要素 9)、D-005 の規則(怯まない 3 状態、接触は突進ごとに最初の重なりで 1 回だけ、遠い方は出現を決める時点で選ぶ)。
- 範囲外: 欠陥 D(被弾直後のダッシュ中のダメージ)の修正、新しい入力ボタン、Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更。

## Decisions already made

- D-001: 攻撃とダッシュのワンボタン戦闘。新ボタンなし。
- D-002: 主軸は部屋の構成と進行。併用は予告つき Grub 突進の 1 つだけ。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。部屋は突進スイッチで外せる。
- D-004: 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ。
- D-005: 突進型は 3 状態で怯まない。接触は突進ごとに最初の重なりで 1 回だけ。「遠い方」は出現を決める時点で選ぶ。
- D-006: 突進の予告は地面のレーン + 熾火の点灯 + 沈み込み。赤橙は害になる状態だけに使う。
- D-007: 台帳 7 項目と、前提が崩れたときの戻し先。
- D-008: Owner が Option C を選んだ。変更内容の記述で Build 完了。結果に模擬であることを明記する。

## Constraints

- 変更内容は、シミュレーターが観察可能な挙動を導ける精度で書く。部屋ごとの構成(敵の種類と数、波、出現位置、突進スイッチ)、時間の値(予告 0.7 秒などの仕様の数値)、状態と遷移、視覚要素、接触結果の通知、30/60 FPS で同じ挙動になる扱いを含める。
- 仕様の数値を勝手に変えない。仕様が曖昧、矛盾、または欠落している場合は決めず、`outcome: question` で返す(Studio が `game-designer` に回す)。
- 実行していないことを実行したと書かない。ビルド、テスト、動作確認は行っていない。受け入れ基準については「どの変更で満たす想定か」の対応表を書き、満たしたとは書かない。
- 模擬ビルドを自分で書かない。それはシミュレーターの仕事で、この Build の成果物ではない。
- 開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は D-004 のとおり開発ビルド限定で、プレイヤー向けの入力は足さない。
- 欠陥 D の原因に結び付く推測は書かない。

## Open questions

- 台帳 7 項目のうち、`sim/repo-notes.md` が答えない項目はどれか。その場合の模擬上の前提は何か。
- 視覚仕様の必須要素 1〜6 と要素 9 は、`sim/repo-notes.md` の記述にある仕組みで足りるか。

## Expected output

次の Handoff を `goals/G-001-combat-monotony/22-gameplay-engineer-to-studio.md` として書く。`to: studio`(Verify で `qa` と `art-director` を並列にするため、Studio が受け手ごとに新しい Handoff を組む)。`outcome: done`(曖昧さがあれば `question`)。

Findings に次を書く:

1. 台帳 7 項目の結果(確認(模擬のコード)/ 模擬上の前提)。
2. 変更内容(部屋ごと、敵コントローラ、スポナー、視覚要素、接触結果の通知、開発用補助)。シミュレーターがそのまま読める形で。
3. 受け入れ基準と変更の対応表。
4. 実装していない・確認していないことの一覧(実行、ビルド、テスト、実機の感触)。

自己評価(確信度、疑い)は `## Sender assessment` に分けて書く。`qa` と `playtester` には渡されない。

## Sender assessment

(Studio が書いた routed Handoff のため、なし。)

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.3.md、project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md、decisions/D-002-combat-direction-rooms-and-grub-charge.md、decisions/D-003-grub-charge-and-room-rules.md、decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
