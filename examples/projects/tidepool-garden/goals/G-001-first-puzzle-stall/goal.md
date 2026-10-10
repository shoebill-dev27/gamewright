---
kind: goal
id: G-001
project: tidepool-garden
status: active
created: 2026-10-10
---
# G-001: Children stall at the first puzzle

## Owner request

> 最初のパズルで子どもが手を止めてしまう。直したい

## Interpretation

Success condition: when children in the target group (ages 7–10) play the first puzzle (level 1 in
build 0.2), they begin purposeful touch interaction with the puzzle on their own, without a long
pause and without an adult having to explain what to do. How long a pause counts as "a stall" is
not set here; Observe reports what actually happens and Design turns it into a player-observable
acceptance criterion.

Out of scope:

- Levels 2 and later. If the same problem shows up there, it becomes a proposed new Goal.
- Changing a vision pillar or Decision D-001 (no failure, no timers). Any fix must stay inside them.
- New art beyond the existing sprite sheet (project constraint).

## Unknowns

Entry questions (`studio/workflows/development-loop.md`) the Project Context cannot answer:

- **Observe** — Has the stall been observed first-hand? No: the Project Context holds only the
  Owner's report. It is an experience problem, not a reproducible defect, so the Role is
  `playtester` (not `qa`). Creates stage 1.
- **Diagnose** — Is the cause understood? No. Creates stage 2 (`game-designer`). `art-director` is
  not added now; it is added at Route if the observation points to something visual.
- **Design** — Is the intended behavior of the fixed first puzzle specified? No:
  `design/onboarding.md` specifies the current level 1 and its teaching intent, not a fix. Creates
  stage 3. If Diagnose finds an ordinary defect against the existing spec, Route drops this stage.
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4.
- **Verify** — Always after Build. Stage 5.
- **Play** — Is the Goal about how the game plays or feels? Yes. Stage 6, in a fresh context
  without the implementation history.
- **Review** — Is it an experience Goal? Yes. Stage 7 (`game-director`).
- **Next** — Always. Stage 8.

Skipped for now:

- **Decide** — Is there a real choice of direction, priority or scope? Not at this point. Choosing
  among fixes for player-facing behavior inside the approved direction is `game-designer`
  authority. Route adds Decide if Diagnose or Design produces options that change direction,
  priority or scope, and escalates if a trigger fires.
- **Plan** — Is the technical approach non-obvious, risky, cross-system or parallelizable? Not
  knowable until a fix is specified; a level 1 teaching change is expected to be local. Route
  re-asks this after Design and adds Plan if the answer is yes.

Flag for Diagnose (not a conclusion): `project.md` lists "No mechanic may depend on reading text"
as a constraint and says level 1 teaches with a text bubble, for players some of whom are early
readers.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | open | 02-playtester-to-game-designer.md |
| 2b | Diagnose | art-director | visual-review | open | 03-studio-to-art-director.md |
| 3 | Design | game-designer | write-design-spec | planned | — |
| 4 | Build | gameplay-engineer | implement-change | planned | — |
| 5 | Verify | qa | verify-change | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

- Intake check (Route step 4) on 01: the first draft told the Playtester the Owner's report and
  asked "where do players stall", which primes the observation. Rewritten with a neutral play focus
  (levels 1–3) and the Owner's report withheld. Load narrowed to `project.md#player-profile`.
- Route after step 1 (`02-playtester-to-game-designer.md`): the outcome fits the plan (two of three
  children stalled 20–35 s at the start of level 1; the report is observation only). No escalation
  trigger fires, and no `tentative` stage exists to confirm or drop. Added step 2b: `art-director`
  `visual-review` in parallel with step 2, as the Intake note reserved for this point. The report
  contains visual facts (tide pool in the same pastel tone as the sand; crab with a darker outline
  that bobs; two of three children touched the crab first), so the cause may be visual. Steps 2 and
  2b are independent (both read only the observation), so they run in parallel and Route waits for
  both before step 3. Step 2's handoff was completed at Route: the Owner's words, the success
  condition, the out-of-scope list and the text-constraint flag were added (the `game-designer` did
  not have them); `project.md#vision`, `#constraints`, `#player-profile`, `design/onboarding.md` and
  D-001 were put in its Load. Not added: a `qa` Observe step. The playtester reported the missing
  response to taps on the crab and the home as observed; whether that contradicts the design
  documents is for step 2 to say, and if it does, the return rules send that part to `qa`.
  Step 3 may need `art-director` for what the player sees; decide after step 2 and 2b.

## Next action

Run steps 2 and 2b (Step operation, in either order or in parallel): `game-designer` on
`02-playtester-to-game-designer.md` and `art-director` on `03-studio-to-art-director.md`. Then
Route, which waits for both. Phase 1: the Studio stops after every Route and states the next
action.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
