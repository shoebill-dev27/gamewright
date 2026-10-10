# Gamewright 仕様書

## 1. 概要

Gamewrightは、CodexやClaude CodeなどのAIエージェントを、ゲーム開発スタジオ内の異なる専門ロールとして協調させるための仕組みである。

単なるRole定義集ではなく、**人間から与えられたゲーム開発上のGoalを受け取り、そのGoal達成に必要な調査・設計・実装・検証・Playtestを適切なRoleへ割り当て、開発サイクルを進める仮想ゲームスタジオ**を目指す。

---

## 2. 目的

目的は、AIを単なるコード生成ツールとしてではなく、ゲーム開発を継続的に進める仮想スタジオとして利用できる状態を作ることである。

人間が毎回、

- どのRoleを使うか
- 何を調査するか
- 誰にレビューさせるか
- 何を実装するか
- 次に何をするか

を逐次指定する必要を減らす。

人間は主としてOwnerとしてGoalや方向性を与え、Studio側が必要な開発活動へ展開する。

---

## 3. 想定利用モデル

Gamewrightの基本的な入口は、Role指定ではなくGoalである。

例えば人間は、

```text
戦闘が単調なので改善したい
```

```text
序盤30分で離脱する原因を見つけて直したい
```

```text
このプロトタイプを製品として遊べる品質まで持っていきたい
```

といった要求をStudioへ渡す。

StudioはGoalを解釈し、その達成に必要な工程を決定する。

例えば、

```text
Owner Goal
↓
Playtest
↓
Game Design Analysis
↓
Director Decision
↓
Detailed Design
↓
Technical Planning
↓
Implementation
↓
QA
↓
Re-Playtest
↓
Review
```

のように進める。

ただし、すべてのGoalで全Roleを利用するわけではない。

単純な不具合であれば、

```text
QA
↓
Engineer
↓
QA
```

だけで完結してよい。

Studioの責務は工程を増やすことではなく、**Goal達成に必要な専門判断だけを選択すること**である。

---

## 4. 目指すユーザー体験

最終的には、人間がCodexやClaude Codeそのものを逐次操作するのではなく、Studioへ依頼する形を目指す。

例えば、

```text
今のビルドを遊んで、
面白さを阻害している最大の問題を1つ改善して
```

という依頼に対して、Studioが内部で必要なRoleを選択し、

- Playtest
- 問題分析
- 改善案作成
- 実装
- QA
- 再Playtest

まで進める。

人間へ返すのは主に、

- 実施結果
- 重要な判断結果
- 次の課題
- Owner判断が必要な事項

とする。

---

## 5. Owner Escalation

Studioはすべての判断を自律的に確定してはならない。

以下のような判断はOwnerへ戻す。

- ゲームの根本コンセプトを変える
- 大きな方向性が複数存在する
- scopeやリスクが大きく変わる
- 人間の好みや価値観が主要判断基準になる
- irreversibleな変更
- Studioに与えられたGoalそのものの再解釈が必要

その場合、単に「判断してください」と返すのではなく、

```text
Option A
Option B

Studio recommendation: B

理由:
...

Owner decision required:
A / B
```

のように、判断可能なところまで整理して返す。

Ownerが判断したら、そのDecisionを保存して開発サイクルを再開する。

---

## 6. ProjectとStudioの分離

Gamewright自体は特定のゲームに依存しない。

StudioとゲームProjectは分離する。

概念的には以下。

```text
Virtual Game Studio
├─ Project A
├─ Project B
└─ Project C
```

各Projectは少なくとも、

- repository
- game vision
- current state
- constraints
- relevant design
- decisions

などのContextをStudioへ提供する。

同じRole / Skill / Workflowを複数ゲームで再利用できることを目指す。

---

## 7. 基本思想

### 7.1 RoleとAIモデルを分離する

```text
Role ≠ Model
```

Roleは責任、Modelは実行手段である。

Codex / Claude Codeなどの割当を変更してもStudio構造は変わらない。

---

### 7.2 RoleとSkillを分離する

Roleは「誰が何に責任を持つか」。

Skillは「その仕事をどう行うか」。

RoleとSkillは独立して再利用できること。

---

### 7.3 Project ContextをRoleから分離する

Roleは特定ゲーム専用にしない。

Project固有のVision、Design、Current State、Constraints、DecisionはContextとして外部から与える。

---

### 7.4 Workflowを固定しすぎない

Studioには標準的な開発ループを持たせるが、毎回同じ工程を強制しない。

Goal、問題の種類、現在状態に応じて必要なRoleだけを選択する。

---

## 8. Roleの責任分離

代表的なRoleは以下。

### Game Director

ゲーム全体の方向性、優先順位、重要判断を担当する。

### Game Designer

プレイヤー体験をルールやシステムへ落とし込む。

### Technical Director

承認された仕様を技術的に実現可能な計画へ変換する。

### Gameplay Engineer

承認済み設計を実装する。

### Art Director

視覚表現とビジュアル上の一貫性を担当する。

### QA

実装結果を独立して検証する。

### Playtester

プレイヤーとしてゲーム体験を評価する。

詳細はRole Contractとして別管理する。

---

## 9. 責任境界

各Roleが、自分で問題を発見し、自分で仕様を変え、自分で実装し、自分で承認する状態を避ける。

Engineerが仕様上の問題を見つけた場合はGame DesignerやDirectorへ戻す。

QAは検証対象のproduction codeを自ら修正しない。

Playtesterは内部実装ではなく、プレイヤーから観測可能な体験を評価する。

---

## 10. Handoff

Role間の仕事は、明示的なHandoffによって引き継ぐ。

Handoffには少なくとも、

- Task
- Context
- Findings
- Decisions already made
- Constraints
- Open questions
- Expected output

を含める。

会話履歴だけに依存せず、別モデル・別セッションでも継続可能にする。

---

## 11. Decision

重要な判断は会話履歴だけに残さずDecisionとして保存する。

Decisionには、

- 何を決めたか
- なぜそうしたか
- 他にどんな案があったか
- 何が変われば再検討するか

を残す。

---

## 12. 標準開発ループ

標準的には以下の循環を持つ。

```text
Observe
↓
Diagnose
↓
Decide
↓
Design
↓
Plan
↓
Build
↓
Verify
↓
Play
↓
Review
↓
Next
```

これは固定パイプラインではなく、必要に応じて短縮・分岐できる。

---

## 13. Studio Orchestration

StudioはGoalを受け取ったら、

1. Goalを理解する
2. 現在のProject Contextを確認する
3. 何が未確定かを特定する
4. 必要なRole / Skillを選ぶ
5. 実行順序または並列化を決める
6. 各結果をHandoffとして次へ渡す
7. Owner Escalationが必要か判断する
8. Goal達成または次の明確な判断点まで進める

ことを責務とする。

このオーケストレーション能力が、単なるRole集との最も大きな違いである。

---

## 14. Subagent

SubagentはRoleそのものではなく、Roleの仕事を実行するAIプロセスである。

必要な場合は専門調査を並列化できる。

最終判断は多数決ではなく、その判断責任を持つRoleが行う。

---

## 15. Worktree

Worktreeは独立したコード変更を安全に並列実行するための手段として利用できる。

Role分離そのものをWorktreeで表現しない。

---

## 16. Tool固有機能との関係

Studioの基本仕様はCodexやClaude Codeの特定機能へ依存させない。

概念的には、

```text
Virtual Studio
↓
Role / Skill / Workflow / Context
↓
Tool-specific execution
├─ Codex
└─ Claude Code
```

とする。

Tool固有機能は実行方法として利用し、Studioの責任モデルには埋め込まない。

---

## 17. コンテキスト効率

毎回すべてのRole・Skill・文書を読み込ませない。

原則として、

```text
Current Role
+
Required Skills
+
Current Task
+
Relevant Project Context
+
Relevant Decisions
+
Previous Handoff
```

だけを利用する。

---

## 18. 段階的な実現

最終形は高い自律性を持つStudioだが、初期段階から完全自動化する必要はない。

初期段階では、

```text
Goal
↓
Studioが次のRoleを決定
↓
人間が実行を開始
↓
結果保存
↓
Studioが次工程を決定
```

でもよい。

その後、

```text
Goal
↓
Studioが複数工程を自動実行
↓
Owner判断が必要な時だけ停止
```

へ段階的に進化できることを前提とする。

---

## 19. 人間の役割

人間は主としてOwnerとして振る舞う。

Ownerが担うのは、

- Goal
- 大きな方向性
- 好み
- 価値判断
- 高リスク判断
- Studioでは決めるべきでない事項

である。

調査、設計、実装、検証、Playtest、問題分析は可能な限りStudio側が担当する。

---

## 20. この仕組みによって得たい価値

### AIへの細かな指示を減らす

人間が毎回工程を組み立てなくてもよくする。

### 専門観点を分離する

「実装できる」「バグがない」「分かりやすい」「面白い」を別々に評価できる。

### AIモデルを交換可能にする

Codex、Claude Code、将来の別モデルへ差し替え可能にする。

### 複数ゲームへ再利用する

ゲームごとにAI開発組織を作り直さなくてよい。

### 長期開発に耐える

Role、Skill、Decision、Handoff、Contextによってセッションを跨いで設計意図を維持する。

### 人間をOwnerへ近づける

細かなAI操作ではなく、ゲームそのものへの要求と判断に集中できる。

---

## 21. 非目標

以下は目的ではない。

- 実在スタジオの組織を完全再現する
- Role数を増やす
- Agent数を増やす
- 全工程を常に複数Agentで処理する
- 特定モデルへ最適化する
- 人間のクリエイティブ判断を完全排除する
- 最初から完全自律開発を実現する

必要な複雑さだけを追加する。

---

## 22. 成功状態

成功状態は、

```text
Owner Goal
↓
Virtual Game Studio
↓
必要な調査・設計・実装・検証・Playtestを編成
↓
Goal達成、またはOwner判断が必要な地点まで進行
↓
結果をOwnerへ返す
```

という使い方ができることである。

ユーザーが毎回「次はDesigner」「次はEngineer」とAIを操作するのではなく、Studioへゲーム開発上のGoalを依頼できること。

また、個々のAIの性能だけに依存せず、

**役割、責任、専門能力、判断履歴、引き継ぎ、オーケストレーションによってゲーム開発全体の品質と継続性を高めること**

を最終目標とする。