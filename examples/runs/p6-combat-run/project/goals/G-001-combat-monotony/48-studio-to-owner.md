---
kind: escalation
goal: G-001
seq: 48
from: studio
to: owner
status: resolved
decision: D-010
---
# 48: Owner decision needed — AC-15 の再実行（`run_tests` を 40/40 で通す）をどう行うか

## Question

修正済みの `ManualTest` を、変更していない `manual.md` と一緒に実行する作業を、前回と同じくオーナーにお願いしてよいですか（それとも QA の作業場所に `manual.md` を置きますか）。

## Why this needs the Owner

`studio/orchestration.md` の「どの役割も用意できない情報・資料でブロックされている」に該当します。AC-15 の合否には、`repo/` の隣にある変更前のままの `manual.md` が必要です。QA の作業場所にはそれがありません（29、40）。エンジニアの作業場所にあるかも確認できず、47 ではスイートを実行していません。どの役割も `manual.md` を編集・配置できないため、Studio は決められません。QA を同じ入力不足のまま三度目に送ることは、ループ上限で禁止されています。

## Options

### Option A — オーナーが `run_tests` を実行して結果を報告する（D-008 と同じ手順）

`manual.md` が `repo/` の隣にある環境で、`repo/` から `python3 -m unittest discover -s tests` を実行します。`manual.md` は変更しないでください。報告してほしいのは、実行総数、失敗数、失敗があればそのメッセージの原文です。
期待結果は 40/40 です。コストは数分で、元に戻せます。実行の独立性は QA より弱いものの、結果はテスト出力そのものなので十分に客観的です。
If chosen: 結果を Decision（`decided_by: owner`）に記録します。40/40 なら AC-15 は合格で、次に Play（8）を開きます（許された情報だけで Studio が Handoff を作成）。失敗が残る場合は、D-009 の「見直し条件」に従いデザイナーが裁定します。

### Option B — オーナーが変更していない `manual.md` のコピーを QA の作業場所の `repo/` の隣に置く

その後、QA が独立して `run_tests` を実行します。独立性は最も高く、今後の再検証でも入力不足が再発しません。ただし、QA の作業場所にオーナーが置けるかは Studio には分かりません。置けない場合は A に戻ります。
If chosen: QA への Verify Handoff（7l）を、`manual.md` が置かれていることを前提に作成します。合格すれば Play（8）、失敗なら通常の戻りルールに従います。

## Studio recommendation

Option A。

## Reasoning

A は前例（D-008）があり、確実に1回で終わります。結果が 40/40 なら、AC-15 の判定に必要な証拠はそろいます。B は独立性が高いものの、QA の作業場所へ置けるか不明で、置けなければ時間を失います。QA の作業場所に置ける手段が簡単にあるなら B に変えてもかまいません。

## Meanwhile

すべての残りのステップ（7l、Play、Review）は、この答えに依存します。独立して進められる作業はありません。

## Owner decision required

A / B — 選択肢と条件があれば返信してください。A の場合は、`run_tests` の出力（総数、失敗数、失敗メッセージ）も添えてください。

---

**Owner response (2026-10-15):** A。manual.md は変更せず repo/ の隣に置いた環境で python3 -m unittest discover を実行しました（Owner の代理、サンドボックス内）。結果: Ran 40 tests — OK（40件中40件成功、失敗0）。

**Resolution:** Option A を採用。D-010 に記録。AC-15 は合格、Play（8）を開く。
