---
kind: decision
id: D-021
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-20
supersedes: D-020
---
# D-021: テキストビルドとStudio内検証でBuildへ進む

## Decision

Ownerは22の案Aを選択し、供給・検証・予算の回答権限者をすべてOwnerとした。実機ホスト・実gamepad・外部配員を今回の開始条件から除き、既存のテキスト表示とスクリプト実行によるBuildを承認した。

Ownerの回答全文：

> 案A。回答の権限者はすべて Owner（私）で、ここで回答します。(1) 実行経路: project.md の build: と run_tests / run_play / run_trace / run_bots がそのまま実行経路です。gameplay-engineer と qa は Step の中で @run を使い、サンドボックスでテスト・プレイ・トレース・ボットを実行できます（G-001 と同じ）。基線は repo/ の現状で、指定 sha の確認は不要です。project.md の「build 0.4」は古い記述で、repo/ が正です。(2) 実機・gamepad・デスクトップの表示環境はなく、用意もしません。Constraints の「Desktop, keyboard and gamepad」は製品の対象環境で、今回の検証環境の要求ではありません。検証は G-001 と同じく、テキスト表示のビルドとスクリプト実行で行います。(3) 独立した QA と Play は、Studio の qa と playtester の Step が担います。外部の配員はありません。(4) 費用: 購入・外部委託・追加の金銭は一切ありません。予算は Studio の通常の Step の範囲で、人日の見積もりは不要です。以上で D-020 の条件は満たされたものとして、Build へ進んでください。

実行基線は作業開始時のrepo/とし、指定shaとの照合は要求しない。project.mdのbuild 0.4表記は基線の根拠にしない。購入・外部委託・追加金銭支出は認めない。人日見積もりや外部検証枠の取得を開始条件にしない。

D-020に代わる開始条件として本Decisionを適用する。D-020に由来する実機ホスト、実gamepad、外部配員、費用見積もり取得の要求は後続計画より本Decisionを優先する。D-015〜D-019のゲーム体験、共有戦闘回帰、30/60 FPS、実測後Designer判断は維持する。独立QA・限定Art Verify・独立PlayはStudio内の別Stepで行う。

これはOwnerによる開始許可と検証範囲の変更であり、実行成功、受け入れ基準合格、体験Goal達成の証拠ではない。

## Rationale

Owner自身から不足していた供給・実行経路・予算方針への回答があり、今回の検証をG-001と同じテキストビルド方式に限定した。Studioが同じ供給確認を繰り返す必要はなく、既存仕様・計画に基づくBuildへ進める。

## Alternatives considered

- 実機ホストと実gamepadを用意する：Ownerが用意しないと明示したため採らない。
- 見積もり・調達条件を取得する案B：追加金銭を使わず通常Step内で進めるため採らない。
- 条件整備まで停止する案C：OwnerがBuild開始を明示したため採らない。

## Revisit when

通常のStudio Stepでは実行できない具体的な障害、追加支出の必要性、またはテキスト方式では仕様の意味を定められない矛盾が判明したとき。製品の実機対応を検証する別のGoalを開始するとき。
