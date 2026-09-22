> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/coordination/root_agent.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/coordination/root_agent.md).
> Upstream commit `56e9ae982c2fdd00c7c0b9afc49af035470dd310`; Apache-2.0. See bundled LICENSE and NOTICE.

## Adaptation and execution contract

This reference is technical guidance for the selected test family, not a grant of
scope or a list of commands to run indiscriminately. Follow the skill's scope,
tool-adaptation, evidence, and fix-mode contracts. Historical example hosts, paths,
tool flags and framework/CVE versions must be checked against the actual target
and current primary documentation. Verify installed tool help before using a flag.
Use synthetic data, minimal proof, controlled callbacks and agreed effect limits.
Post-exploitation examples describe possible impact; do not collect real secrets,
establish persistence, claim resources, or expand scope to demonstrate it.

Every applicable technique below becomes a concrete coverage row: prerequisite,
security invariant, legitimate baseline, controlled probe, expected secure result,
counterevidence, captured evidence and outcome. Missing capabilities create a gap;
they do not turn a test into a pass. Tool names inherited from Strix refer to the
replacement operations in [tool adaptation](tool-adaptation.md), not available APIs.
Use [evidence rules](evidence-and-reporting.md) when an older section demands runtime
proof for everything: complete static traces and exact advisory matches are separate
reportable classes with their limitations. Audit is the default; changes require
fix intent. Preserve behavior and retest the boundary, not only one payload.

## Adapted technical playbook

# Assessment coordination

Use the workflow in assessment-workflow.md. The coordinator establishes scope,
capabilities, a shared threat model, an inventory and coverage matrix. Source-based
models precede active tests; URL-only models follow baseline reconnaissance.

Delegate only through the host's available, permitted agent tools and only when
independent work benefits. Give each specialist a bounded surface/risk, explicit
scope and identity, evidence directory and completion contract. Check overlap
before assigning. With no delegation, perform discovery, independent re-check and
reporting sequentially in the current agent; absence of subagents is not a blocker.

Keep a shared worklist and one coordinator-owned ledger. Specialists return evidence,
counterevidence, closure state, open proof gaps and source changes. They must not
overwrite peers' work. Correct threat-model assumptions as new evidence arrives.
Update existing coverage rows rather than creating conflicting resolutions.

Before completion, read all handoffs, resolve feasible follow-ups, account for every
planned technique, deduplicate without dropping distinct instances, and report
partial coverage honestly. Do not use Strix lifecycle functions or require three
agents per finding. In fix mode, derive and verify the patch while its context is
fresh; avoid a second agent re-deriving the same fix.
