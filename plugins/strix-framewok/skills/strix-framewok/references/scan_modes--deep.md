> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/scan_modes/deep.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/scan_modes/deep.md).
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

# Deep assessment depth

Expand the standard matrix to sibling code paths, alternate transports, identities, encodings, multi-step state transitions and justified chains. Keep complete source/runtime provenance and mark unexamined techniques. Broader enumeration and intrusive operations remain bounded by explicit scope and host limits.

Use the lifecycle and test-row contract in assessment-workflow.md and evidence
classes in evidence-and-reporting.md. Depth does not grant broader asset permissions,
authorize high load or bypass the default audit-only mode. Run through actual tools;
do not stop at a plan when execution is available. Report gaps precisely.

Diff scope can overlay this mode: resolve the actual merge base, follow changed
behavior through relevant callers and controls, and separate pre-existing findings.
Support native subagents when permitted or sequential specialist passes otherwise.
Finish after coverage reconciliation; a completed run may still have partial coverage.
