> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/naabu.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/naabu.md).
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

# Naabu CLI Playbook

Official docs:
- https://docs.projectdiscovery.io/opensource/naabu/usage
- https://docs.projectdiscovery.io/opensource/naabu/running
- https://github.com/projectdiscovery/naabu

Canonical syntax:
`naabu [flags]`

High-signal flags:
- `-host <host>` single host
- `-list, -l <file>` hosts list
- `-p <ports>` explicit ports (supports ranges)
- `-top-ports <n|full>` top ports profile
- `-exclude-ports <ports>` exclusions
- `-scan-type <s|c|syn|connect>` SYN or CONNECT scan
- `-Pn` skip host discovery
- `-rate <n>` packets per second
- `-c <n>` worker count
- `-timeout <ms>` per-probe timeout in milliseconds
- `-retries <n>` retry attempts
- `-proxy <socks5://host:port>` SOCKS5 proxy
- `-verify` verify discovered open ports
- `-j, -json` JSONL output
- `-silent` compact output
- `-o <file>` output file

Agent-safe baseline for automation:
`naabu -list hosts.txt -top-ports 100 -scan-type c -Pn -rate 300 -c 25 -timeout 1000 -retries 1 -verify -silent -j -o naabu.jsonl`

Common patterns:
- Top ports with controlled rate:
  `naabu -list hosts.txt -top-ports 100 -scan-type c -rate 300 -c 25 -timeout 1000 -retries 1 -verify -silent -o naabu.txt`
- Focused web-ports sweep:
  `naabu -list hosts.txt -p 80,443,8080,8443 -scan-type c -rate 300 -c 25 -timeout 1000 -retries 1 -verify -silent`
- Single-host quick check:
  `naabu -host target.tld -p 22,80,443 -scan-type c -rate 300 -c 25 -timeout 1000 -retries 1 -verify`
- Root SYN mode (if available):
  `sudo naabu -list hosts.txt -top-ports 100 -scan-type syn -rate 500 -c 25 -timeout 1000 -retries 1 -verify -silent`

Critical correctness rules:
- Use `-scan-type connect` when running without root/privileged raw socket access.
- Always set `-timeout` explicitly; it is in milliseconds.
- Set `-rate` explicitly to avoid unstable or noisy scans.
- `-timeout` is in milliseconds, not seconds.
- Keep port scope tight: prefer explicit important ports or a small `-top-ports` value unless broader coverage is explicitly required.
- Do not spam traffic; start with the smallest useful port set and conservative rate/worker settings.
- Prefer `-verify` before handing ports to follow-up scanners.

Usage rules:
- Keep host discovery behavior explicit (`-Pn` or default discovery).
- Use `-j -o <file>` for automation pipelines.
- Prefer `-p 22,80,443,8080,8443` or `-top-ports 100` before considering larger sweeps.
- Do not use `-h`/`--help` for normal flow unless absolutely necessary.

Failure recovery:
- If privileged socket errors occur, switch to `-scan-type c`.
- If scans are slow or lossy, lower `-rate`, lower `-c`, and tighten `-p`/`-top-ports`.
- If many hosts appear down, compare runs with and without `-Pn`.

If uncertain, query web_search with:
`site:docs.projectdiscovery.io naabu <flag> usage`
