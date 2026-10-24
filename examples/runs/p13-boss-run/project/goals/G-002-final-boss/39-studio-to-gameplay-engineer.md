---
kind: handoff
goal: G-002
seq: 39
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 39: studio → gameplay-engineer — 保存版を実行して検証し、失敗を直し、測定を取る

## Task

38で提出した変更（source_id、boss対応dodger、開始hearts指定、play_run、test_bots_boss.py）を、保存後のソースで実行する。最初のアクションは実行にする。コマンドは38 Findings「実行が必要なコマンド」のとおり。失敗は修正し、測定値をsource idと対応付けて返す。

## Context

G-002はD-015〜D-021の範囲で最終ボス付き連続ランをBuild中。34・36・38は実装と試験を提出したが、保存後の実行結果がない。38は実行枠の割当をStudioに求めて返したが、Studioは枠を割り当てられない。このStepで利用可能な実行経路（プロジェクトのrun_tests／run_bots／run_play）を自分で使う。Owner承認の再取得は不要（D-021）。

## Findings

38の本文を参照。要点:

- 36の追加5試験・文書統合は保存済み（本文確認）。BUILDは0.6-g002-public-32のまま。
- 38の変更は一度も実行されていない。供給済みの98／103件の成功は今回の保存版に帰属しない。
- 38の提出物の構文・回帰（部屋1〜4のdodger結果が不変か）が最大のリスク。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託を加えない。未実行を成功としない。fixtureや独立部屋の時間合算を通常ラン到達の証拠にしない。完成前に独立QAへ送らない。

## Open questions

- 仕様の不足・矛盾があればDesignerへ。なければ「なし」。
- 実行が一度もできなかった場合は、試みたコマンド、出力、具体的な阻害条件を返す。Studioはこれを同じ欠落入力の2回目として扱い、Ownerへ戻す。

## Expected output

1. 保存後suiteの実件数・失敗・source id。失敗は修正して再実行する。
2. 独立3・4（rooms 3,4、bots camper,walker,dodger、fps 30と60別実行）、保持分（rooms 1-2、rooms 3,4のdodger dash、rooms 1-4のFPS比較）、新5番（rooms 5、hearts 3,2、limit、30と60）の結果。dodger部屋1〜4が提出前と同じかを明記。
3. 通常ラン（mode run、fps 30|60、limit 1200、全bot）の同一試行測定。
4. 余力があればV1補完（legacy route表示、弾ID・消滅理由、長時間蓄積）と契約試験の細目。
5. すべて実行済み／未実行を分けて書く。完成後は完成資料つきで`studio`宛て（独立QAへ渡す材料として）。部分成果なら残作業を列挙して`studio`宛て。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/run_driver.py
- Project: repo/session.py
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/38-gameplay-engineer-to-studio.md
