---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（今回のsha: dc0138c2b6d1）。既存第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装報告済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

repo/で実行：試験は`python3 -m unittest discover -s tests`、プレイは`python3 play.py --view player {script}`、状態表示は`python3 play.py --view trace {script}`、botは`python3 bots.py {script}`。source fc07c7db6383で161 tests OKの記録がある。今回のshaでの再試験は本Resumeでは未実施。

G-002はD-027により費用を理由に未達・検証未完了で打切り。実装は保持する。公開情報限定botの実接続・記憶、被弾差の原因確定、経路監査、接触診断全体、ボス4条件・保持回帰の再測定、公開再生の証拠確認が未完了。独立QAの再検証、限定Art Verify、独立Play、実測後Designer判断、最終Reviewも未実施。試験成功は体験Goal達成を示さない。

変更前ビルド不在による歴史的一致の確認不能は別途残る。通常ラン勝利時間のBuild報告は約87〜104秒で、15〜20分Visionとの整合は未評価。再開の必要性は別GoalとしてOwnerが判断する。

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
