> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/nmap.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/nmap.md).
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

# Nmap CLI Playbook

Official docs:
- https://nmap.org/book/man-briefoptions.html
- https://nmap.org/book/man.html
- https://nmap.org/book/man-performance.html

Canonical syntax:
`nmap [Scan Type(s)] [Options] {target specification}`

High-signal flags:
- `-n` skip DNS resolution
- `-Pn` skip host discovery when ICMP/ping is filtered
- `-sS` SYN scan (root/privileged)
- `-sT` TCP connect scan (no raw-socket privilege)
- `-sV` detect service versions
- `-sC` run default NSE scripts
- `-p <ports>` explicit ports (`-p-` for all TCP ports)
- `--top-ports <n>` quick common-port sweep
- `--open` show only hosts with open ports
- `-T<0-5>` timing template (`-T4` common)
- `--max-retries <n>` cap retransmissions
- `--host-timeout <time>` give up on very slow hosts
- `--script-timeout <time>` bound NSE script runtime
- `-oA <prefix>` output in normal/XML/grepable formats

Agent-safe baseline for automation:
`nmap -n -Pn --open --top-ports 100 -T4 --max-retries 1 --host-timeout 90s -oA nmap_quick <host>`

Common patterns:
- Fast first pass:
  `nmap -n -Pn --top-ports 100 --open -T4 --max-retries 1 --host-timeout 90s <host>`
- Very small important-port pass:
  `nmap -n -Pn -p 22,80,443,8080,8443 --open -T4 --max-retries 1 --host-timeout 90s <host>`
- Service/script enrichment on discovered ports:
  `nmap -n -Pn -sV -sC -p <comma_ports> --script-timeout 30s --host-timeout 3m -oA nmap_services <host>`
- No-root fallback:
  `nmap -n -Pn -sT --top-ports 100 --open --host-timeout 90s <host>`

Critical correctness rules:
- Always set target scope explicitly.
- Prefer two-pass scanning: discovery pass, then enrichment pass.
- Always set a timeout boundary with `--host-timeout`; add `--script-timeout` whenever NSE scripts are involved.
- Keep discovery scans tight: use explicit important ports or a small `--top-ports` profile unless broader coverage is explicitly required.
- In sandboxed runs, avoid exhaustive sweeps (`-p-`, very high `--top-ports`, or wide host ranges) unless explicitly required.
- Do not spam traffic; start with the smallest port set that can answer the question.
- Prefer `naabu` for broad port discovery; use `nmap` for scoped verification/enrichment.

Usage rules:
- Add `-n` by default in automation to avoid DNS delays.
- Use `-oA` for reusable artifacts.
- Prefer `-p 22,80,443,8080,8443` or `--top-ports 100` before considering larger sweeps.
- Do not use `-h`/`--help` for routine usage unless absolutely necessary.

Failure recovery:
- If host appears down unexpectedly, rerun with `-Pn`.
- If scan stalls, tighten scope (`-p` or smaller `--top-ports`) and lower retries.
- If scripts run too long, add `--script-timeout`.

If uncertain, query web_search with:
`site:nmap.org/book nmap <flag>`
