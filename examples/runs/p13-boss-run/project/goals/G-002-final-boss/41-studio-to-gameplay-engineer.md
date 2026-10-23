---
kind: handoff
goal: G-002
seq: 41
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 41: studio → gameplay-engineer — 保存版に残った契約試験・V1補完・pause/retry計測を完了する

## Task

40で実行できた保存版（source id 5145454ab956）を土台に、未実施分を実装・実行して完成資料にする: 契約試験の細目、V1補完、pause・retryを含む通常ラン計測、dodger部屋1〜4の回帰固定。結果はsource idと対応付けてstudioへ返す。

## Context

39の求めに対し、40で保存版のsuite 112件OK、独立3・4、保持分、新5番、通常ラン（dodger勝利: 30fpsで86.967 s、60fpsで103.533 s、被弾0、retry0、pause0）が得られた。コード修正は不要だった。ただし40自身が部分成果としている。独立QAは完成資料を受けてから開く。

## Findings

40から引き継ぐ事実:

- 実行済み: tests 112件OK。独立3・4はdodgerが30/60とも両部屋clear、失0、dash 13/14。新5番は開始hearts 3/2とも30/60でclear、失0。通常ランはcamper・walkerが部屋1で死亡、dodgerのみ勝利。
- 未実施:
  1. V1補完: legacy route表示、弾ID・消滅理由、長時間の観測蓄積。
  2. 契約試験の細目: B3毎frame軌道、B6／B7実dash接触、B9接触無害、B10帯内外、T1〜T4・C2・C3のボス絡み、共有回帰の細目（design/final-boss-and-continuous-run.md、D-017・D-019に従う）。
  3. pause・retryを含む通常ラン計測（run_driverのcontrol構文経由）。botsのplay_runは両方を行わない。
  4. dodger部屋1〜4が提出前と同じか: 提出前の数値の記録はない。今回の実測値（40の保持分の表）を回帰固定の基準として記録し、固定できないものは理由を書く。
  5. 任意: 新5番で30と60の秒数・dashが異なる（約11 s、8対12）。`log on`の判断ログで原因を診断するのは、コストが小さい場合のみ。
- botが被弾0であることは攻撃を回避した根拠にならない。B5〜B10の実接触試験が、ボス攻撃が実際に当たり、かつ回避可能であることの確認になる。
- 通常ランの実測が約1.5〜1.7分でVisionの15〜20分と差があることは、Designerの実測後判断（D-019）の入力であり、ここでHP増加や待機で合わせない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。実機・実gamepad・指定sha照合は不要。

## Constraints

- 第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託は加えない。
- 過去の試験成功を保存版に帰属させない。コードを変更したら再実行し、実行時のsource idを併記する。
- 15〜20分のための調整はしない。

## Open questions

- 仕様が曖昧・矛盾・不足の場合は、決めずにgame-designerへ戻す（Roleの契約）。
- 実行が再び一度も行えない場合は、試みたコマンドと具体的な阻害条件を返す。

## Expected output

- 実装・テストの変更（repo/）と、実行結果（suite件数、新規試験の件数と対象、source id）。
- pause・retry込みの通常ラン計測と、dodger部屋1〜4の回帰固定の結果。
- 完了した項目と未完了の項目の区別。完成資料として独立QAへ送れるかの自己判断。
- 結果は`studio`宛て（Studioが独立QAのHandoffを作るため、Sender assessmentに実装の確信度を分けて書く）。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/public-driver.md
- Project: repo/source_id.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_run_driver.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
