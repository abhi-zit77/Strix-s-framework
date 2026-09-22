# Maintaining Strix Framewok

The installable skill is instruction-only. Python is required only for the optional
standalone installer and development checks. Work on the canonical package under
plugins/strix-framewok; do not duplicate workflows for each host.

## Validation

Create a task-local Python 3.12+ environment, then install development dependencies:

```bash
python -m venv .venv
# Activate .venv using your shell's standard activation command.
python -m pip install -r requirements-dev.txt
python scripts/validate_package.py
python -m ruff check .
python -m mypy
python -m bandit -r scripts evals/fixtures/safe -c pyproject.toml -ll
python -m pytest
```

The deliberately vulnerable fixture is excluded from the passing security audit;
its faults are exercised by semantic regression tests. No suppression covers the
installer, validator or safe controls. Fixtures contain only synthetic data,
never contact an external target, and are not
part of the installed plugin/skill. They are evaluation inputs, not application code.

When Claude Code is available, validate both the repository marketplace and plugin:

```bash
claude plugin validate . --strict
claude plugin validate plugins/strix-framewok --strict
```

Validate the Codex manifest with the skill-creator/plugin-creator tools available
in your host, or use the repository validator for portable structural checks.
Keep structural validation separate from live host loading and behavioral evidence.

## Upstream updates

Pin a new Strix commit explicitly. Compare the complete internal playbook inventory,
consumer skills, system prompt, runtime/reporting implementations and relevant tests.
Review each changed technique and its tool/version assumptions. Update adapted
references, attribution, source hashes, extraction matrix and section catalog together.
Do not import upstream scope assumptions, private tool calls or provider configuration
as executable requirements. Preserve the host-native evidence and permissions contracts.

Increment both plugin manifest versions and skill metadata. Re-run fixture tests and
independent skill-guided assessments on changed workflows. Document which host and
tool combinations actually ran; never turn a source review into a runtime pass.
