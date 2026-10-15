---
kind: escalation
goal: G-001
seq: 79
from: studio
to: owner
status: open
decision:
---
# 79: オーナーの作業依頼 — AC-15 のテスト実行と V-15 マニュアル文の配置

## Question

`repo/` の隣に現在の `manual.md` を置いたままテストスイートを実行し、結果を教えていただけますか。あわせて 73 の V-15 の文を `manual.md` に入れていただけますか。

## Why this needs the Owner

QA の環境には `manual.md` が無く、QA は `manual.md` を置けません(77)。AC-15 の `ManualTest` 2件が実行できず、V-15 の文もまだ入っていません。どちらもオーナーにしかできない作業です(以前の D-007〜D-010 と同じ手順)。

## Options

### Option A — 実行して、文も入れる

`python3 -m unittest discover -s tests` を、変更前の `manual.md` を `repo/` の隣に置いて実行し、テスト数と失敗したテスト名を報告。続いて 73 の V-15 の文を `manual.md` に入れる(`manual.md` を変えた後は、再度スイートを実行して結果を報告)。
If chosen: Studio は結果を Decision に記録し、AC-15 を確定します。V-15 は QA が確認します。失敗があればデザイナーへ(2回目の AC-15 失敗はテクニカルディレクターへ)。

### Option B — 実行だけ(V-15 は後で)

スイートの結果だけ報告。
If chosen: AC-15 は確定しますが、V-15 は未確認のまま残り、Review では「未確認」として扱います。

## Studio recommendation

Option A。QA の見込みでは 73 テスト・失敗 0(`ManualTest` が通れば)です。

## Reasoning

QA は `manual.md` を読んで AC-15 を通ると見ています。実行結果で確定できます。V-15 を入れないと、Verify が閉じられません。

## Meanwhile

アートディレクターの視覚レビュー(78)は並行して進みます。この返事を待たずに進みます。

## Owner decision required

A / B — 選択肢と、テスト数・失敗名(あれば)を返信してください。
