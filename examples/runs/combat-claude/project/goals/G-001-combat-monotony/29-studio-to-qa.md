---
kind: handoff
goal: G-001
seq: 29
from: studio
to: qa
stage: Verify
outcome: routed
---
# 29: studio → qa — 模擬ビルド 0.4 を受け入れ基準 V1〜V12 に照らして検証する

## Task

模擬ビルド(`sim/build-0.4.md`)が、`design/combat.md` の受け入れ基準 V1〜V12 を満たすかを、仕様とビルドだけから検証し、基準ごとの pass/fail と退行の有無を報告する。

## Context

G-001「戦闘の単調さの改善」。方向は D-002 で決まり、部屋の構成と進行を主軸に、予告つきの Grub 突進を 1 つ加えた。Build は D-008 により、変更内容の記述の完了で完了した。このプロジェクトに実コードはなく、ビルドは変更内容の記述からシミュレーターが作った模擬ビルドである。したがって、報告は「模擬ビルドに基づく」と明記すること。実機の証拠として書かない。

## Findings

(Studio が組んだ Handoff。実装側の説明や自己評価は含めない。)

検証の対象と基準:
- 受け入れ基準は `design/combat.md` の V1〜V12(V7 と V12 は波の出現条件に関する)。数値と規則は仕様の本文を正とする。
- 波の出現条件の規則は D-009、怯み・接触・「遠い方」の規則は D-005 に書かれている。
- V12 の補足: 仕様(§4.1、D-009)の規則に従うと、出現位置の待ちの間にプレイヤーが先に出ていた敵を倒し、待ちの敵が出現中に入った時点で生きている敵が K 体以下になっていれば、次の波はすぐ出る。この場合は「すぐ出る」を期待値として読むこと。
- 見た目の基準(`design/grub-charge-telegraph.md` の A 系)は、`art-director` が並列に別の Handoff で確認する。この Handoff の範囲外。

## Decisions already made

- D-005: 怯み・接触の解決・「遠い方」の選択時点の規則。
- D-008: 判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- デスクトップ、キーボードとゲームパッド。30 FPS と 60 FPS の両方で正しく動くこと(`project.md#constraints`)。
- 新しい入力ボタンなし(D-001)。
- 確認できなかった項目は、pass にせず「未確認」と理由を書く。
- 仕様にない期待値が必要になったら、推測で判定せず、「期待される挙動が未定義」と報告する。

## Open questions

- ビルドの記述から読み取れない、または基準を測れない項目があれば、どの基準でなぜかを報告する。

## Expected output

基準ごとの pass/fail/未確認、根拠(ビルドのどの記述か)、退行の確認結果、重大度を、Handoff として書く。結果の宛先は `studio` とする(後続の Play の Handoff を Studio が組むため)。同じ基準が 2 回失敗した場合は、戻りルールで Plan に回る。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md、project.md#constraints、sim/build-0.4.md
- Decisions: decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: none
