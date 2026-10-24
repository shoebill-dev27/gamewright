---
kind: handoff
goal: G-002
seq: 37
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 37: studio → gameplay-engineer — 観測・対応botを実装し、保存版の検証資料を完成する

## Task

36の提出変更の保存状態を確認し、公開観測とボス対応botを優先して残る統合Buildを進める。利用可能な実行経路で保存後suite、両FPS比較、正規敵撃破による通常ラン同一試行測定を行い、実装残と実行基盤依存を分けてstudioへ返す。

## Context

36は34の短射修正と2試験の存在をパケット本文で確認し、追加契約試験と文書EDITを提出した。保存後実行は行っておらず、観測・bot・契約網羅・測定は未完了である。独立QAの開始条件は満たされていない。

D-021のBuild承認は有効。新しい仕様質問やOwner承認待ちはない。36が報告した実行枠枯渇は前Stepの条件であり、本Stepでの回復も継続も仮定しない。このRouteは実行枠を割り当てたという証拠ではない。

## Findings

36の基準別対応表と再現手順を未完了一覧として使用する。供給された98／103 tests等の成功記録は今回保存版への帰属が未確定であり、保存後成功として扱わない。

優先順：
1. 実ファイルまたは今回供給された正規本文で、36の試験・文書変更の保存状態を確認する。未保存なら必要な変更を出力プロトコルで提出し、保存済みとは区別する。
2. V1の表示・イベント識別・弾観測を補い、ボス対応botが公開観測のみで判断できる経路を整える。長時間の観測蓄積も確認する。
3. 独立1〜4の既存方針を保持し、ボス対応dodger、開始3／2 hearts指定、clear／death／unfinishedの明示を実装する。
4. 36の基準表に沿い不足契約試験と共有回帰対応を完成する。
5. 利用可能な実行経路で下記測定を取得する。実行枠がなくても、それだけを理由に可能な実装を止めない。

実行対象はgame.py、session.py、play.py、run_driver.py、bots.py、testsを含むソース集合で識別する。BUILD文字列だけで識別を済ませない。正規本文と未保存提案、変更前結果と変更後結果を分離する。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。実機・指定sha・費用承認の再取得は不要。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託・追加金銭を加えない。

未実行を成功としない。fixture、状態注入、独立部屋時間の合算を通常ラン到達・時間の証拠にしない。仕様の不足・矛盾はEngineerが決めず、具体的なケースを返す。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。明白な対処不能・到達不能が判明したら証拠を添えて返す。

## Open questions

- 36の提出変更は今回の正規ソースに保存されているか。
- 今回利用可能なtests／trace／botsまたは代替実行経路は何か。
- 未完了実装と測定のうち、本Stepで何が保存・実行できたか。

実行経路が使えない場合は、今回直接確認した条件、未確認の経路、必要な基盤対応を分けて記す。存在しない実行枠や利用権限を仮定しない。同じ入力不足だけで再返却する場合は、その旨を明示する。

## Expected output

実装・試験・文書変更と、studio宛てHandoffを提出する。次を含める：

- 保存済み／今回提出／未完了の区別と対象ソース識別。
- 保存後suiteの実コマンド、実件数、結果。実行不能なら具体的な阻害条件。
- 基準別の証拠と残件。追加試験は合格判定と区別する。
- 独立3・4の全bot×30/60 FPS、保持する1〜2比較・3〜4dash、新5の対応dodger開始3／2 hearts別の比較。方針、反応0.15秒、limit、初期位置・向きを記録する。
- 正規敵撃破によるmode runをまずlimit1200で実施し、同一試行の部屋時間、4遷移、ボス入場hearts、被弾、反撃、終端、retry、pauseを記録する。run／room時刻、driver秒、processing実時間を分離し、死亡・未完了も報告する。
- 各入力・結果と実行対象ソースの対応。pauseと終端待機を戦闘時間へ加えない。

完成前に独立QAへ送らず、完成資料または具体的な阻害報告をstudioへ返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_run_driver.py
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
- Previous handoff: goals/G-002-final-boss/36-gameplay-engineer-to-studio.md
