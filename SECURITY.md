# Security Policy

## Supported Versions

| Component | Version | Support |
|-----------|---------|---------|
| Open Grace Governance | 1.x | Active |
| Open Grace Runtime | 2.x | Active |
| Open Grace Registry DB | 1.x | Active |

## Reporting a Vulnerability

Report security issues affecting Open Grace packages to the WISE architecture office via your organization's standard security channel. Do not open public GitHub issues for undisclosed vulnerabilities.

Include:

- Affected package and version
- Reproduction steps or proof of concept
- Impact assessment (confidentiality, integrity, availability)

We aim to acknowledge reports within 5 business days.

## Supply Chain Controls

Open Grace uses the following automated controls (see `.github/workflows/open-grace-*.yml`):

- **CI tests** — `pytest tests/open_grace` on every relevant change
- **Dependency audit** — weekly `pip-audit` against installed Open Grace packages
- **SBOM** — CycloneDX SBOM generated on main branch pushes
- **Secret scan** — placeholder pattern scan; integrate organizational secret scanning

## Secure Development

- Governed agent execution uses pre-execution gates (capability, risk, benchmark)
- Constitutional agents are `read_only` by schema validation
- Registry changes require lifecycle FSM transitions and audit records
- JSON file stores are the default; PostgreSQL persistence is additive via `open-grace-registry-db`

## Dependencies

Open Grace packages pin minimum versions in `pyproject.toml`. Review dependency updates through the Open Grace CI and dependency audit workflows before merging.
