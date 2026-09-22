# What is transferred from Strix

Analyzed source: [usestrix/strix at 56e9ae9](https://github.com/usestrix/strix/tree/56e9ae982c2fdd00c7c0b9afc49af035470dd310),
observed 2026-09-22. This is a source-backed architecture and targeted quality
review, not a claim of running the upstream penetration-testing engine or all its
tests. The inventory covers all 75 internal Markdown playbooks and nine consumer
skills. Detailed manual inspection focused on orchestration, tools, evidence,
coverage, source review, fixing, packaging and representative vulnerability stacks.

## The reusable advantage

The strongest transferable design is the combination of task-specific knowledge
with an evidence lifecycle. The public source supports a concrete workflow:
map the system, model attacker authority, locate high-risk paths, formulate
hypotheses, test them, look for counterevidence, maintain coverage, and verify fixes.
It is not just a list of vulnerability names or a single prompt.

| Mechanism | Source evidence | Transfer |
| --- | --- | --- |
| Role and risk specialization | [System prompt](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/agents/prompts/system_prompt.jinja), coordination playbooks | Native host subagents where permitted; equivalent sequential passes otherwise |
| Layered skill loading | [Prompt renderer](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/agents/prompt.py), [skill loader](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/__init__.py) | Concise entrypoint, always-relevant evidence rules and on-demand technical references |
| Source-aware discovery | Analysis, source-aware SAST and white-box coordination playbooks | Entry/control/sink mapping, sibling instances, AST/scanner triage, source-to-runtime correlation |
| Shared threat model | [Threat-model tools](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/tools/threat_model/tools.py) | Per-run model with attributed corrections; no stale assumptions silently inherited |
| Counterevidence and severity | Analysis playbooks and [reporting validation](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/tools/reporting/tool.py) | Explicit strongest contrary evidence, confidence and severity-change conditions |
| Negative-space coverage | [Coverage tools](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/tools/coverage/tools.py), [completion tool](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/tools/finish/tool.py) | Coverage ledger records reported, cleared, not applicable, unresolved and untested cases |
| Evidence-backed reporting | Reporting tools verify real proxy exchange IDs and structured fields | Actual host HTTP artifacts or real proxy IDs, never invented tool evidence |
| Dependency finding class | Dependency CVE playbook and dedicated reporting path | Lockfile/advisory match separated from application exploitation and reachability |
| Fix verification | Analysis fix-verification playbook | Applicability, closure, bypass review, preserved behavior and repository checks |
| Context and deduplication | [Compaction](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/llm/compaction.py), [deduplication](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/report/dedupe.py) | Durable run artifacts and explicit duplicate/instance reconciliation through the current agent |

## How assessment flows differ

**White-box:** derive the initial threat model from source, run available static,
AST, secrets and supply-chain passes, trace reachable controls/sinks, and validate
at runtime where possible. A scanner hit is a hypothesis. Inspect separately
reachable siblings and branch-specific transformations rather than reporting
one generic issue per helper.

**Black-box:** browse and capture baseline traffic first, map roles and workflows,
then derive a provisional model and test selected risks. Compare real identities,
state transitions and negative controls. Source fixes are unavailable without source.

**API specification:** build method/path/schema/auth inventory and exercise relevant
operations with baseline, adverse and role-separated cases. The adaptation changes
upstream's assumption that spec base URLs are already authorized: scope must come
from the user, not the input document.

**Diff review:** use the real merge base and follow changed behavior through callers
and controls. The diff narrows report scope without lowering the evidence bar.
Existing issues are separated from introduced/worsened ones.

**Remediation:** state the invariant, repair the controlling boundary, and test
closure plus bypasses and legitimate behavior. Do not equate a tidy minimal diff
with a complete security fix.

## Code-quality observations and limits

The pinned tree contains 93 Python `tests/test_*.py` files. Inspected tests cover
report field validation, coverage persistence/deduplication/history, missing
coverage warnings, tool arguments, API specs, and runtime lifecycle behavior.
These are useful behavioral seams, not proof of a measured vulnerability detection
rate. Upstream tests were inspected; the full upstream suite was not executed here.

Ruff, mypy, Pyright, Bandit and pre-commit configuration are present. The Makefile's
`lint` target runs `ruff check --fix`, and `check-all` includes formatting: neither
is a read-only audit command. The adaptation's validation uses read-only checks.

The inspected GitHub build-release workflow pins action SHAs, builds across five
platform targets and checks artifact packaging/version execution. It does not
itself run the full pytest suite. That is a limit of this workflow's evidence,
not proof that no other external CI exists or that upstream is broken.

The reporting module centralizes extensive validation and persistence but is large
(approximately 100 KB in this snapshot), increasing review surface. Nonempty
counterevidence/fix-verification text is schema-checked; that check alone cannot
prove the text is truthful or the fix is correct. The new skill preserves the
verification procedure but cannot reproduce code-enforced gates with Markdown.

Coverage reconciliation warns about missing and unresolved coverage; it does not
make every unresolved test a hard failure. This adaptation retains explicit partial
results and makes untested techniques visible. No clean full-assessment claim may
be inferred from zero reports or a completed lifecycle.

## Contradictions resolved in the adaptation

- Some scan playbooks require a dynamic PoC for every report, while counterevidence,
  diff guidance and reporting tests accept complete static traces with lower
  confidence. The portable contract distinguishes these evidence classes explicitly.
- Dependency CVEs use advisory/lockfile proof; forcing an application exploit PoC
  would discard legitimate inventory findings. Reachability remains separately evidenced.
- Root delegation, lifecycle tool names and a preconfigured Docker/Caido environment
  are engine assumptions. They become capability discovery, tool mapping and persisted
  artifacts rather than fictional callable APIs.
- Maximum-impact/pivot language and example commands are bounded by supplied scope,
  synthetic data and minimal adequate proof. Depth does not expand authorization.
- Upstream edition labels and version-specific examples are historical claims to
  verify, not current advisories. The adaptation does not promise universal framework
  or OS compatibility without tool/runtime evidence.

## What is not reproduced

The skill does not reproduce Docker isolation, the OpenAI Agents SDK runtime,
automatic Caido bootstrap, model/provider routing, paid cloud integrations,
independent model-based dedupe, hosted PR autofix, scheduling, telemetry, billing,
dashboards, or runtime-enforced report validation. The current host supplies actual
execution, permissions, context and concurrency. Tool gaps are surfaced rather
than hidden behind an asserted equivalence.

Strix's README also documents ChatGPT subscription login and local-model support.
The distinction here is removal of the separate Strix runtime/model integration,
not a claim that Strix can only run with a paid metered API key.

See [the extraction matrix](extraction-matrix.md) and [evaluation](evaluation.md)
for source coverage and this package's actual verification evidence.
