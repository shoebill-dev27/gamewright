---
kind: escalation
goal: G-001
seq: 21
from: studio
to: owner
status: resolved
decision: D-005
---
# 21: オーナーの判断が必要 — `manual.md` を誰がどうやって書くか

## Question

ビルド 0.5 のコードは完成しましたが、プロジェクト直下の `manual.md` を書ける担当がいません。Owner が手で置くか、書き込み権限を与えるか、`manual.md` なしで先へ進むかを選んでください。

## Why this needs the Owner

`manual.md` の作成が2回続けて同じ理由(書き込み権限がない)で差し戻されました(18 と 20)。その間に新しい入力はありません。`studio/orchestration.md` の Loop limits により、同じ入力不足を3回目も Role に回すことはできません。Owner への escalation が必要です。どの Role も作れない材料(書き込み権限)で作業が止まっているケースにも当たります。

状況:
- コード T1–T7, T9 は完了し、34 テスト中 33 が通っています(18)。
- 残りは T8 の `manual.md` だけです。ドラフトは `18-gameplay-engineer-to-studio.md` の "Draft `manual.md`" にあります。
- `ManualTest` は `REPO.parent / "manual.md"`(プロジェクト直下)を読みます。`repo/` 以下に置いても満たされません。
- QA の AC-15 と V-5 は `manual.md` に依存します。
- gameplay-engineer がドラフトを実装と照らし合わせて読んだ限り、矛盾はなく、そのまま置けるはずです。ただしテストは未実行です。

## Options

### Option A — Owner がドラフトを手で置く

Owner が 18 の "Draft `manual.md`" を、変更せずにプロジェクト直下へ `manual.md` として保存します。
コスト: Owner の手作業が1回。リスクは小さく、いつでも元に戻せます。
If chosen: Owner が置いたと返信したら、Studio は gameplay-engineer に `run_tests`(34/34 の確認)だけを依頼します。通れば QA(Sender assessment なしの新しい Handoff)と art-director(視覚レビュー)を並列で開きます。

### Option B — gameplay-engineer に `manual.md` の書き込み権限を与える

次の gameplay-engineer のステップの書き込み許可リストに `manual.md` を加えます。
コスト: 実行環境の設定変更。D-004 の項目5(マニュアルは gameplay-engineer の担当)に沿います。
If chosen: Studio は 19 と同じ内容で gameplay-engineer を再実行します(ドラフトを配置し、`run_tests` を確認)。通れば Option A と同じ Verify へ進みます。

### Option C — `manual.md` なしで Verify に進む

`manual.md` をいったん後回しにして、QA と art-director に進みます。
コスト: AC-15 と V-5 は検証不能になり、`ManualTest` が失敗したままです。後で同じ問題に戻ります。
If chosen: QA の Handoff に「AC-15・V-5・ManualTest は対象外」と明記して Verify を開きます。`manual.md` は最終 Review 前に再度 escalate します。

## Studio recommendation

Option A(手軽さを優先するなら)。実行環境の設定を変えられるなら Option B でも構いません。

## Reasoning

ドラフトは確認済みで、置くだけで済みます。Option A はすぐできて、Option B と結果は同じです。Option B は担当の筋は通りますが、設定変更が必要です。Option C は問題を先送りするだけで、AC-15・V-5 が未検証のまま Play と Review に進むことになるため勧めません。ドラフトの実装との整合は読んで確かめただけでテストは未実行ですが、置いた後に `run_tests` で確認できます。

## Meanwhile

Nothing; all remaining steps depend on this answer. (Verify、Play、Review はすべて `manual.md` の有無に依存します。)

## Owner decision required

A / B / C — 選択肢を返信してください(条件があれば併せて)。A の場合は、置き終わったことも知らせてください。

---

**Owner response (2026-10-15):** A。18 の Draft manual.md を変更せずにプロジェクト直下の manual.md として置きました（Owner の代理として Studio の推奨案を採用）。

**Resolved:** D-005 (`decisions/D-005-owner-places-manual-draft.md`).
