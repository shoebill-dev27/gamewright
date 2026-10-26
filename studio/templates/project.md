---
kind: project
id: <project-id>
name: <display name>
repository: <path or URL of the game repository>
owner_language: <language for Owner-facing text, e.g. en, ja>
player_visible: <optional: files a Playtester may load, e.g. builds or captures; player-facing files that change with the build belong inside the build directory>
build: <optional: the directory holding a build that commands can run>
run_tests: <optional, with build: command that runs the build's tests>
run_play: <optional, with build: command that plays a script ({script}) and shows the player view>
run_trace: <optional, with build: command that plays a script and shows internal state>
page: <optional, with build: a page of the build that a browser opens; Steps may then take screenshots of it (`shot`)>
---
# Project: <display name>

## Vision

<What the game is and why it exists. Pillars: the few things that must stay true.>

## Player profile

<Who plays it, what they enjoy, what they are not comfortable with.>

## Current state

<What exists now: build, content, known problems, how to run it.>

## Constraints

<Platforms, performance targets, budgets, things that need Owner approval to change.>

## Art direction

<Style, palette, readability rules. Omit until the project has one.>

## Design index

<Links to design documents under design/, one line each.>
