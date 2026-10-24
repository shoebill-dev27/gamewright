---
kind: handoff
goal: G-002
seq: 8
from: game-director
to: studio
stage: Design
outcome: done
---
# 08: game-director → studio — 最終戦の体験方向を確定し、Designへ進める

## Task

D-016を方向として、Game Designerへボスと連続ランの仕様化をルーティングする。仕様化後はTechnical DirectorのPlanで範囲・費用・依存を評価し、実装の前提を整える。

## Context

Owner要望は「最後に手応えのあるボス戦がほしい」。D-015で、連続ラン、第5部屋の単体ボス、最終勝利・死亡、ラン先頭からの再挑戦が承認された。

今回はその範囲内の体験優先度と境界をD-016に記録した。詳細設計、技術方式、実装、QA、Goal達成判定は行っていない。

## Findings

### 確定した方向

最終戦は、危険を読んで位置を選び、回避から反撃へ戻る判断を問う山場とする。難度のために読みやすさを犠牲にせず、単なるHP増加や同じ回答の長時間反復を避ける。

連続到達と再挑戦も評価対象である。Designは前半の行動の意味と、ボスで対処を学ぶ余地を両立する継承・回復を定める。具体的な回復方式、攻撃数、フェーズ数、数値は未採択である。

### Designに必要な成果

- 第4部屋からの接続、ボス開始状態、攻撃構成、予兆、照準固定、危険範囲、対処、攻撃機会、中断可否を仕様化する。既習の読み取りをどう活用し、どの判断で山場を作るか説明する。
- 部屋順序、遷移条件、hearts・位置・向き・タイマー・弾・保持入力・予約入力・反応ルールの継承／リセットを明記する。
- 部屋クリアと最終勝利を区別し、同時勝利／死亡、残弾、終端後の進行と操作、再挑戦手段、再挑戦時の初期化を定める。ラン先頭から再挑戦する境界は変更しない。
- 部屋内時刻とラン時刻、入力の時刻基準、ポーズの扱い、時間切れと勝敗の区別を定める。現行ビルドにポーズや実機入力層があると仮定せず、必要な対応をPlanへの依存として示す。
- player viewで攻撃種、予兆と危険範囲、回復機会、ボスの残り耐久、進行・勝敗・再挑戦をどう認識できるか定める。現在のテキスト表示で成立する要求とし、表現上の不足があればArt Directorへの限定依頼を提案する。
- 30/60 FPSそれぞれで独立検証できる受け入れ基準を作る。攻撃・保護・接触消費などの共有ルール、連続到達、境界、勝敗、再挑戦の確認を含める。新攻撃へ既存の接触端例外を自動適用しない。
- ボスとランの時間目標を置く場合は、暫定値の根拠と実測後の見直し条件を示す。独立した部屋のbots時間合算を連続ラン実測に使わない。

### 旧第5部屋と既存Decisionの扱い

旧第5部屋の混成構成・配置、そのブルート位置、旧混成戦を前提とする評価は置換対象である。旧第5部屋を含むdodger比較や3〜5部屋合計の成績は、そのまま新ボスや連続ランの合格条件にしない。

ただし、基準本文は今回の入力にないため、基準番号ごとの削除・置換は確定していない。Studioは次のDesignに現行戦闘仕様、該当基準とテストを渡し、保持・置換・要Decision変更の対応表を作らせる。

特に次を区別する。

- D-004：第4部屋のcue gap、ブルートの非中断、その他の既存敵ルールを維持する。旧第5部屋からスピッターを取り除くことは、共有ルールの撤回やボスへの自動適用を意味しない。
- D-005：既存の弾消費・突進の一撃消費・接触判定を維持する。新しい攻撃にも適用関係を明記し、難度のために暗黙変更しない。
- D-006：3〜5部屋のwalker合計と2部屋クリアという基準は、独立した旧部屋と各3 heartsを前提とする。置換後への有効性は未確認であり、7を新ボスや連続ランへ移植しない。対応表でD-006に関わる変更を明示し、適切な権限で解決する。本Stepでは廃止・改訂しない。

### 証拠の限界とPlanへの依存

play／botsは今回実行していない。04は静的所見であり、指定shaとの一致、既存テスト、player／trace、botsの成功を示さない。project.mdのbuild 0.4と他資料の0.6の差も未解決である。

Planでは対象ビルドの同定と基準資料の整合、単体敵の攻撃切替、進行・終端、表示、入力・時刻、実行上限、bots対応、共有コードへの影響を評価する。60秒上限の現行play経路で必要な長さを検証できると仮定しない。必要な実行・計測経路と工数・依存・リスクを示すこと。

## Decisions already made

- D-015：連続ラン、第5部屋の単体ボス、最終勝利・死亡、ラン先頭からの再挑戦をOwnerが承認。
- D-016：読み取り、位置取り、回避後の反撃を最終戦の中心とする。継承・回復の方式と詳細ルールはDesignに残す。
- D-001：戦闘の基本は攻撃とダッシュ。追加の戦闘入力はOwner承認が必要。
- D-004／D-005／D-006：既存Decisionとして存続。第5部屋置換に伴う適用関係と必要な変更は個別に特定する。

## Constraints

- 第1〜4部屋の構成と共有戦闘ルールを維持する。
- ボス専用チェックポイント、追加の戦闘入力、第6部屋、通常敵との同居、既存部屋の全面改修を含めない。
- 15〜20分のVisionを維持し、時間合わせだけのHP増加や待機の水増しを行わない。
- Desktopのキーボード／ゲームパッド、30/60 FPSへの対応を要求として維持する。現行で実装済みとは扱わない。
- 承認範囲を超える規模・費用・リスク、Owner DecisionまたはVisionの変更が必要なら、実装前にOwnerへ戻す。
- 今回は新たなOwner判断を要する具体的な衝突は確定していない。DesignとPlanを進める。
- 独立QA、独立Play、Reviewを省略しない。Playtesterへの引き継ぎには実装内容や期待結果を渡さない。

## Open questions

1. どの攻撃構成と攻撃機会が、通常戦と異なる判断を生むか。
2. どの継承・回復ルールが、道中の意味とボスでの学習余地を両立するか。
3. 勝敗、残弾、終端後操作、再挑戦、時刻と入力の契約をどう仕様化するか。
4. 旧第5部屋依存のどの基準を置換し、どのDecisionに別途変更が必要か。
5. 表現仕様にArt Directorの参加が必要か。
6. Planで承認範囲内の実現性と検証経路を確保できるか。連続ランの実測がVisionから外れた場合、どこまで範囲内で調整できるか。

## Expected output

StudioはD-016と本Handoffを次のDesignへ渡す。Game Designerは詳細仕様、観測可能な受け入れ基準、旧基準とDecisionの対応表、未解決の依存を作成しStudioへ返す。

その後、Technical DirectorがPlanを行う。範囲・費用・依存の評価を経るまでBuildを開かず、Owner判断を要する拡大や衝突があれば具体的な変更と影響を添えて戻す。続く経路はBuild → 独立QA → 必要に応じたArt Director確認 → 独立Play → Reviewとする。Goalは未達成・進行中として維持する。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/prepare-owner-escalation.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: goals/G-002-final-boss/02-game-designer-to-studio.md
- Project: goals/G-002-final-boss/04-technical-director-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Previous handoff: goals/G-002-final-boss/07-studio-to-game-director.md
