---
kind: handoff
goal: G-002
seq: 35
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 35: studio → gameplay-engineer — 保存版を検証し統合Buildを完成する

## Task

34に記録された保存対象を現行repo/と照合し、保存版の検証から統合Buildを継続する。承認済み仕様・計画に従い、基準別不足、公開表示・観測、対応bot、文書統合、正規撃破による同一試行測定を完成し、結果をstudioへ返す。

## Context

34は短射の発射frameに移動・加齢しない変更と2試験を報告したが、保存後の実行は行っていない。前Stepの実行round残数は0だった。今回の実行可能回数や、実行環境が回復したことは未確認である。

新しい仕様質問やOwner承認待ちはない。D-021により現状repo/とStudio内のテキスト検証で進める。実機供給、指定sha照合、開始承認の再取得は不要。

## Findings

34の「基準別対応と未達」「測定条件と値」「再開・独立再現のための手順」を残作業一覧として使う。対応表は合格判定ではない。

優先して次を行う。

1. repo/game.pyとrepo/tests/test_boss_contract.pyを確認し、34の短射修正と2試験の保存有無を特定する。提案のみの試験や未保存の内容を実装済みと扱わない。
2. 実行が可能なら保存版suiteを実行する。短射の発射位置・age0、次frameからの移動・加齢、発射1秒後の寿命消去と回復開始、早期接触・吸収でもactive時間が変わらないことを両FPSで確認する。
3. R1〜R5、B1〜B10、T1〜T4、C1〜C3、V1と共有回帰の不足を補う。公開出力、旧構文経路、弾の識別と消去理由、pause、終端・retry、反応記憶・未来入力破棄も含める。
4. 公開観測のみを使うボス対応dodgerを実装し、反応間隔0.15秒、同一方針・limitで独立5番の開始3／2 heartsをそれぞれ30／60 FPSで比較する。独立3・4の全bot結果と、D-019が保持する共有比較も分けて報告する。
5. 正規敵を倒す同一試行で通常ランを測定する。部屋別時間、4回の遷移、ボス入場hearts、被弾、回復中反撃、終端、retry、pauseを記録する。simulation run／room時刻、driver時刻、processing実時間を区別する。
6. manual／READMEを公開driverへ統合し、実装・検証状態を正確に記載する。

公開driverの識別文字列だけでは34の戦闘修正前後を区別できない。測定対象のソースを特定できる識別を付け、コマンド、入力、条件、結果と対応付ける。供給済み96／102 tests成功を今回の保存版へ帰属させない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示の仕様契約。
- D-019：旧集計の適用終了、保持する共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repo/とStudio内テキスト検証でBuildを進める。実機・指定sha・費用承認を再取得しない。

## Constraints

第1〜4部屋の構成、共有戦闘規則と保持対象の回帰を維持する。旧13集計を復活させない。新戦闘入力、ボスcheckpoint、時間合わせのHP増加・待機、購入・外部委託・追加金銭を追加しない。

仕様の曖昧さはDesignerへ、計画の不成立はTechnical Directorへ判断を返す。数値ゲートやゲーム内容をStudioの指示として新設しない。

未実行を成功と報告しない。fixtureや独立部屋時間の合算を、通常ラン到達・所要時間の証拠にしない。

## Open questions

現在の操作で保存後suite・trace・botsを実行できるか。前Stepの上限枯渇は今回の実行可否を証明しないため、利用可能な実行経路と上限を確認する。

実行不能なら、実行しないまま進められる承認内の実装を進め、何の実行経路が不足し、Role内で解消できるか、誰が何を供給する必要があるかを具体的に返す。同じ入力を求めるだけの継続依頼にしない。

## Expected output

studio宛てのHandoffに以下を揃える。

- 保存された変更、対象ソースの識別、実行コマンド・入力・実結果。
- 基準別の実装・試験対応と未完了事項。
- 両FPSのbot結果、同一試行の通常ラン測定条件と値、独立再現手順。
- 公開表示・文書の利用方法と検証状態。
- 実行不能や仕様・計画上の問題が残る場合、その具体的な阻害条件。

独立QAへの投入可否はStudioが完成資料から判断する。明白な対処不能・到達不能が見つかれば、証拠を添えて報告しDesigner判断を前倒しできるようにする。後続は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewとする。

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
- Previous handoff: goals/G-002-final-boss/34-gameplay-engineer-to-studio.md
