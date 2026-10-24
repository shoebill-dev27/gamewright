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
