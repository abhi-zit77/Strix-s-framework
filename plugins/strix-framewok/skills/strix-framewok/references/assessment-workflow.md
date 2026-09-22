# Assessment workflow

## Modes and ordering

| Mode | Work | Completion boundary |
| --- | --- | --- |
| Quick | Supplied changes and high-value auth, access, injection, outbound fetch, secrets paths | Record skipped applicable families; no full-app claim |
| Standard (default) | Map supplied assets and critical workflows; systematically test applicable families | Every planned surface/risk has evidence or a gap |
| Deep | Expand enumeration, identities, state transitions, sibling paths, and justified chains inside scope | Account for expanded matrix; depth is not unlimited traffic or time |
| Diff overlay | Establish merge base; inspect changed controls and their callers/sinks | Report introduced or materially worsened issues; separate pre-existing observations |

Do not impose an arbitrary timer if the user supplied none. Prioritize risk and
continue feasible work until planned coverage is reconciled, the user stops, or
the host budget prevents further work. Mark budget-limited assessments partial.

For source targets, derive the first threat model from code before dynamic tests.
For URL-only targets, perform benign reconnaissance first and mark inferred model
elements. Correct the shared model when observations contradict it.

## Threat model and source map

Record assets, entrypoints, attacker positions, identities, tenant boundaries,
trusted/untrusted inputs, privileged services, sensitive data, business invariants,
and deployment uncertainty. Distinguish intended privileged operations from bypasses.
Map source entrypoint → transforms → controls → sink, including all reachable
branches. A library name is not proof that its safe API/configuration is used.

Source triage aims for Semgrep, one AST structural pass, secrets inspection, and
dependency/misconfiguration inspection. Run available passes; record precise gaps
for absent tools. Never install a scanner merely to satisfy a count when equivalent
evidence for the scoped question exists. State differences in coverage honestly.

## Build the executable worklist

Read each selected playbook's techniques and validation guidance. Expand concrete
techniques into rows; an entire playbook is not one executed test. Use these fields:

`test_id, surface, risk_area, technique, prerequisites, invariant, baseline,
probe, expected_secure_result, evidence_refs, outcome, reason, history`.

Test roles and tenants independently, including read/write/delete/list/export and
background/job paths where applicable. Use separate synthetic records and stable
identities. API contracts provide a starting inventory, not authoritative live
coverage or permissions. Mark unresolved references/variables and inaccessible roles.

## Execution loop

Select the highest-value feasible row, run the baseline, change one relevant input
or identity, observe the invariant, test counterevidence, and persist the result.
Escalate testing depth only when the result justifies it and the effect remains in
scope. Repeat ambiguous results with controlled baselines; do not brute force an
unreachable environment. Once impact is proven, stop data access at minimal proof.

When chaining, connect only proven steps with compatible identities and state.
Record each unmet chain precondition. A separate runtime or different tenant/session
does not automatically compose with a source-only finding.

## Roles and handoffs

Discovery produces hypotheses, source paths, and proposed tests. Validation checks
those claims and counterevidence. Reporting reconciles distinct instances and
evidence. In fix mode, the person/agent with fresh understanding derives the patch
and records its verification; avoid redundant rediscovery by another fixer.

Delegated tasks specify scope, selected references, identity, rate/side-effect
limits, evidence directory, task ownership, and expected handoff. Specialists must
not overwrite another agent's source edits or ledger entries. One coordinator
merges their artifacts; equivalent sequential passes are valid without subagents.

## Fix workflow

Preserve the original failure, name the invariant, inspect native helpers, and fix
the controlling boundary. Re-run the original adverse case and a different input
class; exercise legitimate behavior and add a regression that fails without the
security change. Run the repo's applicable lint, type, security, focused and owning
package tests. Distinguish existing unrelated failures from introduced failures.
Do not commit, publish, deploy, or mark verified a change with an unresolved required
gate. If a public-API/product decision blocks a correct fix, present the concrete
decision and continue independent findings.

## Deliverables

The run contains scope/capabilities, threat model, source/endpoint inventory,
coverage ledger, finding artifacts, redacted evidence, and final report. Never
include tokens, private customer data, or live secrets in reusable/public examples.
Final status separates execution completion from coverage and from fix verification.
