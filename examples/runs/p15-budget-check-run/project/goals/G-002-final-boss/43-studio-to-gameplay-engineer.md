---
kind: handoff
goal: G-002
seq: 43
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 43: studio → gameplay-engineer — 契約試験の細目を、エンジン内部ファイルを読んだうえで実装・実行する（41の分割A）

## Task

保存版（source id `5145454ab956`）に対し、まず現状の試験を実行して基線を確認する。そのうえで契約試験の細目（B3・B6・B7・B9・B10・T1〜T4・C2・C3、共有戦闘の回帰があれば含める）を `game.py`・`session.py`・`play.py` の実際の内部状態に基づいて追加し、実行する。

## Context

G-002（最後に手応えのあるボス戦）のBuild中。40で保存版が初めて実行され、suite 112件OKと測定が得られた。41は残項目（契約試験の細目、V1補完、pause・retry込みの通常ラン計測、dodger部屋1〜4の回帰固定）を求めたが、41のLoadに `game.py`・`session.py`・`play.py`・`manual.md` が無く、42は推測で試験を書くのを避けて何も変更せずに返した。今回はそれらをLoadに追加した。残項目が大きいため、Studioは次のとおり分割する。

- 分割A（本Step、43）：基線確認と契約試験の細目。
- 分割B（後続）：V1補完（legacy route表示、弾ID・消滅理由、長時間観測）と、`bots.play_run` の pause・retry拡張。
- 分割C（後続）：pause・retry込みの通常ラン計測と、dodger部屋1〜4の回帰固定。

## Findings

42の報告（Studioは未検証。内容は取り込まず、事実としてのみ扱う）：

- 42では repo/ の変更も実行もなく、source id は `5145454ab956` のまま。
- `run_driver.py` の `control <秒> pause|resume|retry` は既にある。retry は通常ランの終端でのみ受理される。
- 40の dodger 部屋1〜4の実測（参考値）：両FPSとも4/4 clear、失hearts 0。30fps の dash 合計26、60fps は33。秒数・dash数は診断用の参考で、提出前の記録は無く、提出前との同一性は確認できない。
- 分割Aの受け入れの根拠は、ボス攻撃が実際に当たり、かつ回避できることを示す実接触試験（B5〜B10）である。botの被弾0は根拠にならない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。実機・実gamepad・指定sha照合は不要。

## Constraints

- 第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。
- 新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託は加えない。15〜20分に合わせる調整はしない。
- 内部名（弾ID、消滅理由、`spent`、保護の残り時間、イベント名）は `game.py`・`session.py`・`play.py` の実コードで確認してから使う。推測した名前で試験を書かない。
- 過去の試験成功を保存版に帰属させない。コードや試験を変更したら再実行し、実行時のsource idを併記する。
- 設計と矛盾する挙動を見つけたら、実装側を直す前に仕様（design/final-boss-and-continuous-run.md、D-017）と照らし、仕様が欠けているなら推測せず返す。
- 実行手段の割当はStudioからは保証できない。使える実行経路で次の順に進める：(1) `tests` で112件と source id を確認、(2) 試験を追加して `tests`、(3) 失敗は試験の誤りか実装の不具合かを切り分けて修正し再実行。

## Open questions

- 仕様の不足・矛盾が見つかった場合のみ、具体的な箇所を示して返す。現時点でDesignerへの質問はない。
- 提出前の dodger 数値は、パケットに記録が無いため存在を確認できていない。分割Cで、40の表を診断用の参考値とし、試験は clear・失hearts 0・両FPS差・部屋3〜4のdash有無といった緩い性質に限る方針とする。本Stepでは不要。

## Expected output

- 項目ごと（B3・B6・B7・B9・B10・T1〜T4・C2・C3・共有回帰）に、追加した試験名、実行結果、実行時のsource idを対応付けた表。実行できなかった項目は理由とともに未実施と明記する。
- 実装の不具合を見つけて直した場合は、その内容と再実行結果。
- 分割B・Cに回す残項目の一覧。
- 結果は `studio` 宛てに返す（次のStepは独立QAではなく、残りのBuildまたはQAの選択をStudioが行う）。一部しか終えられなくても、事実どおりの項目別状況を返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/public-driver.md
- Project: repo/source_id.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_run_driver.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/42-gameplay-engineer-to-studio.md
