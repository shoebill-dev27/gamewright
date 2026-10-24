---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
