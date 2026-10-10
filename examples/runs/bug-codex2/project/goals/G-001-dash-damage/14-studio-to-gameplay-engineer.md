---
kind: handoff
goal: G-001
seq: 14
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 14: studio → gameplay-engineer — 発生源別の無敵管理を模擬実装する

## Task

既存仕様、QA の AC-1〜AC-6、technical-director の計画と D-003 に従い、無敵の競合解除を修正する。dry-run の Build として、変更内容・対象・試し方を具体的に記した Handoff を Studio に返す。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」。QA は仕様と模擬ビルドの不一致を確認し、受け入れ条件を作成した。technical-director は実装資料を調査し、修正計画を完成させた。

実リポジトリは存在しない。`sim/repo-notes.md` が実装資料であり、Build Handoff に変更を正確に記載すると変更が成立し、実行環境の simulator が `sim/` を更新する。実機試験やコード実行を行ったとは報告しない。

## Findings

`13-technical-director-to-studio.md` が診断・実装順序・検証条件・資料要件の正本となる。担当は、単一の無敵フラグをダッシュ終了と被弾保護終了がそれぞれ解除し、他方の保護まで失わせる構造を実装資料から特定した。これは資料上の診断であり、新しい再現試行の結果ではない。

計画の要点：

- ダッシュ由来と被弾由来の保護を分離し、有効な無敵を両者の論理和で判定する。各終了処理は自分の発生源のみを解除する。
- ダッシュ保護は既存のダッシュ開始・終了に結び付ける。
- Grub 接触と Spitter 弾命中の両経路で、被害や入力不能の適用前に有効な無敵を確認する。
- 防いだ命中で被害処理や保護時間の再開始を行わない。
- 共通フラグの旧設定・解除・参照箇所を整理し、解除漏れや旧経路の残存を防ぐ。
- 両終了順序、両保護終了後の通常被害、防いだ連続命中で保護が延長されないことを回帰確認する。

QA の受け入れ条件の参照元は `11-qa-to-studio.md`。計画では、AC-1 は先行被弾なしのダッシュ保護、AC-2 は入力不能終了後のダッシュ、AC-3 は被弾保護が先に終了する重なり、AC-4 はダッシュが先に終了する重なり、AC-5 は通常被弾とその保護、AC-6 は移動・時間・クールダウン・攻撃予約の維持を扱う。

全 AC を PC の 30 / 60 FPS × キーボード / ゲームパッドの4環境で確認する。AC-1〜AC-4 は接触と弾命中を別試行とする。時刻例や詳細な記録項目は計画を参照し、予定条件を観察結果として扱わない。

## Decisions already made

- `decisions/D-001-one-button-combat.md`: 攻撃・ダッシュ・ポーズ以外の入力を Owner 承認なく追加しない。
- `decisions/D-002-resume-with-owner-observations.md`: Owner の部分的な観察を用いて元の修正 Goal を継続する。
- `decisions/D-003-independent-invulnerability.md`: 発生源別の保護を論理和で判定し、既存の時間・入力仕様を維持する。

これらは受領した計画の要約。実装前に Load の Decision 本文を確認する。

## Constraints

- 戦闘の方向性、バランス、敵 AI、移動・壁処理、攻撃の威力・硬直を変更しない。
- ダッシュは4タイル・0.25秒・クールダウン0.6秒、ダッシュ中の攻撃入力は終了時発動を維持する。
- 通常被弾は1ハート減少、0.3秒入力不能、被弾後0.8秒までの保護を維持する。
- 可変 delta time を使い、固定フレーム数への置換や、ダッシュより先に保護が切れる別タイマーを追加しない。
- 入力不能中の予約入力、完全同時イベントの優先順位、クールダウン起点の新仕様を決めない。
- 実装を並列化しない。保存形式変更は計画外であり、保存互換性への影響が判明した場合は報告する。
- 観察、期待、未実施を区別する。Owner の体感値を計測値にしない。
- この Route では、Load に指定した未提供資料の本文を確認していない。次の packet に不足があれば、具体的な欠落と進められる範囲を Studio に返す。

## Open questions

Build 内で確認・具体化する事項：

- 両命中経路と共通無敵フラグの全操作箇所。
- 再現用配置、実際のイベント順序、既存クールダウン起点。
- 各 FPS で計画した前後関係が成立する試行条件。
- simulator が生成する更新ビルドと QA 用観察資料の識別・参照方法。

仕様判断が不可欠なら具体的な競合例を添えて Studio に返し、game-designer への差し戻しを求める。計画が成立しない実装事情が判明した場合は technical-director による再計画を求める。追加の Owner 計測は現時点の開始条件ではない。

## Expected output

次の連番の gameplay-engineer → studio Handoff を作成する。

1. 何を、どの模擬実装項目で、どう変更したか。両命中経路と旧共通解除の扱いを明示する。
2. 変更後のビルド識別子と実行・確認方法、simulator に依頼する資料更新を明示する。更新前のものを更新済みと報告しない。
3. `13-technical-director-to-studio.md` の資料要件に従い、開発者向け実装資料、プレイヤー向け模擬ビルド、QA 用試行資料を区別する。
4. QA が全 AC・全4環境・必要な命中源を評価できる配置、初期状態、入力、接触／命中、時刻・フレーム・順序、ハート前後値を具体化する。無効な試行を合格の根拠に数えない。
5. 自己確認の結果と理由は `## Sender assessment` に分離する。実施不能・資料不足・未解決事項を明示する。

結果は必ず Studio に返す。Studio は模擬資料更新後、自己評価と実装理由を除いた仕様・受け入れ条件・ビルド・観察資料を用意し、新しい executor の QA に Verify を依頼する。Build の自己確認は独立 QA の合格を代替しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/13-technical-director-to-studio.md
