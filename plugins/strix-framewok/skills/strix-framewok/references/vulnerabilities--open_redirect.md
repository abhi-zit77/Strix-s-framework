> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/vulnerabilities/open_redirect.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/vulnerabilities/open_redirect.md).
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

## Portable test and retest recipe

- **Applicability:** select the attack surfaces and prerequisites documented below; establish actual target versions and identities.
- **Invariant / expected secure behavior:** Untrusted destinations cannot escape the intended navigation/credential boundary.
- **Execution and proof:** Compare accepted internal and rejected external/encoded destinations; follow redirects only within controlled scope.
- **Counterevidence:** test a legitimate baseline and a protected negative case; inspect the actual guard and why it runs on this path.
- **Remediation when requested:** Prefer relative destinations or strict parsed-origin allowlists; validate after normalization and at every redirect hop.
- **Retest:** replay the original case, a different encoding/shape/identity or sibling path, and the legitimate case; add a regression and run repository checks.
- **Record:** evidence kind, actual observations, confidence, named limitations, and coverage outcome. Runtime unavailable means static proof or an open gap, never fabricated execution.


## Adapted technical playbook

# Open Redirect

Open redirects enable phishing, OAuth/OIDC code and token theft, and allowlist bypass in server-side fetchers that follow redirects. Treat every redirect target as untrusted: canonicalize and enforce exact allowlists per scheme, host, and path.

## Attack Surface

**Server-Driven Redirects**
- HTTP 3xx Location

**Client-Driven Redirects**
- `window.location`, meta refresh, SPA routers

**OAuth/OIDC/SAML Flows**
- `redirect_uri`, `post_logout_redirect_uri`, `RelayState`, `returnTo`/`continue`/`next`

**Multi-Hop Chains**
- Only first hop validated

## High-Value Targets

- Login/logout, password reset, SSO/OAuth flows
- Payment gateways, email links, invite/verification
- Unsubscribe, language/locale switches
- `/out` or `/r` redirectors

## Reconnaissance

### Injection Points

- Params: `redirect`, `url`, `next`, `return_to`, `returnUrl`, `continue`, `goto`, `target`, `callback`, `out`, `dest`, `back`, `to`, `r`, `u`
- OAuth/OIDC/SAML: `redirect_uri`, `post_logout_redirect_uri`, `RelayState`, `state`
- SPA: `router.push`/`replace`, `location.assign`/`href`, meta refresh, `window.open`
- Headers: `Host`, `X-Forwarded-Host`/`Proto`, `Referer`; server-side Location echo

### Parser Differentials

**Userinfo**
- `https://trusted.com@evil.com` → validators parse host as trusted.com, browser navigates to evil.com
- Variants: `trusted.com%40evil.com`, `a%40evil.com%40trusted.com`

**Backslash and Slashes**
- `https://trusted.com\evil.com`, `https://trusted.com\@evil.com`, `///evil.com`, `/\evil.com`

**Whitespace and Control**
- `http%09://evil.com`, `http%0A://evil.com`, `trusted.com%09evil.com`

**Fragment and Query**
- `trusted.com#@evil.com`, `trusted.com?//@evil.com`, `?next=//evil.com#@trusted.com`

**Unicode and IDNA**
- Punycode/IDN: `truѕted.com` (Cyrillic), `trusted.com。evil.com` (full-width dot), trailing dot

### Encoding Bypasses

- Double encoding: `%2f%2fevil.com`, `%252f%252fevil.com`
- Mixed case and scheme smuggling: `hTtPs://evil.com`, `http:evil.com`
- IP variants: decimal 2130706433, octal 0177.0.0.1, hex 0x7f.1, IPv6 `[::ffff:127.0.0.1]`
- User-controlled path bases: `/out?url=/\evil.com`

## Key Vulnerabilities

### Allowlist Evasion

**Common Mistakes**
- Substring/regex contains checks: allows `trusted.com.evil.com`
- Wildcards: `*.trusted.com` also matches `attacker.trusted.com.evil.net`
- Missing scheme pinning: `data:`, `javascript:`, `file:`, `gopher:` accepted
- Case/IDN drift between validator and browser

**Robust Validation**
- Canonicalize with a single modern URL parser (WHATWG URL)
- Compare exact scheme, hostname (post-IDNA), and an explicit allowlist with optional exact path prefixes
- Require absolute HTTPS; reject protocol-relative `//` and unknown schemes

### OAuth/OIDC/SAML

**Redirect URI Abuse**
- Using an open redirect on a trusted domain for redirect_uri enables code interception
- Weak prefix/suffix checks: `https://trusted.com` → `https://trusted.com.evil.com`
- Path traversal/canonicalization: `/oauth/../../@evil.com`
- `post_logout_redirect_uri` often less strictly validated

### Client-Side Vectors

**JavaScript Redirects**
- `location.href`/`assign`/`replace` using user input
- Meta refresh `content=0;url=USER_INPUT`
- SPA routers: `router.push(searchParams.get('next'))`

### Reverse Proxies and Gateways

- Host/X-Forwarded-* may change absolute URL construction
- CDNs that follow redirects for link checking can leak tokens when chained

### SSRF Chaining

- Server-side fetchers (web previewers, link unfurlers) follow 3xx
- Combine with an open redirect on an allowlisted domain to pivot to internal targets (169.254.169.254, localhost)

## Exploitation Scenarios

### OAuth Code Interception

1. Set redirect_uri to `https://trusted.example/out?url=https://attacker.tld/cb`
2. IdP sends code to trusted.example which redirects to attacker.tld
3. Exchange code for tokens; demonstrate account access

### Phishing Flow

1. Send link on trusted domain: `/login?next=https://attacker.tld/fake`
2. Victim authenticates; browser navigates to attacker page
3. Capture credentials/tokens via cloned UI

### Internal Evasion

1. Server-side link unfurler fetches `https://trusted.example/out?u=http://169.254.169.254/latest/meta-data`
2. Redirect follows to metadata; confirm via timing/headers

## Testing Methodology

1. **Inventory surfaces** - Login/logout, password reset, SSO/OAuth flows, payment gateways, email links
2. **Build test matrix** - Scheme × host × path variants and encoding/unicode forms
3. **Compare behaviors** - Server-side validation vs browser navigation results
4. **Multi-hop testing** - Trusted-domain → redirector → external
5. **Prove impact** - Credential phishing, OAuth code interception, internal egress

## Validation

1. Produce a minimal URL that navigates to an external domain via the vulnerable surface; include the full address bar capture
2. Show bypass of the stated validation (regex/allowlist) using canonicalization variants
3. Test multi-hop: prove only first hop is validated and second hop escapes constraints
4. For OAuth/SAML, demonstrate code/RelayState delivery to an attacker-controlled endpoint

## False Positives

- Redirects constrained to relative same-origin paths with robust normalization
- Exact pre-registered OAuth redirect_uri with strict verifier
- Validators using a single canonical parser and comparing post-IDNA host and scheme
- User prompts that show the exact final destination before navigating

## Impact

- Credential and token theft via phishing and OAuth/OIDC interception
- Internal data exposure when server fetchers follow redirects
- Policy bypass where allowlists are enforced only on the first hop
- Cross-application trust erosion and brand abuse

## Pro Tips

1. Always compare server-side canonicalization to real browser navigation; differences reveal bypasses
2. Try userinfo, protocol-relative, Unicode/IDN, and IP numeric variants early
3. In OAuth, prioritize `post_logout_redirect_uri` and less-discussed flows; they're often looser
4. Exercise multi-hop across distinct subdomains and paths
5. For SSRF chaining, target services known to follow redirects
6. Favor allowlists of exact origins plus optional path prefixes
7. Keep a curated suite of redirect payloads per runtime (Java, Node, Python, Go)

## Summary

Redirection is safe only when the final destination is constrained after canonicalization. Enforce exact origins, verify per hop, and treat client-provided destinations as untrusted across every stack.
