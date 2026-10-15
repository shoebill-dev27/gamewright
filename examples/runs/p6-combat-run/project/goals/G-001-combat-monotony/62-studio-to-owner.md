---
kind: escalation
goal: G-001
seq: 62
from: studio
to: owner
status: open
decision:
---
# 62: オーナーの判断が必要 — マニュアル更新分をいつ置くか

## Question

`manual.md` の更新分(デザイナーの草案とアートディレクターの V-15 文面)を、Build の完了を待たず今すぐオーナーが置いてよいですか。

## Why this needs the Owner

`manual.md` はオーナーが置く運用です(D-005、D-007)。Studio も各 Role もこのファイルを書きません。作業に支障はなく、どの時点で置くかはオーナーの運用上の選択です。

## Options

### Option A — 今すぐ置く(推奨)

`goals/G-001-combat-monotony/59-game-designer-to-studio.md` のマニュアル草案と、`design/combat-visuals.md` の V-15 が指す `manual.md#on-screen`・`manual.md#what-you-hear-and-read` の文面を `manual.md` に置く。Build と並行して進むので、Verify の時点でマニュアルが揃っており、AC-15(`ManualTest`)を再度ブロックせずに済む。Build 中に仕様が変わった場合は、置いた文面を一度修正する可能性がある。
If chosen: Build(61)は継続。Verify(13a)は、マニュアルが置かれた状態で `run_tests` を含めて走らせる。結果は D-0xx として記録する。

### Option B — Build の完了後にまとめて置く

Build の結果を見てから、一度で置く。文面の手戻りは減るが、Verify の開始が置くまで遅れる。
If chosen: Build 完了後の Route で再度この依頼を出し、Verify はそのあとに開く。

## Studio recommendation

Option A。

## Reasoning

過去の経緯(D-008〜D-010)では、マニュアルが `repo/` の隣になかったために AC-15 が何度も止まりました。先に置いておけば同じ停止を避けられます。Build で仕様が変わる可能性は小さく(表示とテキストのみ)、変わっても修正は一度で済みます。

## Meanwhile

Build(61)は並行して進みます。マニュアル更新分には依存しません。

## Owner decision required

A / B — オプションを返信してください。置いたら、置いた箇所(節名)も一言添えてください。
