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

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（G-003時のsha: 660c1787ff32）。第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

repo/で実行：試験は`python3 -m unittest discover -s tests`、プレイは`python3 play.py --view player {script}`、状態表示は`--view trace`、botは`python3 bots.py {script}`。G-003のBuild報告で180 tests OK。

G-003（ダッシュの再使用可否）は達成（確認範囲に限る）。各画面に`dash: ready/active/N s`欄、早押しは`dash not ready — N s left`、再使用可能時に`dash ready`を表示（30 FPSは0.90秒まで許容、D-029）。第1部屋・60/30 FPS・スクリプトで読み取れた。未確認: 部屋移動リセット、bot整合、被弾・硬直中の押下、実機・適応プレイ、他部屋。変更前ビルドがなくタイミング不変は確認不能。ビルドID表記（b62005468da6等）の食い違いは未整理。

G-002はD-027により未達・検証未完了で打切り。実装は保持。ボス・公開情報限定botの検証、独立QA/Play/Reviewは未完了。試験成功は体験達成を示さない。通常ラン勝利時間は約87〜104秒で、15〜20分Visionとの整合は未評価。

候補Goal: 被弾時のダッシュ不可理由表示、`(nothing happens)`の診断、グラブ警告の古いカウントダウン、未確認項目の検証。

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
