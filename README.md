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
- `graph/starting-flow.yaml`: the seeds of the first end-to-end slice.
- `data-model/<module>.yaml`: entities and enums, one file per module.
- `docs/user-stories/`: the MVP user stories, one file per persona, generated from the graph. Never edited by hand.
- `tools/`: validation, lookup, listing, and the canvas and user stories builds.

## Use

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/validate.py                      # every check; CI runs this
.venv/bin/python tools/validate.py --suite data-model   # one suite
.venv/bin/python tools/get_requirement.py REQ-TIME-0005 # a requirement with everything it needs
.venv/bin/python tools/list_requirements.py --ready     # what can be built next
.venv/bin/python tools/list_requirements.py --blocking  # what each blocking decision stops
.venv/bin/python tools/list_decisions.py --markdown     # open questions, grouped by who answers
.venv/bin/python tools/build_canvas.py                  # write canvas/ (git ignores it)
.venv/bin/python tools/build_user_stories.py            # rewrite docs/user-stories/ after any graph change; CI checks it
.venv/bin/python tools/set_starting_flow.py --add REQ-UNIT-WEB-0007   # change the flow's seeds
.venv/bin/python tools/next_requirement_id.py TIME      # the next unused id for a module
.venv/bin/python tools/check_approvals_kept.py --base origin/main   # CI runs this on pull requests
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
requirement_actors: [SYSTEM, UNIT_USER]    # INSTAWORK_ADMIN | PROGRAM_USER | UNIT_USER | AGENCY_USER | WORKER (P3) | SYSTEM
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
requirement_starting_flow: true            # written by tools/set_starting_flow.py from graph/starting-flow.yaml
requirement_review: {status: draft, by: null, at: null, notes: null}
requirement_delivery: {status: not_started, pull_requests: []}
```

### Citations

A citation is `KEY detail`. Keys and their precedence, highest first:

| Rank | Keys | Detail required |
| --- | --- | --- |
| 1 | SHEET, START | SHEET: a feature id (`TS-7`), a capability id (`4.3`), or a tab |
| 2 | FEEDBACK, SESSIONS, SLACK | FEEDBACK: the comment; SESSIONS: the session name |
| 3 | PRD | the section, such as `§2 Shifts` |
| 4 | OPS, FAQ | FAQ: the question; OPS optional |
| 5 | DEMO | the file or model |

When sources disagree the source with the smaller rank number wins (rank 1 is highest) and the
disagreement is logged in `graph/conflicts.yaml`. `GRAPH <reason>` marks a rule the graph itself supplies; such a rule
should also cite the decision that records the assumption. A rule no source states needs a
decision.

### Data model

Tables follow the Instawork Django model conventions (D-262) on MySQL 8 with InnoDB, the database
Instawork runs (D-263):

- Every table has an integer primary key `id`, assigned in sequence by the database and never
  reused, plus `created_at` and `updated_at`. They are not listed in `data-model/`; the validator
  rejects them there, and the canvas and `get_requirement.py` show them on every entity.
- Types: `text` (up to 255 characters), `longtext` (free text with no limit), `int`, `decimal`,
  `money`, `date`, `time`, `timestamp`, `bool`, `json`, `ref:Entity`, `enum:Name`, and
  `list:<type>`. Fields are required unless `nullable: true`. An empty `text` is stored as an empty
  string, not null.
- A `ref:Entity` field is an integer column holding that entity's `id`, named `<name>_id`, with no
  database foreign-key constraint (Instawork's `db_constraint=False`), so the application keeps
  references whole. Deleting a record deletes, in the same save, the rows that exist only for it,
  such as a Request template's lines or a Tip Pool's shares. A record anything else points at is
  deactivated or ended instead of deleted.
- A record linked to many others gets a join entity with one row per pair, such as `WorkerPosition`.
  A `list:` holds enum values only, never references, and is stored as a JSON array of their text.
- A field that may point at a record of any entity is an `int` `<name>_id` beside a `text`
  `<name>_type` holding the entity's name, such as `AuditEvent.record_type` and `record_id`. A
  `text` field ending in `_id` holds an outside system's id.
- A `bool` field starts with `is_` or `has_`.
- `unique` lists named unique constraints. None of them is a primary key: a Position is found by
  its `id`, and its unique `name` only stops two rows sharing one name.
- An enum is stored as the text of its value, such as `APPROVED`.
- Money is USD to the cent, stored as a decimal with two places. Hours are stored as whole minutes.
  An amount is rate × minutes ÷ 60, rounded as D-41 says.
- A `timestamp` is an instant. A `date` or `time` at a Unit is in that Unit's `timezone`.
- A requirement writes only its own module's entities. To change another module's records it
  depends on the requirement that owns them. A user-interface requirement writes nothing directly.
- A requirement that reads another module's entity depends, directly or not, on a requirement
  that writes it.
- Every status enum lists its transitions and the requirement that makes each one. That
  requirement writes the status field, and every value can be reached.
- `SettingKey`, `NotificationType`, and `UploadType` take their values from `graph/catalogs/`.
- In a `unique` key, an empty value counts as a value: two rows that match, including where both
  are empty, conflict. MySQL cannot enforce that for an empty reference, because a unique index never
  matches two NULLs, so the requirement that writes the entity checks those rows itself under the
  simultaneous-requests convention. The canvas marks each such key.
- No table or field is named with a MySQL reserved word, so analysts' queries never need quoting.
  `key` is allowed, as Instawork already uses it.
- The tables for every entity of a phase are created from `data-model/` before that phase's first
  requirement is built. A requirement adds behavior, not tables, so a `ref:` never waits for another
  requirement.

## Conventions every requirement assumes

These hold everywhere unless a rule says otherwise, so rules do not repeat them.

- **Saving together.** One user action, file, or job run is one transaction: its record changes,
  their Audit Trail entries, and the Notifications it queues save together or not at all.
  Notifications are delivered after the save.
- **Simultaneous requests.** A stated limit, such as a headcount or one active record, holds when two
  requests arrive at once: the second is refused as if it came later. A save based on a record that
  changed since it was read is refused, and the screen reloads the record.
- **Refusals.** Every refusal names the rule that refused it, such as `REQ-WORKFORCE-0003.R2`, so
  screens and tests can tell refusals apart.
- **Reactions.** When requirement B changes its records because requirement A changed its own, such
  as removing Workers when a Shift is cancelled, B owns the rule and depends on A. A rule of A names
  B. A publishes a named event when the change is made, B handles it in the same transaction, and A
  never calls B's code. The validator fails when a rule names a requirement with no dependency path
  either way.
- **Timed work.** A rule that acts when a time passes, or each day, runs as a job of
  `REQ-JOBS-0001`, whose rules say how late it may run, that it runs once, and in which timezone.
  Refusing an action after a time is checked when the action is made; a job only changes stored
  state that the time makes stale.
- **Acting role.** A User signs in to one role and context (`REQ-SHELL-0002`), and every request
  carries it. `REQ-ORG-0009` checks that the User holds an unrevoked grant for that role and context.
  Rules that say "the acting role" read it from the request.
- **Names.** A name in a file or a typed request matches a stored name when the two are equal after
  trimming, collapsing inner spaces, and ignoring case, among the records the sender may see. No match
  or several matches is a problem on the row. No match offers the three closest names, with the
  closest as the suggested fix when one is closest alone, and several matches offers every matching
  record, for the sender to pick (`REQ-AGENT-0002.R19`, `R24`; D-225).
- **Emails and phones.** Emails are stored trimmed and in lower case. Phones are US numbers (D-144),
  stored as `+1` followed by 10 digits; `REQ-IDENTITY-0001.R3` says which typed forms are accepted.
- **Screens.** A screen that opens another screen names it by requirement id. A screen changes
  records only through the product requirements it depends on. What a screen built earlier shows of a
  feature built later, such as a link, a tab, a field, or an upload button, is added by the later
  requirement (D-107).
- **Stack and providers.** The graph does not choose the stack or the email, SMS, voice, language
  model, OCR, or verification providers; Instawork engineering does. Each provider sits behind the
  one platform requirement that uses it, so the choice changes one requirement.

### Decisions

Open questions live in `graph/decisions.yaml`, each with the assumption the graph builds on
until Compass answers. A decision asks one question, and its assumption states the choice in one or
two sentences; the rules that cite it carry the detail. Each decision names who must answer it with
`answer_from`:
`COMPASS_OPERATIONS`, `COMPASS_HR_LEGAL_PAYROLL`, `COMPASS_FINANCE`, `INSTAWORK_PRODUCT`, or
`INSTAWORK_ENGINEERING`. A `blocking: true` decision stops approval of every requirement that
cites it or depends on one that does. When a decision is answered, set `status: answered`
and `answer`, then update the requirements that cite it.

## Workflow

1. Change graph files on a branch and run `tools/validate.py` until it passes.
2. Open a pull request. A reviewer in `graph/reviewers.yaml` sets `requirement_review` to
   `approved`, with `by` and `at`. A requirement is approved only after everything it depends on.
   An edit to an approved requirement keeps the approval only when a reviewer records it with a
   new `by` and `at`; CI fails a pull request that drops or downgrades an approval.
3. The factory builds requirements that `tools/list_requirements.py --ready` lists: approved,
   not delivered, with every dependency delivered. Start with `--starting-flow`.
4. When the code merges, set `requirement_delivery` to `delivered` with the pull request URLs.

Ids are never reused or renumbered; take new ones from `tools/next_requirement_id.py`. To remove
a requirement, delete it and add it to `graph/retired.yaml`; the validator fails on an id that
git history has and neither the graph nor the retired list does. Rule ids are append-only within
a requirement.

## Sources

Every source is listed in `graph/sources.yaml`. The sheet, the Confluence Start here page,
Kenneth's demo feedback, and the session notes override the PRD; the PRD overrides the Ops
page, the FAQ, and the deck; the demo repository fills small gaps only.
