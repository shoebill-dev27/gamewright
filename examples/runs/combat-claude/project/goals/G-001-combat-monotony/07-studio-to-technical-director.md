---
kind: handoff
goal: G-001
seq: 7
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 07: studio → technical-director — 戦闘仕様(部屋の構成と進行、予告つき Grub 突進)の実現性を確認し、技術計画を立てる

## Task

`design/combat.md` の仕様について、既存システムでの実現性を確認し、リスク・テスト・順序・並列化可否を含む技術計画を作る。特に §9 の確認事項(状態の追加、判定の取りこぼし、波の出現、部屋データ、時間の進め方)に答える。

## Context

Goal G-001「戦闘が単調なので改善したい」。プレイテスターの観察と診断を経て、`game-director` が D-002 で方向を決めた(主軸は部屋の構成と進行、敵の挙動の追加は予告つき Grub 突進の 1 つのみ)。`game-designer` がそれを `design/combat.md` に仕様化し(Handoff 06)、D-003 で突進の規則を記録した。実装の前に、技術的な実現性を確認する段階である。突進の予告の見た目は `art-director` が別の独立したステップで扱うため、ここでは扱わない。

## Findings

仕様の概要(詳細は `design/combat.md`):

- §2〜3: 敵の共通規則(出現中 0.8 s、弾の扱い)と Grub 突進の状態・数値・規則。
- §4: 5 部屋の進行、波の規則、部屋ごとの構成表、突進スイッチをオフにした版。
- §5: 突進が他の脅威と重なったときの読みやすさの規則。
- §6: 検証の観点(qa 向け V1〜V10)。
- §7: 調整項目。§8: 未定義のまま残した項目。§9: 技術確認。§10: art への条件。
- 数値はすべて暫定値。プレイヤー側の数値とキットは変えていない。
- 設計者が挙げた確認事項は §9 にある。波の出現や状態の追加が既存システムで大きな費用になる場合の扱いは、下の Open questions を参照。

この Handoff に既存実装についての調査結果はない。コードの状態は `sim/repo-notes.md` と、ビルド 0.3 の記述(`sim/build-0.3.md`)を確認すること。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。新ボタンは Owner の承認なしでは不可。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進の 1 つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない。
- D-003: 突進は同時に 1 体、方向固定、予告中は無害。Windup は全部屋で同じ。部屋ごとに突進スイッチで外せる(スイッチをオフにすると同じ数・同じ位置の通常 Grub に置き換わる)。

## Constraints

- デスクトップ、キーボードとゲームパッド。30 FPS と 60 FPS の両方で正しく動くこと。時間はすべて秒で定義されており、フレーム数に依存させない。
- 小さなチーム: 既存システムを再利用する変更を優先する。
- D-001、D-002、D-003 の範囲内。部屋数(5)とラン長(15–20 分)は変えない。
- 仕様を変える必要が出た場合は、技術的な判断で仕様を書き換えず、下の戻りルールで返す。
- 欠陥 D(被弾直後のダッシュ中のダメージの疑い)は別ステップ(`qa` による再現)で扱う。この計画の対象に含めない。ただし、無敵・ダッシュの判定を触る実装になる場合は、その影響を計画に記す。

## Open questions

- §9 の確認事項それぞれについて、既存システムで可能か、追加が必要か、その費用の大きさ。
- 突進スイッチと波の出現を、部屋データでどう持たせるのが最小の変更か。
- 突進の判定(最大 7.0 タイルを 8.0 タイル/s で移動)が 30 FPS でも取りこぼしなく働くか。
- 実装を並列化できるか(できる場合は分割案)。

## Expected output

- 技術計画: 確認事項への回答、技術的リスク、テスト方針(`design/combat.md` §6.1 の V1〜V10 を 30 FPS と 60 FPS で確認できること)、実装の順序、並列化の可否。置き場所は、この結果を載せる Handoff の Findings とする。
- 結果の Handoff は `to: studio` 宛てにする(`art-director` の並列ステップの完了を待って Build に進めるため、Studio が両方の結果を見てから次へ回す)。
- 仕様が実現困難・範囲外の費用になる場合は、`outcome: question` で Studio に返し、理由と代替案を書く。Studio が戻りルールに従って Design(`game-designer`)または Decide(`game-director`)へ回す。技術的な判断で仕様を書き換えない。

## Sender assessment

なし。Studio は game design や技術の判断をしていない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: design/combat.md(特に §2〜4、§6、§9)、project.md#constraints、sim/repo-notes.md、sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/06-game-designer-to-studio.md
