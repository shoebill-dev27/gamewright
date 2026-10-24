---
kind: handoff
goal: G-002
seq: 10
from: game-designer
to: studio
stage: Design
outcome: done
---
# 10: game-designer → studio — ボスと連続ランの詳細仕様、旧基準の変更依存を返す

## Task

詳細仕様を確認し、Technical DirectorのPlanを開く。併せてD-006の旧第5部屋依存基準について、実装前に必要なDecision変更を適切な判断経路へルーティングする。

## Context

OwnerはD-015で第1〜4部屋からの連続到達、第5部屋の単体ボス、勝利・死亡、ラン先頭からの再挑戦を承認した。D-016の読み取り・位置取り・回避後の反撃という方向を、実装・独立検証可能な契約へ具体化した。

実装、実行検証、QA判定、Goal達成判断は行っていない。

## Findings

成果の正本は以下。

- `design/final-boss-and-continuous-run.md`：ボス、継承、回復、終端、retry、入力・時刻、pause、player表示、30/60 FPSの受け入れ基準、旧基準対応表、未解決依存。
- `decisions/D-017-final-boss-and-run-contract.md`：Designer権限内の主要選択。既存Decisionは改訂しない。

ボスはHP12、固定順の突進と短射。突進0.7秒予兆→0.3秒有効→1.2秒回復、短射0.8秒予兆→1.0秒有効→1.4秒回復。どちらも照準を予兆開始時に固定する。非致死スワイプで中断せず、回復中は無害。横へ避けて近くに残ると反撃しやすく、遠くへ逃げると接近に時間を使う構成である。

生存クリア後に1 heart回復、上限3。ボス到達は2または3 heartsとなる。位置・向き・戦闘タイマー・危害・保持入力・予約攻撃を部屋境界でリセットする。反応ルール定義は継承し、直前の観測と反応記憶は初期化する。

同フレーム結果は死亡優先。確定後に残弾・予兆を消し、戦闘を凍結する。retryは第1部屋の新規状態へ戻す。pauseとretry、通常ランの時刻入力、長時間の観測経路は新設要求であり、現行で実装済みとは扱わない。

仕様§8に、combat.mdの基準番号、補足仕様、テスト、D-001〜D-007／D-011〜D-016の適用関係を整理した。旧第5部屋の構成・ブルート位置、spitter gap試験、旧5番のdodger成績は置換対象。第1〜4部屋と共有ルールは保持する。新ボスの同速度・同半径の危害への接触帯適用は、自動継承でなく明示採択した。

未解決の中心はD-006である。3〜5部屋合計のwalker3〜7 hearts、2部屋clear、dodger／camper比較は旧独立部屋を前提とする。新ボスや継承ランへ移植しない。推奨は旧集計を過去ビルドの記録として残し、新構成の合否ゲートから外すこと。代案は旧5番fixtureを維持することだが、新ランの難度評価にはならず保守が増える。本Stepでは改訂を確定していない。関連テストだけを削って解決済みにしない。

仕様とテストの違いも記録した。room3の静止12秒試験の最大3というassertはD-007の一般上限5を検証する試験ではない。walkerテストの旧上限6コメントよりstep44／D-006が正本。終端と残弾の現行挙動は04の静的所見に留まる。

根拠は09／08、D-015／D-016、combat.md、step44・46・59・68・72・94、visual spec、manual、README、test_game.py、および04の静的調査。指定shaとの一致、build0.4／0.6の差、実行成功、所要時間は未確認。play／botsは実行していない。独立部屋bots時間の合算を連続ラン実測とはしない。

Art Directorの限定Verifyを推奨する。対象はテキストでの攻撃種・危険範囲・実弾・回復・HP・終端とretryの識別。グラフィカル制作や戦闘ルール変更を依頼しない。

## Decisions already made

- D-001：追加の戦闘入力なし。
- D-004／D-005：既存敵、保護、接触消費の共有ルールを保持。
- D-006：存続。旧集計の新構成への適用変更は未採択。
- D-007／D-011／D-012：room3と既存メッセージの正本を保持。
- D-013／D-014：G-001の判断と既知ギャップを保持。新機能への検証免除にはしない。
- D-015／D-016：連続ランと単体ボスの承認範囲・方向。
- D-017：本Stepのボス・継承・終端・時刻・表示の詳細契約。

## Constraints

第1〜4部屋の構成と部屋内共有戦闘ルールを維持する。通常敵同居、第6部屋、ボスチェックポイント、新しい戦闘入力、成長・報酬システムは追加しない。

15〜20分のVisionは保持するが、HPや待機時間だけで合わせない。時間・成功率の実測値はない。

技術方式、工数、実装順序はPlanに残す。60秒上限、pause、実機入力、retry、連続モードを実装済みと仮定しない。独立QA、限定Art確認、独立Play、Reviewを経る。Playtesterへ設計の期待結果やReview用体験信号を転記しない。

## Open questions

1. Studio：D-006の旧集計を新構成のゲートから外す提案を、どのDecision変更として確定するか。
2. Technical Director：指定shaと対象ビルド、資料差、既存テストの実行基線を同定できるか。
3. Technical Director：連続到達、同時勝敗、retry、両時刻、pauseを観測できる実行経路と費用は何か。60秒超のplayer／traceをどう確保するか。
4. Technical Director：通常ラン／独立試験の指定、pause／resume、終端retry、再試行入力の公開構文と実機操作の対応をどう具体化するか。
5. Technical Director：Desktopキーボード／ゲームパッド対応の不足と、承認範囲を超える費用・リスクがあるか。
6. Studio：Art Directorの限定Verifyを正式経路に含めるか。

## Expected output

Studioは仕様と未解決Decision依存を確認し、Technical DirectorへPlanを渡す。Planは実現・計測・入力・表示経路、共有コードへの影響、検証、工数・リスクを示す。D-006に関わる変更は実装前に適切な判断権限で解決する。

承認範囲を超える規模やVisionとの具体的衝突があれば、Build前にGame Director経由でOwnerへ返す。Planと必要な判断の後、Build→独立QA→限定Art確認→独立Play→Reviewへ進む。G-002は進行中のまま維持する。

## Load

- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: goals/G-002-final-boss/04-technical-director-to-studio.md
- Previous handoff: goals/G-002-final-boss/09-studio-to-game-designer.md
