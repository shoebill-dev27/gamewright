# Phase 13 設計：Goal に予算を持たせ、使い切ったら工程を増やさない

状態: **設計**（2026-10-23。Owner の指示「私が判断しないといけないこと以外は止まらずにそっちで判断して進めて」により、承認待ちで止めずに実装する）

## 1. 課題（Phase 10〜12 の実測。`docs/phase12.md` §8.4）

1. **G-002（ボス戦）が閉じない。**
   - Phase 10 から 131 回の executor を使っても、まだ Build の中にいる。
   - 最初の計画（D-017〜D-020）が、契約試験や証拠の台帳を大量に求めている。その後の Route は、工程を足し続けた（6a〜6l、E0、E1……）。
   - 同じ時期に動かした小さな不具合の Goal は、16 回で閉じた。
2. **Studio には、コストの手がかりがない。**
   - Route は、その Goal にどれだけの手間をかけたかを知らない。
   - orchestration には「範囲・コスト・リスクが、Goal の想定を大きく超えたら Owner に確認する」とある。しかし、何が想定なのかが書かれていないので、この規則が働かない。

## 2. 方針

1. **Goal に予算を持たせる。** `goal.md` に `budget:`（その Goal に要るオペレーションの数の見込み）を書く。Intake が見積もる。
2. **ランナーが、使った数を数えて Route に見せる。**
3. **予算を使い切ったら、Route は工程を増やせない。**
   - 残りの計画のうち、Owner の依頼に要るものだけを進める。
   - 要らないものは `skipped` にする。何が要るかは Goal の中の範囲の判断なので、`game-director` が決める。
   - または、コストを Owner に確認する。
4. 予算を変えられるのは Owner だけ（Resume で）。

## 3. 設計

### 3.1 予算

- `templates/goal.md` の frontmatter に `budget: <N>` を足す。
- **Intake:** 必ず書く（ないと拒否する）。目安は「計画した工程 1 つにつき 2（その Step と、後の Route）、加えて 1 回の戻り分」。
- **Route:** 変えられない（変えたら拒否する）。
- **Resume:** Owner の判断として変えてよい。
- 予算のない古い Goal は、40 として扱う。

### 3.2 数え方と見せ方

- ランナーは、その Goal の Intake、Step、Route、Resume の記録を数える。連続実行（run）の記録は数えない。
- Route と Resume の packet の見出しに、`goal_budget: 65 of 40 operations used — over budget: …` のように書く。

### 3.3 使い切った後

- **ランナーの検証:** 使った数が予算以上のとき、Route が route 表の行を増やしたら拒否する。
  - エラーの文: 「工程を足さない。Owner の依頼に要る計画の仕事を進め、残りは `skipped` にする（範囲は game-director が決める）。またはコストを Owner に確認する。」
- 行を増やさないかぎり、計画済みの工程（QA、Play、Review など）へは進める。
- `orchestration.md` の Loop limits に、この規則を書く。

### 3.4 実地検証：G-002 を予算の規則のもとで続ける

- `runs/p12-boss-run` を `runs/p13-boss-run` にコピーして続ける。
- G-002 の `goal.md` には予算がないので、既定の 40 になる。すでに約 70 オペレーションを使っているので、最初の Route から「予算超過」になる。
- 見ること:
  - Route が工程を足さずに進むか。
  - `game-director` に範囲を決めさせるか、Owner に確認するか。
  - Close に至るか。
- executor: Codex。使えなければ Claude。予算は executor を 40 回追加。
- Owner 確認には、これまでどおり私が推奨案で答える。

## 4. 退けた案、見送った案

| 案 | 理由 |
|---|---|
| 受け入れ基準を「必須」と「あれば良い」に分ける | 設計書、検証、Review の手順を全部変える必要がある。executor がすべてを「必須」にすれば効かない。まず、コストの手がかりと工程を増やさない規則で試す |
| 予算を超えたら Goal を止める | Owner の依頼に要る仕事まで止めてしまう。計画済みの工程には進めるほうがよい |
| 予算を executor の回数で数える | 実行の要求や拒否のやり直しで変わり、Route には見積もりにくい。オペレーションの数のほうが、route 表と対応する |

## 5. 前提とリスク

- 見積もりは粗い。Intake が少なく見積もると、すぐ予算超過になる。その場合も、計画済みの工程には進めるので、Goal は止まらない。
- 行の数だけを見るので、行を書き換えて中身を増やすことは防げない。まずこの単純な形で効くかを見る。

## 6. 変更するファイル

| ファイル | 変更 |
|---|---|
| `scripts/studio_run.py` | 予算の読み取りと数え方、Route と Resume の見出し、Intake と Route の検証 |
| `studio/templates/goal.md` | `budget:` |
| `studio/orchestration.md` | Intake の見積もり、Loop limits の予算の規則 |
| `studio/execution.md` | `goal_budget` の説明 |
| `tests/test_phase2.py` | テスト用の goal に `budget:` |
| `tests/test_phase13.py` | 新規 |
| `docs/phase13.md` | 本書と結果 |

## 7. 検証計画

**決定的テスト**

- Intake は予算を書く。ない場合や、整数でない場合は拒否する。
- Route の packet に、使った数と予算が出る。
- 予算超過のとき:
  - 行を増やす Route は拒否される。
  - 計画済みの工程へ進む Route は通る。
- Route が予算を変えたら拒否される。
- 予算のない Goal は既定の 40 になる。
- 数えるのは、その Goal の Intake、Step、Route、Resume だけ。
- 既存の 147 件がすべて通る。

**実地検証**

- §3.4 のとおり。
