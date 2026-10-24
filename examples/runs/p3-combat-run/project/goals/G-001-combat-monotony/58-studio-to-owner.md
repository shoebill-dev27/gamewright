---
kind: escalation
goal: G-001
seq: 58
from: studio
to: owner
status: resolved
decision: D-010
---
# 58: Owner decision needed — 数えた記録がないまま Phase 1 をどう扱うか

## Question

Phase 1 のプレイテストは、このドライランでは実プレイも回数の記録もできませんでした。基準 1・2 を「未判定」として Review に進めてよいですか。それとも実プレイの記録を用意しますか。

## Why this needs the Owner

`orchestration.md` の escalation トリガー「どの Role も作れない情報で作業が止まっている」に当たります。必要なのは、ビルドを実際に動かして数えた記録です(Part A の 50 回の試行、Part C の測定値)。Playtester はテキストの記述 `sim/build-0.8.md` しか読めず、手元には時計もログも操作入力もありません(ハンドオフ 57)。再実行しても同じ結果になります。D-009 は基準 1・2 を「プレイテストで回数から判定する」と決めており、数えた記録なしに「達成」とは言えません。Goal の扱い(判定を保留して進むか、止めるか)を決めるのは Owner です。

## Options

### Option A — 基準 1・2 を「未判定」として受け入れ、Review へ進む

Phase 1 は「検証済み。基準 1・2 は未判定」と記録します。Game Director が Review で、記述からの読み取りだけで足りるか、Phase 2 に進むかを判断します。リスクは、単調さが本当に減ったかを実測できないことです。判断は D-002 の「B の次に A」に従う読み取りになります。やり直しは可能です。後から実プレイの記録が出れば、再 Review できます。
If chosen: Decision(`decided_by: owner`)を記録します。`game-director` に Review(ステップ 12)を、Phase 1 を「達成」とは扱わない条件付きで渡します。Phase 2(ステップ 9 以降)は Review の結果次第です。

### Option B — 実プレイの記録を用意する

Owner、または実行環境のある人が、`sim/build-0.8.md` に相当するビルドを実際に動かします。記録票(ハンドオフ 56 の Part A・B・C)を埋めて渡します。
If chosen: 記録を受け取った後、Studio が Playtester 用の新しいハンドオフを作り直します。回数を確認して Review に進みます。

### Option C — ここで止める

Goal を現状のまま `abandoned` にするか、Phase 1 までの結果で閉じます。
If chosen: Studio が Outcome に現状の結果と未解決事項を書いて Goal を閉じます。

## Studio recommendation

Option A。

## Reasoning

これはドライランで、実ビルドも実リポジトリもありません。B を満たせる環境は現状にありません。A なら、「達成」と言わずに「未判定」と記録することで、Review の正直さを保ったまま進められます。Game Director が Phase 2 の要否を判断できます。実プレイの記録が手に入る見込みが現実にある場合は、B のほうがよい推奨になります。

## Meanwhile

Nothing; all remaining steps (Review, Phase 2) depend on this answer.

## Owner decision required

A / B / C — 選んだ選択肢と条件があれば返信してください。

---

**Owner response (2026-10-11):** A。模擬専用のサンプルなので、基準1・2は未判定のまま Review に進めてください。Phase 2（挙動のバリエーション）は今回は行わず、Review の結果で Goal を閉じてください。

**Resolved:** recorded as [D-010](../../decisions/D-010-owner-accepts-unjudged-criteria-and-skips-phase-2.md).
