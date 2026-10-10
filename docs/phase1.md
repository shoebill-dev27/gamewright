# Phase 1 設計ノートと dry-run 報告

正典は `docs/spec/initial-spec.md`。本書は Phase 1 で何をどう作り、dry-run で何が分かったかの記録であり、仕様を拡張するものではない。

## 1. 結論

Goal から必要な工程だけを選び、Role 間を永続化された Handoff で進め、Owner 判断の地点で止まって再開する。この構造が Markdown だけで成立した。

- バグ Goal は QA → Engineer → QA の短経路を通った。
- 体験 Goal は Playtest から Review までに展開し、途中で Owner 判断（停止と再開）と仕様差し戻しが起きた。
- **前提知識のない新しい実行者（cold-start probe）3 回が、リポジトリの文書だけで Intake / Step / Route を実行できた。** 責任境界も守った。例えば Engineer は仕様の穴を自分で埋めず、Designer へ差し戻した。
- probe は手順上の曖昧さを計 30 件以上報告した。大半は文書を直して解消した。残りは §6 にまとめる。

## 2. 構成と責務分離

| 責務 | 置き場所 | ツール依存 |
|---|---|---|
| Specification（何を・なぜ） | `docs/spec/initial-spec.md` | なし |
| 概念定義とカタログ | `studio/README.md` | なし |
| Studio Orchestration（Intake / Step / Route / Resume / Close、Escalation、決定権限） | `studio/orchestration.md` | なし |
| Workflow（ステージ表、戻りルール、経路の先例） | `studio/workflows/development-loop.md` | なし |
| Role Contract × 7（責任、決めること、してはいけないこと、入力、出力、差し戻し条件） | `studio/roles/` | なし |
| Skill × 11（仕事のやり方。Role に所有されない） | `studio/skills/` | なし |
| Artifact の形式（goal / handoff / decision / escalation / project） | `studio/templates/` | なし |
| Project Context（ゲーム固有の情報） | `examples/projects/<id>/`（実運用ではゲーム repo 内など任意の場所） | なし |
| Tool 固有 entry point | `AGENTS.md`、`CLAUDE.md`、`.claude/skills/studio/SKILL.md` | **ここだけ** |
| 検証 | `tests/test_studio.py` | なし（Python 標準ライブラリのみ） |

`studio/` とサンプル Project の artifact には、AI ツール名・ベンダー名・モデル名・ゲーム名が一切出てこない。テストでこれを強制している。

## 3. 主要な設計判断

| 判断 | 理由 | 退けた案 |
|---|---|---|
| **Studio（工程を決める機能）と Game Director を分けた** | Director を司令塔にすると、全 Goal が Director を通る。バグ修正の短経路と両立しない | Director にオーケストレーションを兼務させる |
| **ステージは「答えの出ていない問い」から選ぶ。** 各ステージに入る条件となる問い（entry question）を置く | 固定パイプラインにしないための中核。Project Context で答えが出ている問いのステージは飛ばす | Goal 種別ごとのテンプレート経路（先例として残したが、強制はしない） |
| **Handoff を自己完結の作業パケットにし、Load 一覧を持たせた** | 仕様 §17 のコンテキスト選択を明示的なデータにした。別セッション・別モデル・人間でも、Handoff 1 枚から仕事を始められる | 会話履歴に頼る、全文書を読ませる |
| **ステージ遷移の判断は Route 操作だけが行う。** Role は `to` を提案し、Route が確定させる | 「誰が次に働くか」は Studio の責務で、Role の責務ではない | 各 Role が次の担当を確定させる |
| **Playtester への Handoff は Studio が作り直す** | QA や Engineer が書くと、実装内容や期待される結果が漏れて観察が誘導される。probe A で実際に起きた | 送り手が直接 Playtester へ渡す |
| **Skill はフラットな Markdown にし、ツールの skill 機構には登録しない** | Skill を選ぶのは Studio であり、ツールの自動起動ではない。どのツールでもファイルとして読める | `.claude/skills` や `.agents/skills` に Skill を全登録する（全 Skill の説明が常に読み込まれる） |
| **コードはテスト 1 ファイルだけ。** artifact は frontmatter 付き Markdown | Phase 1 は Markdown で成立する。frontmatter（`from` / `to` / `outcome` / `status`）は将来の自動化で機械的に読める | runner や CLI を先に作る |
| **Project Context はディレクトリで表し、置き場所を固定しない** | Decision をゲームのコードと一緒にバージョン管理できる。複数 Project を扱える | Studio repo に全 Project を集約する |
| **`owner_language` を Project Context に置いた** | Owner 向けの文書（Escalation と Outcome）は Owner が読む言語で書く | 言語をハードコードする |
| **Escalation の各選択肢に「選ばれたら次にどう進むか」を書く** | Owner 判断のあと、Resume で機械的に再開できる | 判断後に経路を毎回考え直す |

## 4. 受け入れ基準との対応

| 基準 | 根拠 |
|---|---|
| 新規 repo として単独で成立 | `git init` から始めた。外部依存なし |
| 仕様書が実装と分離された正典 | `docs/spec/`。AGENTS.md で編集禁止を明記 |
| Role Contract と Skill の分離 | `roles/` と `skills/`。Skill には `Typical roles` があるだけで所有者はいない。テストで確認 |
| Role と Model / Agent の分離 | 概念表の「Role ≠ Executor」。Role 定義にモデル名がないことをテストで確認。probe は別モデル（Sonnet）で実行した |
| Project Context が Studio から分離 | `studio/` にゲーム名がないことをテストで確認。2 つの Project で同じ Role ファイルを Load したこともテストで確認 |
| Handoff / Decision が明示的な artifact | 仕様 §10 / §11 の必須項目をテストで確認 |
| Goal から次の Role / Skill / 工程を判断する構造 | `orchestration.md` の Intake と Route、`development-loop.md` のステージ表と戻りルール |
| バグは短経路 | lantern-depths の G-001。参加者が {studio, qa, gameplay-engineer} だけであることをテストで確認 |
| 「面白くない」は展開する | G-002。tidepool-garden の G-001 は probe が実行した |
| 固定 Workflow にしない | 2 つの Goal で経路が違う。Art Director は tidepool では選ばれ、lantern G-002 では選ばれない（テストで確認） |
| Owner escalation の条件と再開 | `orchestration.md` の Escalation と Resume。G-002 の 04 → D-002 → 05 |
| 複数 Project で再利用 | lantern-depths と tidepool-garden |
| Claude Code 部分を除いても成立 | Claude Code 固有の内容は entry point 3 ファイルだけ。probe は `/studio` skill を使わず、AGENTS.md から実行した |
| 人間が各 Step を開始する運用 | Intake と各 Route のあとで停止し、Next action を書く |
| README で「Goal を依頼する仕組み」と分かる | README の冒頭と「How a Goal flows」 |

## 5. dry-run 結果

### 5.1 手書きのトレース（lantern-depths）

ビルドとコードは `sim/` で模擬した。どの Step も、Handoff の Load 一覧に載ったものだけを根拠に書いた。

- **G-001 再現可能なバグ**
  - 経路: Studio → QA（再現と受け入れ基準）→ Engineer（修正）→ QA（**30 FPS で fail**）→ Engineer（時間ベースで再修正）→ QA（pass）→ Close。
  - Director / Designer / Art Director / Playtester は通していない。理由は goal.md の Unknowns 表に書いた。
- **G-002 戦闘が単調**
  - 経路:
    1. 事前情報なしの Playtest
    2. Designer の分析（選択肢 A / B / C）
    3. Director が C を A に統合（Director の権限内）。B は Owner の Decision である D-001 を変えるため、Owner へ escalation
    4. **停止**。Owner が「A。長押し溜めは将来なら可」と回答し、D-002 に記録して**再開**
    5. 詳細設計 → 技術計画
    6. Engineer が「予兆中に被弾したら中断するか」という仕様の穴を見つけ、**差し戻し**
    7. Designer が回答（D-003、Designer の権限で記録）
    8. 実装 → QA pass
    9. QA は結果を Studio へ返し、Studio が Playtester 用の Handoff を新しく作成（事前情報なし）
    10. 再 Playtest → Director が goal-met と判定
  - 新しく見つかった視認性の問題は、スコープを広げずに提案 G-003 として Owner へ返した。

### 5.2 cold-start probe

文書が設計を本当に運べているかを試すため、会話の文脈を一切持たない新しい実行者を起動し、リポジトリだけを読ませて操作させた。

| probe | 内容 | 結果 |
|---|---|---|
| A: Intake | tidepool-garden で「最初のパズルで子どもが手を止めてしまう」を AGENTS.md 経由で依頼 | 経路は妥当だった（Playtester から開始し、Decide と Plan は理由付きでスキップ、自分の仮説は Playtester に渡さない）。**ただし Playtester への Handoff に Owner の訴えを書き、観察を誘導した。** 原因は Intake が受け手の Role Contract を読まない手順だったこと。手順を修正し、該当 Handoff には Route のチェックを適用した（goal.md の Route changes に記録） |
| B: Step + Route | 同じ Goal で `Studio next` | Playtester は観察だけを報告し、原因や修正案は書かなかった。Route は、観察に視覚的な要因があることを根拠に **Art Director を並列で追加**した（必要なときだけ選ばれることの実例）。Step と Route の読み込み範囲の矛盾などを 11 件報告 |
| C: Engineer | lantern G-002 の step 7 時点を複製し、`Studio next` | **ヒントなしで、既存の Flinch と予兆の関係が仕様にないことを発見した。** 選択肢と技術コストを並べたうえで、自分では選ばずに Designer へ差し戻した（`docs/probes/engineer-handback.md`）。手書きの TD 計画の誤り（「正面 120°」を ±120° と読める）も指摘したので修正した |
| D: Codex | Codex で、tidepool のバグ Goal を Intake | **未実行。** Codex の利用上限（10/10 14:36 まで）。§6 を参照 |

### 5.3 テスト要件との対応（`python3 -m pytest tests/`、20 件パス）

| 要件 | テスト |
|---|---|
| バグで Director や Art Director を強制しない | `test_bug_goal_takes_the_short_route_and_qa_failure_returns_to_build` |
| 体験改善で Playtest や Design が選ばれる | `test_experience_goal_expands_only_to_needed_roles` |
| 前段の Handoff から次の仕事を始める | `test_every_role_starts_from_a_previous_handoff` と probe B / C |
| Engineer が仕様不明を差し戻す | `test_engineer_hands_spec_gaps_back_to_the_designer` と probe C |
| QA の failure が修正工程へ戻る | 上記のバグ経路テスト |
| Playtest 由来の問題が Designer / Director へ戻る | `test_playtest_findings_return_to_design_roles` |
| Owner 判断で停止し、選択肢・根拠・推奨を返す | `test_owner_escalation_stops_with_options_and_resumes` |
| 同じ Role Contract を別の Project で使う | `test_same_role_contracts_serve_multiple_projects` |
| 共通仕様が Claude Code 固有機能に依存しない | `test_studio_and_project_artifacts_are_tool_neutral` |

テストが空振りしないことは、ミューテーションで確認した。規則違反を 6 種類わざと入れ、6 種類とも検出された。

## 6. dry-run で判明した曖昧さ

### 文書の修正で解消したもの

- Intake が受け手の Role Contract を読まず、Playtester への誘導が漏れた（probe A）。Intake の手順に Route steps 4–5 を適用するよう変えた。
- 後段のステージを今決めるのか、保留するのか（probe A）。`tentative` ステータスを追加した。
- Step の「Load 一覧以外は読まない」とテンプレートの参照が矛盾していた（probe B / C）。テンプレートは常に読めるようにした。
- Route の読み込み範囲に受け手の Role Contract が入っていなかった（probe B / C）。追加した。
- 次の各点を定義していなかった: `outcome` の値の一覧、パスの基準、「Previous handoff」の意味、Route 表の Handoff 列の意味、並列ステップの番号の付け方、Expected output を誰が書くか（probe B / C）。テンプレートに明記した。
- 欠陥と体験問題を分ける基準がなかった（probe A）。`development-loop.md` に追加した。
- Intake のあとで停止するのか（probe A）。停止すると明記した。
- Owner 向けの言語をどこに適用するか（probe A）。範囲を明記した。
- 送り手が「Playtester の前だから Studio 宛てにする」とどう知るのか（自己レビュー）。Route が Expected output で指示する形にした。
- 差し戻し中に、ブロックされていない作業を進めてよいか。細かい仕様の穴で Designer に負荷をかけすぎないか（probe C）。`implement-change` に規則を追加した。

### 未解決（Phase 1 の限界として報告）

1. **Playtester が実際にゲームを遊ぶ手段がない。** dry-run では `sim/` の文章を読んで代用した。実運用には、入力の注入や画面キャプチャなど、実行環境側の仕組みが要る。dry-run と実運用の間で最大のギャップ。
2. **Route の判断の質は実行者次第。** 「視覚的な要因かもしれない」の線引き（probe B）や、表現の小さな誤りに tentative な Plan を足すかどうか（probe C）は判断に依存する。文書で決定論的にはできない。
3. **Step と Route を同じ実行者が続けて行うと、Role が自分の差し戻しを自分で経路決定できてしまう。** Phase 1 では人間が開始するので抑えられているが、仕組みとしての分離はない。
4. **独立性のチェックは部分的。** テストが検出するのは、Owner の訴えの原文が漏れた場合と Load 一覧の違反だけ。言い換えたヒントは検出できない。`file#section` で節だけ読む指定も、実行者の規律に依存する。
5. **dry-run で通っていない経路:** 並列ステップの合流、Intake 直後の escalation、ループ上限、Decision の置き換え（supersede）、Owner が選択肢にない回答をした場合。
6. **Codex での実行は未検証（probe D は利用上限で未実行）。** ツール中立性は次の 2 点で確認した: 静的検査（`studio/` と artifact にツール名がない）、Claude 系の実行者に AGENTS.md の経路だけで操作させた結果。Codex で再実行すれば完全に確認できる。
7. tidepool-garden の G-001 は進行途中で、Route 後の停止状態にある。次の操作は steps 2 / 2b（Designer と Art Director）。

## 7. 意図的に実装しなかったもの

- 自動オーケストレーション（runner、連続実行ループ）、scheduler、queue、DB
- Web UI、dashboard、MCP
- Codex 用のネイティブ skill（`.agents/skills/studio/`）。Codex は AGENTS.md で操作できるので不要と判断した
- Role ごとのモデル割当、worktree の自動化、自動 merge / release
- 実ゲーム、ゲーム固有の設計
- Decision 索引の自動生成、メトリクス

## 8. 次に自動化すると効果が高い箇所

1. **Step runner。** 1 Step ごとに新しい実行者を起動し、Load 一覧のファイルだけを渡す。コンテキストの規律と独立性（QA / Playtester）を機械的に保証できる。probe A〜C で、この方式が機能することは確認済み。§6 の 3 と 4 もここで解消できる。
2. **Route の決定論的な部分のスクリプト化。** 対象は次の 4 つ。判断が必要な部分は LLM に残す。
   - Route 表の更新
   - Handoff の形式チェック（テストの規則を流用）
   - 受け手の Role とステージから Load 一覧の骨格を作ること
   - Playtester 宛ての Handoff の検査
3. **Resume のスクリプト化。** 対象は、Owner の回答を D-NNN として記録すること、Escalation を resolved にすること、経路を差し替えること。手順はすでに定義済みで、自動化は小さく済む。
4. **「Owner escalation まで連続実行」モード。** 上の 1〜3 が揃えば、仕様 §18 の第 2 段階に入れる。
5. **実ビルドの Playtest harness。** §6 の 1 を解消するもの。ゲームのエンジンごとに必要になる。
6. **Codex 用 entry（`.agents/skills/studio/`、SKILL.md 形式は共通）を追加し、probe D を再実行する。**

## 9. 実行環境の確認（2026-10-10 時点）

- Claude Code: プロジェクト skill の置き場所は `.claude/skills/<name>/SKILL.md`。`CLAUDE.md` は `@AGENTS.md` で AGENTS.md を取り込む。
- Codex: リポジトリの skill の置き場所は `.agents/skills/<name>/SKILL.md` で、SKILL.md は Agent Skills 標準と共通の形式。AGENTS.md はリポジトリのルートで読まれる。
- 出典: [Codex: Agent Skills](https://developers.openai.com/codex/skills)、[Claude Code: Skills](https://code.claude.com/docs/en/skills)
