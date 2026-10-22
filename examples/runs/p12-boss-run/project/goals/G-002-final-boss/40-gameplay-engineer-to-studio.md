---
kind: handoff
goal: G-002
seq: 40
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 40: gameplay-engineer → studio — 保存版を実行: suite 112件OK、独立3・4／新5番／通常ランの測定を取得。V1補完・細目の契約試験・retry/pause計測は未実施

## Task

実行結果（source id `5145454ab956`）を受領する。独立QAへ送るか、先に未実施分（V1補完、契約試験の細目、retry/pause計測）を別Stepで補うかを判断する。新5番と通常ランの実測は、D-019に従いDesignerの「実測後判断」へルーティングする。

## Context

39は、38で提出した未実行の変更（source_id、boss対応dodger、開始hearts指定、play_run、test_bots_boss.py）を保存版で実行し、失敗を直し、測定を返すよう求めた。このStepでは@runで次の3種を実行した。

- tests
- 独立3・4、新5番、保持分のbots
- 通常ランのbots

全実行が同じsource idを出力した。コードの修正は不要で、失敗はなかった。変更したのはrepo/README.mdの「未実行」記述だけである。

## Findings

### 実行済み

**1. 保存後suite**

- `python3 -m unittest discover -s tests`: **112件、失敗0、OK**（0.208 s）。
- 実行時のsource id: `5145454ab956`（以下の全bots実行のヘッダと同じ）。
- 供給済みの98／103件は今回の保存版に帰属しない。今回の112件が保存版に対する件数である。
- 内訳は未確認で、test_bots_boss.pyの件数は確認していない。

**2. 独立3・4（rooms 3,4。fps 30と60を別実行。開始3 hearts、limit 60 s）**

| bot | FPS | 部屋3 | 部屋4 |
|---|---|---|---|
| camper | 30 | 死亡 6.3 s、失hearts 3（shot 3）、攻撃0、dash0 | 死亡 6.7 s、3（shot 3）、攻撃1、dash0 |
| camper | 60 | 死亡 6.3 s、3（shot 3）、攻撃0、dash0 | 死亡 6.8 s、3（shot 3）、攻撃1、dash0 |
| walker | 30 | clear 8.9 s、失1（grub 1）、攻撃8、dash0 | clear 9.9 s、失1（grub）、攻撃7、dash0 |
| walker | 60 | clear 9.2 s、失1（grub 1）、攻撃8、dash0 | clear 9.8 s、失1（grub）、攻撃7、dash0 |
| dodger | 30 | clear 15.6 s、失0、攻撃8、dash6 | clear 18.3 s、失0、攻撃7、dash7（合計13） |
| dodger | 60 | clear 15.0 s、失0、攻撃8、dash6 | clear 17.0 s、失0、攻撃7、dash8（合計14） |

- 各行の終了時heartsと outcome は上表から導ける（camperは0／death、walkerは2／clear、dodgerは3／clear）。
- 方針とビルドの識別はsource idと出力ヘッダにある。
- dodgerのdashは各FPSで1回以上（13／14）。combat.md15の独立3・4条件は満たす。
- 新たな合計ゲートは設けていない（D-019 2）。

**3. 保持分（rooms 1-4。30と60を別実行）**

| bot | FPS | 部屋1 | 部屋2 | 部屋3 | 部屋4 | 合計 |
|---|---|---|---|---|---|---|
| camper | 30 | 死亡 5.7 s、失3 | clear 10.2 s、失2 | 死亡、失3 | 死亡、失3 | clear 1/4、失11 |
| camper | 60 | 死亡、失3 | 死亡 8.9 s、失3 | 死亡、失3 | 死亡、失3 | clear 0/4、失12 |
| walker | 30 | 死亡 4.9 s、失3 | clear 8.4 s、失2 | clear、失1 | clear、失1 | clear 3/4、失7 |
| walker | 60 | 死亡 5.2 s、失3 | clear 8.4 s、失2 | clear、失1 | clear、失1 | clear 3/4、失7 |
| dodger | 30 | clear 6.6 s、失0、dash3 | clear 20.7 s、失0、dash10 | clear 15.6 s、dash6 | clear 18.3 s、dash7 | 4/4、失0、dash 26 |
| dodger | 60 | clear 9.6 s、失0、dash5 | clear 25.1 s、失0、dash14 | clear 15.0 s、dash6 | clear 17.0 s、dash8 | 4/4、失0、dash 33 |

- combat.md14（独立1〜2、各FPS別）:
  - walkerの失hearts合計は30で5、60で5（1以上）。
  - dodgerは両FPSで両部屋clear、失0（1以下）。
  - この解釈は「失hearts」。
- dodgerの1〜4 FPS比較は、clear結果が同一（4/4）で、hearts lost差は0。
- 注意: camperは部屋2のclear結果が30と60で異なる。camperには成績一致条件がない（D-019 7）ので、報告のみとする。

**dodger部屋1〜4が提出前と同じか**: **確認できていない**。パケットに提出前の数値がない。コード上は、`_dangers`と`dodger`に追加したboss用の分岐が`e.kind == "boss"`のときだけ働くため、部屋1〜4では発火しない。ただしこれは設計上の推定であり、実行による同一性の証明ではない。比較できる提出前の記録（G-001の測定値など）があればQAが照合してほしい。

**4. 新5番（rooms 5、hearts 3,2、limit 120、30と60を別実行。boss対応dodger、`log on`なし）**

| FPS | 開始hearts | 結果 | 秒数 | 失hearts | 攻撃 | dash |
|---|---|---|---|---|---|---|
| 30 | 3 | clear | 21.6 s | 0 | 12 | 8 |
| 30 | 2 | clear | 21.6 s | 0 | 12 | 8 |
| 60 | 3 | clear | 32.9 s | 0 | 12 | 12 |
| 60 | 2 | clear | 32.9 s | 0 | 12 | 12 |

- FPS比較（D-019 4・5）: 3 heartsの対も2 heartsの対も、同じclear結果で、hearts lost差は0。比較条件は満たす。
- 秒数は30と60で約11 s差、dashは8対12と差がある。秒数差に閾値はなく、診断はログで行う。`log on`の判断ログは取っていない。
- 次の2点はDesignerに渡す観察である。
  - botは被弾0でボスを倒す。
  - 開始heartsが3でも2でも軌跡が同一であり、被弾が一度も起きていない。
- これは攻略可能性の証拠でもFPS差の診断でもない。診断はログが必要。B5〜B10の実接触の確認にもならない（未実施）。

**5. 通常ラン（`mode run`、limit 1200、全bot、fps 30と60を別実行、各1試行）**

| bot | FPS | 結果 | ラン時刻 | 部屋別戦闘時間（room time）・備考 |
|---|---|---|---|---|
| camper | 30 | 部屋1で死亡 | 5.733 s | 失3（grub）、攻撃5 |
| camper | 60 | 部屋1で死亡 | 5.700 s | 失3（grub）、攻撃4 |
| walker | 30 | 部屋1で死亡 | 4.867 s | 失3（grub）、攻撃5 |
| walker | 60 | 部屋1で死亡 | 5.233 s | 失3（grub）、攻撃4 |
| dodger | 30 | **勝利** | **86.967 s** | 6.63 / 20.73 / 15.63 / 18.33 / 21.63 s |
| dodger | 60 | **勝利** | **103.533 s** | 9.62 / 25.07 / 15.02 / 16.97 / 32.87 s |

- dodgerの共通項目:
  - 遷移はすべて1.0 s（4回）。
  - ボス入場heartsは3。
  - 被弾0。
  - 部屋5の攻撃12回はすべてボスに命中（boss hits 12）。
  - retries 0、pause 0.0 s。
  - attempt 1。
  - driver秒とラン時刻は同じ（30で86.967 s、60で103.533 s）。
  - processing 0.02〜0.03 s（実時間であり、プレイ時間ではない）。
- 試行数は各botで1。結果は決定的なので、再実行で変わるとは期待しない。
- 独立部屋時間の合算ではなく、`RunSession`の同一試行の時計から出した値である。fixtureや状態注入は使っていない。
- camperとwalkerは部屋1で死亡して終わるため、ボスには到達しない。
- 15〜20分のVisionとの差:
  - 実測は1.5〜1.7分で、大幅に短い。
  - この測定は被弾0・retry0・待機0の理想的なbotによる下限に近い。
  - 人間のプレイは含まず、参考にはならない。
  - 時間合わせのHP増加や待機はしない（Constraints）。
  - Designerによる実測後の判断（D-019）と独立Playに渡す。

### 変更したファイル

- repo/README.md: 「実行されていない」記述を、step 40で実行済み・source id・結果の所在に更新した。
- コードとテストは変更していない（失敗がなかったため）。BUILDは0.6-g002-public-32のまま。

### 未実施

- V1補完（legacy route表示、弾ID・消滅理由、長時間の観測蓄積）。
- 契約試験の細目: B3毎frame軌道、B6／B7実dash接触、B9接触無害、B10帯内外、T1〜T4・C2・C3のボス絡み、共有回帰の細目。
- pause・retryを含む通常ラン計測（run_driverのcontrol構文経由）。botsのplay_runは両方を行わない。
- ボス部屋の`log on`による判断ログ診断（差が約11 sあるため、必要なら取る）。
- V2（実機入力）はD-021により対象外。
- 現行の他のrun経路（`play.py --view trace`）の実行は、このStepでは行っていない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託は加えていない。独立部屋の時間合算を通常ラン到達の証拠にしない。完成前に独立QAへ送らない。

## Open questions

- 仕様の不足・矛盾: なし。Designerへの質問はない。
- Studioへ（ルーティング判断）:
  1. 未実施の契約試験・V1補完を、独立QAへ送る前に別のGameplay Engineer Stepで完了させるか。全て完了とは言えないので、このハンドオフは完成資料ではなく部分成果として扱うのが妥当。
  2. 新5番のbot成績（被弾0、両FPSで同一clear、時間約22 s／33 s）と通常ランの総時間（約1.5〜1.7分）をDesignerの実測後判断へ回すこと。その際、botが被弾0であり、ボスの攻撃が実際に回避された根拠はB5〜B10の接触試験で別途確認する必要がある点を添える。
  3. dodger部屋1〜4が提出前と同じかについて、比較できる提出前の記録の有無。

## Expected output

Studioは次を行う。

- 上記の判断に従い、未実施の契約試験・V1補完・retry/pause計測を別のGameplay Engineer Stepとしてルーティングする。または、QAが追加試験を行う前提で独立QAへ送る。
- Designerの実測後判断（新5番、通常ラン時間）をReview前にルーティングする。
- 完成資料はまだない（部分成果）。

## Sender assessment

- 38の変更はそのまま通った。112件OK、全botの実行も例外なく完了し、保存版の構文リスクは解消した。
- 未実行リスクのうち、部屋1〜4への漏れは、コード上は発火しない構造で、結果も不自然ではない。ただし提出前との数値比較はできていない。
- dodgerがボス戦で被弾0なのは、方針が「警告中は線外で停止、線上なら即dash／step」と保守的だからだと考える。ただしログを見ていないので推測である。
- 30と60で秒数・dash数が違う理由（約11 s、8対12）は未診断。
- 2 heartsと3 heartsで軌跡が同じなのは、被弾が一度もないため当然である。ボス戦の死亡リスクは、このbotでは測れていない。
- 確信度: suiteとbots出力の事実としての正確さは高い。難度・体験・FPS差の原因については結論を持たない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/README.md
- Project: repo/tests/test_bots_boss.py
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/39-studio-to-gameplay-engineer.md
