---
kind: handoff
goal: G-002
seq: 57
from: studio
to: qa
stage: Verify
outcome: routed
---
# 57: studio → qa — 連続ランと最終ボスの独立検証

## Task

保存ビルドを仕様・受入基準から独立検証する。30/60 FPSを別々に実行し、公開経路での連続到達・終端・再挑戦、ボス契約、共有戦闘と独立部屋の回帰を確認する。

## Context

G-002は第1〜4部屋を連続して進み、第5部屋の単体ボス、勝利・死亡・最初からの再挑戦までを成立させるGoal。Buildが完了し、独立Verifyを開始する。今回の対象はD-021が承認したテキスト表示・スクリプト実行であり、実機供給や実gamepad検証は要求しない。

## Findings

検証対象は現在のrepo/。実行はrepo/を作業ディレクトリとする。

- 全suite：`python3 -m unittest discover -s tests`
- プレイヤー表示：`python3 play.py --view player SCRIPT`
- トレース：`python3 play.py --view trace SCRIPT`
- botと判断ログ：`python3 bots.py SCRIPT`

公開構文はmanual.mdとpublic-driver.mdを使用する。既存の再現用スクリプト生成器も利用可能：

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
```

各スクリプトをplayer/trace両viewで実行する。生成済み入力の再生とcontrolled fixtureは区別し、fixtureの成功を通常到達の代用にしない。既存テストの合格だけで独立判定を終えず、仕様に照らして出力・イベント・状態を確認する。

## Decisions already made

- D-017：二攻撃のボス、連続進行、回復、終端優先、pause/retryと時計の契約。
- D-019：旧集計の適用終了、保持する独立部屋回帰とFPS比較、実測後のDesigner判断。
- D-021：Studio内のテキスト・スクリプト検証で進める。
- D-022：旧経路注記、弾ID・消滅理由、観測間隔と全attempt summary。

## Constraints

- 正本はdesign/final-boss-and-continuous-run.md、関連Decisions、共有戦闘仕様。
- 第1〜4部屋と共有戦闘ルールの保持を検証する。廃止された部屋3〜5集計ゲートを復活させない。
- 実装者の自己評価・原因説明・期待される測定値は入力に含めない。
- 通常ラン時間、pause、終端待機、headless処理時間を分ける。独立部屋の時間合計を通常ラン時間としない。
- テスト用状態設定・botの成功を人間の体験評価としない。新しい数値ゲートや難度調整はQAが決めない。
- コードや仕様を変更せず、失敗・仕様不足は具体的証拠とともにStudioへ返す。

## Open questions

1. R1/C1：通常の敵撃破から部屋1→5へ到達し、部屋5がB単体となるか。部屋時計、回復、初回ボス到達hearts、四つの遷移時間は契約どおりか。
2. B1〜B10/T1〜T4/C1〜C3：二攻撃、予兆・固定方向・実弾・接触・防御・終端優先などが仕様を満たすか。
3. C2/T4：有限pauseが戦闘、両時計、clear表示を凍結するか。勝利・自然死亡からretryでき、完全な初期状態と入力破棄が成立するか。遠い未来の入力が短い試行で出ないだけでは破棄の証明としない。
4. 各attemptのsummaryがイベントと一致するか。到達部屋、攻撃・ボス命中・dash・hurt、pause、終端待機、retry、driver-limit終了を分離して確認できるか。
5. D-019の保持基準14/15/16c、独立部屋1〜4、ボス開始hearts 3/2の両FPS比較は成立するか。判断ログの入力情報はプレイヤーに観測可能か。
6. V1とD-022：player表示で必要な状態を識別でき、旧経路注記・弾ライフサイクル・長時間観測とsummaryが仕様どおりか。詳細な視覚表現のレビューは後続Art Directorが担当する。

## Expected output

`to: studio`の独立QA報告を作成し、outcomeをpass/fail、仕様不足ならquestionとする。検証した保存ソースID、コマンド・入力、FPS、試行数、基準ごとの判定、再現手順と証拠、未検証範囲を記録する。

通常ランの同一試行による到達・終端・部屋別時間・pause/待機を測定し、botの両FPS結果と判断ログを記録する。時間差や体験上の含意は判定と分けて後続Designerへ引き継ぐ。合格なら限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewの順にStudioがルートする。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/（保存ビルドとtests。上記コマンドで実行）
- Project: repo/manual.md
- Project: repo/public-driver.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: none（独立性のため56と実装履歴を渡さず、必要な実行情報を本Handoffへ転記）
