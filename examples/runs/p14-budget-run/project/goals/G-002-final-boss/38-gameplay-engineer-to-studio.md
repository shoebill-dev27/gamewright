---
kind: handoff
goal: G-002
seq: 38
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 38: gameplay-engineer → studio — 36の保存を確認、boss対応dodger・開始hearts・run計測道具を提出、実行は未実施

## Task

38の変更を保存し、保存後ソースでtests／bots（`hearts 3,2`、`mode run`）を実行できる枠を割り当てる。結果を受けて残る契約試験・観測整備を継続するか、独立QAへ送るかを判断する。

## Context

37は、36の保存状態確認、公開観測とboss対応bot、開始3／2 hearts指定とclear／death／unfinishedの明示、契約試験、測定の取得を要求した。D-021のBuild承認は有効。

本Stepでは@runを使っていない。新規コードを走らせるには先に保存が要り、保存前の本文は走らせられないため、実装と試験を先に提出した。**今回提出した変更は一度も実行していない。** 実行結果はない。

## Findings

### 保存状態（37の優先1）

パケット上の正規本文で次を確認した。

- tests/test_boss_contract.py：34の2試験に次frame移動・加齢のassertが入っている。36の追加5試験（低HP順序、距離0、直交1 tile、全phase非致死、致死予兆）も存在する。
- manual.md、README.md、public-driver.mdに36の文書統合がある。
- run_driver.pyのBUILDは0.6-g002-public-32のまま。36の未保存提案（識別文字列のみの変更）は採用していない。

36の変更は保存済みと判断する。ただし実ファイル読取りではなく供給された本文による確認である。保存後の実行結果はない。供給済みの98／103件は今回の保存版に帰属しない。

### 今回提出した変更（未実行）

| 対象 | 内容 | 根拠 |
|---|---|---|
| repo/source_id.py（新） | game／session／play／run_driver／bots／source_id と tests/*.py のsha256先頭12桁 | 対象ソース識別（BUILDだけでは識別できない） |
| repo/run_driver.py | measurement辞書にsource_idを追加 | 同上 |
| repo/bots.py `_dangers` | boss予兆（固定方向・残秒・突進3.0／短射3.4の線）と突進active中の線を危険線に追加 | V1の公開観測のみ。D-019 6 |
| repo/bots.py `dodger` | boss予兆・active中は線上なら既存のdash／sidestep、線外なら停止して保持。予兆を止めるswipeはしない。回復中は既存の接近・swipe | D-019 6。部屋1〜4にbossはなく挙動は不変のはず（未回帰確認） |
| repo/bots.py `play_room` | `hearts=`引数、戻り値にhearts_start／hearts_end／outcome(clear/death/unfinished)／limit。`hearts_lost`は開始hearts基準（既定3で従来と同値） | D-019 5 |
| repo/bots.py `read_script`／`main` | `hearts 3,2`（値ごとに実行）、`mode run|room`、`limit`未指定のrunは1200秒、出力にsource id・方針・反応0.15秒・初期位置（8,4）右向きを表示 | 同上 |
| repo/bots.py `play_run` | RunSessionを使い正規敵のみで1→5の1試行を実行。ラン時刻、部屋別戦闘時間、4遷移、ボス入場hearts、被弾源、部屋別attack／boss hit／dash、driver秒、processing秒（実時間）、pause 0、retry 0を分離して返す | 37の測定項目。fixtureや状態注入は使わない |
| repo/tests/test_bots_boss.py（新） | 危険線の検出、予兆中にswipeしないこと、開始hearts・outcome、limitでunfinished、ログ有無で結果不変（両FPS）、play_runの煙試験、script解析、source_id | D-019 4〜6。到達や攻略の合格は主張しない |
| repo/README.md | 上記を反映。dodger非対応の記述を差し替え | — |

play_runは、各botの判断をRunSession.pressへ中継するプロキシ経由で行う。入力はセッションのログに載り、クリア表示中は拒否される。入場ごとにBrain（反応記憶）を初期化する。retryとpauseは今回の道具では行わないので、0として「未実施」と明記してある。

### 実行結果

| 項目 | 結果 |
|---|---|
| 保存後suite | 未実行。実件数なし |
| bots／trace／run | 未実行 |
| 独立3・4の全bot×両FPS、新5番の3／2 hearts別比較、通常ラン同一試行 | 測定値なし |

実行が必要なコマンド（保存後。repo/で）：

1. `python3 -m unittest discover -s tests` — 件数と失敗、出力のsource idを記録する。
2. 独立3・4：script `rooms 3,4` / `fps 30` と `fps 60` を別実行し、`bots camper,walker,dodger`。
3. 新5番：script `bots dodger` / `rooms 5` / `hearts 3,2` / `limit 120`（limit値は選定が必要）/ `log on` を30と60で。
4. 保持分：`rooms 1-2`と`rooms 3,4`のdodger dash、1〜4のdodger FPS比較（`rooms 1-4`）。
5. 通常ラン：script `mode run` / `fps 30|60` / `limit 1200`、全bot。
6. 反応間隔と初期位置は出力ヘッダに出る。

### 未完了（優先順）

1. 上記の実行。特にdodgerの回帰（部屋1〜4の結果が提出前と同じか）とboss方針の効果は、実行まで不明。boss方針が戦闘に勝てない、あるいは30／60で差が出る可能性があり、その場合は判断ログで診断する。
2. V1：旧構文（legacy route）のboss表示、弾ID・消滅理由、長時間の観測蓄積確認は未着手。`drive`はeventsを逐次処理するので蓄積は線形のはずだが、未確認。
3. 契約試験：B3毎frame軌道、B6／B7実dash接触、B9接触無害、B10帯内外、T1〜T4・C2・C3のボス絡み、共有回帰の細目は36の表のとおり未網羅。
4. retryとpauseを含む通常ラン計測は、公開scriptのcontrol構文でrun_driver経由が必要。botsのplay_runでは行っていない。
5. 実機入力（V2）はD-021により対象外。

### 実装上の注意・既知リスク

- boss予兆中に線外で停止する方針は、予兆後の反撃位置へ戻る動きが遅れるかもしれない。判断は未測定。
- `_threat`の長さ・eta式は既存grub／弾と同じ近似であり、突進の丸い端や短射の弾速を厳密には反映しない。
- 仕様の不足・矛盾は見つけていない。Designerへの質問はない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託を加えない。未実行を成功としない。fixtureや独立部屋の時間合算を通常ラン到達の証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。完成前に独立QAへ送らない。

## Open questions

- 保存後のtests／botsを走らせる@run枠をどのStepに割り当てるか（Owner承認の再取得は不要）。
- 新規の仕様質問はない。同じ入力不足だけで再返却する場合は、その旨をStudioが明示する。

## Expected output

Studioは38のファイルを保存し、次のGameplay Engineer Step（またはqa運用が許す実行付きStep）に、上記コマンドの実行を指示する。結果を受けて、失敗の修正、残る契約試験とV1の補完、完成資料を作成してから独立QAへ送る。

## Sender assessment

実行ゼロのため、構文・回帰の確信度は低い。`_Proxy.__getattr__`は読み取り専用の使い方で、botは位置・hearts・敵・弾・stunを読むだけにしてある。play_roomの終了条件は従来のまま。リスクは、dodgerの変更が部屋1〜4へ漏れていないか（bossがなければ分岐は発火しない設計）の実行確認。

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
- Project: repo/source_id.py
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_boss_contract.py
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/37-studio-to-gameplay-engineer.md
