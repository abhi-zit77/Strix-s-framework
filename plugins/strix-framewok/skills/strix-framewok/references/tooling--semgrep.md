> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/semgrep.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/semgrep.md).
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

# Semgrep CLI Playbook

Official docs:
- https://semgrep.dev/docs/cli-reference
- https://semgrep.dev/docs/getting-started/cli
- https://semgrep.dev/docs/semgrep-code/semgrep-pro-engine-intro

Canonical syntax:
`semgrep scan [flags]`

High-signal flags:
- `--config <rule_or_ruleset>` ruleset, registry pack, local rule file, or directory
- `--metrics=off` disable telemetry and metrics reporting
- `--json` JSON output
- `--sarif` SARIF output
- `--output <file>` write findings to file
- `--severity <level>` filter by severity
- `--error` return non-zero exit when findings exist
- `--quiet` suppress progress noise
- `--jobs <n>` parallel workers
- `--timeout <seconds>` per-file timeout
- `--exclude <pattern>` exclude path pattern
- `--include <pattern>` include path pattern
- `--exclude-rule <rule_id>` suppress specific rule
- `--baseline-commit <sha>` only report findings introduced after baseline
- `--oss-only` force OSS engine only

Agent-safe baseline for automation:
`semgrep scan --config p/default --metrics=off --json --output semgrep.json --quiet --jobs 4 --timeout 20 /workspace`

Common patterns:
- Default security scan:
  `semgrep scan --config p/default --metrics=off --json --output semgrep.json --quiet /workspace`
- High-severity focused pass:
  `semgrep scan --config p/default --severity ERROR --metrics=off --json --output semgrep_high.json --quiet /workspace`
- OWASP-oriented scan:
  `semgrep scan --config p/owasp-top-ten --metrics=off --sarif --output semgrep.sarif --quiet /workspace`
- Language- or framework-specific rules:
  `semgrep scan --config p/python --config p/secrets --metrics=off --json --output semgrep_python.json --quiet /workspace`
- Scoped directory scan:
  `semgrep scan --config p/default --metrics=off --json --output semgrep_api.json --quiet /workspace/services/api`
- Pro engine check or run:

Critical correctness rules:
- Always include `--metrics=off`; Semgrep sends telemetry by default.
- Always provide an explicit `--config`; do not rely on vague or implied defaults.
- Prefer `--json --output <file>` or `--sarif --output <file>` for machine-readable downstream processing.
- Keep the target path explicit; use an absolute or clearly scoped workspace path instead of `.` when possible.
- If Pro availability matters, check it explicitly with a bounded command before assuming cross-file analysis exists.

Usage rules:
- Start with `p/default` unless the task clearly calls for a narrower pack.
- Add focused packs such as `p/secrets`, `p/python`, or `p/javascript` only when they match the target stack.
- Use `--quiet` in automation to reduce noisy logs.
- Use `--jobs` and `--timeout` explicitly for reproducible runtime behavior.
- Do not use `-h`/`--help` for routine operation unless absolutely necessary.

Failure recovery:
- If scans are too slow, narrow the target path and reduce the active rulesets before changing engine settings.
- If scans time out, increase `--timeout` modestly or lower `--jobs`.
- If output is too broad, scope `--config`, add `--severity`, or exclude known irrelevant paths.

If uncertain, query web_search with:
`site:semgrep.dev semgrep <flag> cli`
