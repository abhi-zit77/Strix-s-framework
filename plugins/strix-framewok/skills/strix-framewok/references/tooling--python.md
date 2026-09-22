> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/python.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/python.md).
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

# Python through the available host terminal

Check the available interpreter/version and the target manifest first. Use a
task-local virtual environment for additional dependencies. Standard-library HTTP,
JSON, SQLite and filesystem tools are often sufficient for small controlled proofs.
Do not assume requests, httpx, PyJWT, caido_api, uv, or a Strix sandbox is installed.

Write a task-unique script in the private run workspace, inspect it, and execute it
through the host shell with explicit paths and a timeout. Keep target credentials
out of the script and command history. Prefer structured arguments over interpolated
shell commands. Distinguish Python HTTPX from the ProjectDiscovery httpx binary.

Use an existing proxy's actual documented SDK only if it is available and configured.
Otherwise capture direct request/response pairs; do not claim interception or invent
proxy request IDs. Redact sensitive evidence, record errors and exit status, and
do not silently treat empty output as a negative finding. Run controlled baseline,
adverse and negative-control cases and preserve their environment identities.
