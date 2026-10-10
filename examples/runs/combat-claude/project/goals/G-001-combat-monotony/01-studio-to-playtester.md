---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — ビルド 0.3 をプレイし、戦闘体験を観察報告する

## Task

ビルド 0.3 をプレイヤーとして遊び、戦闘に注目して、観察できた体験を報告する。

## Context

プレイヤー視点の体験観察が必要な Goal の最初のステップ。プレイヤーに見えるものと感じたことだけを報告する。

## Findings

該当なし(実装に関する情報は渡さない)。

## Decisions already made

None

## Constraints

- プレイヤーとして観察できる内容のみに基づく。内部実装や設計意図を推測して書かない。
- ビルドは `sim/build-0.3.md`(ドライランでは、このファイルを読むことが「ビルドを実行する」ことに相当する)。
- 対象は全5部屋を通したプレイ。

## Open questions

None

## Expected output

観察報告(`playtest-session` の形式)。プレイした内容、戦闘中に感じたこと(印象的だった点、退屈・緊張・迷いなど)、その根拠となる具体的な場面を含める。
結果は `studio` 宛てとして、この Goal の `02-playtester-to-studio.md` に書く。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.3.md
- Decisions: none
- Previous handoff: none
