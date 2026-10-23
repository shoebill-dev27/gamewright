---
kind: goal
id: G-003
project: lantern-depths
status: done
created: 2026-10-23
budget: 9
---
# G-003: ダッシュの再使用可能タイミングを分かりやすくする

## Owner request

> ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい

## Interpretation

Success condition: while playing, the player can tell from what the game shows (the player view and `repo/manual.md`) whether dash is usable now and, if it is not, when it will be usable again. They do not need to guess, count frames, or find out by pressing dash and failing.

This is an experience (readability) problem. Dash is presumably limited after use, but the Project Context does not state the rule. The Designer confirms it from `design/combat.md` and the build.

Out of scope:
- Changing dash's role in combat or its rules or numbers. The goal is making the existing rule visible. If readability turns out to depend on a rule change, the Designer records that as an option and the Studio routes it (Decide) instead of building it.
- New input buttons (D-001).
- Reopening G-002 items (final boss and the verification left unfinished when it was stopped).
- Numeric thresholds, which belong to Design. The final verdict belongs to Play and Review.

Constraint: it must work correctly at 30 and 60 FPS. Reuse existing systems (project.md#constraints).

## Unknowns

- Observe: skipped. The Owner's first-hand report names the problem.
- Diagnose: done (inside Design). The player view showed no dash state; the documented rule was ambiguous. No rule change needed.
- Decide: skipped. No choice of direction or scope arose.
- Design: done (Handoff 05, D-028). No rule or number change.
- Plan: skipped. Local change reusing existing display and state.
- Build: done (Handoff 06).
- Verify: done (Handoff 08), no failure at 30 and 60 FPS. Not verified: DR8 and DR9 (a)/(c), for lack of old-build output.
- Play: done (Handoff 10). Dash readiness read clearly in rooms 1 and 3 at 30 and 60 FPS. Not observed: dash invulnerability meeting a lunge or shot, gamepad feel, rooms 2/4/5.
- Review: skipped. Play was unambiguous on the Goal and implied no direction change; new issues become proposed Goals.
- Art Director: skipped. Text build, informational cue.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Diagnose + Design | game-designer | diagnose-experience, write-design-spec | done | 01-studio-to-game-designer.md (result: 02-game-designer-to-gameplay-engineer.md) |
| 2 | Build | gameplay-engineer | implement-change | done | 02-game-designer-to-gameplay-engineer.md (result: 03-gameplay-engineer-to-studio.md) |
| 3 | Design (rulings) | game-designer | write-design-spec, make-decision | done | 04-studio-to-game-designer.md (result: 05-game-designer-to-gameplay-engineer.md) |
| 4 | Build (fix) | gameplay-engineer | implement-change | done | 05-game-designer-to-gameplay-engineer.md (result: 06-gameplay-engineer-to-studio.md) |
| 5 | Verify | qa | verify-change | done | 07-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 6 | Play | playtester | playtest-session | done | 09-studio-to-playtester.md (result: 10-playtester-to-studio.md) |
| 7 | Review | game-director | review-outcome | skipped | — |

## Route changes

After step 6: Play confirmed dash readiness reads clearly; the 30 FPS 0.05 s lag is within D-028's 2-frame bound. Review skipped (no ambiguity, no direction change). Room 3 readability goes to a proposed Goal. Goal closed.

## Next action

None. The Goal is closed; the Owner decides on the proposed new Goals.

## Outcome

結果: ダッシュの再使用可否がプレイヤー表示だけで分かるようになった。ダッシュのルールと数値は変えていない。
- プレイヤー表示に`dash: ready` / `recharging N s`の行が出る。使用時は「ready again in 0.85 s」、拒否時は「dash not ready: N s left」、復帰時は`dash ready`が出る。被弾後の再充電も同じ行で分かる。拒否された入力は保存されない。
- QAは30/60 FPSで不合格なし。プレイテスターは部屋1・3で、行・メッセージ・実際の復帰時刻が一致することを確認した。

決定: D-028（準備完了の許容は0.85 sに対し2フレーム、被弾後のスタンは再充電として表示、クールダウンはダッシュ終了から数える）。

残る注意点:
- 旧ビルドの出力と元の検証スクリプトがなく、DR8とDR9 (a)/(c)は未検証。
- 30 FPSでは復帰が約0.05 s遅れる（許容内）。
- ダッシュ中の無敵が弾や突進に当たる場面は未観測。被弾後の無敵は表示されない。ゲームパッドの操作感、部屋2・4・5、ボスは未確認。

次のGoal案:
1. 部屋3の読み取りにくさ: スピッター3体の狙い線が重なり同時に撃つ。プレイテスターはこのせいで12秒で死亡した。Diagnoseから始める。
2. ダッシュ無敵と被弾後無敵の見せ方: 追加のプレイ確認。
3. G-002の再開要否（D-027で打切り中）: Ownerの判断が必要。

Ownerへの依頼: 上記Goal案のうち、どれを進めるか選んでください。
