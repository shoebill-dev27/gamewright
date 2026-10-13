# Isolated Execution

How a runtime executes the operations in `orchestration.md` so that the separations in the Role
contracts hold mechanically, not only by instruction. Manual execution stays valid; this file
defines what an isolated runtime must guarantee when one is used.

## Guarantees

1. **One operation, one fresh executor.** Every Intake, Step, Route and Resume runs in a new
   executor with no prior conversation. The executor is discarded when the operation ends, and its
   session cannot be resumed.
2. **The packet is the whole input.** The executor receives exactly one packet. It has no tools,
   no file access, and no ambient instructions or memory. Where a runtime cannot remove a tool,
   every tool use is recorded and an operation that used one is rejected.
3. **Only artifacts carry over.** The executor's output is parsed for file blocks, and only files
   on the operation's write list are written. Everything else is discarded and never enters a
   later packet. Each operation sees earlier work only through artifacts.
4. **Steps do not route; Route does not do the work.** A Step writes only its one outgoing Handoff
   (or Escalation) and the project files its Role may write. Only Route and Resume write `goal.md`.
   The executor of a Step never chooses which Role runs next: its `to` is a proposal that a
   separate Route executor confirms or changes, using artifacts only. Only the runtime appends to
   the Goal log (`orchestration.md`); it is on no write list.
5. **Every operation leaves a record** (see Records).

## Packets

A packet is a short header (operation, goal, Role, write list) followed by input files, each as a
file block. Its manifest lists every input with a content hash.

| Operation | Inputs |
|---|---|
| Intake | executor instructions; `studio/README.md`, `orchestration.md`, `workflows/development-loop.md`; each Role's `#works-from` and `#independence` sections; templates `goal.md`, `handoff.md`; `project.md`; the project file list; Decision titles; the Owner request |
| Step | executor instructions; the incoming Handoff; every file in its Load list (only the named section for `file#section`); the templates the Role may write |
| Route | executor instructions; `orchestration.md`, `workflows/development-loop.md`, `studio/README.md`; each Role's `#works-from` and `#independence` sections; templates `handoff.md`, `escalation.md`, `goal.md`; `goal.md`; the last 5 entries of the Goal log; every artifact produced since the previous Studio operation on this Goal (all parallel Steps' results); `project.md`; the project file list; Decision titles |
| Resume | as Route, with the Escalation (the Owner's words appended verbatim) in place of the Step artifact, and template `decision.md` |

A Step's packet is derived from its Handoff alone: **the Load list is the allowlist.** The project
file list gives names only, never contents.

**Context request (Route only, once).** Instead of routing, a Route may answer with a single
`@need` block listing up to 8 project or Studio files, one per line. The runtime adds exactly those
files to the packet and runs a new executor once more; a second request is rejected. The request
and the enlarged packet are recorded.

## Continuous execution

A runtime may repeat Steps and Routes without a person starting each one. It runs every open Step
(parallel Steps one after another), then one Route, and repeats until a stop condition holds:

| Stop | Meaning |
|---|---|
| Goal `done` or `abandoned` | The Owner reads the Outcome. |
| Goal `blocked-on-owner` | The Owner answers the Escalation; Resume, then continue. |
| Output rejected after its retry | A person looks at the record; nothing was written. |
| Runtime error | The executor could not run (e.g., a usage limit); continue later. |
| Operation budget reached | A person decides whether to continue. The budget is checked between cycles, so a cycle (its Steps and Route) is never cut in half. |
| No progress | A Role handed back `question` twice and would be opened again, or a Role would be opened a 4th time in one continuous run. A mechanical backstop for the loop limits in `orchestration.md`. |

Every stop is recorded with its reason, what the Owner should read, and how to continue. A
continuous run never decides anything a Route or Role would not decide one operation at a time.

## Independence policies

Role contracts declare machine-checkable policies in their frontmatter. The runtime enforces them
when it builds a Step packet and when it validates any Handoff addressed to that Role.

| Key | Meaning |
|---|---|
| `receives_from` | Allowed senders of the incoming Handoff |
| `load_only` | Every Load entry must match one of these patterns; `@player_visible` expands to the project's `player_visible` patterns |
| `load_forbid` | No Load entry may match these patterns |
| `strip_sections` | Sections removed from every Handoff before it enters the packet |
| `writes` | Project files the Role may create or change besides its outgoing artifact |

Values are comma-separated; patterns are paths relative to the project (or `studio/...`) with `*`
wildcards. Further checks on Handoffs to independent Roles:

- **To `playtester`:** the Goal's Owner request, Decision ids, and `## Sender assessment` must not
  appear.
- **To `qa` from `gameplay-engineer`:** the implementer's self-assessment (own test verdicts, root
  cause reasoning, confidence) belongs under `## Sender assessment`, which `qa` never receives.

A Project Context that lets Playtesters run a build declares the player-visible files in
`project.md` frontmatter: `player_visible: <patterns>`.

## Output protocol

Every file the executor creates or changes is written as one complete block:

```text
<<<FILE <path relative to the project>
<full file content>
>>>END
```

The runtime rejects blocks outside the write list, artifacts that fail the Studio's structural
rules, and Handoffs that break a recipient's policy. A rejected operation writes nothing and may be
re-run with a fresh executor.

## Records

Each operation keeps: the packet, its manifest, the raw output (for audit only — never an input to
another operation), and a record with the operation, goal, Role, runtime, model, session identity,
tools available to the executor, timing, files written with hashes, and validation results. Session
identities differ for every operation.

After an Intake, Route or Resume is written, the runtime appends that operation's entry to the
Goal log, named by its record. The first entry of a Goal that predates its log preserves the
*Route changes* text it had. Older entries reach a Route only through a context request for
`log.md`.

A written `goal.md` must stay small: *Route changes* at most 600 characters, *Unknowns* at most
3,000, each Stage and Status cell at most 80, and the file at most 20,000 bytes without its
Outcome.

## Dry-run simulation

When a project's build is simulated (`sim/`), the runtime runs a simulator after a Build step that
finished: a fresh executor that rewrites the build description from the implemented change, so
that Verify and Play observe the change rather than the implementer's intent. The simulator is a
test harness, not a Role, and its output is limited to `sim/`.

## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
