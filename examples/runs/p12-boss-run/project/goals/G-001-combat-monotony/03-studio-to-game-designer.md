---
kind: handoff
goal: G-001
seq: 3
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 03: studio → game-designer — Diagnose why combat feels monotonous

## Task

Diagnose, in design terms, the causes of the monotony the playtester observed, and offer solution options (with trade-offs) that stay within the vision and D-001. Do not write the spec yet.

## Context

Goal G-001: the Owner said "戦闘が単調なので改善したい" (combat is monotonous; we want to improve it). It is an experience problem, not a defect report. Step 1 (Observe) is done: a playtester played the build and wrote the report in `02-playtester-to-studio.md`. The next planned steps after your diagnosis are Decide (only if there is a real choice of direction or scope, or a D-001/pillar impact) and Design.

## Findings

Summary of the playtester's observations (full report in the previous handoff):

- Method limits: played via reaction-rule input scripts, not live; one attempt per room; rooms 1, 2, 3 and a practice room (one spitter). Rooms 4–5 and hand-timed play were not covered. The practice-room script was flawed (spitter out of the script's trigger range), so that session is not a fair fight. The playtester lost all four sessions (all 3 hearts), runs lasting 5–15 s.
- Grubs (rooms 1–2): a repeated loop of walk toward, swipe twice, trade a hit. Nearly every grub landed a hit. No dodge or spacing opportunity and no readable cue for when a grub hits. Rooms 1 and 2 felt identical apart from enemy count. Idle walking toward the last enemy (~1.3 s). Impact: high.
- Spitters (room 3): the only session with tension and decisions. Volleys from several spitters at once (every 2 s each) fill the screen with shots. The playtester dashed ~9 times in 15 s, killed one spitter early, then never reached the others (corners at the far edge) and only dodged. Dodging was engaging for ~8 s, then felt like an endless chore with no way to progress. Hits sometimes came right after a dash; the dash did not feel reliably safe and safe paths were unreadable. Impact: high / medium–high.
- Only swipe and dash were used, the same way each time. No healing or recovery seen (medium).
- Positives: shots (`*`) and hit events were visually clear; room 3 gave a taste of the wanted dodging and spacing; short runs suit the profile.
- Playtester's open questions: is grub combat still repetitive when played by hand with deliberate timing? what do rooms 4–5 add? does the dash give any protection?

## Decisions already made

- D-001: combat uses one attack button plus dash; no new input buttons without Owner approval.

## Constraints

- Vision pillars: one-button combat, short runs (15–20 min), readable threats.
- Desktop, keyboard and gamepad; must play correctly at 30 and 60 FPS; small team, prefer reuse of existing systems.
- Out of scope: new buttons, changing run length, unrelated new biomes/content, changing the core concept. If every viable option would break D-001 or a pillar, say so; the Studio will escalate.
- Treat the playtester's report as observations of experience, not as authority on internals. It comes from scripted play, so the playtester's own losses may partly reflect script quality rather than build balance.

## Open questions

- Which causes are supported by `design/combat.md` (enemy behavior, damage and invulnerability rules, dash properties) versus only suggested by a thin sample? Answer the playtester's dash-invulnerability question from the design.
- You may use the project's `run_bots`, `run_trace` and `run_tests` commands (see `project.md` front matter) to check whether the observations hold more generally (e.g., clear times, hearts lost, actions used per room). Rooms 4–5 have not been observed by anyone; say whether further observation (e.g., by `playtester`) is needed before a decision, and why.
- Is there a real choice of direction or scope among your options (needs Decide), or one clearly best within your authority?

## Expected output

A diagnosis with causes (separating evidence-backed from hypothesized) and solution options with trade-offs, effort (reuse of existing systems) and impact on the pillars and D-001, plus your recommendation. Put it in Findings of the outgoing Handoff and address the result to `studio` so the Studio can route it (to Decide if a real choice or escalation trigger exists, otherwise to Design).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#current-state, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-studio.md
