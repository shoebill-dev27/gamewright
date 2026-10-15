---
kind: escalation
goal: G-001
seq: 36
from: studio
to: owner
status: resolved
decision: D-007
---
# 36: オーナー判断のお願い — `manual.md` に練習部屋の段落を入れてください

## Question

`manual.md` の `## On screen` セクションに、下記の英文1段落を (文言そのままで) 追記してもらえますか。

## Why this needs the Owner

作業は、どのロールも作れない素材 (書き込めない `manual.md`) で止まっています。D-005 により `manual.md` はオーナーが置くもので、エンジニアの書き込み範囲にも入っていません。同じ入力 (`manual.md` の更新) が3回続けて足りず、その間に新しい材料も供給されていないため、ロールへは再度回さずオーナーに上げます (orchestration.md の「ロールが作れない情報・素材で止まる場合」)。

## Options

### Option A — オーナーが段落を追記する (推奨)

`manual.md` の `## On screen` セクション (記号表のあと、"With color on…" 段落の前後どちらでも可、セクション内であること) に次の段落を一字も変えずに入れます。`manual.md` は `repo/` と同じ階層に置いてください (`ManualTest` がそこを参照します)。

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

数分の作業で、可逆です。AC-15 (D-006 の練習部屋の記載) が満たされ、`ManualTest` 2件が通るようになります。
If chosen: Resume。D-007 として記録し、Goal を `active` に戻し、QA (7g) の AC-15 確認を `ManualTest` 込みで行います。7h (アートディレクター)、Play、Review は計画どおりです。

### Option B — 今後 `manual.md` をロールが編集できるようにする

オーナーが実行環境の書き込み許可を広げ (または D-005 を改め)、エンジニアが `manual.md` を直接編集できるようにします。以後の手戻りは減りますが、D-005 (オーナーが置く) の方針変更になり、設定変更の手間もあります。
If chosen: D-005 を改める Decision を記録し、7f を書き込み許可付きで再度エンジニアに回します。

### Option C — 練習部屋の段落を見送る

AC-15 のうち練習部屋の記載を外し、プレイヤー向けマニュアルは現状のままにします。D-006 の「練習部屋は On screen セクションに載せる」という裁定を覆すので、game-designer / game-director の再判断が必要です。
If chosen: Design (game-designer) に戻して AC-15 と D-006 を見直し、`ManualTest` の該当テストを削ります。

## Studio recommendation

Option A。

## Reasoning

文面はすでに確定していて (D-006、AC-15)、必要なのは追記だけです。B は恒久的な方針変更、C は既存の裁定を覆すため、この小さな欠落には釣り合いません。A が長引く場合に B を検討してください。

## Meanwhile

描画変更 (F1/AC-18、F3、AC-17) の検証は `manual.md` に依存しないため続行します。QA 7g (37) を開き、AC-15 と `ManualTest` は「未実行」として扱います。アートディレクターの 7h は 7g の後に、Play と Review はその後に続きます。

## Owner decision required

A / B / C — 選択肢と条件を返信してください。

---

**Owner response (2026-10-15):** A。36 の段落を一字も変えずに manual.md の ## On screen セクションの末尾に追記しました（Owner の代理として Studio の推奨案を採用）。

**Resolved (2026-10-15):** Option A を D-007 として記録。Goal は `active` に戻し、AC-15 と `ManualTest` の確認は QA 7i (38) で行う。
