---
kind: handoff
goal: G-002
seq: 3
from: studio
to: technical-director
stage: Diagnose
outcome: routed
---
# 03: studio → technical-director — 現行終端とボス戦の実現範囲を確認する

## Task

現行ビルドの部屋選択・遷移・終端・死亡・再挑戦の実態を確認し、ボス戦の配置候補ごとの技術的な変更範囲とリスクを整理する。Game Directorが配置と今回の到達範囲を判断できる材料をStudioへ返す。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。初回Designでは、資料から連続ランの有無や終端の契約を確定できず、仕様化を保留した。

Game Designerは、A：第5部屋を単体ボス戦へ置換、B：第5部屋の後にボス戦を追加、C：第5部屋の混成戦にボスを同居、を提示し、Aを第一候補として推奨している。どの案も未承認。配置と到達範囲の判断は今回の技術調査後にGame Directorへ渡す。

## Findings

- 資料では5部屋が定義され、manualは部屋を選択するセッションを説明している。連続ランが存在しないとはまだ確認されていない。
- 資料に自動遷移、最終勝利、死亡後の再開地点、部屋間の状態継承の具体的説明がない。
- 反応ルールを使うセッションの最大60秒という説明がある。実際の制約と変更の必要性は未確認。
- `project.md`のCurrent stateと戦闘資料のビルド表記に差がある。調査対象は現在の `repo/`、sha `27fe16268ac8`。
- 単体敵の複数攻撃切替、状態・HP・危険範囲の識別表示を既存基盤でどこまで実現できるかは未確認。
- 初回Designでは実行調査をしていない。資料の記述と実行結果を区別して報告すること。

## Decisions already made

- D-001：追加の戦闘入力にはOwner承認が必要。
- D-002/D-003：既存接触判定の限定的な接触端例外。新しい攻撃形状への自動適用はしない。
- D-004/D-005：既存の予兆中断、cue gap、無敵接触時の消費規則を参照する。
- G-002の配置・攻撃構成・難度・終端範囲に承認済みDecisionはない。

## Constraints

- 調査のみ。コード、仕様、既存Decisionを変更しない。
- 配置、既存第5部屋の存廃、Goalの達成範囲は決めない。技術上の選択肢と影響を提示する。
- Desktop、キーボードとゲームパッド、30/60 FPS。新しい入力は追加しない。
- 小規模チームとして既存システムの再利用を優先する。既存部屋の全面改修を前提にしない。
- 15〜20分はVision上の目標であり、現行ランの実測値とは扱わない。
- プレイヤー向け表示は現行のテキストビルドを前提とする。
- 秘密情報・個人情報を出力やハンドオフに含めない。

## Open questions

1. 個別部屋のセッションと連続ランのどちらが実装されているか。入場、クリア、死亡、再開始時の表示、遷移、状態リセット・継承はどうなっているか。
2. 第5部屋または追加部屋を「最後」として扱うために必要な仕組みは何か。選択可能な最終部屋と、連続ランから最終勝利まででは変更範囲がどう違うか。
3. A/B/Cそれぞれで変更するシステム、既存第5部屋固有の挙動や検証への影響、主なリスクは何か。現段階で確定できない点は何か。
4. 単体ボスの攻撃切替、固定照準、予兆・回復・HP表示をどこまで再利用できるか。表現仕様をArt Directorへ依頼すべき具体的な不足はあるか。
5. 60秒上限はどの実行経路に適用されるか。戦闘時間の設計・計測・独立検証に与える制約は何か。
6. 現在の実行手段で所要時間について何が測れるか。15〜20分のラン目標と比較する際に不足する情報は何か。

## Expected output

確認した実行コマンドと結果、根拠となるファイル、現行終端の事実、候補別の変更範囲・リスク・未確定事項を整理する。実行不能な項目は理由と必要な材料を明記し、推測で補わない。

結果は `04-technical-director-to-studio.md` として `to: studio` で返す。これは確定仕様に対する実装計画ではない。Studioは調査結果と初回Designの選択肢をGame Directorへ渡し、配置・範囲の判断後にGame Designerへ仕様化を戻す。Goalの再解釈や大幅な範囲変更が必要と判明した場合は、その根拠を明記する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Build: repo/ (sha 27fe16268ac8)。repo/を作業ディレクトリとして、`python3 -m unittest discover -s tests`、`python3 play.py --view player {script}`、`python3 play.py --view trace {script}`、必要なら `python3 bots.py {script}`。スクリプト形式はmanualで確認する。
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-002-final-boss/02-game-designer-to-studio.md
