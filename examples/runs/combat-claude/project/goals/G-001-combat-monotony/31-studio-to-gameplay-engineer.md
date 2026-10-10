---
kind: handoff
goal: G-001
seq: 31
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 31: studio → gameplay-engineer — 変更内容の修正(F-1)と、V7・V10 で確認できなかった点の明記

## Task

模擬ビルド 0.4 の検証(Handoff 30)で見つかった仕様との食い違い F-1 を、変更内容の記述(Handoff 28 の 2.1〜2.4)で仕様に合わせて直す。あわせて、QA が記述から確認できなかった V7(Grub の速度、遠い角が同距離のときの規則)と V10(プレイヤー側の数値)を、変更内容に明記して確定する。

## Context

G-001 は戦闘の単調さの改善。D-008 により、Build は変更内容を Handoff に正確に書いた時点で完了で、模擬ビルド(`sim/build-0.4.md`)はその記述からシミュレーターが作る。Verify(Handoff 30)では V1〜V12 のうち fail はなかったが、V7 と V10 の一部は記述から確認できず pass にできなかった。基準の外で、仕様と模擬ビルドの食い違い(F-1)が 1 件あった。すべて模擬ビルドの記述に基づく結果で、実機の観測ではない。

## Findings

Handoff 30(`qa` の報告)から、客観的な事実だけを抜き出す。

1. **F-1(仕様との食い違い)**: 突進の再開始の待ち時間の起点が違う。
   - 仕様 `design/combat.md` §3.3: 前回の **Recovery が終わってから** 2.5 s 以上。
   - 模擬ビルド: 前回の**突進が終わってから** 2.5 s 以上(Recovery 0.8 s を含む)。
   - 影響: 同じ Grub の次の突進の条件が仕様より 0.8 s 早くそろい、突進の頻度が上がる。V1、V5、§3.5 は壊れない。
2. **V7 の未確認 1: Grub の速度**。仕様は部屋 1〜5 で 2.0 / 2.0 / 2.2 / 2.2 / 2.4。模擬ビルドは部屋 3 を「部屋 1〜2 より少し速い」、部屋 5 を「最も速い」としか書いておらず、部屋 4 に言及がなく、数値がない。
3. **V7 の未確認 2: 「遠い角」が同距離のとき**。FL を選ぶ規則と、距離を中心間で比べることが、模擬ビルドの記述にない。
4. **V10 の未確認**: 模擬ビルドの記述にあるプレイヤー側の数値はダッシュの 0.25 s の保護だけで、仕様と整合する。攻撃の回復 0.35 s、ダッシュのクールダウン 0.6 s、被弾の硬直 0.3 s と無敵 0.8 s は、変更した・していないのどちらの記述もない。
5. **補足(確認のみ。修正を求めない)**: V12(c) について、同じ波の複数スロットの待ちが「波を出すと決めた時点から同時に始まる」ことが模擬ビルドに明記されていない(「スロットごとに別々」とだけある)。基準の結果には影響しない。記述に 1 文あると確認しやすい。
6. **範囲外(触らない)**: 欠陥 D(被弾直後のダッシュ中にダメージを受けることがある)。模擬ビルドはこの挙動を記述しており、仕様は意図的に未定義。規則は `game-designer` が決める事項で、この Step では変更も原因の推測もしない。

## Decisions already made

- D-001: 攻撃とダッシュのみ。新ボタンなし。
- D-004: 技術方針(共通コントローラへの状態追加など)。
- D-005: 怯み、接触の解決、「遠い方」は出現を決める時点で選ぶ。
- D-007: 前提の台帳。確認できない項目は「模擬上の前提」と明記する。
- D-008: Build は変更内容を正確に書いた時点で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- 仕様は `design/combat.md` が正。食い違いは仕様に合わせて変更内容側を直す。
- 仕様に数値や規則がなく、決められない場合は決めずに返す(Skill どおり)。その場合は、仕様のどの節が欠けているかを書く。
- 実コードで確認済みと書かない。確認できない項目は「模擬上の前提」と明記する。
- 新しい入力ボタンを足さない。プレイヤー側の数値を変えない。
- 欠陥 D の原因を推測して書かない。

## Open questions

1. F-1 は、仕様 §3.3 の文面どおり「Recovery が終わってから」でよいか。仕様の文面が曖昧と判断する場合は、直さずに `game-designer` への質問として返す。
2. 遠い角が同距離のときの選び方は、仕様または D-005 に定義があるか。ある場合はそれを変更内容に明記する。ない場合は決めずに返す。
3. Grub の速度(部屋 1〜5)は、仕様の数値をそのまま変更内容に書いてよいか。変更内容にすでに数値があるなら、模擬ビルドで落ちた理由は分からないので、そのとおり報告する。

## Expected output

- Handoff を `to: studio` で書く(Verify で `qa` に渡す Handoff を Studio が組み直すため)。
- Findings に、**修正後の変更内容 2.1〜2.4 の全体**を自己完結で書く(Handoff 28 を読まなくても分かる形)。次を含める。
  - F-1 の修正(起点を Recovery 終了後にする)。
  - 部屋 1〜5 の Grub 速度の数値。
  - 遠い角が同距離のときの規則と、距離の比べ方(仕様に定義がある場合)。
  - プレイヤー側の数値(攻撃の回復、ダッシュの保護とクールダウン、被弾の硬直と無敵)を変更していないという明記。
  - 追加の 1 文: 同じ波の複数スロットの待ちは、波を出すと決めた時点から同時に始まる(仕様 §4.1、D-009 と矛盾しない場合のみ)。
- 変更した箇所を、Handoff 28 との差分として一覧する。
- 模擬上の前提が残る項目を一覧する。
- 自己評価は Sender assessment にだけ書く。
- 仕様の欠落や矛盾があれば、決めずに `outcome: question` で返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md、sim/build-0.4.md、goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md(修正する変更内容の元。自分で書いたもの)
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/30-qa-to-studio.md
