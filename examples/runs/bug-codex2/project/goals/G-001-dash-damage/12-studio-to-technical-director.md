---
kind: handoff
goal: G-001
seq: 12
from: studio
to: technical-director
stage: Diagnose / Plan
outcome: routed
---
# 12: studio → technical-director — ダッシュ中被ダメージの技術調査と修正計画

## Task

QA の不具合報告と実装資料を照合し、ダッシュ中の被ダメージの原因と変更箇所を調査する。既存仕様を維持する修正計画と、Build 後に独立した QA が受け入れ条件を評価できる模擬資料の要件を作成し、Studio に返す。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」である。D-002 により Owner の部分的な観察を使って元の修正 Goal を継続している。

QA は `11-qa-to-studio.md` で、模擬ビルドの「ダッシュ途中の被ダメージ」と既存仕様の「全ダッシュ時間無敵」の不一致を確認し、不具合報告と AC-1〜AC-6 を作成した。詳細条件の独立した再現や実装原因の特定は未完了だが、追加の Owner 計測を必須とせず技術調査へ進めると報告している。

このプロジェクトには実リポジトリがなく、`sim/repo-notes.md` が実装資料に相当する。Build は gameplay-engineer が変更内容を Handoff に正確に記述し、実行環境の simulator が `sim/` に反映する方式で行う。

## Findings

以下は QA 報告の要約であり、Studio が独自に検証した結果ではない。詳細な不具合報告・比較手順・受け入れ条件は前の Handoff を参照する。

- ダッシュは 0.25 秒間すべて無敵。移動距離は 4 タイル、クールダウンは 0.6 秒。ダッシュ中の攻撃は終了時に発動する。
- 通常被弾は 1 ハート減少と 0.3 秒の入力不能を伴い、被弾後 0.8 秒まで無敵となる。
- Owner は PC・60 FPS・ゲームパッド、部屋1〜2で、Grub による被弾と硬直終了後に少し待ってダッシュすると、ダッシュ後半の別の Grub 接触で 1 ハート失うと報告した。
- 被弾から約 0.5〜0.8 秒、約 10 回中 6 回という値は体感・概数であり、計測結果ではない。Spitter 弾でも 1 回の観察があるが詳細は不明。
- 実装原因、安定再現に必要な配置・時刻、発生境界は未確認。時間条件の重なりだけから実装方式や原因を断定しない。

修正計画が満たすべき QA の受け入れ条件は次のとおり。

| ID | 検証対象 |
|---|---|
| AC-1 | 未被弾時のダッシュ中は Grub 接触・Spitter 弾命中でハートが減らない |
| AC-2 | 被弾後の入力不能終了直後に開始したダッシュ中もハートが減らない |
| AC-3 | ダッシュ途中で被弾後 0.8 秒が経過しても、ダッシュ終了前の接触・弾命中ではハートが減らない |
| AC-4 | ダッシュ終了後に被弾由来の無敵時間が残る場合、その時間内はハートが減らない |
| AC-5 | 通常時の Grub 接触で 1 ハート減少、0.3 秒入力不能、被弾後 0.8 秒まで追加被害なしを維持する |
| AC-6 | ダッシュの距離・時間・クールダウンと、ダッシュ中の攻撃入力の終了時発動を維持する |

全条件を PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せで評価する。現在はすべて未検証である。

本 Route packet には `sim/repo-notes.md`、設計・Decision 本文、technical-director の契約全文と Skill 本文がない。Studio は提供された Works from と QA 報告から必要な入力を選定したが、未提供本文との整合性は確認していない。次の Step では Load の実資料を用い、要約を資料の代用にして原因や結果を創作しない。

## Decisions already made

- `decisions/D-001-one-button-combat.md`: 攻撃・ダッシュ・ポーズ以外の入力追加には Owner 承認が必要という既存制約を守る。
- `decisions/D-002-resume-with-owner-observations.md`: Owner の部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。

Decision 本文の詳細は Load 資料で確認する。

## Constraints

- 既存仕様への修正に限定し、方向変更、新しい入力、無関係なバランス調整を行わない。
- 小規模チームのため既存システムの再利用を優先し、PC・30 / 60 FPS・キーボード・ゲームパッドを対象とする。
- この Step は技術調査・計画であり、Build や QA の合否判定を代行しない。
- 模擬資料の記述、Owner の体感、仕様から算出した検証条件、実施済みの結果を区別する。
- 入力不能中の予約入力や、ダッシュ開始・終了と命中が完全同時の場合の優先順位を新たに決めない。必要なら game-designer の判断へ戻す。
- 必須資料が欠ける場合は欠落と影響を具体的に報告する。実リポジトリがないこと自体は、この dry-run の障害ではない。

## Open questions

- 実装資料から仕様不一致を説明する原因と変更箇所を特定できるか。証拠と仮説をどこまで分離できるか。
- 既存仕様を維持して修正するための手順、影響範囲、回帰リスクは何か。
- 安定再現の条件と、AC-1〜AC-6 の各環境での評価に必要なイベント順序・観察情報を、後続の模擬資料でどう示すか。
- 設計判断や追加情報を必要とする具体的な阻害事項はあるか。

## Expected output

技術調査・修正計画を記載した outgoing Handoff を `to: studio` で返す。少なくとも以下を含める。

- 実装資料に根拠を置いた診断、未確認事項、必要なら切り分け手順。
- gameplay-engineer が実施できる変更箇所・変更内容・順序と、維持すべき既存挙動。
- AC-1〜AC-6 への対応、全4環境組合せの確認手順、回帰リスク。
- 更新後の模擬ビルドと観察資料に必要な内容。実際の接触・命中、イベント時刻・順序、ハート変化など、QA が期待結果だけから合格を推測せず評価できる情報を示す。
- Build に進めるか、未解決の仕様判断や不足資料があるか。

Studio は結果を受けて Build へルーティングし、その後は独立した Verify を必ず行う。技術的な重要判断が後続作業を制約する場合は Role の権限内で Decision として記録する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/11-qa-to-studio.md
