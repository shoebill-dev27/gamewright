# Phase 11 設計：Build の続きを「質問」と分け、書いたビルドをその場で試験する

状態: **設計**（2026-10-21。Owner の指示「どんどん進めてって」「次は」により、承認待ちで止めずに実装する）

## 1. 課題（Phase 10 の実測。`runs/p10-boss-run`、`docs/phase10.md` §8.5）

1. **「作業の続き」が `question` として返された。**
   - エンジニアは 12 回のうち 8 回、`question` を返した。仕様に分からない点はなく、作業が残っているだけだった。
   - `question` は本来「足りない情報がある」という意味である。
     - 歯止めは「`question` が 2 回続いたら止める」ので、作業が進んでいても run が止まった。
     - orchestration の規則では、「同じ情報が足りないまま `question` が 2 回続いたら Owner に確認する」。誤った Owner 確認につながりうる。
2. **書いたビルドは、その Step の中では試験されない。**
   - 実行の要求（run round）は、変更案に対して行われる。最後の答えで書いたファイルそのものは、誰も試験しないまま次の Step に渡る。
   - Codex は「保存後の試験が要る」と言って毎回作業を残した。この条件は、その Step の中では満たせない。
3. **Technical Director はビルドを実行できない。**
   - Role に `runs:` がない。
   - そのため、実行の経路を確かめられないことが Owner 確認の理由になった（2 件目）。
4. **G-002 が Close していない。** Close での `project.md` の現状の更新を、実地で確かめられていない。

## 2. 方針

1. Handoff の結果（outcome）に **`partial`** を足す。意味は「作業の途中で、同じ Role の次の Step で続ける。足りない情報はない」。
2. **ビルドのファイルを書いた Step の後、ランナーがそのビルドで試験を走らせ、結果を Handoff に書き足す。**
3. Technical Director に、試験とトレースの実行を許す。
4. G-002 を Close まで進める。

## 3. 設計

### 3.1 `partial`（課題 1）

- `templates/handoff.md` の outcome に `partial` を足す。
- `orchestration.md` の規則:
  - `partial` を受けた Route は、同じ Role に続きを開く。Owner への確認の理由にはしない。
  - 歯止め: 同じ仕事で `partial` が 3 回続いたら、`technical-director` に回して、分け方や計画を見直す（Loop limits に 1 行足す）。
- ランナーの歯止め:
  - 「`question` が 2 回続いたら止める」は、`question` だけを数える。`partial` は数えない。
  - 「1 回の run で同じ Role を 4 回目に開こうとしたら止める」は、そのまま残す。
- エンジニアの Role の「Hands back」に、`partial` の使い方を書く。

### 3.2 書いたビルドの試験（課題 2）

- 対象: ビルドのファイルを 1 つ以上書いた Step。プロジェクトが `run_tests` を宣言している場合に限る。
- 手順:
  - 答えが検証を通った後、書き込む前に、ランナーが行う。
  - 書かれるファイルを当てたビルドの新しいコピーで、`run_tests` をサンドボックスの中で走らせる（実行要求と同じ仕組み）。
  - 結果を、出す Handoff の `## Load` の前に、`## Build check` として書き足してから書き込む。

  ```text
  ## Build check

  The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as
  this step wrote it: exit 0 (0.4 s).

  （出力の末尾。最大 2,000 字）
  ```

- 試験が失敗しても、答えは拒否しない。結果を事実として残し、Route が戻し先を決める。
  - 拒否にすると、作業途中（`partial`）の Build を書けなくなる。
- 記録: 結果を `build-check.json` に保存する。Handoff のハッシュは、書き足した後の内容で記録する。
- executor への案内:
  - 末尾の「答えの形」に、1 文を足す: 「書いたビルドは、ランナーがその場で試験し、結果を Handoff に添える。最後の答えの後に、もう一度試験を求める必要はない。」
  - `execution.md` の Build runs の節にも同じことを書く。

### 3.3 Technical Director の実行（課題 3）

- `studio/roles/technical-director.md` の frontmatter に `runs: tests, trace` を足す。
- 計画のために、現状のビルドを試験・トレースできる。ビルドを書く権限は持たないまま。

### 3.4 G-002 を Close まで（課題 4）

- `runs/p10-boss-run` を `runs/p11-boss-run` にコピーし、そのまま続ける（記録 062 以降が Phase 11）。
- executor: Codex。Phase 10 で問題が出たモデルで、§3.1 と §3.2 が効くかを確かめる。
  - 利用上限で止まったら、戻るのを待って再開する。
- 予算: executor を 40 回追加（合計 118 回まで）。超えそうなら止めて報告する。
- Owner への確認には、これまでどおり私が推奨案を採用して答える。
- Close したら、次のものを確かめる。
  - `project.md` の現状が更新されたか。
  - 外部の判定 B1〜B3。

## 4. 退けた案、見送った案

| 案 | 理由 |
|---|---|
| 1 回の Step の実行回数（3 回）を増やす | 実行 1 回ごとに executor が 1 回増える。§3.2 で、最後の確認は executor なしで行える |
| 試験に失敗した最後の答えを拒否する | 途中の Build を書けなくなる。拒否のやり直しも executor を使う |
| `partial` を歯止めの回数からすべて外す | 終わらない Build を止める仕組みがなくなる。「4 回目」の歯止めを残す |
| 計画が膨らむことへの上限（Phase 10 の候補 4） | **見送り。** 何を数えるかの根拠がまだない。今回の Build の進み方を見てから決める |

## 5. 前提とリスク

- Codex が `partial` を使うかどうかは分からない。使わなければ、Phase 10 と同じく歯止めで止まる。数えて報告する。
- `## Build check` はランナーが書く節で、送り手の自己評価ではない。QA にもそのまま届く。QA は自分でも検証するので、独立性は損なわない。
- 試験に時間がかかるビルドでは、Step ごとに最大 30 秒増える。

## 6. 変更するファイル

| ファイル | 変更 |
|---|---|
| `scripts/studio_run.py` | 書いたビルドの試験と `## Build check`、歯止めの数え方、答えの形の 1 文 |
| `studio/templates/handoff.md` | outcome に `partial` |
| `studio/orchestration.md` | `partial` の扱いと歯止め |
| `studio/execution.md` | Build check の説明、歯止めの表 |
| `studio/roles/gameplay-engineer.md` | `partial` の使い方 |
| `studio/roles/technical-director.md` | `runs: tests, trace` |
| `tests/test_studio.py` | outcome の一覧に `partial` |
| `tests/test_phase11.py` | 新規 |
| `docs/phase11.md` | 本書と結果 |

## 7. 検証計画

**決定的テスト**

- ビルドを書いた Step の Handoff に、`## Build check` が `## Load` の前に入る。結果は書いたファイルそのものに対するもので、失敗も記録される。
- ビルドを書かない Step、`run_tests` のないプロジェクトでは、何も足さない。
- `partial` が 2 回続いても、`question` の歯止めは止めない。「4 回目」の歯止めは止める。
- Technical Director の packet で、実行の要求が使える。
- 既存の 126 件がすべて通る。

**実地検証（Codex）**

- G-002 を Close まで進める（executor を 40 回追加まで）。
- 確かめること:
  - エンジニアの `partial` と `question` の数。
  - `## Build check` の結果。
  - Close での `project.md` の更新。
  - B1〜B3。
