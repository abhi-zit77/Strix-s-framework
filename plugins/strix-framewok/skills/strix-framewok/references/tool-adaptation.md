# Tool adaptation

These are capability mappings, not callable APIs. Read the actual host tool schema
before acting. Never call an upstream Strix function by name merely because a
reference mentions it. Prefer an already-connected tool over adding infrastructure.

| Need | Preferred available capability | Fallback and evidence limit |
| --- | --- | --- |
| Source, manifests, diffs | Native file/search tools; shell `rg`, Git | Connector source reads; no claim of local build execution |
| Browser workflows | Host browser/Playwright/MCP with documented session API | Installed browser CLI; HTTP cannot confirm DOM execution |
| HTTP baseline/replay | Host HTTP/proxy tools with request/response capture | `curl.exe` on Windows, curl or installed Python client; save redacted exchanges |
| Interception | Existing scoped proxy or browser network capture | Direct replay; mark interception-dependent tests unavailable |
| Local checks | Host terminal in target worktree, correct interpreter | Source-only traces; explicit runtime gap |
| Static and AST analysis | Installed Semgrep, ast-grep/tree-sitter, language tooling | Manual source-to-sink review and scoped `rg`; not equivalent scanner/AST coverage |
| Secrets | Installed Gitleaks/TruffleHog in offline/non-verifying mode | Targeted source/history inspection; never validate live credentials without scope |
| Dependencies | Lockfile-aware scanner and advisory sources | Manual exact-version/advisory match; record DB date and reachability uncertainty |
| Specialist agents | Host's permitted subagents/tasks with bounded responsibilities | Sequential discovery, validation, counterevidence, reporting passes |
| Findings/coverage/threat model | Task-local JSON/Markdown artifacts using bundled templates | User-visible structured output if writes are unavailable; state persistence gap |
| CVSS | Installed correct-version calculator or authoritative calculator | Qualitative severity with rationale; never fabricate a numeric score |

## Capability discovery

1. Inventory tool names/descriptions exposed in this session. Load relevant tool
   documentation. A tool being listed does not prove it can reach this target.
2. Check only binaries useful for the chosen tests (`Get-Command` on PowerShell,
   `command -v` on POSIX), versions, and package manifests. `httpx` may refer to
   different projects; verify which executable is installed. `sg` is similarly
   ambiguous. Avoid `npx` auto-install as a presence test.
3. Run the smallest benign operation: read one source file, open the scoped app,
   make one baseline request, or query tool help. Record permission/connection
   failures. Do not switch channels to bypass a host access restriction.
4. Map tests to verified capabilities. Use the least additional setup needed.
   Explain an install command before installing into a task-local environment;
   respect host approval and network rules. Docker is optional, never assumed.
5. Continue useful work while blocked tests are recorded. Missing Playwright does
   not block source review; missing source does not imply source review passed.

## Browser workflow

Use Playwright or the host's browser tool when it is present. Open the scoped
origin, capture current DOM/accessibility state, identify controls, interact using
observed locators, then refresh state after navigation or dynamic changes. Keep
test identities in separate contexts or supported sessions. Record role, URL,
action, expected state, observed state, and relevant response/DOM evidence.

For XSS, prove harmless execution in the intended context with a synthetic marker;
reflected text alone is insufficient. For CSRF, distinguish a real cross-origin
browser request with its actual cookie behavior from direct HTTP replay. For
authorization, compare at least owner/non-owner and unauthenticated cases where
available. For stored data, verify persistence and clean up only created fixtures.

Use screenshots as supplementary evidence. A screenshot does not replace a
request/response or source trace. Record network events only when the actual
browser API supports them. Do not claim Caido history exists without a connected
proxy. Mocked responses test UI behavior, not server security.

Use already configured test-account sessions or the host's secure credential input.
Request user participation only when login/MFA genuinely requires it. Persist cookies
only in an approved private run location. Video/tracing is optional: use it only
when the connected tool documents the capability, avoid recording credentials, and
record the returned artifact path. Do not require browser recordings to establish
an HTTP or source finding.

## HTTP and shell workflow

Verify origin, redirects, method, identity, and side effects for each probe. Disable
automatic redirects when they could leave scope; inspect each hop before following.
Bind local fixture servers to loopback. Pass structured arguments, quote paths
for the actual shell, set timeouts, and constrain concurrency. Do not paste POSIX
pipelines into PowerShell. Replace illustrative endpoints and paths before running
any reference command; no example hostname authorizes traffic.

Write complex probes to small inspected scripts instead of opaque one-liners.
Capture exit status and stderr as well as output. A scanner crash, empty/truncated
artifact, stale database, or time budget exhaustion is not a clean result. Preserve
raw sensitive evidence only in an approved private location; publish redacted copies.

## Strix runtime operation replacements

| Upstream operation | Host-native action |
| --- | --- |
| `create_agent`, `send_message`, `wait_for_agents`, `agent_finish` | Delegate/message/wait only through available host tools; otherwise sequential role passes and written handoffs |
| `get_threat_model`, `save_threat_model`, `amend_threat_model` | Read/write the run's threat-model document; keep attributed corrections |
| `record_coverage`, `update_coverage`, `list_coverage` | Maintain one row per surface/risk/technique in coverage.json with history |
| `create_vulnerability_report`, `update_vulnerability_report`, `get_report`, `list_reports` | Write/read finding artifacts with stable IDs; update instead of duplicating |
| `create_dependency_report` | Same finding contract with evidence kind dependency_advisory and dependency fields |
| `create_note`, `update_note`, `list_notes`, todos | Run notes and worklist; store credential references, never credential values |
| `load_skill` | Read the selected bundled reference through host file tools |
| `exec_command`, `apply_patch`, Python executor | Actual host terminal/editor; Python only if available |
| `list_requests`, `view_request`, `repeat_request`, `caido_api` | Real connected proxy API or direct HTTP capture/replay; never fabricate IDs |
| `finish_scan` | Reconcile artifacts, mark complete/partial/interrupted honestly, deliver final report |

## Completion and interruption

Persist after each material finding or coverage change, before context compaction,
and before handing off. Resume by rereading scope, current source/runtime identity,
artifacts, and changed capabilities. A changed revision needs targeted revalidation.
Stop failed setup attempts after two distinct reasonable approaches unless new
evidence suggests a solution; record the blocker and spend remaining effort on
other tests. Do not create a background monitor or paid service as a fallback.
