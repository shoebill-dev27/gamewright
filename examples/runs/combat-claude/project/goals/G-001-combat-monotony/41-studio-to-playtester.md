---
kind: handoff
goal: G-001
seq: 41
from: studio
to: playtester
stage: Play
outcome: routed
---
# 41: studio → playtester — ビルド 0.6 を遊んで、戦闘の体験を報告する

## Task

ビルド 0.6 を、下のプレイヤー像のプレイヤーとして遊び、体験したことをそのまま報告する。今回は特に戦闘に注意を向ける。

## Context

ランタンの光る洞窟を 1 部屋ずつ下りる、短時間のトップダウン・アクション・ローグライトの試作版を遊んでもらう。このプロジェクトでは「ビルドを動かす」とは、プレイヤーに見える記述 `sim/build-0.6.md` を読み、その場面を遊んだつもりで体験を報告することを指す(ドライランの約束事)。

## Findings

(この Handoff は Studio が組んだ。Playtester に渡す実装・変更に関する情報はない。)

プレイヤー像(`project.md#player-profile`):
短時間で濃いランを求めるアクション好き。回避と間合いには慣れているが、コンボ表を覚えるのは好まない。主にゲームパッドで遊ぶ。

## Decisions already made

None

## Constraints

- 入力はビルド記述にある操作だけで遊ぶ。
- 見えたこと、感じたこと、起きたことだけを書く。原因の推測や設計の提案は、観察と分けて書く。
- 記述を読むだけでは判断できなかったこと(実時間の感触、画面の実際の見え方、ゲームパッドの操作感など)は、「確認できなかった」と明記する。推測で埋めない。

## Open questions

None

## Expected output

観察報告(`playtest-session` の形式)を `goals/G-001-combat-monotony/42-playtester-to-studio.md` に書く(`to: studio`)。次の Review の Handoff を Studio が組むためで、判定や解決策の決定は求めない。不具合らしい挙動を見つけたら、観察としてそのまま書く。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile、sim/build-0.6.md
- Decisions: none
- Previous handoff: none
