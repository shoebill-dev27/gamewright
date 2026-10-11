---
kind: handoff
goal: G-001
seq: 22
from: studio
to: technical-director
stage: Owner escalation 準備
outcome: routed
---
# 22: studio → technical-director — 検証資料へのアクセス不足を Owner 向け選択肢にする

## Task

`prepare-owner-escalation` を用い、必要な外部資料へのアクセスを確保できない blocker について、日本語の Owner 向け Escalation を作成する。追加の技術計画や同じ資料生成依頼ではなく、提供・範囲縮小・中止それぞれの具体的な結果と再開経路を示す。

## Context

Owner はダッシュ中の被ダメージ修正を依頼し、D-002 で補足観察を提供して修正継続を選択した。模擬実装の対象は `sim/build-0.4.md`、変更識別子 `0.3-G001-15`。

Handoff 19 の文書評価分岐を実施した独立 QA は、Handoff 21 で文書評価完了・総合 question を返した。条件別生成観察が不足し、文書整合は全4環境の合格を代替できないと判断している。

既存の引継ぎでは runtime 管理側の窓口・照会手段は確保されていない。次の Role が問い合わせや試行生成を実施できるという前提は置けない。

新しい Owner 宛ての open Escalation はまだない。Goal は active のまま、この brief 作成 Step を open とする。

## Findings

- QA は具体的な仕様不一致を確認していない。fail や二度目の AC 失敗ではなく、必須証拠不足である。
- 必須資料は、対象変更と対応した観察の来歴・モデル情報、全4環境の AC-1〜AC-6 と回帰のイベント記録、命中成立・入力受理・状態遷移・ハート値・移動・予約攻撃・再使用の記録、試行一覧と集計根拠である。詳細は Handoff 21 にある。
- 既存の引継ぎによると、`sim/repo-notes.md#limits-of-available-implementation-detail` は、衝突形状・速度・座標・弾道・発射位相が得られず、フレーム別試行や試行総数を復元できないと明記している。
- project の dry-run 規約は runtime の simulator による更新を定めるが、モデル・記録へのアクセス方法や生成能力を保証していない。
- 取得経路の状態は「照会手段未確保」。問い合わせ実施済み、モデル不存在、永久に取得不能とは記録しない。Owner がモデルを保有するとも仮定しない。
- QA と既存の引継ぎによると、`design/combat.md#player-kit` は “Cooldown 0.6 s.”、repo-notes は既存起点を維持するとするだけで、起点を特定できない。これは観察不足と別の仕様問題である。継続時に既存原資料を回復できなければ game-designer に返す。
- 新規 simulator 開発・実機試験は現在の dry-run の範囲として承認されていない。必要となれば別途 scope の判断を求める。

Handoff 19 が想定した runtime 管理側への確認は未実施であり、その escalation 条件がすべて成立したとは扱わない。今回の blocker は、その確認自体に必要な窓口・アクセスがなく、QA が必須と判断した証拠を現 packet 内の Role 作業では作れないことである。

## Decisions already made

- D-001：Owner 承認なしに戦闘入力を追加しない。
- D-002：元の修正 Goal を継続する。部分観察は計測ログではなく、仕様や AC を変更する決定ではない。不可欠な情報を既存資料や Role の作業から得られない場合は再検討できる。
- D-003：発生源別保護の論理和を採用する。クールダウンの時間・起点や同時イベントの優先順位は変更しない。

## Constraints

- Studio は routing のみを判断している。仕様、技術方式、QA の verdict を変更しない。
- AC-1〜AC-6、30／60 FPS × キーボード／ゲームパッド、必要な命中源・回帰を維持する。
- 文書評価・生成観察・実測を区別し、未知の件数や時刻を創作しない。
- Owner に追加計測を当然の義務として求めない。必要なのはまず資料または取得窓口へのアクセスである。
- 窓口がないことをモデル不存在の証明としない。
- 新しいモデルや一般的な挙動宣言を作って検証結果に見せない。
- クールダウン起点の新規仕様判断は game-designer の権限に残す。
- Goal は active。この Step では brief 作成を進め、依存する実装・検証は開始しない。Studio が Owner 宛ての open Escalation を Route するときに blocked-on-owner へ変更する。

## Open questions

Owner が選べるよう、少なくとも次の選択肢を具体化する。

1. 元の Goal を維持し、runtime 管理側の窓口・アクセス、または出典付き既存モデル・記録の提供を手配する。提供後は technical-director の計画に沿って入力照合・必要な補完を行い、独立 QA に戻す。提供だけで合格を保証しない。
2. Goal を現資料による調査・文書評価報告へ縮小する。Owner の明示的な再解釈が必要であり、「修正の独立検証完了」とは報告しない。
3. 未検証事項を明記して中止する。Goal を abandoned とし、検証合格を主張しない。

アクセス提供による継続を推奨案の出発点とし、実行可能性・費用が不明な点と、何が判明すれば推奨を変えるかを明示する。提供期限や開発費を捏造しない。

## Expected output

`studio/templates/escalation.md` に従う、`from: technical-director`、`to: owner`、`status: open` の Escalation。

以下を含める。

- Owner が単独で読んで回答できる質問。
- 外部入力 blocker と、範囲縮小には Owner 判断が必要である理由。
- 必要資料・候補提供元・取得経路の未確保・影響する検証条件。
- 2〜3 個の選択肢、各選択の範囲・費用やリスクの不確実性・次の route。
- Studio recommendation と根拠。
- 依存工程は開始していないこと。

作成後は Studio の Route を経て Owner に提示する。その時点で Studio が Goal を blocked-on-owner にし、Owner の回答待ちを記録する。選択、資料取得、検証、仕様判断をこの Step で実施済みとしてはならない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/escalation.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/combat.md#player-kit
- Project: sim/repo-notes.md#limits-of-available-implementation-detail
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/21-qa-to-studio.md
- Supporting plan: goals/G-001-dash-damage/19-technical-director-to-studio.md
