# Package review

Reviewed 2026-09-22 with the code-reviewer checklist, security-auditor evidence
rules and lint-and-validate workflow. This standalone package has no GSD phase;
the GSD review's inline fallback was used with findings recorded here.

Scope: installer/validator, fixtures/tests, manifests, CI, invocation documentation,
reference reachability, upstream provenance and tool adaptation. Independent
behavioral evaluation is recorded separately.

## Findings resolved before publication

| Finding | Resolution and prevention |
| --- | --- |
| Browser guide linked absent companions | Replaced with bundled guidance; tests reject missing/escaping links |
| Empty marketplace array could crash validation | Added shape check and regression; CLI reports malformed data as failure |
| Linux CI parsed inline SSTI sample as a local link | Excluded inline code spans and added regression; retain both OS jobs because Windows path normalization hid it |
| Strict marketplace check warned about missing description | Added metadata; native Claude validation passes |
| Next.js examples assumed universal route/environment enumeration | Guarded optional Pages hints; removed environment enumeration; require observed/source coverage |
| Severity always demanded numeric CVSS | Aligned qualitative/unscored option and confidence with main contract |
| Comparison helper could be mistaken for root authorization | Documented trusted-root contract; preserved independent root-authority finding |
| Supabase examples assumed legacy credential types | Added primary-documentation guidance for keys, identity, grants and RLS |
| Initial behavioral scan contained a suppression | Recorded its limitation; removed suppression in published vulnerable input and excluded that input from passing audit |

Installer review confirms explicit destination selection, overwrite refusal,
source-link rejection and no host-config modification/deletion. The validator is
a package-specific consistency checker, not a general security sandbox or complete
Markdown/JSON schema implementation.

CI has read-only repository permissions, pinned action revisions and synthetic
local tests. No model key or target credential is required. Upstream commands are
templates governed by actual scope and tool contracts.

No unresolved blocking defect was identified within this review's scope. Known
host/behavioral gaps remain in [evaluation](evaluation.md). Passing review or
schema checks do not prove exhaustive security or host-runtime parity.
