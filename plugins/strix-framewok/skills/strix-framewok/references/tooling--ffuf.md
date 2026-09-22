> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/tooling/ffuf.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/tooling/ffuf.md).
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

# ffuf CLI Playbook

Official docs:
- https://github.com/ffuf/ffuf

Canonical syntax:
`ffuf -w <wordlist> -u <url_with_FUZZ> [flags]`

High-signal flags:
- `-u <url>` target URL containing `FUZZ`
- `-w <wordlist>` wordlist input (supports `KEYWORD` mapping via `-w file:KEYWORD`)
- `-mc <codes>` match status codes
- `-fc <codes>` filter status codes
- `-fs <size>` filter by body size
- `-ac` auto-calibration
- `-t <n>` threads
- `-rate <n>` request rate
- `-timeout <seconds>` HTTP timeout
- `-x <proxy_url>` upstream proxy (HTTP/SOCKS)
- `-ignore-body` skip downloading response body
- `-noninteractive` disable interactive console mode
- `-recursion` and `-recursion-depth <n>` recursive discovery
- `-H <header>` custom headers
- `-X <method>` and `-d <body>` for non-GET fuzzing
- `-o <file> -of <json|ejson|md|html|csv|ecsv>` structured output

Agent-safe baseline for automation:
`ffuf -w wordlist.txt -u https://target.tld/FUZZ -mc 200,204,301,302,307,401,403,405 -ac -t 20 -rate 50 -timeout 10 -noninteractive -of json -o ffuf.json`

Common patterns:
- Basic path fuzzing:
  `ffuf -w /path/wordlist.txt -u https://target.tld/FUZZ -mc 200,204,301,302,307,401,403 -ac -t 40 -rate 200 -noninteractive`
- Vhost fuzzing:
  `ffuf -w vhosts.txt -u https://target.tld -H 'Host: FUZZ.target.tld' -fs 0 -ac -noninteractive`
- Parameter value fuzzing:
  `ffuf -w values.txt -u 'https://target.tld/search?q=FUZZ' -mc all -fs 0 -ac -t 30 -noninteractive`
- POST body fuzzing:
  `ffuf -w payloads.txt -u https://target.tld/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=admin&password=FUZZ' -fc 401 -noninteractive`
- Recursive discovery:
  `ffuf -w dirs.txt -u https://target.tld/FUZZ -recursion -recursion-depth 2 -ac -t 30 -noninteractive`
- Proxy-instrumented run:
  `ffuf -w wordlist.txt -u https://target.tld/FUZZ -x http://127.0.0.1:48080 -mc 200,301,302,403 -ac -noninteractive`

Critical correctness rules:
- `FUZZ` must appear exactly at the mutation point in URL/header/body.
- If using `-w file:KEYWORD`, that same `KEYWORD` must be present in URL/header/body.
- Always include `-noninteractive` in agent/script execution to prevent ffuf console mode from swallowing subsequent shell commands.
- Save structured output with `-of json -o <file>` for deterministic parsing.

Usage rules:
- Prefer explicit matcher/filter strategy (`-mc`/`-fc`/`-fs`) over default-only output.
- Start conservative (`-rate`, `-t`) and scale only if target tolerance is known.
- Do not use `-h`/`--help` during normal execution unless absolutely necessary.

Failure recovery:
- If ffuf drops into interactive mode, send `C-c` and rerun with `-noninteractive`.
- If response noise is too high, tighten `-mc/-fc/-fs` instead of increasing load.
- If runtime is too long, lower `-rate/-t` and tighten scope.

If uncertain, query web_search with:
`site:github.com/ffuf/ffuf <flag> README`

Alternate tool for path/file enumeration: `dirsearch -u <url> -e php,html,js,json`
ships with curated wordlists, sane defaults, and built-in recursion. Reach
for ffuf when you need surgical fuzzing of any input position (header,
body, vhost) or precise filter control; reach for dirsearch for a quick
broad sweep with no setup.
