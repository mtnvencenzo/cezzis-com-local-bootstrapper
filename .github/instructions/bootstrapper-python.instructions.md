---
name: Bootstrapper Python Instructions
description: "Use when writing or reviewing Python source for the bootstrapper. Covers command-handler structure, option-driven bootstrapping, Injector wiring, and repo-standard validation."
applyTo: "src/cezzis_com_bootstrapper/**/*.py"
---

# Bootstrapper Python Instructions

- Keep the existing `application`, `domain`, and `infrastructure` layering intact.
- New bootstrapping behavior should usually be added as a concern-specific command and handler under `application/concerns/`.
- Register new handlers, options, and services in `src/cezzis_com_bootstrapper/app_module.py`.
- Keep `main.py` focused on runtime startup, option checks, and dispatching commands through `Mediator`.
- Preserve feature-flag-driven behavior through `BootstrapperOptions` and the related settings models under `domain/config/`.
- Put external integration logic behind the existing service interfaces in `infrastructure/services/`.
- Prefer async-friendly patterns that match the surrounding code when touching service or handler flows.
- Keep changes scoped to the requested concern. Avoid unrelated cleanup or broad restructuring.
- When Python code changes, run both `make standards` and `make test` before considering the work complete.