---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-10
---
# G-001: ダッシュ中の被ダメージに関する文書評価を完了する

## Owner request

当初の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

2026-10-11 の範囲変更：

> B。模擬専用のサンプルなので、模擬ビルド記述に基づく文書評価をこの Goal の検証とし、計測できない項目は未判定として明記したうえで Goal を閉じてください。

## Interpretation

D-004 に基づき、現資料と最新の模擬ビルド `sim/build-0.4.md`（変更識別子 `0.3-G001-15`）による文書評価を本 Goal の検証とする。確認できる文書上の整合、計測できず未判定となる項目、仕様不足、再開条件を報告し、変更後の完了条件に対する Review を経て閉じる。

全4環境の挙動実証や不具合解消の保証は完了条件としない。追加取得・計測、新規 simulator 開発、実機試験、追加実装、仕様変更、巻き戻し、無関係なバランス調整は対象外。

## Unknowns

- Observe：仕様不一致の照合と AC-1〜AC-6 の作成は完了。Owner の詳細条件の独立した試行再現とは扱わない。
- Diagnose / Plan：D-003 と模擬実装定義は存在する。25で現資料による文書評価、限界、再開条件の報告を完了した。
- Decide：Owner が D-004 で文書評価への範囲変更を決定済み。
- Design：クールダウン0.6秒の起点は未定義。今回は不足として報告し、新たな仕様判断は行わない。
- Build：模擬変更の定義は完了。今回の範囲では追加修正を行わない。
- Verify：Handoff 21 の文書評価は完了、総合結果は `question`。条件別証拠と全4環境の計測は不足したまま。D-004 に従い文書評価を今回の検証とし、実証できない項目は未判定で残す。
- Play：体験評価を求める Goal ではないため省略。
- Review：27で game-director が変更後の完了条件に対して `goal-met` と判断した。
- Next：Studio が Review を受け、未判定事項と再開条件を Outcome に記録して Close 完了。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 01-studio-to-qa.md |
| 1b | Observe | qa | reproduce-defect | done | 03-studio-to-qa.md |
| 1c | Observe | qa | reproduce-defect | done | 05-studio-to-qa.md |
| 1d | Observe | qa | reproduce-defect | done | 07-studio-to-qa.md |
| 1e | Observe | qa | reproduce-defect | done | 10-studio-to-qa.md |
| 2 | Diagnose / Plan | technical-director | technical-plan | done | 12-studio-to-technical-director.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | skipped | — |
| 4 | Design | game-designer | write-design-spec | skipped | — |
| 5 | Plan | technical-director | technical-plan | skipped | — |
| 6 | Build | gameplay-engineer | implement-change | done | 14-studio-to-gameplay-engineer.md |
| 6b | Build 資料照合・補完 | gameplay-engineer | implement-change | done | 16-studio-to-gameplay-engineer.md |
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | done | 18-studio-to-technical-director.md |
| 7 | Verify 文書評価・証拠充足性確認 | qa | verify-change | done | 20-studio-to-qa.md |
| 7a | Owner escalation 準備 | technical-director | prepare-owner-escalation | done | 22-studio-to-technical-director.md |
| 7a-owner | Decide 検証範囲変更 | owner | — | done | 23-technical-director-to-owner.md |
| 7b | Design クールダウン起点 | game-designer | write-design-spec | skipped | — |
| 7c | Verify 補完後の独立検証 | qa | verify-change | skipped | — |
| 7d | Diagnose 文書評価報告の整理 | technical-director | technical-plan | done | 24-studio-to-technical-director.md → 25-technical-director-to-studio.md |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review 変更後の完了条件 | game-director | review-outcome | done | 26-studio-to-game-director.md → 27-game-director-to-studio.md |
| 10 | Next | studio | — | done | 27-game-director-to-studio.md → 本記録の Outcome |

done は作業終了を示し、再現成功や検証合格を意味しない。主要結果は 11（不具合報告・AC）、13（計画）、15（模擬実装定義）、17（資料照合、question）、19（条件付き再計画）、21（文書評価、question）、23（Owner escalation、D-004 により resolved）、25（文書評価報告、done）、27（変更後の完了条件に対する Review、goal-met）。

行 7b・7c の省略は不足の解消ではなく、D-004 による完了条件の変更による。既存 QA 判定の再採点や、同じ不足入力での QA 再依頼は行わない。

## Route changes

2026-10-10 — 02・04・06・08 の入力不足が解消せず、09 で Owner に escalation。D-002 の継続判断と補足観察を受け、11 の不具合報告・AC、13 の計画と D-003 に基づき Build へ進んだ。

2026-10-11 — 15 の模擬実装定義と17の資料照合により build-0.4 と変更識別子の対応を採用。資料不足は19で再計画し、21の独立 QA は文書評価を完了したが証拠不足により question とした。

2026-10-11 — 外部照会手段未確保のため22で brief 作成を依頼し、23を Owner に提示して blocked-on-owner とした。問い合わせ済み・モデル不存在・検証 fail とは扱っていない。

2026-10-11 — Resume：Owner の B と文書評価による完了条件を D-004 に記録し、23を resolved、Goal を active に変更。追加計測・仕様判断は省略し、24で文書評価報告を technical-director に依頼。

2026-10-11 — 25で文書評価報告が完了し、26で game-director の Review を開始。未判定事項は承認済み範囲内の報告事項として扱った。

2026-10-11 — 27の `goal-met` を受けて Review を完了し、予定どおり Close。既存 QA の `question` と未判定事項を保持し、将来の課題は新規 Goal 候補とした。追加の escalation は不要。

## Next action

G-001 は終了。次に開始する Step はなく、追加の Owner 回答も不要。

挙動実証が必要になった場合、または条件別証拠へのアクセスが得られた場合は、下記の再開条件を用いて新規 Goal として扱う。

## Outcome

2026-10-11、G-001 を文書評価の Goal として終了した。game-director は `27-game-director-to-studio.md` で、D-004 による変更後の完了条件を満たしたと判断した（`goal-met`）。

対象は `sim/build-0.4.md`（変更識別子 `0.3-G001-15`）。文書評価を完了し、ダッシュ中と被弾後の保護、通常被害、移動、予約攻撃について既存仕様との文書上の整合を確認した。クールダウンは0.6秒という数値のみ確認でき、起点は未定義のため完全な文書適合は未判定である。

### 検証の限界

- Desktop の30／60 FPS × キーボード／ゲームパッドの全4環境で、条件別挙動と回帰は未判定。実際の不具合解消や全条件合格は実証していない。独立 QA の Handoff 21 の総合判定は `question` のまま維持する。
- 試行総数・有効数・無効数・不具合発生数は不明であり、ゼロ件や非発生を意味しない。時刻例や全環境への適用宣言は条件別試行記録ではなく、修正前後の同一条件比較も実施済みとは扱わない。
- 30 FPS の実際の終了表示フレームや更新順序は観察・実装詳細不足であり、継続時間違反とは断定しない。完全同時の命中優先順位、入力不能中の予約入力、丸め規則、許容差は新たに定めていない。
- 外部照会は手段未確保・問い合わせ未実施。モデル不存在や永久的な取得不能は確認されていない。
- Review は提供された模擬ビルド・仕様・AC・独立 QA と25の報告に基づく。Review に原文が提供されなかった `sim/repo-notes.md` 等の再照合は行っていない。

### Decisions

- D-001：Owner 承認なしに戦闘入力を追加しない制約を維持した。
- D-002：Owner の補足観察を受けて修正を継続した。完了条件は後に D-004 で変更した。
- D-003：保護を発生源別に管理し、その論理和で判定する方針を採用した。防いだ命中では保護を開始・延長しない。
- D-004：Owner が模擬ビルド記述による文書評価を今回の検証とし、未判定事項と再開条件を報告して Review 後に閉じることを決定した。

今回の Review では新たな方向性・仕様・技術方式を決定しておらず、追加の Decision は作成していない。

### 将来の課題と再開条件

以下は新規 Goal 候補であり、今回の終了の追加条件ではない。

1. **条件別の独立した挙動検証。** 不具合解消や全4環境での保証が必要になった場合、または条件別証拠・モデルへのアクセスが得られた場合に、Studio を通じて対象ビルド、範囲、仕様、AC、必要入力を再確認する。取得経路・資料の来歴と表現範囲を確認し、各環境・命中源・回帰の記録と試行集計を揃えて独立 QA に渡す。
2. **再使用と時間境界の期待値補完。** クールダウン起点の既存原資料を回復し、得られなければ game-designer に判断を返す。30 FPS の更新順序等は資料を先に確認し、期待値がなお定まらない場合だけ仕様判断へ進む。同時境界や予約入力は検証上必要になった場合に扱う。

新規 simulator 開発、実機試験、追加実装は今回の承認範囲外であり、必要になった際に別途範囲を判断する。現時点で Owner に求める判断・提供物はない。
