---
kind: handoff
goal: G-002
seq: 42
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 42: gameplay-engineer → studio — 41の未実施分は未着手。この Step では実装も実行もできなかった。必要な入力と分割案を返す

## Task

41の未実施分（契約試験の細目、V1補完、pause・retry込みの通常ラン計測、dodger部屋1〜4の回帰固定）が、このStepの入力だけでは安全に実装できないことを受け取り、Loadと実行の組み立てを直して再ルーティングする。

## Context

41は、source id `5145454ab956` の保存版を土台に、40で未実施の項目を実装・実行して完成資料にするよう求めた。このStepでは、repo/ のファイルを1つも書かず、`@run` も1回も使っていない。コードも試験も変更していないので、source id は 40 のまま `5145454ab956` で、このStepによる新しい実行結果はない。

## Findings

### 1. このStepで何をしたか

- 41の5項目を、パケットのファイルと照らして検討した。
- repo/ への書き込み、`@run`、試験の追加はしていない。
- 書かなかった理由は次のとおり。
  - 契約試験の細目（B3・B6・B7・B9・B10・T1〜T4・C2・C3・V1）は、`game.py` と `session.py`、`play.py` の内部状態に直接触れる。
    - 弾ID・消滅理由、`spent`、保護の残り時間、イベント名などが該当する。
  - この3ファイルは41のLoadに含まれておらず、パケットに本文がない。
  - 見えているのは試験や `bots.py` から推測できる断片だけである。
    - 例：`Game.place_player`、`Shot(...)`、`boss.spent`、`shot_removed` イベントの `reason`、`boss_swipe`。
  - 名前や挙動を推測した試験は、失敗の原因が試験の誤りか実装の不具合かを区別できない。
  - 実行しない試験を「追加済み」として渡すのは、過去の成功を帰属させないという制約に反する。

### 2. 41の項目ごとの状態

| 項目 | 状態 | 備考 |
|---|---|---|
| 1. V1補完（legacy route表示、弾ID・消滅理由、長時間観測） | 未着手 | `play.py`、`game.py` が必要 |
| 2. 契約試験の細目 | 未着手 | 同上。`session.py` も必要 |
| 3. pause・retry込みの通常ラン計測 | 未着手 | 下記3の設計案あり。未実行 |
| 4. dodger部屋1〜4の回帰固定 | 基準の記録のみ（下記4）。固定の試験は未追加 | |
| 5. 任意：新5番の30／60差の診断 | 未着手 | `log on` の実行が必要 |

### 3. pause・retry込みの通常ラン計測の設計案（未実装・未実行）

- `run_driver.py` の `control <秒> pause|resume|retry` 構文は既にある。
  - ただし retry は通常ランの終端でしか受理されない（`RoomSession.control` と `session.py` の既存規則）。
  - 終端到達時刻は bot の勝敗次第で変わる。そのため、固定秒の `control` だけで dodger を駆動する計測は組みにくい。
  - `when` ルール（`play.Rule`）で dodger の方針を再現するのも現実的でない。
- 現実的な案は `bots.py` の `play_run` の拡張である。
  - 引数に次を追加する。
    - `pause_at`: 走行中のラン時刻の列。
    - `pause_seconds`: 1回あたりのドライバ上の停止長。
    - `retries`: 終端後の retry 回数。
  - ポーズは `RunSession.control("pause")` と `("resume")` 経由とする。ポーズ中は `session.step()` を呼ばず、ドライバ時間だけ進める。
  - retry は `won` か `dead` の終端で `control("retry")` を呼ぶ。
    - `attempt` を2にし、Brain の反応記憶を初期化する。
    - 前試行の未来入力は渡さない。
  - 出力は、ラン時刻、ポーズを分けた実経過、部屋別時間、遷移、ボス入場hearts、被弾・反撃・再挑戦回数とする。
    - これは仕様§9の計測項目と同じである。
- 受け入れ観点（実行して確認する）：
  - ポーズの前後でラン時刻、部屋時刻、予兆の残り、dash・保護の残りが変わらない（C2）。
  - 再挑戦後の初期状態が新規通常ランと一致する（T4）。
  - 再挑戦後のラン時刻・部屋時刻・試行番号が正しい。
- ここまで書いておきながら実装しなかった理由は、`session.py` の `control`、`pause`、`retry` の実装が見えず、戻り値やイベント名を推測する必要があるからである。

### 4. dodger部屋1〜4の回帰固定の基準（40の実測値。提出前の数値ではない）

これは、今後の変更の回帰を検出するための基準として記録する。source id `5145454ab956`、開始3 hearts、limit 60 s、決定的な bot による値。提出前の数値の記録がないため、提出前と同じだったかの確認にはならない。

| FPS | 部屋1 | 部屋2 | 部屋3 | 部屋4 | 合計 |
|---|---|---|---|---|---|
| 30 | clear 6.6 s、失0、dash3 | clear 20.7 s、失0、dash10 | clear 15.6 s、失0、dash6 | clear 18.3 s、失0、dash7 | 4/4、失0、dash 26 |
| 60 | clear 9.6 s、失0、dash5 | clear 25.1 s、失0、dash14 | clear 15.0 s、失0、dash6 | clear 17.0 s、失0、dash8 | 4/4、失0、dash 33 |

- 固定できる範囲：
  - clear 4/4、失hearts 0、両FPSの hearts lost 差 0。
  - 各部屋が clear すること。
  - 部屋3・4の dash が各FPSで1回以上。
- 固定できない、または固定に向かない範囲：
  - 秒数とdash数の完全一致を試験で固定するのは勧めない。
  - これらは bot の方針や共有ルールの正当な調整でも動く。
  - 固定すると、意図した変更を回帰として誤検出する。
  - 表の値は診断用の参考値に留める。
  - 提出前との同一性は、提出前の記録が存在しないため、現時点で確認できない。
- 固定の試験を追加していないのは、本Stepで実行して確認できていないからである。試験案：
  - `bots.play_room(dodger, room, fps, 60)` を部屋1〜4、両FPSで呼ぶ。
  - `outcome == "clear"` と `hearts_lost == 0` を確認する。
  - 両FPSの hearts lost 差が1以下であることを確認する。
  - 部屋3・4の dash が1以上であることを確認する。

### 5. 完成資料として独立QAへ送れるか

**送れない。** このStepで追加した成果がなく、41の未実施項目はすべて残っている。40は引き続き部分成果である。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。実機・実gamepad・指定sha照合は不要。

## Constraints

- 第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。
- 新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託は加えない。
- 15〜20分に合わせる調整はしない。
- 過去の試験成功を保存版に帰属させない。コードを変更したら再実行し、実行時のsource idを併記する。
- このStepでは何も変更していないので、再実行も不要だった。

## Open questions

仕様の不足・矛盾はなく、Designerへの質問はない。Studioへの依頼は次のとおり。

1. 次のGameplay Engineer Stepに、`repo/game.py`、`repo/session.py`、`repo/play.py`、`repo/manual.md` をLoadへ追加する。
   - 契約試験の細目とV1補完に必要な内部状態は、この3ファイルにある。
2. 実行は `@run` を最大3ラウンド使う前提でよい。次の順に分割するのが安全である。
   - ラウンド1：`tests`。現状の112件が再現するか、source id が `5145454ab956` と一致するかを確認する。
   - ラウンド2：新しい契約試験を追加してから `tests`。失敗が出れば、試験の誤りか実装の不具合かを切り分けて修正する。
   - ラウンド3：`bots`。`play_run` を拡張した pause・retry 込みの通常ランと、dodger部屋1〜4の回帰固定を測る。
3. 41が求める項目は量が大きい。1つのStepでは重い場合の分割案：
   - Step A：契約試験の細目（B3・B6・B7・B9・B10・T1〜T4・C2・C3）。
   - Step B：V1補完と、`play_run` の pause・retry 拡張。
   - Step C：計測と回帰固定。
   - どの分割でも、Aの結果として B5〜B10 の実接触試験が通ることが、ボス攻撃が実際に当たり、かつ回避可能であることの根拠になる。bot の被弾0は根拠にならない。
4. 提出前の dodger 部屋1〜4の数値が存在するか（G-001の測定記録など）をStudioが確認する。無ければ、上記4の基準を以後の回帰基準として使うことにDesignerまたはQAが同意する。

## Expected output

Studioは、上記のLoadと実行方針で 41相当のStepを再ルーティングする。あるいは項目を分割して再ルーティングする。完成資料は、未実施項目が実行され、source id と結果が揃ってから独立QAへ送る。新5番と通常ランの時間は、40のまま Designer の実測後判断にルーティングする。

## Sender assessment

- 確信度：このStepについて述べられるのは、「何も実装・実行していない」ことと「その理由」だけである。それは高い確信で言える。
- 難度、体験、FPS差の原因、提出前との同一性については、結論を持たない。
- 推測で試験を書かなかったのは、実行できない試験が通るかのように見えるのを避けるためである。
- 下記の設計案は未実装・未実行で、`session.py` を見て調整が必要になる可能性がある。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/public-driver.md
- Project: repo/source_id.py
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/manual.md
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_run_driver.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/41-studio-to-gameplay-engineer.md
