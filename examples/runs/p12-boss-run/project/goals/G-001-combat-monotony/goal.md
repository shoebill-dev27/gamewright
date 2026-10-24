---
kind: goal
id: G-001
project: lantern-depths
status: done
created: 2026-10-16
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player playing the current build's combat experiences it as varied and engaging instead of monotonous. Different situations call for noticeably different play (positioning, timing, use of attack and dash), and the player can tell why. The improvement stays inside the vision pillars: one-button combat (attack + dash only, D-001), short runs, readable threats. Numeric thresholds belong to Design; the final verdict belongs to Review.

Out of scope: new input buttons (needs Owner approval per D-001), changing run length, new biomes or content unrelated to combat variety, and any change to the core concept. Not a defect report: nothing in the request says combat is broken.

## Unknowns

- Observe: done (playtests 02, 27, 53, 63, 88; QA checks to 90). Contact-edge graze accepted (D-002, D-003). QA 90: playtest room 4 hits not reproduced, no defect.
- Diagnose: two passes done (04, 31); a third is barred by the loop limit. No new cause since.
- Decide: skipped. Review pass 3 (D-013) found no Owner-level question; row 11 skipped.
- Design: D-004 to D-007, D-011, D-012 stand. The wording spec (94, design/combat-step94.md) is corrected (102): W1 spitter (15,7) now south-east, W5 brute timing added. The stray last line of D-007 cannot be removed by any step: an Owner item at Close.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: wording round done (96). Manual stray marker removed (101); the marker search of game.py and tests and the suite run were not done by the engineer.
- Verify: 29f done (104, pass): manual line and markers clean, suite 69 OK, W1 (15,7) doc check consistent and shown live at 60 FPS. Known gaps for Review (no further full QA round): room 3 sidestep and 30 FPS cancel/recovery swipe; W2 at 30 FPS, W3, W4, W6, W7 and bots only partly shown. Visual V1–V11 need a graphical build (proposed new Goal at Close); V12 open.
- Play: four scripted passes done. Open observations: grub encounters feel the same in all rooms; spitter rooms mostly dodging; brute tail in room 5 empty. Only a live player can settle these.
- Review: passes 1–3 goal-not-met; pass 3 narrowed the gap to "the player can tell why" for shot hits and late swipes. Pass 4 (106, D-014): goal-met on the text-view build; paper check, no live player yet. Closed.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md (result: 07-game-designer-to-studio.md) |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | done | 06-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 5 | Plan | technical-director | technical-plan | skipped (approach local; see Unknowns) | — |
| 6 | Build | gameplay-engineer | implement-change | done | 09-studio-to-gameplay-engineer.md (result: 10-gameplay-engineer-to-studio.md) |
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | done | 11-studio-to-game-designer.md (result: 14-game-designer-to-studio.md) |
| 7b | Verify (visual) | art-director | visual-review | done | 12-studio-to-art-director.md (result: 15-art-director-to-studio.md) |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | done | 13-studio-to-qa.md (result: 16-qa-to-studio.md) |
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (result: 18-gameplay-engineer-to-studio.md) |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | done (question: graze) | 19-studio-to-qa.md (result: 20-qa-to-studio.md) |
| 8b | Design (graze, cap, margin, doc conflicts) | game-designer | write-design-spec | done | 21-studio-to-game-designer.md (result: 22-game-designer-to-studio.md) |
| 8c | Build (contact test / cap) | gameplay-engineer | implement-change | skipped (graze and cap accepted as built) | — |
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | done (pass) | 23-studio-to-qa.md (result: 24-qa-to-studio.md) |
| 9a | Play | playtester | playtest-session | done | 25-studio-to-playtester.md (report: 27-playtester-to-studio.md) |
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | done | 26-studio-to-game-designer.md (result: 30-game-designer-to-studio.md) |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | done | 28-studio-to-game-designer.md (result: 31-game-designer-to-studio.md) |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | done (not a defect) | 29-studio-to-qa.md (result: 32-qa-to-studio.md) |
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | skipped (not fired in pass 3, D-013) | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | done (pass) | 49-studio-to-qa.md (result: 50-qa-to-studio.md) |
| 18a | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | done | 51-studio-to-playtester.md (report: 53-playtester-to-studio.md) |
| 18b | Design (criterion 11d wording, non-blocking) | game-designer | write-design-spec | done (no build change) | 52-studio-to-game-designer.md (result: 54-game-designer-to-studio.md) |
| 18c | Observe (late swipe vs lunge; hit with no cue; message wording) | qa | reproduce-defect | done (not a defect) | 55-studio-to-qa.md (result: 56-qa-to-studio.md) |
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (D-008 proposed, later D-011) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | done (goal-not-met; D-010) | 65-studio-to-game-director.md (result: 67-game-director-to-studio.md) |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | done (D-007 stands; D-011 accepted) | 66-studio-to-game-designer.md (result: 68-game-designer-to-studio.md) |
| 22a | Build (D-011 messages, manual wording) | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md (result: 71-gameplay-engineer-to-studio.md) |
| 22b | Design (room 3 variety, existing enemies) | game-designer | write-design-spec | done (D-012) | 70-studio-to-game-designer.md (result: 72-game-designer-to-studio.md) |
| 23 | Build (room 3 change, D-012) | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md (result: 74-gameplay-engineer-to-studio.md) |
| 24 | Verify (22a + 23; V-a..e, R3-1..10; 30 and 60 FPS) | qa | verify-change | done (fail: red test only) | 75-studio-to-qa.md (result: 76-qa-to-studio.md) |
| 25a | Build (fix test, test code only) | gameplay-engineer | implement-change | done | 77-studio-to-gameplay-engineer.md (result: 79-gameplay-engineer-to-studio.md) |
| 25b | Design (doc conflicts, documents only) | game-designer | write-design-spec | done (D-007 stray line left) | 78-studio-to-game-designer.md (result: 80-game-designer-to-studio.md) |
| 26 | Verify (re-verify; close R3-8, R3-4 gaps) | qa | verify-change | done (no defect; 5 items unjudged) | 81-studio-to-qa.md (result: 82-qa-to-studio.md) |
| 26b | Verify (R3-8 timed run, R3-4 in room 3) | qa | verify-change | done (no defect; 60 FPS items unshown) | 84-studio-to-qa.md (result: 86-qa-to-studio.md) |
| 26c | Design (doc wording, D-007 stray line) | game-designer | write-design-spec | done (wording fixed; D-007 line is an Owner item) | 85-studio-to-game-designer.md (result: 87-game-designer-to-studio.md) |
| 27 | Play (fresh, new build, reaction rules) | playtester | playtest-session | done | 83-studio-to-playtester.md (report: 88-playtester-to-studio.md) |
| 27b | Observe (room 4 hits, swipe-and-still-hit; last bounded 60 FPS items) | qa | reproduce-defect | done (no defect; 2 readability gaps) | 89-studio-to-qa.md (result: 90-qa-to-studio.md) |
| 28 | Review (pass 3) | game-director | review-outcome | done (goal-not-met; D-013) | 91-studio-to-game-director.md (result: 92-game-director-to-studio.md) |
| 29a | Design (wording: shot-hit source, late-swipe line) | game-designer | write-design-spec | done | 93-studio-to-game-designer.md (result: 94-game-designer-to-studio.md) |
| 29b | Build (wording only) | gameplay-engineer | implement-change | done | 95-studio-to-gameplay-engineer.md (result: 96-gameplay-engineer-to-studio.md) |
| 29c | Verify (text appears; reaction rules, bots, suite; 30 and 60 FPS) | qa | verify-change | done (fail: manual marker; gaps) | 97-studio-to-qa.md (result: 98-qa-to-studio.md) |
| 29d | Build (manual.md stray marker, text only) | gameplay-engineer | implement-change | done | 99-studio-to-gameplay-engineer.md (result: 101-gameplay-engineer-to-studio.md) |
| 29e | Design (W1 bullet for spitter at (15,7)) | game-designer | write-design-spec | done | 100-studio-to-game-designer.md (result: 102-game-designer-to-studio.md) |
| 29f | Verify (manual line, marker search, suite, W1 doc check) | qa | verify-change | done (pass) | 103-studio-to-qa.md (result: 104-qa-to-studio.md) |
| 30 | Review (pass 4, paper check; known gaps from 98, 104) | game-director | review-outcome | done (goal-met; D-014) | 105-studio-to-game-director.md (result: 106-game-director-to-studio.md) |
| 31 | Next | studio | — | done (Close) | — |

## Route changes

After Review pass 4 (106, goal-met, D-014): fits the plan, no escalation trigger. Row 30 done, Close (Next) done, status set to done. Proposed Goals and the D-007 Owner item are listed in Outcome.

## Next action

None. The Goal is closed. Waiting for the Owner only on the items in Outcome (D-007 stray line; whether to open the proposed Goals).

## Outcome

**結果**: 戦闘の単調さは、テキスト表示ビルド（build 0.6.1 以降）で解消されたと判断しました（Review 第4回、D-014: goal-met）。

- 状況ごとに求められるプレイが明確に異なります。ランナー、通常のグラブ、ブルート、スピッターはそれぞれ違う対応を要求し、部屋4・5ではそれらが組み合わさります。部屋3にも第2の要求を追加しました（D-012）。
- 「なぜそうなったか」がプレイヤーに分かるようになりました。弾に当たったときは「どの方向から」撃たれたかが表示され、遅すぎたスワイプでは「突進がすでに始まっていたため止められなかった」という説明が出ます。マニュアルにも同じ内容を記載しました。
- 1ボタン戦闘（D-001）、短いラン、読みやすい脅威という柱は維持されています。新しい入力ボタンは追加していません。

**記録した Decision**: D-002〜D-014（接触端のかすり許容、キューの間隔、ウォーカー上限、バリアント名表示、部屋3の変更、Review 各回の判断など）。

**制限**: 証拠はすべてスクリプト実行と QA のトレースによるものです。実際の人間のプレイヤーが新しい文言を試した結果はまだありません。

**次の課題（新しい Goal の提案。G-001 には含めません）**:
1. グラフィカルビルドでの視認性（視覚基準 V1〜V12。V1〜V11 はテキスト表示では確認できず、V12 は未決）。
2. 実プレイヤー1人による新しい文言の確認（1と一緒に、またはその最初のステップとして）。
3. グラブの単調さ、スピッター部屋が回避中心になる点、部屋5のブルート終盤が空になる点。実プレイヤーから報告があった場合にのみ着手します。ブルートの最初の手段は D-004 の選択肢3、スピッター部屋は間隔とオフセットの調整です（D-005、D-012）。

**Owner の対応が必要な項目**:
- D-007 の末尾にある不要な1行は、どのステップからも削除できません。削除するか、残す場合はその旨を確認してください。
- 方向性に関する Owner の判断は不要です。上記の提案 Goal を開始するかどうかだけご指示ください。
>>>REPLACE
