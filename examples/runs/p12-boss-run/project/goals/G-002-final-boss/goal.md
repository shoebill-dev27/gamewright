---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-20
---
# G-002: 最後に手応えのあるボス戦

## Owner request

> 最後に手応えのあるボス戦がほしい

## Interpretation

既存の第1〜4部屋を連続して進み、第5部屋を置き換えた単体ボスへ到達する。プレイヤーが位置取り、攻撃とダッシュのタイミング、敵の挙動への対応を通じて手応えを感じられる最終戦とし、最終勝利・死亡・ランの最初からの再挑戦まで成立する。短いランと、被害を受ける前に脅威を読み取れる体験を維持する。

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。

D-021により、今回はrepo/のテキスト表示とスクリプト実行で実装・検証する。Desktop、keyboard、gamepadは製品対象であり、実機ホストや実gamepadの供給・検証を今回の要件としない。基線はrepo/の現状とし、指定sha確認は不要。独立QA・PlayはStudio内の別Stepが担う。購入・外部委託・追加金銭を使わず、通常Stepの範囲で進める。具体的な追加支出や承認範囲を超える変更が必要になった場合はOwnerへ戻す。

## Unknowns

- Observe：skipped。既存不具合の再現依頼ではない。
- Diagnose：done。既存基盤の不足と計画上の回帰対応を整理済み。24に変更前のtests基線（69 tests、OK）が報告されている。
- Decide：done。D-015〜D-019で範囲・体験方向・仕様契約・旧基準の適用関係を確定。
- Design：done。design/final-boss-and-continuous-run.mdとD-017・D-019が正本。24では実装変更なし。変更後の検証は未実施。
- Plan：done。16・20の計画と回帰対応を使用する。D-021と衝突する実機ホスト・実機供給・外部配員・見積もり取得の要求は適用しない。
- Decide（供給・承認）：done。22へのOwner回答をD-021に記録。Ownerは実行経路とStudio内検証を指定し、Build開始を承認。実機供給、指定sha照合、人日見積もりは不要。
- Plan補完：skipped。新しいOwner条件を後続Stepへ直接渡せるため、同じ供給質問で再発行しない。具体的な技術上の不成立が判明した場合に限り戻す。
- Build：done。56でSplit Cを納品。runtimeの保存ソース04fa2b1c168aは全suite152件OK。pause/retry込み通常ランの同一試行計測、dodger独立1〜4の回帰固定、ボス判断ログを提出済み。報告された通常ラン勝利時間は30 FPS 86.967 s／60 FPS 103.533 s。履歴値との報告精度での一致と、変更前の厳密な同一性の未証明を区別する。Build証拠であり独立検証・体験判定ではない。
- Verify：未完了。60はfail。製品戦闘の再現済み不具合や同一基準の修正後再失敗2回とは扱わない。同じ不足のまま第三のQA依頼は出さず、D-023に合わせた基準整理・再計画・試験道具対応・再測定後に独立QAを再開する。全文保存先は存在しないため、検証対象を明示した出力と直列分割で必要な証拠を構成し、未確認を合格にしない。
- Plan（検証供給・試験道具）：done。62で公開情報だけのボス判断境界、接触診断、完全証拠保存、4条件再測定、独立1〜4回帰、変更前基線調査を計画。実行・修正・基線探索は未実施。仕様・難度・秒数ゲートは変更しない。
- Decide（検証供給）：done。D-023で案Aと供給上限を確定。Loadは個別ファイル本文、@needは一度8ファイルまで、@runはStepごとに3回まで、出力は最大2万字で全文保存先なし。変更前ビルドは存在しない。D-021のまま進める。
- Design（変更前一致）：done。65とD-024で、歴史的一致の確認不能、独立1〜4 dodgerの40の記録精度での比較、現行仕様照合・現行内対照を分離した。確認不能はpass・免除にせず最終Reviewへ残す。
- Plan（供給条件への適合）：done。68が62の実行計画を置換する。E0棚卸し→E1公開情報bot→E2接触診断→E3ボス4条件→E4保持回帰→E5公開再生→独立Q1〜Q6を直列実行する。各Step最大3回・各出力2万字以内、欠落は未確認。存在しない保存機構や変更前ビルドを前提にしない。
- Build（試験道具・再測定）：open。74はE1の連続partial 2回目（72・74）。70は別作業E0のため加算しない。保存済みsource b0770a4180c9は159件OKだが実dodger未接続。未保存接続案2集合は公開再生の無傷assertに失敗し不採用。75で実経路接続・被弾差診断・記憶初期化・全分岐試験・判断出力を継続する。13ファイル配布台帳と追加5IDのQ1/Q4割当を保持する。切断部分は未確認。次もE1 partialならTechnical Directorへ分割・再計画を戻す。E2以降は未着手。
- Decide（後続工程条件）：planned。歴史的確認不能を残して限定Art Verify以降へ進む条件をGame Directorに判断してもらう。Engineer・QAは先行可能。現行検証の完了を全基準passやGoal達成に読み替えない。
- Play：planned。独立したプレイヤー観察で最終戦・到達体験・通常ランの所要時間を評価する。実装内容と期待結果は渡さない。
- Design（実測後）：planned。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、追加数値ゲート・調整の要否を判断する。不要でも理由を記録。明白な対処不能・到達不能はPlay前に戻す。
- Review：planned。Game Directorが体験Goalの達成を判断する。
- Next：結果と残課題をOwnerへ返す。

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
| 7b-e1b | Build | gameplay-engineer | implement-change | open | 75-studio-to-gameplay-engineer.md |
| 7b-build | Build | gameplay-engineer | implement-change | planned | 68のE2→E3群→E4群→E5群を直列分割。70の残作業を継承 |
| 7c | Verify | qa | verify-change | planned | E0の全試験台帳を使い68のQ1〜Q6を直列分割 |
| 7d | Decide | game-director | make-decision, prepare-owner-escalation | planned | 歴史的確認不能を保持した後続評価工程の条件判断 |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。68に従いE0→E1→E2→E3群→E4群→E5群→独立Q1〜Q6を進める。E0の全試験台帳からQAの個別Loadを割り当て、追加試験も含め未配布を残さない。現行必須検証、公開情報条件、再測定、記録差へのDesigner回答が揃い、歴史比較以外の不足を解消した後、Game Directorが歴史的確認不能を保持した評価継続の条件を判断する。認められた場合、限定Art Verify→独立Play→Designer実測後判断→Reviewへ進む。各StepのLoadは個別ファイル指定。全文保存先・別実行枠・変更前ビルドを待たない。明白な対処不能・到達不能や規定外の比較差はDesignerへ戻す。並列Stepは開かない。

## Route changes

74をE1の連続partial 2回目（72・74）として受領し、75で同Roleへ継続する。70はE0であり同じE1の回数に含めない。保存済み159件成功と未保存接続案の失敗を区別し、E2は開かない。次もE1 partialならTechnical Directorへ分割・再計画を戻す。

## Next action

Gameplay Engineerが75-studio-to-gameplay-engineer.mdでE1を継続する。公開再生の被弾差を診断し、既存assertを保持して実dodger接続・記憶・全分岐・判断本文を整える。未保存案を保存済み基線へ混同しない。次のE1結果もpartialならTechnical Directorへ戻し、E1完了確認まではE2を開かない。

## Outcome

未完了。公開境界prototypeの限定監査を受領したが、実dodger接続は未完了。保存済みsource b0770a4180c9の159件成功は独立QAや基準充足を示さない。未保存接続案は公開再生の無傷assertに失敗し不採用。同じE1のpartialは2回であり同Roleへ継続し、次もpartialなら再計画へ戻す。未表示・切断・未対応を合格にしない。歴史的確認不能、記録精度に限定した比較、試験道具対応・再測定、独立QA、後続工程条件判断、限定Art Verify・独立Play・Designer判断・Reviewを残す。戦闘本体の不具合・難度・時間Visionとの差は未判定。project.mdは変更しない。
