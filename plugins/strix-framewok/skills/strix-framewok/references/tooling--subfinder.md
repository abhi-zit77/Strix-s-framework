> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/subfinder.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/subfinder.md).
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

# Subfinder CLI Playbook

Official docs:
- https://docs.projectdiscovery.io/opensource/subfinder/usage
- https://docs.projectdiscovery.io/opensource/subfinder/running
- https://github.com/projectdiscovery/subfinder

Canonical syntax:
`subfinder [flags]`

High-signal flags:
- `-d <domain>` single domain
- `-dL <file>` domain list
- `-all` include all sources
- `-recursive` use recursive-capable sources
- `-s <sources>` include specific sources
- `-es <sources>` exclude specific sources
- `-rl <n>` global rate limit
- `-rls <source=n/s,...>` per-source rate limits
- `-proxy <http://host:port>` proxy outbound source requests
- `-silent` compact output
- `-o <file>` output file
- `-oJ, -json` JSONL output
- `-cs, -collect-sources` include source metadata (`-oJ` output)
- `-nW, -active` show only active subdomains
- `-timeout <seconds>` request timeout
- `-max-time <minutes>` overall enumeration cap

Agent-safe baseline for automation:
`subfinder -d example.com -all -recursive -rl 20 -timeout 30 -silent -oJ -o subfinder.jsonl`

Common patterns:
- Standard passive enum:
  `subfinder -d example.com -silent -o subs.txt`
- Broad-source passive enum:
  `subfinder -d example.com -all -recursive -silent -o subs_all.txt`
- Multi-domain run:
  `subfinder -dL domains.txt -all -recursive -rl 20 -silent -o subfinder_out.txt`
- Source-attributed JSONL output:
  `subfinder -d example.com -all -oJ -cs -o subfinder_sources.jsonl`
- Passive enum via explicit proxy:
  `subfinder -d example.com -all -recursive -proxy http://127.0.0.1:48080 -silent -oJ -o subfinder_proxy.jsonl`

Critical correctness rules:
- `-cs` is useful only with JSON output (`-oJ`).
- Many sources require API keys in provider config; low results can be config-related, not target-related.
- `-nW` performs active resolution/filtering and can drop passive-only hits.
- Keep passive enum first, then validate with `httpx`.

Usage rules:
- Keep output files explicit when chaining to `httpx`/`nuclei`.
- Use `-rl/-rls` when providers throttle aggressively.
- Do not use `-h`/`--help` for routine tasks unless absolutely necessary.

Failure recovery:
- If results are unexpectedly low, rerun with `-all` and verify provider config/API keys.
- If provider errors appear, lower `-rl` and apply `-rls` per source.
- If runs take too long, lower scope or split domain batches.

If uncertain, query web_search with:
`site:docs.projectdiscovery.io subfinder <flag> usage`
