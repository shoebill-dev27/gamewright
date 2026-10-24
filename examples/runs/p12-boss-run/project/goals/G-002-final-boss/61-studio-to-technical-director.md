---
kind: handoff
goal: G-002
seq: 61
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 61: studio → technical-director — 検証供給障害の整理とOwner escalation準備

## Task

独立QAが二度報告した入力・実行機能の不足を技術的に整理し、Ownerが回答できる具体的なEscalationを準備する。併せて、D-019のボスbot観測条件に関する所見を確認し、試験道具の対応と独立再検証の順序を計画する。

## Context

58と60は全基準の独立検証未完了としてfailを返した。59ではtests本文・追加実行・完全ログを要求したが、60では実行枠0、tests本文なし、ログ切断が再報告された。同じ不足を解消せず第三のQAへ渡すことはLoop limitsにより禁止する。

D-021はテキスト・スクリプト実行とStudio内独立検証を承認している。その承認の取り直しではなく、承認された実行経路を実際に供給できていない具体的な障害を扱う。通常Step内の技術的作業はRoleが計画し、Roleが生産できない供給条件だけをOwnerへ問う。

## Findings

60を主要な技術問題報告として用いる。

- 全収録出力のsource_idは`04fa2b1c168a`、BUILDは`0.6-g002-public-32`。保存ファイルからの独立再算出は未実施。現在のrepo/と一致すると仮定しない。
- 152 tests成功だけでは、本文の条件・assertと受入基準の対応を確認できない。
- 不足はtests全文、省略なしのログ・検証入力、独立実行枠、L1/O3等の変更前比較基線、完全証拠の永続参照経路。収録済み出力の再評価だけを繰り返さない。
- `bots.py::_dangers`がactive chargeで内部`phase_left`を読み、危険経路長の判定に使うとの具体的所見がある。player viewはactive残時間を表示しない。D-019項目6と仕様§8への適合を確認できず、現状の数値だけでボスFPS比較をpassにできない。
- `_hurt_lines`のboss被弾補助文は突進接触位置の証拠にならないとの所見もある。
- これらをゲーム本体の戦闘不具合、対処不能、難度不合格へ拡張しない。
- 58・60は同一受入基準の修正後再失敗2回ではない。今回の再計画理由は反復した供給障害と試験道具の具体的問題である。

## Decisions already made

- D-019：公開情報に基づくボス対応bot、両FPS・開始3/2 hearts別比較、保持回帰、実測後Designer判断を要求。
- D-021：repo/のテキスト・スクリプト方式とStudio内独立QA・Playを承認。実機供給、旧指定sha照合、外部配員、人日見積もりは要求しない。
- 仕様§11：旧経路表示、弾ライフサイクル、長時間観測の契約を保持。

## Constraints

- このStepは計画とbriefの準備。製品コード・bot・仕様を変更せず、QAの合否を上書きしない。
- 技術的な修正方法はTechnical Directorが決める。Studioは内部残時間を何に置き換えるかを指定しない。
- 公開player表示をbot都合で拡張するなど、プレイヤー向け契約の変更が必要ならDesignerへ返す。
- 新たな難度・時間ゲートを設けない。変更前比較を現行suite成功で代用しない。基線が得られなければ未確認として残す。
- 購入、外部委託、追加金銭、実機・gamepadの調達を前提にしない。
- QAの証拠と独立Playの資料を分離する。Playへ期待結果・実装履歴を渡さない。
- 並列Stepは開かない。

## Open questions

1. tests本文と完全な検証入力は既存repo/から供給できるか。packetへの収録・閲覧制約は誰が解消できるか。
2. D-021で指定されたStep内実行が0枠になっている具体的な障害は何か。独立QAが実行し、完全ログを保存・参照するために最低限何が必要か。
3. L1/O3等の変更前比較に利用できる保存ソースまたは出力はあるか。存在しない場合、どの判断をどのRoleへ戻す必要があるか。
4. botの全判断経路を公開情報条件へ適合させるには、どの作業・試験・ログが必要か。独立1〜4への影響をどう確認するか。
5. Ownerが提供・調整すべき供給と、通常Roleが生産できる証拠を明確に分けられるか。

## Expected output

`to: studio`の結果Handoffに、影響システム、順序、依存、リスクと対策、証拠保存方法、独立QAの再開条件を記載する。実行できたことと未実行を区別する。

加えて、`studio/templates/escalation.md`に従うOwner宛Escalationを日本語で準備する。質問は一つにまとめ、検証に必要な供給を整える案、Goalを狭める案、停止する案から妥当な2〜3案を示す。各案の具体的な必要供給、失う検証範囲、次のroute、推奨理由を明記する。推奨はD-021の承認を維持して供給障害を解消する方向を第一に検討し、実現性を断定しない。

二度の同じ不足報告がescalationの手続上の理由であることと、Roleには解消できない具体的な障害を区別して説明する。不明な供給機能をあると仮定せず、再び同じQA依頼だけを提案しない。Ownerへの実際の提示とGoalのblocked-on-ownerへの変更は次のStudio Routeが行う。

bot対応が必要なら、Engineerによる試験道具対応→両FPS・hearts 3/2の再測定→独立QAという計画を含める。既存1〜4方針の保持または変更影響を追跡する。全QA合格後の限定Art Verify→独立Play→Designer実測後判断→Game Director Reviewを残す。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/handoff.md
- Template: studio/templates/escalation.md
- Project: project.md#constraints
- Project: project.md（実行コマンドを含むfront matter）
- Project: design/final-boss-and-continuous-run.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting report: goals/G-002-final-boss/58-qa-to-studio.md
- Supporting request: goals/G-002-final-boss/59-studio-to-qa.md
