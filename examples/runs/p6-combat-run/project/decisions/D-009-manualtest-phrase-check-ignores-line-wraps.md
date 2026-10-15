---
kind: decision
id: D-009
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-009: The `ManualTest` phrase check ignores line wraps; `manual.md` stays unchanged

## Decision

`test_manual_lists_glyphs_and_lines` failed on `run over` only because `manual.md` wraps the line between `run` and `over`. The manual's content and the build's wording (`run over — rooms cleared: N`, `press attack to start again`) agree. The fix is in the test: the phrase check runs on whitespace-collapsed text (`" ".join(text.split())`). The glyph check, the phrase list and the other test stay as they are.

Limits:
- `manual.md` is not edited (D-005, D-007).
- No change to the build, D-001, D-003, D-006 or `design/combat.md`.
- AC-15 passes only when the full suite gives 40/40 with the unchanged `manual.md` beside `repo/` (D-008).

## Rationale

The manual is correct and the test was stricter than the spec's intent. Collapsing whitespace makes the test robust to Markdown hard wraps and avoids an Owner round-trip for a formatting detail.

## Alternatives considered

- Owner joins the two lines in `manual.md`: fixes this run, but breaks again on any rewrap.
- Change the build text: unnecessary; it already matches the manual.

## Revisit when

- The rerun shows another phrase missing or a different failure.
- A phrase the player needs is really absent from the manual.
