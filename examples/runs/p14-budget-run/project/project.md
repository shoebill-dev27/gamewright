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

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（sha: 9e1e50f3311a）。第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

G-003でダッシュの再使用可否を表示（D-028）。プレイヤー表示に`dash: ready`/`recharging N s`、使用時・拒否時のメッセージ、`dash ready`通知がある（再充電0.85 s、被弾後も再充電表示、先行入力は保存しない）。Build報告で167 tests OK。QAは30/60 FPSで不合格なし、Playは部屋1・3で表示の一致を確認。未検証：旧ビルド比較（DR8, DR9 a/c）、ダッシュ無敵の実観測。30 FPSでは復帰が約0.05 s遅れる（許容内）。

実行（repo/で）：試験`python3 -m unittest discover -s tests`、プレイ`python3 play.py --view player {script}`、状態表示`--view trace`、bot`python3 bots.py {script}`。

既知の問題：部屋3は3体のスピッターが同期して狙い、狙い線が重なり読み取りにくい（Play所見、未対応）。G-002はD-027で未達・検証未完了のまま打切り（実装は保持）。ボス再測定・独立Play・Reviewは未実施。通常ラン勝利は約87〜104秒で、15〜20分Visionとの整合は未評価。

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
