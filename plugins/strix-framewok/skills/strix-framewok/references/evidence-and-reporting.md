# Evidence and reporting contract

## Evidence classes

| Class | Minimum proof | Allowed claim |
| --- | --- | --- |
| runtime_confirmed | Reproducible adverse effect, legitimate baseline, identity/environment, and control comparison | Confirmed in the tested environment |
| static_trace | Attacker input, complete reachable source → control → sink → impact trace, exact locations | Source-supported finding; runtime unverified; confidence at most medium |
| dependency_advisory | Exact resolved package/version, manifest/lockfile, matching authoritative advisory and affected range | Known vulnerable dependency; application exploitation is a separate question |
| hypothesis | Suspicious pattern or incomplete reachability/impact | Work item only; never a confirmed finding |

Confidence and severity are different dimensions. Missing deployment evidence
reduces confidence; observed restrictive deployment may reduce severity. Assign
CVSS only with an explicit version and justified metrics using a real calculator.
Otherwise give qualitative severity. Verify current advisories and framework versions
before matching CVEs; do not assert historical playbook examples remain current.

## Candidate closure and coverage

A candidate closes as confirmed, ruled_out, or open_proof_gap. A coverage row is
more granular and has one of these outcomes:

- `reported`: linked finding with a qualifying evidence class.
- `ruled_out`: named effective control on this exact reachable path; explain timing
  and why it cannot be bypassed in the tested conditions.
- `no_issue_found`: the recorded test ran successfully and showed no issue; narrow
  result, not proof that the surface is universally safe.
- `not_applicable`: concrete reason the technique cannot apply to this surface.
- `needs_follow_up`: plausible candidate or attempted test with missing evidence.
- `untested`: applicable planned work that has not been executed.

Use one stable row per surface + risk area + technique + relevant identity context.
Update it with history when evidence changes. Distinct sibling paths remain separate
even if the same remediation might fix them. Deduplicate findings by root cause,
affected instances, boundary, and impact; preserve the location/instance list.

## Finding content

Use the bundled JSON template and write an accompanying human-readable finding.
Include ID, title, asset, affected instances/locations, attacker prerequisites,
invariant, evidence class, reproduction, baseline/adverse/control observations,
impact, counterevidence, confidence/rationale, severity/rationale, conditions that
would change severity, remediation, and verification results. Local HTTP evidence
IDs refer to real saved exchanges; proxy IDs are used only when a proxy returned
them. Preserve method, path, identity label, redacted headers/body, response, and
timestamp. Never invent request IDs or cite a screenshot as a server-side PoC.

Dependency findings also record advisory URL/date, ecosystem, package, resolved
version, vulnerable/fixed range, direct/transitive introduction path, production/dev
context, database freshness, and reachability evidence. Use `unknown` when the
call path cannot be established. Advisory severity and contextual severity remain
separate; an import is not proof of an exploitable call path.

## Fix verification

Record each gate as passed, failed, blocked, or not_applicable, with command/result
and evidence. Required gates: applicability, security closure, alternate bypass,
preserved behavior, regression, and repository checks. Add `method: executed` or
`method: reasoned`; a reasoned source trace does not mean a runtime test passed.
Only say runtime verified when its actual required runtime gates passed.

## Partial, interrupted, and clean outcomes

`run.status` describes lifecycle: in_progress, completed, interrupted, or blocked.
`run.coverage` describes complete or partial coverage of the explicitly selected
matrix. Completed plus partial is valid and must appear prominently in the report.
The word clean may only describe executed tests with no confirmed finding, alongside
their coverage limit. Unavailable tools, unreachable services, lack of credentials,
empty diffs, timeouts, and no output never prove safety.

Use the final report template. Report root cause, evidence, fix applied or proposed,
how to retest, and prevention for each issue. Keep customer reports separate from
the reusable skill repository. No auto-upload, notifications, or paid fallback.
