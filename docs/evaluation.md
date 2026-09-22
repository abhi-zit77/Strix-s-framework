# Evaluation record

Date: 2026-09-22. This records actual local execution. It does not establish
benchmark parity or exhaustive behavioral testing of all 75 playbooks.

## Scope

Package structure, standalone installation, attributed source coverage, representative
local security cases, host-tool adaptation, and skill-guided assessment/fixing.
The broad playbook catalog is not claimed to be fully behaviorally tested.

## Package and development checks

Windows 11, Python 3.14.5. All listed checks passed before publication:

| Check | Result |
| --- | --- |
| Repository validator with pinned upstream checkout | All 75 internal and nine consumer source hashes match; links and standalone dependencies resolve |
| Ruff | No errors |
| Strict MyPy | No issues in 13 source files |
| Bandit on installer, validator and comparison fixtures | No findings or warnings; deliberately vulnerable examples excluded |
| Pytest repository suite | 20 passed; installation, packaging, malformed-input validation and representative security fixtures |
| Codex skill-creator `quick_validate.py` | Skill valid |
| Codex plugin-creator `validate_plugin.py` | Plugin valid |
| Claude Code 2.1.280 `plugin validate . --strict` | Marketplace passed with no warnings |
| Claude Code 2.1.280 `plugin validate plugins/strix-framewok --strict` | Plugin passed with no warnings |

Claude's validator ran from a task-local official native package. The npm
postinstall was not enabled; its native executable was invoked directly.
No global skill/plugin installation or authenticated Claude session was performed.
Codex checks include bundled validators and a Codex-host evaluator, not plugin
loading in every Codex release. GitHub Actions repeats repository checks on Linux
Python 3.12 and Windows Python 3.14; consult its run results for remote evidence.
The first Linux run caught inline example syntax being mistaken for a link;
the checker now excludes inline code, with a dedicated regression.

## Independent skill-guided evaluation

A separate evaluator received the canonical skill, raw target/comparison source
copies, and a local audit-and-fix request. It did not inspect repository tests or
intended answers. It used real terminal/file/Python tools with separate sequential
discovery, validation and reporting passes. No external target was contacted.

The contract treated function parameters as caller inputs except the authenticated
principal. Four findings were reproduced: record ownership bypass, SQL syntax
injection, requested-path escape, and separate caller-controlled root authority.
The last affected both target and comparison. Containment within a root alone
cannot authorize a caller who can choose that root.

| Runtime check | Result |
| --- | --- |
| Original target | 8/19 security and legitimate-use expectations met |
| Unchanged comparison | 17/19 expectations met under the caller-root contract |
| Fixed target | 19/19 expectations met |
| Authored regression tests | 11 failing cases before repair; 19 passed afterward |
| Fixed-target Ruff, MyPy, Bandit and syntax checks | All exit codes 0 |
| Comparison preservation | Source hash unchanged |

The repair preserved the download signature but restricted accepted roots to
application-owned `PUBLIC_ROOT`. This is an intentional contract change. A
general-purpose reader whose root is trusted has a different boundary. The
repository comparison helper models that trusted-root contract; its docstring
now makes it explicit.

See [case evidence](evaluation-results.json) for sanitized before/control/after
observations, timestamps and source hashes. Cases use synthetic values. A separate
source-only pass executed no target code, classified four corrected paths as
reasoned closures and capped confidence at medium. Prior runtime results were
not presented as executions performed by that source-only pass.

## Feedback incorporated

The evaluation identified excess applicability work for local libraries and
conflicting numeric-severity wording. The final package adds a local-function
recipe with case-to-ledger guidance and aligns severity with the main qualitative/
unscored option. Those documentation changes were structurally checked; the
independent evaluation was not repeated afterward.

## Limits

- Windows denied symlink creation (error 1314): blocked, not passed.
- NTFS edge cases and concurrent filesystem mutation were not exercised.
- No deployment, HTTP/browser target, dependency manifest or Git history was
  supplied. Semgrep/Gitleaks were unavailable.
- The original evaluation copy contained a `nosec B608` suppression. Its clean
  Bandit output is not evidence of SQL safety or scanner detection quality. The
  published vulnerable fixture removes that suppression and is intentionally
  excluded from the passing development audit; semantic tests exercise its bugs.
- Browser/Playwright adaptation is documented but was not exercised against a web
  app. No real SaaS, cloud credential, payment or production flow was tested.
- No full-catalog, hosted-Strix, cross-host behavioral or model-quality equivalence
  follows from these checks.

Repeat package checks using [CONTRIBUTING](../CONTRIBUTING.md). For future behavior
evaluations, follow the [evaluation protocol](../evals/README.md).
