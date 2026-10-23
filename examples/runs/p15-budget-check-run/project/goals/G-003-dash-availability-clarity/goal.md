---
kind: goal
id: G-003
project: lantern-depths
status: done
created: 2026-10-23
budget: 17
---
# G-003: Make it clear when dash can be used again

## Owner request

> ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい

## Interpretation

Success condition (qualitative): a player using only what the build shows them (text player view and `repo/manual.md`) can tell, at any moment, whether dash is available now, and when it is not, when it will be available again. They no longer have to guess or press dash to find out.

This is an experience (readability) Goal. The dash rules themselves (recovery length, invulnerability, input set) are assumed to stay as they are. Changing them would be a different Goal.

Out of scope:
- Rebalancing dash or combat.
- New input buttons (D-001).
- Reopening G-002 (stopped by D-027) or its unfinished verification.
- Any other readability issue the work happens to find (these become proposed Goals).

## Unknowns

- Observe, Diagnose, Decide, Design, Plan, Build, Verify, Play: done or skipped (see Route). The cause was missing information, not rules; no dash timing or rule change was made.
- Review: done (20, `goal-met`, limited to what was observed; D-030 scope cut).
- Not observed, now `skipped`: Q5, Q7, P12 via public replay scripts, P8/P9/P11, attack-refusal half of P13, Q3/Q4/Q6/Q10/Q11, Q9 gaps.
- Unverifiable (no baseline build): baseline-dependent parts of Q8/Q12 and "timing unchanged".
- Build identity: ids seen are `b62005468da6`, `aa28af2ce710`, `3951a3656940`; QA saw only `3951a3656940`. Unreconciled.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Diagnose | game-designer | diagnose-experience | done | 02-game-designer-to-studio.md |
| 2 | Decide | game-director | make-decision | skipped (no option changes dash rules or direction) | — |
| 3 | Design | game-designer | write-design-spec | done | 04-game-designer-to-studio.md |
| 4 | Build | gameplay-engineer | implement-change | done | 08-gameplay-engineer-to-studio.md |
| 5 | Verify | qa | verify-change | done (fail at 30 FPS; spec questions) | 10-qa-to-studio.md |
| 6 | Design (return) | game-designer | write-design-spec | done (D-029) | 12-game-designer-to-studio.md |
| 7 | Build (fixes) | gameplay-engineer | implement-change | done (partial; comparison not possible) | 14-gameplay-engineer-to-studio.md |
| 8 | Verify (re-check) | qa | verify-change | done (no failure; not a pass) | 17-qa-to-studio.md |
| 9 | Play | playtester | playtest-session | done | 18-playtester-to-studio.md |
| 10 | Review + scope cut | game-director | review-outcome | done (goal-met, limited; D-030) | 20-game-director-to-studio.md |

## Route changes

After Review (20, goal-met): the Goal is Closed. Unobserved verification items are `skipped` under the D-030 scope cut. Hit-stun reason display, `(nothing happens)`, grub warning countdowns and optional verification become proposed Goals. No Owner cost escalation was needed.

## Next action

None for G-003 (closed). Waiting for the Owner to decide which proposed Goals to open.

## Outcome

結果（ゲームディレクターのレビュー: 達成。ただし確認できた範囲に限る）:
- 各画面の `dash:` 欄が `ready` / `active` / `N s` を示し、早押しは `dash not ready — N s left`、再使用可能になった瞬間に `dash ready` が出ます。ダッシュの可否と再使用までの時間は、確認できた範囲（第1部屋、60/30 FPS、スクリプトによるプレイ）で、画面から読み取れました。
- ダッシュの速度・無敵・入力などのルールとタイミングは変えていません。30 FPSでは0.90秒までの許容です（D-029）。単体試験は180件OKです。
- 判断記録: D-028（旧経路にも表示）、D-029（仕様の裁定）、D-030（レビューの範囲判断）。

未確認・確認不能（合格とは扱いません）:
- QA未確認: 部屋移動でのリセット、bot整合、被弾・硬直中の押下、攻撃拒否側の一部、公開再生スクリプトでの確認など。
- 変更前ビルドがないため、「タイミング不変」と変更前との比較は確認できません。
- 人による確認は、1人・非適応スクリプト・第1部屋のみです。実機・ゲームパッド・ダッシュでの回避プレイ、他の部屋やボスは見ていません。
- ビルドIDの表記（`b62005468da6`、`aa28af2ce710`、`3951a3656940`）が食い違ったままです。QAは `3951a3656940` のみ確認しました。
- 公開ドライバの定期表示は、イベント表示の後に周期が再開します（`public-driver.md` の記載どおり。D-030で容認）。仕様書側の文言は次回の編集時に直します。

次のGoal候補:
1. 被弾後にダッシュが使えない理由を画面に出す（文言のみ、ルール変更なし）。
2. 被弾後に出る `(nothing happens)` の原因診断（不具合ならQAへ）。
3. グラブの警告カウントダウンが画面間で古く見える件（ダッシュ以外）。
4. 未確認項目の追加検証と、他の部屋での実機・適応プレイ（強い保証が必要な場合のみ）。

Ownerへのお願い: 上記1・2を開くか、4の追加検証が必要かをご判断ください。G-003の完了には影響しません。
