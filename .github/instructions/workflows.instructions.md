---
name: Workflow Instructions
description: "Use when writing or reviewing GitHub Actions workflows for this repo. Covers reusable workflow inputs, packaging alignment, release assumptions, and safe CI changes."
applyTo: ".github/workflows/**/*.{yml,yaml}"
---

# Workflow Instructions

- Keep workflow changes aligned with the repo's `makefile`, Poetry packaging, `Dockerfile`, and `.iac/` runtime assumptions.
- This repo uses reusable workflows from `mtnvencenzo/workflows`; preserve the existing contract for inputs, artifacts, versioning, and secrets unless the task explicitly requires changing it.
- When editing Python build inputs, keep them consistent with `pyproject.toml`, `pytest.ini`, `.ruff.toml`, and the actual source package path under `src/cezzis_com_bootstrapper/`.
- When editing artifact names or unpack paths, confirm they still match the package name and release expectations used later in the workflow.
- When editing Docker build or purge behavior, keep image repository names, tags, and ACR settings aligned with the container deployment manifests under `.iac/`.
- Avoid broad workflow cleanup that is unrelated to the requested behavior.
- Do not add commands that mutate external infrastructure unless the workflow change explicitly requires that behavior and the target is clear.