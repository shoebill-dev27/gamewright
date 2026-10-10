---
kind: goal
id: G-002
project: lantern-depths
status: done
created: 2026-10-10
---
# G-002: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success: in a playtest of the 5-room slice, the player has to make different decisions across rooms
(where to stand, when to dash, which enemy first) instead of repeating one pattern, and the Game
Director judges the monotony addressed on that evidence. Out of scope: new biomes,
meta-progression, run length.

## Unknowns

| Entry question | Answer from the Project Context | Stage |
|---|---|---|
| Observed first-hand? | No — the Owner's impression only | Observe (`playtester`; experience problem, not a defect) |
| Cause understood? | No | Diagnose (`game-designer`) |
| Choice of direction, priority, scope? | Likely: several ways to add variety exist, and D-001 limits some | Decide (`game-director`) |
| Intended behavior specified? | No — new behavior will be needed | Design (`game-designer`) |
| Approach non-obvious or risky? | Likely: enemy behavior lives in a shared controller | Plan (`technical-director`) |
| Game must change? | Yes | Build (`gameplay-engineer`) |
| Built something? | Yes | Verify (`qa`) |
| Experience Goal? | Yes | Play (`playtester`), Review (`game-director`) |
| Visual problem? | Unknown | `art-director` tentative — only if a diagnosis points to readability |

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done (escalated) | 03-game-designer-to-game-director.md |
| 4 | Decide | owner | — | done (D-002) | 04-game-director-to-owner.md |
| 5 | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md |
| 6 | Plan | technical-director | technical-plan | done | 06-game-designer-to-technical-director.md |
| 7 | Build | gameplay-engineer | implement-change | done (question) | 07-technical-director-to-gameplay-engineer.md |
| 8 | Design | game-designer | write-design-spec, make-decision | done (D-003) | 08-gameplay-engineer-to-game-designer.md |
| 9 | Build | gameplay-engineer | implement-change | done | 09-game-designer-to-gameplay-engineer.md |
| 10 | Verify | qa | verify-change | done (pass) | 10-gameplay-engineer-to-qa.md |
| 11 | Play | playtester | playtest-session | done | 12-studio-to-playtester.md |
| 12 | Review | game-director | review-outcome | done (goal-met) | 13-playtester-to-game-director.md |
| 13 | Next | studio | — | done | 14-game-director-to-studio.md |

## Route changes

- After step 3: the Director folded Option C into A (own authority) but found Option B would change
  Owner Decision D-001 while the evidence left A and B both viable → escalation triggers → inserted
  step 4 (Owner); all later steps paused.
- After step 4 (Resume): the Owner chose A with a condition → D-002. Remaining route unchanged, per
  the escalation's "If chosen" for A.
- After step 6: `art-director` stays tentative-not-needed; the spec reuses the existing threat color.
- After step 7: the engineer handed back with spec questions (`outcome: question`). Return rule
  "Build: spec missing a case → Design" inserted steps 8–9.
- After step 10: next recipient is a Playtester, so QA reported to the Studio (11) and the Studio
  composed a blind handoff (12).
- After step 12: Review verdict `goal-met`; the readability issue becomes proposed G-003 rather than
  scope growth.

## Next action

None — Goal closed. Proposed G-003 awaits the Owner's go-ahead.

## Outcome

- **結果:** 戦闘の単調さは解消したと Game Director が判断しました。根拠は、事前情報なしで行った再 Playtest です。「隅で連打」の戦法は部屋3で通用しなくなり、部屋3〜5ではダッシュを回避に使うようになりました。プレイヤーは部屋ごとに求められることが違うと感じています。QA は 30 / 60 FPS で全項目合格としました。
- **やったこと:** 敵の攻撃に予兆（オレンジの発光）を追加し、新しい敵を 2 種（突進する Charger、正面をガードする Shieldbearer）入れ、部屋ごとに求めることを変える構成にしました。操作はワンボタンのままです。
- **判断:**
  - **D-002（Owner 判断）:** 案A を採用。ワンボタンは維持し、長押し溜め攻撃は将来の検討候補とする。
  - **D-003（Game Designer）:** 予兆の出た攻撃は、攻撃を当てても中断されない。
- **経路:** Playtest → 分析 → Director → **Owner 判断（停止・再開）** → 詳細設計 → 技術計画 → 実装 → **仕様の不明点を Designer へ差し戻し** → 実装 → QA → 再 Playtest → レビュー。
- **次の課題（提案 G-003）:** 部屋5の暗い場所で、Shieldbearer の予兆が見えにくい問題があります。柱3「脅威は当たる前に見える」に反するため、Art Director を含む視認性改善として扱うことを提案します。着手するかは Owner の判断です。
- **Owner 判断が必要な事項:** G-003 に着手するかどうかのみです。「重い一撃が欲しい」という声は弱まっており、D-002 の再検討条件には達していません。
