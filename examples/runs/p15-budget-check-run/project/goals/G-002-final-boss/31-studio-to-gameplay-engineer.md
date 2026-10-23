---
kind: handoff
goal: G-002
seq: 31
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 31: studio → gameplay-engineer — 公開経路の連続ラン統合と実測を完成する

## Task

保存済みSession基盤を公開parser・driver・player／traceへ接続し、承認済み仕様と計画の統合Buildを完成する。対応bot、不足試験、説明更新、通常ランの同一試行実測を揃え、結果をstudioへ返す。

## Context

30はSession基盤と境界fixtureの8試験を部分成果として報告した。公開CLIではまだ連続ラン・pause・retryを実行できず、Buildは未完了。独立QA投入は保留している。新しい仕様質問や開始承認待ちはなく、実装継続である。

## Findings

- 30による保存成果は `repo/session.py` と `repo/tests/test_session.py`。供給されたRound 2・3の89 tests成功記録は、この保存後の全成果に対する検証ではない。
- `play.py`はGameを直接生成したまま。Session、試行別入力、反応記憶初期化、pause・境界入力処理、公開両時刻と停止理由の統合が残る。
- player／traceの表示・観測契約、ボス対応dodger、manual／README、不足するボス・実終端・制御試験、比較測定、通常ラン実測が未完了。
- fixtureからの終端retry試験は、正規撃破による到達や実終端からのretryを立証しない。
- 明白な攻略不能・到達不能を示す実測証拠はまだない。

30の基準別残作業表と再現手順を引き継ぎ、仕様・計画の正本と照合して実装する。

## Decisions already made

- D-017：二攻撃の単体ボス、部屋間回復、死亡優先、先頭retry、時刻・表示契約。
- D-019：旧集計の適用終了と共有回帰保持。対応botの開始hearts別・FPS別比較と実測後Designer判断。
- D-021：現状repo/のテキスト実行とStudio内検証で進める。実機供給、指定sha照合、人日見積もり、外部配員の取得は開始条件にしない。

## Constraints

第1〜4部屋の構成と共有戦闘ルールを維持する。新しい戦闘入力、ボス専用チェックポイント、時間合わせだけのHP増加・待機、購入・外部委託・追加金銭を追加しない。

30/60 FPSを対象とする。実機ホストや実gamepadの検証を今回の完了条件にしない。未実行を成功と扱わず、独立部屋の時間合算やfixtureを通常ラン実測へ転用しない。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewの順序を維持する。明白な攻略不能・到達不能が測定で判明した場合は、根拠を付けてstudioへ返しDesigner判断を求める。

## Open questions

新しい仕様質問・開始承認待ちはない。仕様の曖昧さが見つかれば具体的な該当箇所とケースを示して返す。計画が成立しなければ技術上の阻害要因を示す。

## Expected output

結果を `studio` 宛てのHandoffで返す。次を完成・報告する。

1. 保存版に対し `repo/` で `python3 -m unittest discover -s tests` を実行し、実際の件数・結果を確認する。
2. Plan16の公開構文とSessionを接続し、同時刻順序、制御先行、境界・pause中入力破棄、入場時反応記憶初期化、retry時の旧未来入力破棄を検証する。
3. player／traceの仕様§6、即時描画、毎フレーム観測、弾IDと消去理由、build識別、長時間limitと勝敗の分離を完成する。
4. 30の残作業表にあるB1〜B10、実終端からのT基準、C基準の不足を補い、共有回帰を確認する。
5. 公開観測を使うボス対応dodgerとmanual／READMEを完成する。
6. 同一build・方針・初期状態・limitで、独立5番の開始3／2 heartsをそれぞれ30/60 FPS比較する。独立3・4は全bot×各FPSの条件と値を報告する。
7. 正規敵撃破による同一試行の通常ランを実行し、部屋別時間、遷移、ボス入場hearts、被弾・反撃、終端、retry、pause、処理実時間を記録する。

変更ファイル、基準対応、実行対象、コマンドと実結果、測定条件と値、未達事項を分けて記載する。独立QAが再現できるスクリプト・実行手順を含める。自己評価・根拠説明は `## Sender assessment` に分離する。全成果が揃うまで独立QAへの投入を要求しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/30-gameplay-engineer-to-studio.md
