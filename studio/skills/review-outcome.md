---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
