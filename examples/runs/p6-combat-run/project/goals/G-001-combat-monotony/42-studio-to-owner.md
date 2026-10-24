---
kind: escalation
goal: G-001
seq: 42
from: studio
to: owner
status: resolved
decision: D-008
---
# 42: Owner decision needed — AC-15 の `ManualTest` をどう確認するか

## Question

QA の環境では `manual.md` が `ManualTest` の読む場所にないため、そのテスト2件を実行できません。ご自身の環境でテストを1回実行して結果を教えていただくか、このテストなしで AC-15 を受け入れるか、どちらにしますか。

## Why this needs the Owner

QA は `manual.md` が欠けていることを 29 と 40 で2回、同じ入力について差し戻しました（間に新しい入力はありません）。ループ制限により、同じ不足入力で3回目を QA に回さず、Owner に確認します。この不足は、どの Role も作れない実行環境側の問題です（Studio も QA ワークスペースを変えられません）。また `manual.md` は D-005 / D-007 により Owner が管理するファイルで、Role は編集しません。

状況:
- QA は段落（`## On screen` の最後）を D-007 の本文と一語一句照合し、一致を確認しました（40）。
- 練習部屋の挙動（敵は script で置いた位置のみ、回復なし、次の部屋なし、ダウン後約2秒で終了、プレイヤーのタイルにいる敵は隣の空きタイルに描画）もビルドと一致しました。
- 残るのは `ManualTest` の2件（`test_manual_lists_glyphs_and_lines`、`test_on_screen_section_lists_x_and_the_practice_room`）だけです。テストは `REPO.parent / "manual.md"` を読み、QA 環境ではこれが `/manual.md` になり `FileNotFoundError` になります。他の38件は通っています。

## Options

### Option A — Owner が実環境で `run_tests` を1回実行して結果を知らせる

`manual.md` が `repo/` の隣にあるプロジェクトのディレクトリで `python3 -m unittest discover -s tests` を実行し、結果（40件中の成否、失敗があればその出力）を返信します。QA 環境に `manual.md` を置く方法をご存じなら、その配置を知らせていただいても構いません。コストは小さく、取り消す必要のある変更はありません。
If chosen: 40/40 なら AC-15 を合格として記録し、7h（41）の結果が出たら Play に進みます。失敗があれば、その出力を持って `manual.md` の内容か期待値かを `game-designer` に確認し、必要なら Build に戻します。配置を知らせた場合は、QA に短い `run_tests` 再実行（`ManualTest` のみ）を回します。

### Option B — QA の静的確認で AC-15 を受け入れる

段落の一致と挙動の一致を根拠に AC-15 を合格とし、`ManualTest` は「QA 環境では未実行」と記録します。Owner の作業はありません。見落としが残るリスク: 用語・記号一覧を調べるテスト（`test_manual_lists_glyphs_and_lines`）は、段落の照合だけでは確認できていません（ただし 29 の静的確認では問題は見つかっていません）。
If chosen: 7i を「合格（ManualTest 未実行）」としてクローズし、7h の結果が出たら Play に進みます。Review で未実行の旨を記録します。

## Studio recommendation

Option A。

## Reasoning

テストの2件は、手動の一覧がビルドの記号・文言とずれていないかを機械的に確認するもので、段落の照合だけでは代わりになりません。実行は1コマンドで、Owner が手元で行えば確実です。コストに対して確認の価値が高いと判断します。ただし、Owner が確認に手間をかけたくない場合、静的確認で問題が見つかっていないため Option B も許容範囲です。結果が40/40でない場合や、Owner が実行できない場合は、推奨を B に変えて構いません。

## Meanwhile

7h（美術ディレクターの視覚レビュー、41）は独立しているので続けます。Play と Review は AC-15 の扱いが決まるまで待ちます。

## Owner decision required

A / B — 選択肢と、あれば条件（A の場合は実行結果）をご返信ください。

---

**Owner response (2026-10-15):** A。manual.md を repo/ の隣に置いた環境で python3 -m unittest discover を実行しました（Owner の代理、サンドボックス内）。結果: 40件中39件成功、1件失敗。失敗: test_manual_lists_glyphs_and_lines (test_game.ManualTest) — AssertionError: 'run over' not found in manual.md の本文（tests/test_game.py 631行目 self.assertIn(phrase, text, phrase)）。ほかの39件は成功。

**Resolved:** D-008 (Option A). 失敗1件は `game-designer` の判断へ（43）。
