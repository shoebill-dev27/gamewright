---
kind: handoff
goal: G-002
seq: 59
from: studio
to: qa
stage: Verify
outcome: routed
---
# 59: studio → qa — 追加実行で独立検証の未確認項目を解消する

## Task

保存ビルドを仕様・受入基準から独立検証し、58で未確認だった項目を、ソース・テスト本文の確認と追加実行で解消する。30/60 FPS別の基準対応表と再現可能な証拠をStudioへ返す。

## Context

58は実行枠を使い切った状態で収録結果を評価し、証拠不足によるfailを返した。再現済みの製品不具合や仕様未定義を示したものではないため、修正依頼ではなく独立QAを継続する。

対象はrepo/のテキスト・スクリプト方式。以前の収録出力の識別はbuild `0.6-g002-public-32`、source_id `04fa2b1c168a`。現在の保存ソースの識別を記録し、異なる場合は証拠を混同しない。旧指定shaとの一致は要求しない。

## Findings

58の詳細な確認済み／未確認区分を引き継ぐ。152 tests成功だけでは、テスト条件・assert・基準対応を確認していない項目のpassにならない。

優先して補う証拠：

1. 保存ソースとテスト本文を確認し、R1〜R5、B1〜B10、T1〜T4、C1〜C3、V1、D-022のL/S/O各基準について、条件・操作列・状態・イベント・assertを対応付ける。既存試験で十分な項目はその根拠を示し、不足条件を追加実行する。
2. 公開連続ランを両FPS・player/traceで再生し、正規敵の撃破、全入場、境界、終端、retry、summaryを対照する。同一試行の部屋別時間・遷移・ラン時刻・pause・終端待機を区別する。
3. 回復hearts境界、遷移入力、両攻撃の照準固定・距離0・壁・弾寿命、直交回避、dash接触消費、保護終了、非致死／致死swipe、回復中攻撃、接触帯を両FPSで確認する。
4. 残弾を持つ終端、同フレーム勝敗優先、終端後の入力と状態不変、pause対象状態、limit優先、retry初期化を確認する。旧未来入力破棄は、新attemptを旧入力時刻より先まで生存させるか、破棄された入力列を直接観測する。旧入力時刻より前の自然死亡では証明にならない。
5. D-019の保持回帰を確認する。walkerの独立1〜2、walker／camperの独立3・4、被弾源と判断ログを補う。ボスbotは同一方針・同一初期状態・観測可能情報のみという条件を、全判断経路と算出元から確認する。dodgerの収録値のみで条件全体をpassにしない。
6. 共有combat基準1〜11、17〜21とstep68・72・94の保持部分を追跡する。cap遅延の一般上限と旧第5部屋の置換範囲を含める。
7. D-022の旧経路表示、弾ID・消滅理由の全ライフサイクル、playerへの非露出、観測間隔変更と既定値、範囲外入力、長時間出力、全終了条件のsummaryを確認する。

通常生成入力再生の収録値は30 FPS 86.966667秒、60 FPS 103.533333秒。独立ボスdodgerは21.63秒／32.87秒。これらは人間の体験時間ではなく、追加の秒数ゲートも定められていない。時間差と判断ログは後続Designerへ残す。

## Decisions already made

- D-017：二攻撃、連続ラン、境界回復、終端、pause・retry・時計の契約。
- D-019：旧集計の適用終了、保持回帰、条件付きbot比較、実測後Designer判断。
- D-021：テキスト・スクリプト方式とStudio内独立検証。実機供給・旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の追加契約。

## Constraints

- 製品コードと仕様は変更しない。検証用入力・一時的な検証スクリプトは製品変更と分け、再現方法を残す。
- 実装者の自己評価・説明を検証根拠にしない。56およびそれ以前のEngineer報告はLoadに含めない。
- controlled fixture、生成入力再生、bot、独立Playを区別する。
- 未確認をpassにしない。明確な基準違反と証拠不足を分ける。
- 新しい難度・時間ゲートを設定しない。実機対応済みと判定しない。
- 実行枠は重要な未確認条件へ配分し、完全ログを保存して報告には必要な抜粋と参照を示す。

## Open questions

- 各基準について、両FPSの独立証拠が揃うか。
- 追加実行で製品の基準違反が再現するか。
- 検証に必要な実行・閲覧機能が不足する場合、具体的に何が利用できず、何を供給すれば残りを検証できるか。

## Expected output

結果を`to: studio`で返す。基準別・FPS別のpass/fail/未確認、使用ソース識別、実行コマンド、入力、観測・assert、完全ログの参照、残る制約を記載する。既存試験を根拠にする場合は対応テストと条件を明記する。

基準違反があれば最小再現と期待／実際を示す。実行機能が足りない場合は不足を具体化し、同じ収録出力の再評価だけで完了としない。作業途中で何も不足していなければpartialとし、残作業を明示する。

合格後は限定Art Verify→独立Play→Designer実測後判断→Game Director Reviewを予定する。QA結果や期待値は独立Play用Handoffへ転記しない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/（全テスト本文。repo/で`python3 -m unittest discover -s tests`を実行）
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/58-qa-to-studio.md
