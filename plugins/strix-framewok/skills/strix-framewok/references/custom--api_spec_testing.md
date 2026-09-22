> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/custom/api_spec_testing.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/custom/api_spec_testing.md).
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

# API Spec Testing

When a target is an API specification (OpenAPI 3.x, Swagger 2.0, or a Postman
collection), the root task lists it under **API Specifications** with the path
to the spec file in the workspace and the authorized base URL(s). Read the spec
file first and build your own endpoint inventory from it — every operation with
its method, path, parameters, request-body schema (resolve `$ref`/`allOf`), and
auth scheme. Do not rediscover the surface by crawling. Walk the inventory
operation-by-operation and prove findings against the live base URL(s), which
must first be matched to user-authorized scope.

## Methodology

**1. Baseline the contract.** For each endpoint, send a well-formed request that
matches the declared schema and record the normal response (status, shape,
auth requirement). This baseline is what every abuse case is compared against.

**2. Enumerate coverage.** Track every `METHOD path` in the inventory and mark it
tested. Undocumented-but-implied siblings are worth probing too (e.g. if
`GET /users/{id}` exists, try `PUT`/`DELETE`/`PATCH` on the same path even when
the spec omits them — specs routinely under-document write operations).

**3. Prioritize by risk.** Object-scoped reads/writes, exports, admin/staff
operations, and anything touching billing, auth, or PII first.

## What to test per endpoint

Test the full range of API weaknesses against each operation, driven by what the
contract reveals — do not treat the following as an exhaustive checklist. The
highest-yield classes on APIs are **authorization** flaws, since the spec hands
you the object identifiers and privilege boundaries to abuse: examples include
BOLA/IDOR (swap `{id}`/`accountId`/`tenantId` across two accounts), BFLA
(privileged operations with a lower-privilege token), and missing/broken auth
(replay with the token stripped or expired against endpoints whose declared auth
says one is required). Beyond authorization, use the declared parameters and
body schema as a launch point for mass assignment and excessive data exposure,
injection and type-confusion on every parameter, and multi-step business-logic
and rate-limit abuse — and follow the contract wherever it suggests something
else worth probing.

## Validation

A finding is only real once reproduced against the live base URL with a
concrete request/response pair. Capture the exact HTTP request (method, path,
headers, body) and the response proving impact (another account's data, a
privileged action succeeding, an injected payload executing). Prefer two-account
diffs for authorization findings: same request, different token, unauthorized
success.

## Tips

- The base URLs in a spec are candidates; send traffic only to origins explicitly within user-authorized scope.
- Path templates use `{param}`; substitute real values from your baseline.
- For Postman collections, saved example values and environment variables are
  strong hints for valid inputs — use them to get past validation quickly.
- Keep a running coverage table so no operation in the inventory is skipped.
