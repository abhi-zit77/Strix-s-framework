# Skill evaluation protocol

Fixtures are synthetic local evaluation inputs, excluded from installed skills and
plugins. Do not deploy them. The `safe` directory supplies negative controls for
specific invariants, not a universal security certification. Its download helper
requires an application-trusted root; caller authority is a separate boundary.

1. Copy raw source to an isolated evaluation directory. Preserve originals/hashes.
   Give an evaluator the skill and an authorized task; withhold expected findings
   and repository regression tests.
2. State input authority: authenticated identity, caller arguments and operator
   configuration. Keep external services out of scope.
3. Request audit, then target-only repair and legitimate/adverse regressions.
   Require actual tools, counterevidence, source identities and coverage gaps.
4. Assess substantiated findings and behavior preservation. Accept additional valid
   findings; a comparison filename is not proof of safety. Review scanner suppressions.
5. Run a separate source-only task without execution. Verify reasoned closure is
   distinct from executed proof.
6. Preserve sanitized observations, tool versions, blockers and contract changes.
   Record host/model identity when available, never infer or invent it.

The checked-in [evaluation](../docs/evaluation.md) records the run performed.
Repository pytest is a repeatable package/fixture check, not the independent
agent evaluation or a benchmark of detection rates.
