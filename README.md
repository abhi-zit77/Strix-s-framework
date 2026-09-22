# Strix Framewok

**Strix-derived security testing workflows inside Claude Code and Codex.**

Invoke the skill and the agent performs the authorized assessment with the tools
it has: source inspection, browser interaction, HTTP probes, available scanners,
evidence validation, reporting, and requested fixes. Playwright/MCP browser tools
work without replacing them with Strix's browser. No Strix runtime, cloud account,
or separate LLM API key is required. Your coding agent's account and usage limits
still apply.

The exact name is **`strix-framewok`**. The spelling is intentional.

## Install and invoke

### Exact `/strix-framewok` command in Claude Code

Clone this repository, then install the standalone skill:

```bash
git clone https://github.com/abhi-zit77/Strix-s-framework.git
cd Strix-s-framework
python scripts/install_skill.py --skills-dir ~/.claude/skills
```

On PowerShell, use `python scripts/install_skill.py --skills-dir "$env:USERPROFILE/.claude/skills"`.
For a project-only install, pass that project's `.claude/skills` directory instead.
The installer refuses to overwrite an existing installation. To update, review the
new package and replace the old skill folder yourself; do not retain two versions.

Start a new Claude Code session and invoke:

```text
/strix-framewok Audit this repository. Use available tools and report evidence and coverage gaps.
/strix-framewok Audit and fix security issues in this local app; verify the fixes.
```

### Claude Code marketplace

Inside Claude Code:

```text
/plugin marketplace add abhi-zit77/Strix-s-framework
/plugin install strix-framewok@strix-framework
```

Reload plugins or start a new session as prompted. Marketplace plugins are always
namespaced by Claude Code, so the marketplace command is:

```text
/strix-framewok:strix-framewok Audit this repository.
```

Use the standalone install above for the exact short `/strix-framewok` command.
This repository supplies a custom marketplace; it does not claim listing in
Anthropic's official marketplace. Both routes use the same skill files.

### Codex

Standalone installation from the cloned repository:

```bash
python scripts/install_skill.py --skills-dir ~/.agents/skills
```

On PowerShell, use `python scripts/install_skill.py --skills-dir "$env:USERPROFILE/.agents/skills"`.
For project scope, use the project's `.agents/skills` directory. Invoke using
Codex's native skill syntax:

```text
$strix-framewok Audit this repository with the available tools.
```

Codex plugin installation is also supported:

```bash
codex plugin marketplace add abhi-zit77/Strix-s-framework
codex plugin add strix-framewok@strix-framework
```

Use a new session if the installed skill is not visible. Codex has its own command
syntax; this package does not claim to register a custom bare slash command there.
Avoid installing both standalone and plugin copies in the same host unless you
deliberately want duplicate discovery entries.

## What the agent does

1. Establish authorized assets, identity, effect limits and available capabilities.
2. Map source or runtime surfaces and build a shared threat model.
3. Select applicable playbooks and expand their techniques into concrete tests.
4. Execute baselines, controlled probes, counterevidence and reproduction.
5. Record findings and coverage, including negative results and proof gaps.
6. When asked to fix, patch the real boundary and verify adverse and legitimate cases.
7. Reconcile coverage and deliver a report with actual evidence and limitations.

Audit is the default. Standard depth is the default; quick, deep and diff-scoped
requests are supported. Example authenticated request:

```text
/strix-framewok Assess https://staging.example.test within the supplied authorization.
Use the two test accounts already configured in this session. Exclude production,
real payments and destructive operations. Use the connected browser and terminal.
```

That URL is an example, not a test target. Supply your own authorized scope.

## Coverage and evidence

The package adapts **75 internal Strix playbooks**, including **29 vulnerability
families**, with frameworks, technologies, protocols, cloud, reconnaissance,
tooling, analysis and coordination guidance. It also maps Strix's nine consumer
skills. A playbook contains multiple techniques; these numbers are not a claim
that 75 executable tests run on every app.

Source-aware and URL-based testing, API contracts, roles/tenants, injection,
authentication, browser security, business logic, supply chain, AI/agent systems,
and framework-specific cases are selected by relevance. Cloud and specialist
techniques require suitable credentials, tools and scope.

Runtime-confirmed findings, static traces, dependency advisory matches and unresolved
hypotheses are distinct. Missing tools or credentials create explicit coverage gaps.
The skill uses permitted host subagents when helpful, or sequential specialist
passes when unavailable. Host permissions and policies remain authoritative.

This is a portable methodology, not the Strix engine or a benchmark-equivalent
replacement. Its Markdown contracts are agent instructions, not enforced runtime
security controls. See the evaluation report for what was actually exercised.

## Repository layout

```text
.claude-plugin/marketplace.json         Claude Code marketplace
.agents/plugins/marketplace.json        Codex marketplace
plugins/strix-framewok/
  .claude-plugin/plugin.json            Claude Code plugin manifest
  .codex-plugin/plugin.json             Codex plugin manifest
  skills/strix-framewok/
    SKILL.md                           Canonical skill entrypoint
    agents/openai.yaml                 Codex skill metadata
    references/                        Lifecycle, tool adapters and 75 playbooks
    assets/                            Evidence templates and source-section catalog
    LICENSE, NOTICE                    Attribution travels with standalone installs
docs/                                  Analysis, extraction matrix and evaluation
evals/fixtures/                        Isolated synthetic vulnerable/safe examples
scripts/                               Installation and package validation
tests/                                 Behavior and package regression checks
```

- [Read the skill](plugins/strix-framewok/skills/strix-framewok/SKILL.md)
- [Upstream analysis](docs/upstream-analysis.md)
- [Complete extraction matrix](docs/extraction-matrix.md)
- [Evaluation results](docs/evaluation.md)
- [Contributing and checks](CONTRIBUTING.md)

## Provenance

Derived from [usestrix/strix](https://github.com/usestrix/strix) at commit
`56e9ae982c2fdd00c7c0b9afc49af035470dd310`. Apache-2.0; modified references
carry source links and change notices. This project is independent of Strix.

Installation conventions follow [Claude Code skills](https://code.claude.com/docs/en/skills),
[Claude Code plugins](https://code.claude.com/docs/en/plugins),
[Codex skills](https://developers.openai.com/codex/skills/), and the
[Agent Skills specification](https://agentskills.io/specification).
