# iris-requirements-graph

The requirements graph for Iris, Instawork's vendor management system for Compass. It is the
base a software factory builds from: each requirement is small enough to build and test on its
own, says what it depends on, names the records it reads and writes, and cites where every
rule came from.

## Layout

- `graph/layers.yaml`: the three layers and their modules.
- `graph/requirements/<layer>/<module>/REQ-*.req.yaml`: one requirement per file.
- `graph/scope/`: the Compass sheet's 31 capabilities and 112 features, verbatim.
- `graph/catalogs/`: settings, notifications, and upload types. Each entry names its owner requirement.
- `graph/sources.yaml`, `decisions.yaml`, `conflicts.yaml`, `inputs.yaml`, `terms.yaml`: the evidence, open questions, overrides, asks, and words.
- `graph/reviewers.yaml` and `graph/retired.yaml`: who may approve, and ids never to reuse.
- `data-model/<module>.yaml`: entities and enums, one file per module.
- `tools/`: validation, lookup, listing, and the canvas build.

## Use

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/validate.py                      # every check; CI runs this
.venv/bin/python tools/validate.py --suite data-model   # one suite
.venv/bin/python tools/get_requirement.py REQ-TIME-0005 # a requirement with everything it needs
.venv/bin/python tools/list_requirements.py --ready     # what can be built next
.venv/bin/python tools/build_canvas.py                  # regenerate the canvas
.venv/bin/python -m unittest discover tools/tests
```

## Layers and edges

| Layer | Holds | May depend on |
| --- | --- | --- |
| user-interface | Screens for one persona | user-interface, product, platform |
| product | Business behavior and rules | product, platform |
| platform | Shared services: sign-in, agent runtime, file intake, messaging, audit, integrations | platform |

`DEPENDS_ON` means the target must be built first: this requirement calls it, reads or writes
records it owns, or cannot be tested without it. Edges never point up a layer or to a later
phase, and the graph has no cycles.

## Requirement file

```yaml
requirement_id: REQ-TIME-0005              # REQ-<MODULE>-<4 digits>; never reused
requirement_target_layer: product
requirement_target_module: TIME
requirement_phase: MVP                     # MVP | P2 | P3
requirement_title: Auto-approve within tolerance and surface exceptions   # <= 80 characters, no period
requirement_statement: >-                  # 1 to 3 sentences, each <= 30 words
  ...
requirement_actors: [SYSTEM, UNIT_USER]    # INSTAWORK_ADMIN | PROGRAM_USER | UNIT_USER | AGENCY_USER | SYSTEM
requirement_rules:                         # each one testable sentence, <= 35 words
- rule_id: R1                              # stable; cite as REQ-TIME-0005.R1; new rules append
  rule_statement: ...
  rule_sources: [SHEET TS-7]               # at least one source or one decision per rule
  rule_decisions: [D-22]
requirement_sources: [SHEET TS-7]          # sources for the statement as a whole
requirement_decisions: []
requirement_features: [TS-7]               # sheet features this requirement delivers
edges:
- {edge_type: DEPENDS_ON, requirement_id: REQ-TIME-0002}
data_model:
  status: covered                          # covered | not_applicable | pending
  reads: [Shift.starts_at, Timesheet.*]
  writes: [Timesheet.status, Timesheet.exception_reasons]
  detail: null                             # required for not_applicable and pending
requirement_starting_flow: true            # part of the first end-to-end slice
requirement_review: {status: draft, by: null, at: null, notes: null}
requirement_delivery: {status: not_started, pull_requests: []}
```

### Citations

A citation is `KEY detail`. Keys and their precedence, highest first:

| Rank | Keys | Detail required |
| --- | --- | --- |
| 1 | SHEET, START | SHEET: a feature id (`TS-7`), a capability id (`4.3`), or a tab |
| 2 | FEEDBACK, SESSIONS, SLACK | SESSIONS: the session name |
| 3 | PRD | the section, such as `§2 Shifts` |
| 4 | OPS, FAQ | optional |
| 5 | DEMO | the file or model |

When sources disagree the higher rank wins and the disagreement is logged in
`graph/conflicts.yaml`. `GRAPH <reason>` marks a rule the graph itself supplies; such a rule
should also cite the decision that records the assumption. A rule no source states needs a
decision.

### Data model

- Types: `uuid`, `text`, `int`, `decimal`, `money`, `date`, `time`, `timestamp`, `bool`,
  `json`, `ref:Entity`, `enum:Name`, and `list:<type>`. Fields are required unless `nullable: true`.
- Every entity also has `id`, `created_at`, and `updated_at`. Do not list them.
- Money is USD to the cent. Hours are stored as whole minutes. An amount is rate × minutes ÷ 60,
  rounded half up to the cent, per Timesheet and per hour class.
- A `timestamp` is an instant. A `date` or `time` at a Unit is in that Unit's `timezone`.
- A requirement writes only its own module's entities. To change another module's records it
  depends on the requirement that owns them. A user-interface requirement writes nothing directly.
- A requirement that reads another module's entity depends, directly or not, on a requirement
  that writes it.
- Every status enum lists its transitions and the requirement that makes each one. That
  requirement writes the status field, and every value can be reached.
- `SettingKey`, `NotificationType`, and `UploadType` take their values from `graph/catalogs/`.

### Decisions

Open questions live in `graph/decisions.yaml`, each with the assumption the graph builds on
until Compass answers. A `blocking: true` decision stops approval of every requirement that
cites it or depends on one that does. When a decision is answered, set `status: answered`
and `answer`, then update the requirements that cite it.

## Workflow

1. Change graph files on a branch and run `tools/validate.py` until it passes.
2. Open a pull request. A reviewer in `graph/reviewers.yaml` sets `requirement_review` to
   `approved`, with `by` and `at`. A requirement is approved only after everything it depends on.
3. The factory builds requirements that `tools/list_requirements.py --ready` lists: approved,
   not delivered, with every dependency delivered. Start with `--starting-flow`.
4. When the code merges, set `requirement_delivery` to `delivered` with the pull request URLs.

Ids are never reused or renumbered. To remove a requirement, delete it and add it to
`graph/retired.yaml`. Rule ids are append-only within a requirement.

## Sources

Every source is listed in `graph/sources.yaml`. The sheet, the Confluence Start here page,
Kenneth's demo feedback, and the session notes override the PRD; the PRD overrides the Ops
page, the FAQ, and the deck; the demo repository fills small gaps only.
