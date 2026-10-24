# Phase 2 設計ノートと実行結果

正典は `docs/spec/initial-spec.md` と `studio/` の共通定義。Phase 2 はそれを変えず、**Phase 1 で論理的に分けた Role / Skill / Workflow の分離を、実行レベルで機械的に保証する**ことを目的とする。

## 1. 結論

Phase 2 の受け入れ基準は、**Codex での Goal の完走を除いて満たした**。

**Phase 2 は完了とする（Owner の判断、2026-10-11）。** 保留していた Codex での完走も、同日、Codex の利用枠が回復したあとに達成した（§4.3 の追記）。

Codex では、同じ fixture からバグ Goal を **25 オペレーション（Close の 2 手前）まで**実行した。そこで Codex の週間利用上限に達し、次の解除は 2026-10-14 17:56（§4.3）。その範囲で、Phase 1 の artifact 形式と隔離が Codex でも成立することを確認した。

- Phase 1 のバグ Goal と戦闘改善 Goal を、**すべてのオペレーションを fresh executor で**、同じ fixture から完走した。合計 67 オペレーション、セッション id はすべて異なる。
- Step に渡された入力は、毎回 Handoff の Load 一覧と一致した。manifest とハッシュで全件を検証している。
- QA には実装者の自己評価が、Playtester には設計・実装・Owner の依頼文が届いていない。カナリアとポリシー検査で、記録済みの全 packet について確認した。
- 次工程の決定は別の executor が成果物だけで行い、記録から再実行しても 3 件とも同じ判断になった。Playtester の結果だけを入力にした Route の判断も含む。
- Owner escalation → Decision 記録 → fresh executor での再開は、2 回成立した（専用 fixture と戦闘改善 Goal）。
- 実行によって、Phase 1 の仕様の穴が 3 つ見つかった。いずれも直した。
  - 「次のステップを `open` にする」規定
  - Handoff 列の書式
  - `#section` のアンカー書式
- 主な限界は 3 つ（§5）:
  - Codex はユーザー全体の指示ファイルを必ず読み込む
  - Route は最新の成果物 1 件しか見ない
  - dry-run の検証は Simulator 経由で循環する

## 2. 方式

### 2.1 1 オペレーション = 1 fresh executor

Intake / Step / Route / Resume、および dry-run 用の Simulator の各 1 回につき、新しい実行プロセスを起動する。

| 保証 | Claude Code での実装（`scripts/studio_run.py`） |
|---|---|
| 会話履歴を持ち越さない | オペレーションごとに別の `claude -p` プロセスを起動。`--no-session-persistence` で終了後は再開不能、`--resume` / `--continue` は使わない |
| packet 以外の入力がない | `--tools ""`（ツールなし＝ファイルを読めない）、`--strict-mcp-config`（MCP なし）、`--disable-slash-commands`（skill なし）、`--setting-sources project`（ユーザー設定・hook・plugin なし）、`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`（自動メモリなし）、`--system-prompt` を最小の固定文に置換、cwd はプロジェクト名を含まない空の一時ディレクトリ |
| 親エージェントの会話が漏れない | packet は**スクリプトが artifact から決定的に組み立てる**。親 LLM は packet を書かない |
| 隔離の監査 | 起動時イベント（stream-json の `init`）でツール一覧と MCP 一覧が空であることを確認する。空でなければ出力を破棄して拒否 |

Codex adapter の構成:

- `codex exec --json --ephemeral --ignore-user-config --ignore-rules -s read-only`
- `-c project_doc_max_bytes=0`、`-c web_search="disabled"`
- ツール系の feature を `--disable` で無効化（shell、exec、apps、browser、computer use、plugins、image、multi-agent など 17 個）
- cwd は空の一時ディレクトリ
- イベント列を監査し、ツールが 1 回でも使われたら拒否する

制約が 1 つある。ユーザー全体の `~/.codex/AGENTS.md` は、どのフラグでも外せなかった（§5）。

`--bare` は使えなかった。OAuth ログインでは認証できず、`ANTHROPIC_API_KEY` が必要なため。そこで上記の個別フラグで同等の隔離を構成し、実測で確認した（§4.1）。

Agent tool の subagent は採用しなかった。会話は新しく始まるが、ツールでリポジトリ全体を読めてしまい、allowlist を機械的に強制できないため。

### 2.2 packet = 許可された入力のすべて

- Step の packet は、受け取る Handoff と、その **Load 一覧に載ったファイルだけ**で構成する。`file#section` はその節だけを入れる。ほかに入るのは executor instructions とテンプレートのみ。
- packet には manifest（パスと sha256）を付け、記録する。
- Route / Intake / Resume の packet は Studio 側の入力である。中身は次のとおり:
  - orchestration、development-loop、カタログ
  - 各 Role の `#works-from` / `#independence` 節
  - goal.md、直前の Step の成果物 1 件、project.md
  - ファイル名の一覧（中身は含まない）、Decision タイトルの一覧
- Step agent の生の出力（ファイルブロック外の推論など）は記録に残すが、**どの packet にも入れない**。

### 2.3 Role ごとの独立性ポリシー（Role Contract の frontmatter）

| Role | ポリシー | 効果 |
|---|---|---|
| playtester | `receives_from: studio`、`load_only:` 自分の Role / Skill、`project.md#player-profile`、`@player_visible`（project.md が宣言するビルドファイル）、`strip_sections: Sender assessment` | Studio が作った Handoff しか受け取らない。設計書・Decision・他の Handoff・実装メモは allowlist の外 |
| qa | `strip_sections: Sender assessment` | 実装者の自己評価（根本原因の推論、自己テストの結果、確信度）は QA の packet から除去される |
| gameplay-engineer | `load_forbid: goals/*/*-playtester-to-*.md` | Playtester の生の報告（誘導情報）を読み込めない |
| 判断を記録する Role | `writes: decisions/*`（と designer / art-director の `design/*`） | Step が書けるファイルを限定する |

追加の検査:

- Playtester 宛ての Handoff に Owner の依頼文、Decision の id、Sender assessment が含まれていたら拒否する。
- Engineer から QA への Handoff で、`## Sender assessment` の外に自己評価の語句が書かれていたら拒否する。

### 2.4 Step 実行と次工程決定の分離

- Step が書けるのは、**自分の出力 Handoff（または Escalation）1 件と、その Role に許されたファイルだけ**。goal.md は書けない。
- Step の出力した `to` は提案にすぎない。別の fresh executor（Route）が artifact だけを見て確定する。
- Route は直前の Handoff をその場で編集してよい。ただし kind / goal / seq / from / to と `## Sender assessment` は変えられない。
- 出力は次の検査をすべて通ったときだけ書き込む。1 つでも失敗したら何も書かない:
  - 書き込みリスト
  - Phase 1 の構造規則
  - 受け手のポリシー
  - open なステップが存在すること
- 失敗した場合は、新しい executor で 1 回だけ再試行する（`--retries`）。その際に渡すのは検証エラーのメッセージだけで、前回の出力は渡さない。

### 2.5 Owner escalation → Decision → 再開

1. `decide <ws> "<Owner の回答>"` で、Owner の言葉を Escalation の末尾にそのまま追記する（ここは決定的な処理）。
2. fresh な Resume executor が D-NNN（`decided_by: owner`）を書き、Escalation を resolved にし、goal.md と次の Handoff を書く。
3. 次の Step も fresh executor であり、D-NNN を Load 一覧経由で受け取る。

### 2.6 dry-run Simulator（Role ではない）

- ゲームが存在しないため、Build のあと fresh な Simulator がビルド記述（`sim/build-X.Y.md`）と実装メモを書き直す。入力は Engineer の Handoff、前のビルド記述、実装メモの 3 つ。
- QA と Playtester は、Engineer の意図ではなくこの「ビルド」を観察する。
- 出力は `sim/` に限る。HTML コメントや Sender assessment をビルド記述に含めたら拒否する。

### 2.7 ツール依存の置き場所

- `studio/execution.md`（保証、packet の構成、ポリシーの語彙、出力プロトコル、executor instructions）はツール名を含まない。Phase 1 のツール中立性テストの対象でもある。
- ツール固有なのは `scripts/studio_run.py` の 2 つの runtime adapter（claude / codex）と、entry point（AGENTS.md / CLAUDE.md / `.claude/skills/studio`）だけ。
- artifact の形式は Phase 1 から変えていない。追加したのは次の 2 点で、いずれも任意:
  - Handoff の `## Sender assessment` 節
  - project.md の `player_visible`

## 3. Fixture

`examples/fixtures/lantern-depths/` は、Phase 1 の lantern-depths を G-001 / G-002 より前の状態（ビルド 0.3、D-001 のみ、修正前の実装メモ）に戻したもの。

カナリア文字列を 2 つ埋めてある。

- `ZX-DESIGN-4420`（設計書）: Playtester に届いてはならない
- `ZX-IMPL-7731`（実装メモ）: Handoff に書かれない限り QA や Playtester に届いてはならない

## 4. 実行結果

### 4.1 隔離の実測（Claude Code）

最小のプロンプトで `claude -p` を起動し、起動時イベントと内容を確認した。

- ツール 0 個、MCP 0 個、skill 0 個。plugin は組み込みのみ。
- 入力は約 900 トークンで、CLAUDE.md、自動メモリ、hook の注入はない。
- カナリア（CLAUDE.md の "Rust Token Killer"、メモリの "cw-pipeline"、hook の "PONYTAIL" など）はすべて不可視だった。
- cwd のパス名だけはモデルに伝わる。そのため、プロジェクト名を含まない一時ディレクトリで実行する。

### 4.2 実行した Goal（モデルは Sonnet。Role に固定しない）

| 実行 | 結果 | オペレーション | 経路の特徴 |
|---|---|---|---|
| `examples/runs/bug-claude`（バグ Goal） | **完走** | 15（＋ replay 2） | 下記 |
| `examples/runs/combat-claude`（戦闘改善 Goal） | **完走** | 52（＋ replay 1） | 下記 |
| `examples/runs/resume-claude`（escalation の fixture から再開） | 成立 | 3 | Owner の回答 → fresh な Resume が D-002（`decided_by: owner`）を記録 → fresh な Designer が D-002 を Load 経由で受け取り、仕様を書いた |

バグ Goal の経路:

- Intake は、QA → Engineer → QA と、tentative な Design / Plan を選んだ。Director、Art Director、Playtester は通らない。
- QA は模擬ビルドでの合格を一度拒否した（#5）。
- 30 / 60 FPS の境界の許容幅が未定義だったため、Design（Designer、D-002）に戻り、QA の最終判定で合格した。

戦闘改善 Goal の経路:

1. 事前情報なしの Playtest。Route は、Playtester が報告した欠陥を別の QA ステップ（2b）として切り出した。
2. Designer の分析を受け、Director が権限内で D-002 を決めた（D-001 に触れないので escalation しないと明記）。
3. 詳細設計の途中で、**Art Director が必要になった時点で初めて加わった**。
4. Build で「リポジトリがない」問題が起き、**Owner escalation → 再開**した（D-008）。
5. Engineer が仕様の穴を Designer へ差し戻した（D-009）。
6. QA が 2 回差し戻した。Route はループ上限を意識していることを明記している。
7. Art Director の確認 → 事前情報なしの再 Playtest → Director のレビュー（goal-met、模擬に基づく判定と明記）で完了した。

### 4.3 Codex（cross-runtime）

`examples/runs/bug-codex2` は、同じ fixture と同じ packet 形式で、バグ Goal を Codex（`gpt-6-astra`、推論 low）だけで実行したもの。

**進み方**

1. Intake
2. QA が「模擬ビルドの記述では再現条件を確定できない」と 3 回差し戻した
3. （#8 の規則を追加したあと）Route が Owner へ escalation した
4. Owner（模擬）が観察を提供し、D-002 として fresh な Resume で再開した
5. QA の不具合報告
6. TD の計画（D-003）
7. Build
8. Simulator
9. Engineer による記述と模擬ビルドの照合、TD
10. QA の検証用 Handoff を作成

**到達点**

- 25 オペレーション、32 セッション（すべて異なる）、ツール使用なし。
- 残りは「QA 検証 → Close の Route」の 2 オペレーション。
- 週間上限が解除されたら `python3 scripts/studio_run.py next examples/runs/bug-codex2 --runtime codex --model gpt-6-astra` を繰り返して完走できる。

**互換性**

- Codex の出力は、Claude と同じ検証器（Phase 1 の構造規則と Role ポリシー）をすべて通った。Phase 1 の artifact 形式は変えていない。
- Codex は、Claude が書かない形を 2 つ使い、どちらも仕様の穴として直した（#3、#4）:
  - Handoff 列をパスで書く
  - アンカーを見出しの文字列で書く

**Codex で表に出た orchestration の穴**

- どの Role も作れない入力（#8）。
- Route がファイルを「読まないと Load に載せられない」と考え、資料の取得を求め続けた。「Load にはファイル名で載せればよく、受け手が読む」と Route 手順 5 に明記したところ、解消した。

**隔離**

- QA の packet に実装側のカナリアは入っていない。
- 混入が判明している唯一の入力は `~/.codex/AGENTS.md`（Owner の判断で受け入れ、記録済み）。

**完走（2026-10-11 追記）**

Codex の利用枠の回復後、Phase 3 の `run --runtime codex` で再開し、**Close（status: done）まで完走**した。

- 合計 35 オペレーション、44 セッション（すべて異なる）、ツール使用 0、QA の packet に実装側のカナリアなし。
- 途中の出来事:
  1. 2 回目の Owner escalation（TD が作成）が起きた。条件別の実測記録は dry-run では作れないためで、Owner（模擬）が「文書評価に範囲を縮小し、計測できない項目は未判定と明記」を選んだ（D-004）。
  2. Game Director のレビューで goal-met（縮小後の条件で）となった。
- Outcome には「全 4 環境での条件別挙動は未判定」などの限界が明記されている。

あわせて、Route が Escalation の作成前に Goal を `blocked-on-owner` にした誤りが見つかった。これを拒否する検証規則と、受理済みの Route をやり直す `route --since N` を追加した（`docs/phase3.md` の §12 #9）。

**最初の試行（`examples/runs/bug-codex`）**

前日の枠で Intake の 1 回目だけが実行され、ランナーのパーサ不備で拒否された。この記録はそのまま残してある。

### 4.4 利用量と時間（Sonnet、記録値）

下表の金額は `claude -p` が報告する `total_cost_usd`（API 価格に換算した推定値）であり、実際の請求額ではない。

- 実行はサブスクリプションの OAuth 認証で行った（起動時イベントの `apiKeySource: none`、`ANTHROPIC_API_KEY` は未設定）。
- そのため実際には、サブスクリプションの利用枠を消費した。14:10 にセッション上限に達して停止している。
- Codex 側も同様に、ChatGPT サブスクリプションの利用枠を消費した。

| 実行 | API 換算の推定値 | executor の実行時間 |
|---|---|---|
| バグ Goal | 約 1.6 ドル | 約 9 分 |
| 戦闘改善 Goal | 約 14 ドル | 約 80 分 |
| 再開テスト | 約 0.4 ドル | 約 4 分 |

### 4.5 テスト

`python3 -m pytest tests/` で 38 件すべて合格した。

- Phase 1 の 20 件は変更なし。
- Phase 2 の 18 件の内訳:
  - packet と allowlist の一致
  - Engineer → QA のカナリア、自己評価の除去
  - Playtester への期待結果の意図的な配置（5 通り）
  - Engineer が Playtester の報告を読み込めないこと
  - Step の書き込み制限
  - Route の入力が成果物だけであることと、その決定性
  - 受け手ポリシー違反の拒否
  - Owner の言葉を落とした Decision の拒否と再開
  - Claude runtime の隔離フラグとツール検出
  - 記録済み run の manifest 照合、セッションの一意性、カナリア
  - cross-runtime の書式
- 隔離の仕組みをわざと壊す変更を 7 種類入れ、7 種類とも検出された。

## 5. 判明した問題と対処

### 実行で見つかり、直したもの

| # | 現象 | 原因 | 対処 |
|---|---|---|---|
| 1 | Intake 直後、次のステップが開かない（`next` が「open なステップがない」で止まる） | Phase 1 の orchestration に「次のステップを `open` にする」という規定がなく、慣例でしかなかった（仕様の穴） | orchestration の Intake と Route に明記した。検証側でも、active な Goal には open なステップを必須にした |
| 2 | Route が Engineer の `## Sender assessment` を Handoff から削除し、記録から消えた | Route 手順 4 の「受け手が受け取ってはいけないものを除く」を文字どおり実行した | Sender assessment はそのまま残す規定を追加した（ランタイムが受け手ごとに除去するため）。in-place 編集で変更したら拒否する |
| 3 | Route 表の Handoff 列が、Claude ではリンク（`[x](x)`）、Codex ではプロジェクト相対パスで書かれ、照合に失敗した | Handoff 列の書式が未定義だった | テンプレートで「goal ディレクトリ内のファイル名」と定義した。パーサはリンクとパスも受け付ける |
| 4 | Codex が `project.md#Constraints` や `#Current` と書き、Claude は `#constraints` と書いた | `file#section` のアンカー書式が未定義だった | 見出しの slug（小文字、空白をハイフン）と定義した。大文字小文字は正規化する。`#Current` のように壊れたものは引き続き拒否する |
| 5 | QA が模擬ビルドでの合格を拒否した。ビルド記述に「未実行・未テスト。変更内容どおり」とあり、実装者の説明に依存することになるため | Simulator がメタな注記を書いた | Simulator の指示を「観測としてのビルド記述。模擬への言及はしない」に直した。QA の独立性は意図どおり機能していた |
| 6 | 戦闘改善 Goal で、Engineer が「リポジトリがないので実装できない」と差し戻しを続け、最後は TD が Owner に escalation した | fixture の Project Context に、dry-run での Build の扱いが書かれていなかった（Phase 1 の probe ではプロンプトで補っていた） | Owner（模擬）が判断し、D-008 として再開した。fixture の Constraints に dry-run の Build の扱いを追記した（Project 固有の規約なので Role 側ではなく Project Context に置いた） |
| 7 | 利用上限で Simulator が途中で失敗し、record.json のない記録が残った | 実行時エラーの経路で記録を書いていなかった | エラー時にも `status: error` の記録を残すようにした。Simulator だけを再実行する `simulate` コマンドを追加した |
| 8 | Codex のバグ Goal で、QA が「模擬ビルドの記述だけでは再現条件を確定できない」と差し戻し、Route が同じ QA へ 3 回戻した（ループ） | orchestration に「どの Role も作れない入力（Owner だけが持つ再現情報など）」の扱いがなかった。既存のループ上限は Verify の失敗と Diagnose の再入しか対象にしていなかった（仕様の穴） | escalation の条件に「どの Role も作れない情報・素材で止まった」を追加した。ループ上限に「同じ不足入力で `question` が 2 回返ったら、Role に戻さず Owner へ escalation」を追加した。修正後、Codex の Route は Owner へ escalation した（必要な観察項目を列挙）。Owner（模擬）の観察を受けて再開した |
| 9 | Codex の Route が、設計書・模擬ビルド・過去の Handoff の原文を取得しないと次の Handoff を組めないとして、`studio` 自身を次のステップに置いた（2 回拒否） | Route は最新の成果物とファイル名しか見ない設計なのに、「Load にはファイル名を載せればよく、読む必要はない」と書いていなかった | Route 手順 5 に明記した。あわせて、次のステップは必ず Role か Owner にすることも明記した。修正後、Codex の Route は QA への検証 Handoff を組めた |

executor の規則違反による拒否は 3 回あり、3 回とも新しい executor での再試行（検証エラーのみを渡す）で通った。内訳:

- Route 表の Role 欄に `playtester / game-director` と書かれた
- Route 表の Role 欄に「ランタイムのシミュレーター」と書かれた
- open なステップが 2 つ書かれた

このほか、ランナー側のパーサが誤って拒否したものが 3 回あった（#3）。これはランナーを直した。

### 未解決（Phase 2 の限界）

1. **Codex のユーザー全体の指示が executor に届く。** Codex は、フラグや設定の上書きをしても `~/.codex/AGENTS.md`（あなたの個人の作業ルール）を必ず読み込む。
   - カナリアで確認した範囲では、プロジェクトの情報（gamewright、lantern）は届いていない。
   - 防ぐ唯一の方法は使い捨ての `CODEX_HOME` だが、認証ファイルの扱いが伴う。
   - **Owner の判断（2026-10-10）: 混入を受け入れて記録する。**
     - 各 Codex 記録に `ambient_instructions` として残す。
     - Codex での実行は「プロジェクト情報の隔離は成立、個人の指示は混入」と区別して扱う。
2. **Codex のツールは一部を無効化できない。** `exec`（code mode。ホストを無効化したので実行時は失敗する）、collaboration 系、`apply_patch` が残る。ツールが 1 回でも使われたら、ランタイムがそのオペレーションを拒否する（監査）。Claude はツール 0 個で起動できる。
3. **Route は最新の成果物 1 件しか見ない。** 後回しにした並列ステップ（戦闘改善 Goal の 2b：Playtester が報告した欠陥の QA 再現）のように、古い成果物に依存する Handoff を Route が組めなかった。
4. **dry-run の検証は循環する。** Simulator は Engineer の変更記述からビルド記述を作るので、QA と Playtester が観察する「ビルド」は、実装者の記述から導かれたものにすぎない。情報の流れは隔離できても、模擬世界の真実性は保証できない。#5 の QA の拒否は、これを正しく指摘していた。実ゲームの自動操作（対象外）が入るまで残る。
5. **Role の判断の質と工程数は executor 次第。** 戦闘改善 Goal は Phase 1 の手書き版より大幅に長くなった（§4 を参照）。原因は次の 3 つ:
   - 差し戻しを慎重に繰り返した
   - Studio が 1 回の Route で Handoff を 1 件しか書けない
   - #6 の fixture の不備
6. **言い換えによる誘導は検出できない。** Playtester 宛ての Handoff に Owner の依頼文がそのまま入れば拒否するが、言い換えた期待結果は機械的には検出できない。Route（独立した executor）の判断に依存する。


## 6. 意図的に実装しなかったもの

- 自律的な連続実行。`next` は Step 1 回と Route 1 回で止まり、続きは人間が開始する。dry-run では小さな駆動スクリプトが「人間の代わりに next を押す」役をした。
- scheduler、queue、DB、UI、自動 merge、Role ごとのモデル固定（モデルは呼び出しごとの `--model`）
- 次工程の判断そのものの自動化。Route は LLM が判断し、スクリプトは規則の検証だけを行う。
- Playtester が実ゲームを操作する仕組み（Simulator で代用）
- 並列ステップの合流の自動化。並列ステップを開くこと自体はできるが、`--handoff` で個別に指定する必要がある。

## 7. 次の候補

1. ~~Codex の Goal を完走する~~ — 2026-10-11 に達成（§4.3）。

   `~/.codex/AGENTS.md` の混入は受け入れて記録する（Owner の判断）。
2. **Route の packet に「保留中の並列ステップが依存する成果物」を含める**（未解決 3）。または、1 回の Route で複数の Handoff を書けるようにする。
3. **「Owner escalation まで連続で進める」モード。** `next` の繰り返しを runner に入れる。上限、停止条件、記録は今のまま流用できる。
4. **実ビルドの Playtest / QA の harness**（未解決 4）。これがないと、dry-run の検証の循環は解けない。
