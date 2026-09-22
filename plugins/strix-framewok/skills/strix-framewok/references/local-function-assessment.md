# Local function and library assessment

Use this recipe when the target is callable source without an HTTP or browser
surface. Apply the main scope, evidence, and fix contracts. Do not fabricate a
deployment just to fit a web playbook.

1. Map public entrypoints and callers. Separate attacker arguments, authenticated
   identity, operator configuration, and trusted dependencies. A caller-controlled
   `root`, tenant ID, role, or allowlist cannot confer its own authority. If the
   contract is unknown, describe conditional findings and inspect real callers.
2. Select applicable source-to-sink families. Mark HTTP sessions, browser behavior,
   cloud services, and dependencies absent only when inspection establishes that.
   Missing manifests or callers remain limits rather than proof of absence.
3. Build an isolated harness with temporary directories, in-memory stores and
   synthetic values. Load only scoped code after inspecting its import side
   effects. Preserve the original source/hash before any repair.
4. Give every case a stable ID. Capture arguments with secrets removed, expected
   result or exception, actual result/exception, selected source hash and runtime.
   A harness exception is not automatically successful denial: establish which
   guard raised it and whether protected state was touched first.
5. Compare normal, adverse and alternate cases against the target and any supplied
   comparison implementation. A file named `safe` is counterevidence to investigate,
   not an oracle. Review shared flaws and contract differences independently.
6. Reproduce before fixing; write regressions that fail on the original. Patch
   only authorized files, run the same cases after the fix, and verify legitimate
   behavior. Explain any tighter public contract rather than hiding it as an
   implementation detail. Run the repository's applicable quality checks.
7. Translate individual cases into the shared coverage ledger and reporting model.
   Preserve before/after evidence. A separate source-only pass must not execute
   the target or inherit runtime confidence without identifying that evidence.

## Minimal case-to-ledger mapping

| Case | Baseline | Probe and oracle | Counterevidence / gap |
| --- | --- | --- | --- |
| Ownership | Owner reads their synthetic record | Different principal cannot read the same record | Establish identity origin; test sibling entrypoints |
| Query syntax | Exact existing and absent values | Quotes, boolean alternatives and a synthetic union marker stay data | Trace binding; a clean scanner result is insufficient |
| Path containment | Read a permitted nested file | Relative escape, absolute path and sibling-prefix path cannot read a synthetic private file | Check canonicalization; symlink/race tests require OS support |
| Root authority | Application sets a trusted directory | Caller-provided alternate root must not expand permitted files | A general-purpose reader may intentionally trust root; state the contract |

For each row use the [coverage template](../assets/coverage.template.json), expand
one case/asset pair per test, and include evidence locations and timestamps in its
history. Link a reported outcome to a finding ID. Use `needs_follow_up` for an
unresolved candidate, `untested` for a blocked selected test, and explain the
condition. Do not convert an OS privilege error into a passed symlink check.

Local function behavior establishes only that boundary. Keep network access,
deployment privilege, real data impact, and full filesystem race resistance
unverified until suitable evidence exists.
