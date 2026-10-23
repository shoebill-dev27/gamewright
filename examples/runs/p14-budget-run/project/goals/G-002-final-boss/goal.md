---
kind: goal
id: G-002
project: lantern-depths
status: abandoned
created: 2026-10-20
budget: 123
---
# G-002: 最後に手応えのあるボス戦

## Owner request

> 最後に手応えのあるボス戦がほしい

## Interpretation

既存の第1〜4部屋を連続して進み、第5部屋を置き換えた単体ボスへ到達する。プレイヤーが位置取り、攻撃とダッシュのタイミング、敵の挙動への対応を通じて手応えを感じられる最終戦とし、最終勝利・死亡・ランの最初からの再挑戦まで成立する。短いランと、被害を受ける前に脅威を読み取れる体験を維持する。

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。

D-021により、今回はrepo/のテキスト表示とスクリプト実行で実装・検証する。Desktop、keyboard、gamepadは製品対象であり、実機ホストや実gamepadの供給・検証を今回の要件としない。基線はrepo/の現状とし、指定sha確認は不要。独立QA・PlayはStudio内の別Stepが担う。購入・外部委託・追加金銭を使わず、通常Stepの範囲で進める。具体的な追加支出や承認範囲を超える変更が必要になった場合はOwnerへ戻す。

## Unknowns

- Design・方向判断：完了。D-015〜D-019で連続ラン、単体ボス、仕様契約と旧基準の適用関係を確定。D-021・D-023でテキストビルドとStudio内検証の供給条件を確定した。
- Build：連続ランと第5部屋の単体ボスは実装報告済み。56には通常ラン、pause/retry、独立1〜4回帰と判断ログのBuild証拠がある。通常ラン勝利時間の報告値は30 FPS 86.967秒／60 FPS 103.533秒。独立検証・体験判定ではない。
- Build（試験道具・再測定）：未完了のまま打切り。80で突進被弾とshot診断を分離し、両FPSの通常命中fixtureを保存。source fc07c7db6383で161 tests OKをruntimeが確認した。公開情報限定の実dodger接続、記憶・全分岐・判断出力、被弾差の原因確定は未完了。必要本文の一部は出力切断で未確認。
- Plan：68の供給適合計画、82のE1 A〜D分割を作成済み。A〜Dの実行完了には至っていない。
- Verify：未完了。58・60の証拠・供給不足は解消済みとしない。E2全体、E3ボス4条件、E4保持回帰・記録比較、E5通常公開再生、独立Q1〜Q6、限定Art Verifyは未完了。再現済み製品戦闘不具合や同一基準の修正後再失敗2回という判定ではない。
- 歴史的比較：D-024により、変更前ビルド不在による厳密な歴史的一致の確認不能を、記録精度での比較、現行仕様照合、現行内対照から分離する。確認不能を合格・免除としない。
- Play・実測後Design・Review：未実施で打切り。最終戦の手応え、到達体験、追加数値ゲート・調整の要否、15〜20分Visionとの整合は未評価。Goal達成のReview verdictはない。
- Decide（終了）：完了。Ownerは85の案Bを選択し、D-027で費用を理由に未達・検証未完了でのCloseを決定。budgetは123のまま。残工程は今回実施しないためskippedとするが、検証免除や合格を意味しない。
- Next：本Resumeで終了。続きの必要性はOwnerが別Goalとして後日判断する。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md → 結果: 02-game-designer-to-studio.md |
| 2 | Diagnose | technical-director | technical-plan | done | 03-studio-to-technical-director.md → 結果: 04-technical-director-to-studio.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done | 05-studio-to-game-director.md → 結果: 06-game-director-to-owner.md |
| 3a | Decide | owner | — | done | 06-game-director-to-owner.md → D-015 |
| 3b | Decide | game-director | make-decision, prepare-owner-escalation | done | 07-studio-to-game-director.md → 結果: 08-game-director-to-studio.md |
| 4 | Design | game-designer | write-design-spec | done | 09-studio-to-game-designer.md → 結果: 10-game-designer-to-studio.md |
| 4a | Decide | game-director | make-decision, prepare-owner-escalation | done | 11-studio-to-game-director.md → 結果: 12-game-director-to-studio.md |
| 4b | Design | game-designer | make-decision, write-design-spec | done | 13-studio-to-game-designer.md → 結果: 14-game-designer-to-studio.md |
| 5 | Plan | technical-director | technical-plan | done | 15-studio-to-technical-director.md → 結果: 16-technical-director-to-studio.md |
| 5a | Decide | game-director | make-decision, prepare-owner-escalation | done | 17-studio-to-game-director.md → 結果: 18-game-director-to-studio.md |
| 5b | Plan | technical-director | technical-plan | done | 19-studio-to-technical-director.md → 結果: 20-technical-director-to-studio.md |
| 5c | Decide | game-director | make-decision, prepare-owner-escalation | done | 21-studio-to-game-director.md → 結果: 22-game-director-to-owner.md |
| 5c-owner | Decide | owner | — | done | 22-game-director-to-owner.md → D-021 |
| 5d | Plan | technical-director | technical-plan | skipped | D-021で供給・承認条件を解決。再照会不要 |
| 6 | Build | gameplay-engineer | implement-change | done | 23-studio-to-gameplay-engineer.md → 結果: 24-gameplay-engineer-to-studio.md |
| 6a | Build | gameplay-engineer | implement-change | done | 25-studio-to-gameplay-engineer.md → 結果: 26-gameplay-engineer-to-studio.md |
| 6b | Build | gameplay-engineer | implement-change | done | 27-studio-to-gameplay-engineer.md → 結果: 28-gameplay-engineer-to-studio.md |
| 6c | Build | gameplay-engineer | implement-change | done | 29-studio-to-gameplay-engineer.md → 結果: 30-gameplay-engineer-to-studio.md |
| 6d | Build | gameplay-engineer | implement-change | done | 31-studio-to-gameplay-engineer.md → 結果: 32-gameplay-engineer-to-studio.md |
| 6e | Build | gameplay-engineer | implement-change | done | 33-studio-to-gameplay-engineer.md → 結果: 34-gameplay-engineer-to-studio.md |
| 6f | Build | gameplay-engineer | implement-change | done | 35-studio-to-gameplay-engineer.md → 結果: 36-gameplay-engineer-to-studio.md |
| 6g | Build | gameplay-engineer | implement-change | done | 37-studio-to-gameplay-engineer.md → 結果: 38-gameplay-engineer-to-studio.md |
| 6h | Build | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md → 結果: 40-gameplay-engineer-to-studio.md |
| 6i | Build | gameplay-engineer | implement-change | done | 41-studio-to-gameplay-engineer.md → 結果: 42-gameplay-engineer-to-studio.md（未着手） |
| 6j | Build | gameplay-engineer | implement-change | done | 43-studio-to-gameplay-engineer.md → 結果: 44-gameplay-engineer-to-studio.md |
| 6k | Build | gameplay-engineer | implement-change | done | 45-studio-to-gameplay-engineer.md → 結果: 46-gameplay-engineer-to-studio.md（部分成果、V1は質問） |
| 6k-d | Design | game-designer | write-design-spec | done | 47-studio-to-game-designer.md → 結果: 48-game-designer-to-studio.md（D-022） |
| 6k-b | Build | gameplay-engineer | implement-change | done | 49-studio-to-gameplay-engineer.md → 結果: 50-gameplay-engineer-to-studio.md（partial、入力不足） |
| 6k-c | Build | gameplay-engineer | implement-change | done | 51-studio-to-gameplay-engineer.md → 結果: 52-gameplay-engineer-to-studio.md（partial、140件OK） |
| 6k-d2 | Build | gameplay-engineer | implement-change | done | 53-studio-to-gameplay-engineer.md → 結果: 54-gameplay-engineer-to-studio.md |
| 6l | Build | gameplay-engineer | implement-change | done | 55-studio-to-gameplay-engineer.md → 結果: 56-gameplay-engineer-to-studio.md |
| 7 | Verify | qa | verify-change | done | 57-studio-to-qa.md → 結果: 58-qa-to-studio.md（証拠不足） |
| 7a | Verify | qa | verify-change | done | 59-studio-to-qa.md → 結果: 60-qa-to-studio.md（供給不足・bot所見） |
| 7b | Plan | technical-director | technical-plan, prepare-owner-escalation | done | 61-studio-to-technical-director.md → 結果: 62-technical-director-to-studio.md |
| 7b-owner | Decide | owner | — | done | 63-studio-to-owner.md → D-023 |
| 7b-design | Design | game-designer | make-decision, write-design-spec | done | 64-studio-to-game-designer.md → 結果: 65-game-designer-to-studio.md（D-024） |
| 7b-plan | Plan | technical-director | technical-plan | done | 66-studio-to-technical-director.md → 結果: 68-technical-director-to-studio.md |
| 7b-e0 | Build | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md → 結果: 70-gameplay-engineer-to-studio.md（partial、棚卸し受領） |
| 7b-e1 | Build | gameplay-engineer | implement-change | done | 71-studio-to-gameplay-engineer.md → 結果: 72-gameplay-engineer-to-studio.md（partial、prototype未接続） |
| 7b-e1a | Build | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md → 結果: 74-gameplay-engineer-to-studio.md（E1 partial 2回目） |
| 7b-e1b | Build | gameplay-engineer | implement-change | done | 75-studio-to-gameplay-engineer.md → 結果: 76-gameplay-engineer-to-studio.md（E1 partial 3回目） |
| 7b-scope | Decide | game-director | make-decision, prepare-owner-escalation | done | 77-studio-to-game-director.md → 結果: 78-game-director-to-owner.md |
| 7b-cost | Decide | owner | — | done | 78-game-director-to-owner.md → D-026 |
| 7b-build | Build | gameplay-engineer | implement-change | done | 79-studio-to-gameplay-engineer.md → 結果: 80-gameplay-engineer-to-studio.md（partial、突進診断の限定修正） |
| 7b-replan | Plan | technical-director | technical-plan | done | 81-studio-to-technical-director.md → 結果: 82-technical-director-to-studio.md |
| 7b-budget | Decide | game-director | prepare-owner-escalation | done | 83-studio-to-game-director.md → 結果: 84-game-director-to-studio.md |
| 7b-budget-owner | Decide | owner | — | done | 85-studio-to-owner.md → D-027 |
| 7b-e1-A | Build | gameplay-engineer | implement-change | skipped | D-027による打切り。82のAは未完了 |
| 7b-e1-B | Build | gameplay-engineer | implement-change | skipped | D-027による打切り。82のBは未完了 |
| 7b-e1-C | Build | gameplay-engineer | implement-change | skipped | D-027による打切り。82のCは未完了 |
| 7b-e1-D | Build | gameplay-engineer | implement-change | skipped | D-027による打切り。82のDは未完了 |
| 7b-e2 | Build | gameplay-engineer | implement-change | skipped | 接触診断全体は未完了。D-027 |
| 7b-e3 | Build | gameplay-engineer | implement-change | skipped | ボス4条件の再測定は未実施。D-027 |
| 7b-e4 | Build | gameplay-engineer | implement-change | skipped | 保持回帰・記録比較は未実施。D-027 |
| 7b-e5 | Build | gameplay-engineer | implement-change | skipped | 通常公開再生は未実施。D-027 |
| 7c | Verify | qa | verify-change | skipped | 独立Q1〜Q6は未実施。D-027 |
| 7d | Decide | game-director | make-decision, prepare-owner-escalation | skipped | D-025により重複条件判断を省略 |
| 8 | Verify | art-director | visual-review | skipped | 未実施。D-027 |
| 9 | Play | playtester | playtest-session | skipped | 未実施。D-027 |
| 9a | Design | game-designer | make-decision, write-design-spec | skipped | 実測後判断は未実施。D-027 |
| 10 | Review | game-director | review-outcome | skipped | 未実施。達成判定なし。D-027 |
| 11 | Next | studio | — | done | D-027に基づき本ResumeでClose |

D-027により残工程を打ち切る。skippedは終了に伴う未実施の記録であり、必須検証の合格・免除を意味しない。新しいHandoffは発行しない。

## Route changes

Ownerの案BをD-027に記録し85をresolvedとする。費用を理由に残工程をskippedとし、G-002を未達・検証未完了でabandonedとしてClose。budgetは123を維持し、成果と不足をOutcomeおよびproject.mdのCurrent stateへ反映する。次Stepは開かない。

## Next action

なし。D-027により終了。続きの必要性はOwnerが別Goalとして後日判断する。

## Outcome

**未達・検証未完了で打切り。** Ownerは、残必須工程44〜48 operationsが今回かけられる費用を超えるとして案Bを選択した。D-027に基づきstatus: abandonedでCloseし、budgetは123のまま追加作業を開かない。

成果として、既存第1〜4部屋から続く連続ランと、第5部屋を置き換える単体ボスが実装報告済み。終端・再挑戦を含むBuild証拠も提出されている。source fc07c7db6383では161件の試験成功をruntimeが確認した。今回のcurrent_buildはrepo/、sha dc0138c2b6d1であり、このResumeで再試験はしていない。実装の削除・巻戻しは行わない。

未完了なのは、E1 A〜Dの出力整備・公開情報限定の実dodger接続と記憶・被弾差の原因確定・実経路監査、E2接触診断全体、E3ボス4条件の再測定、E4保持回帰・記録比較、E5通常公開再生と必要証拠の確認。独立QA Q1〜Q6、限定Art Verify、独立Play、Designer実測後判断、最終Reviewも未実施である。以前のQAの証拠・供給不足は解消済みとしない。161件の成功は、これらの代用でも「手応えのあるボス戦が成立した」という結論でもない。

変更前ビルド不在による厳密な歴史的一致の確認不能は、D-024に従って上記の未実施・未解消事項と区別して残す。Build報告の通常ラン勝利時間は30 FPS 86.967秒／60 FPS 103.533秒だが、15〜20分Visionとの整合や到達・最終戦の体験は未評価である。

D-015〜D-025で範囲・方向・仕様・検証条件を定め、D-026で継続予算を123に変更し、D-027で費用による終了を決めた。続きが必要なら、残検証と体験評価を対象とする別Goalの要否・範囲・予算をOwnerが後日判断する。現在、回答待ちのOwner事項や開いているStepはない。
