---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
