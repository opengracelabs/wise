# Open Grace Supply Chain Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Scope** | OpenSSF-aligned CI controls for Open Grace packages |

## Summary

Sprint 1 establishes baseline OpenSSF supply-chain practices for the Open Grace Agent System through dedicated GitHub Actions workflows and a root `SECURITY.md` policy.

## Controls Implemented

| OpenSSF Practice | Artifact |
|------------------|----------|
| Automated testing | `.github/workflows/open-grace-ci.yml` |
| Dependency vulnerability scanning | `.github/workflows/open-grace-dependency-audit.yml` (`pip-audit`) |
| SBOM generation | `.github/workflows/open-grace-sbom.yml` (CycloneDX via `cyclonedx-py`) |
| Secret scanning | `.github/workflows/open-grace-secret-scan.yml` (placeholder pattern scan) |
| Vulnerability disclosure policy | `SECURITY.md` |

## Workflow Triggers

| Workflow | Trigger |
|----------|---------|
| Open Grace CI | PR/push to `main` when `packages/open-grace-*` or `tests/open_grace/` change |
| Dependency audit | Weekly Monday 06:00 UTC, manual, PR on `pyproject.toml` changes |
| SBOM | Push to `main` on Open Grace `pyproject.toml` changes, manual |
| Secret scan | Weekly Monday 07:00 UTC, manual, PR on Open Grace paths |

## Package Isolation

Each Open Grace package maintains an independent `pyproject.toml`:

- `open-grace-governance`
- `open-grace-agent-registry`
- `open-grace-benchmarking`
- `open-grace-audit`
- `open-grace-knowledge`
- `open-grace-observability`
- `open-grace-runtime`
- `open-grace-registry-db` (new)

## Gaps Remaining

| Gap | OpenSSF alignment | Priority |
|-----|-------------------|----------|
| SLSA provenance attestations | SLSA Build L2+ | High |
| Sigstore artifact signing | Signed releases | High |
| Model weight provenance on `ModelRegistryRecord` | AI supply chain | High |
| Organizational secret scanner (Gitleaks/GitHub Advanced Security) | Secret detection | Medium |
| OSV-Scanner as alternative to pip-audit | Vulnerability DB breadth | Low |

## Score Impact Estimate

OpenSSF maturity in the standards audit was **34/100**. With SBOM, pip-audit gate, CI isolation, and SECURITY.md, estimated revised score: **58/100** (+24 points on the OpenSSF dimension).

*Implementation report. Does not modify canonical architecture.*
