---
kind: handoff
goal: G-001
seq: 19
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 19: studio → technical-director — コードにアクセスできない Build をどう進めるか(D-007 の 7)。Owner への確認が要るかの判断と、要るなら Escalation の作成

## Task

Build がゲームのコードを読み書きできないと報告して返ってきた。D-007 の 7 に従い、この状況での進め方を判断すること。Owner の判断(リポジトリの提供、または範囲・リスクの受け入れ)が要ると判断したら、`prepare-owner-escalation` で Escalation を作ること。

## Context

G-001(戦闘の単調さの改善)は、D-002 の方向(部屋の構成と進行を主軸、併用は予告つき Grub 突進の1つ)で、Design まで完了している。Build の1回目(Handoff 14)は、T0 を実施できず実装に入らなかった。そこで 6a で D-007 を作り、T0 を「前提の台帳」(7 項目)に置き換え、コードを全く読めない場合は再試行せず返す条件(D-007 の 7)を定めた。Build の再開(Handoff 17)は、その条件に該当して `outcome: question` で返ってきた(Handoff 18)。

## Findings

Handoff 18 の客観的な内容:

- Build の実行環境に渡されたのは packet の入力ファイルだけで、ゲームのソースコード、ビルド、テストの実行手段、リポジトリはなかった。コードやテストを変更する経路もなかった。
- `project.md` は `repository: none`(サンプルのドライランで、ビルドは `sim/build-*.md` で模擬)としている。`sim/repo-notes.md` と `sim/build-0.3.md` はコードの代わりの模擬の記述であり、台帳の項目をこれらで「確認した」とは扱えない。
- 台帳 7 項目はすべて未確認:
  1. 部屋データ、スポナー、波
  2. 部屋のコードと敵のコントローラの分離(T2 と T3 は既定どおり直列)
  3. 接触の判定形状、レーン幅の元の値
  4. Spitter の弾の衝突処理
  5. 視覚の仕組み(要素 2〜10)
  6. 接触結果の通知
  7. 敵の挙動が経過時間で進むか(`sim/repo-notes.md` に「可変 delta」とあるが、コードでの確認はない)
- 実装、テスト、状態ログ、30/60 FPS の切り替え、ビルドノートは何も作られていない。QA と `art-director` の Verify に渡せるものはない。
- 仕様、D-001〜D-007、視覚仕様を読み合わせた範囲で、新しい矛盾や欠落は報告されていない(文書上の確認のみ)。
- Handoff 18 が挙げた選択肢:
  - (a) 実際のリポジトリとビルド・テスト手段を Build が使えるようにする。
  - (b) 模擬であることを前提に、Build の範囲を確認し直す(例: 実装ではなく実装計画のレビューまで)。
- (a) が満たされた場合の再開順序は Handoff 17 の台帳のとおり(部屋のタスク冒頭で 1・2、状態追加の冒頭で 7、突進の冒頭で 3・6、弾の処理を読んだ時点で 4、見た目の冒頭で 5)。

## Decisions already made

- D-001〜D-006: 変更しない。
- D-004: 技術方針(共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ)。
- D-007: T0 を前提の台帳に置き換えた。7 は、読める・書けるコードが全くない場合は再試行せず返す条件。今回これに該当した。

## Constraints

- 新しい入力ボタンは足さない(D-001)。ビジョンの柱とランの長さは変えない。
- 30 FPS と 60 FPS の両方で正しく動くこと。小さなチームで既存の仕組みを再利用すること。
- Owner 向けの Escalation は `owner_language`(日本語)で書く。
- 判断の材料にする事実は、上の Findings と `project.md`、`sim/repo-notes.md` に限る。確認していない前提を、確認済みとして扱わない。

## Open questions

1. この状況は、Owner の判断を要するか。Escalation の条件のうち、スコープ・費用・リスクの大幅な変化に当たるか(コードのない環境で Build を進めること、または Build の範囲を模擬に合わせて縮めること)。当たらないと判断する場合は、その理由と、Build の再開の仕方を示すこと。
2. Owner の判断が要る場合、選択肢は (a)(b) で足りるか。他に妥当な選択肢(例: 実装の代わりに、実装計画と受け入れ基準の確定までを成果とするなど)があれば加える。各選択肢で Goal の成功条件(実際に遊んで単調でなくなったかを確かめる)がどう変わるか、Play と Review がどこまで可能かを書くこと。
3. 範囲を縮める選択肢では、Verify・Play・Review のどれが成立しなくなるかを明示すること。

## Expected output

次のどちらか。

- Owner の判断が要る場合: Escalation(`studio/templates/escalation.md`、`goals/G-001-combat-monotony/20-technical-director-to-owner.md`、`to: owner`、`status: open`)。選択肢ごとに「選んだ場合の次の経路」と推奨を書く。Studio が Goal を `blocked-on-owner` にしてOwner に返す。
- 不要と判断した場合: `to: studio` の Handoff(`20-technical-director-to-studio.md`)に、理由と Build の再開の条件、または Build の範囲変更の内容を書く。必要なら Decision を記録する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md, studio/skills/prepare-owner-escalation.md, studio/skills/make-decision.md
- Project: project.md#constraints, project.md#current-state, sim/repo-notes.md, studio/templates/escalation.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md, decisions/D-007-build-without-code-access-assumption-register.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md
- Previous handoff: goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
