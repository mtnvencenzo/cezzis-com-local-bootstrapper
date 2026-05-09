# Cezzis Bootstrapper Copilot Instructions

## Instruction Precedence

- Treat this file as the source of truth for required repo standards and development workflow.
- Treat scoped instruction files under `.github/instructions/` as authoritative for their matching files and domains.
- Use skills under `.github/skills/` as workflow helpers and reinforcement, not as the only place a required standard is defined.
- If a requirement appears in both a skill and these instructions, follow the stricter interpretation.

## Development Workflow

- Prefer the `makefile` for primary developer workflows when a target exists.
- Use `make install` for dependency installation.
- Use `make standards` for linting and formatting checks.
- Use `make test` for the main test run.
- Use `make coverage` when coverage output is needed.
- Use `make build` for packaging and build validation.
- Use `make models` only when OpenAPI-generated models are part of the requested work.
- For code changes, run both `make standards` and `make test` before considering the work complete.
- Treat `make standards` and `make test` as required quality gates because CI relies on clean linting, formatting, and test results.
- Poetry is part of the standard toolchain and is used directly by the `makefile`. Use direct `poetry` commands only when there is no matching `make` target or when the task explicitly requires Poetry.
- Do not default to ad hoc commands when the equivalent `make` target already exists.

## Core Stack

- Python 3.12
- Poetry for dependency management and packaging
- Mediatr for command dispatch
- Injector for dependency injection
- Pydantic Settings for configuration
- OpenTelemetry for tracing and instrumentation
- Azure Blob Storage integration for storage bootstrapping
- Kafka integration for eventing bootstrapping
- RabbitMQ Admin integration for messaging bootstrapping
- pytest, pytest-cov, and pytest-mock for tests
- Ruff for linting and formatting
- Pyright is configured in `pyproject.toml` and should be respected when changing typed code

## Project Shape

- Keep the existing layered structure: `application`, `domain`, and `infrastructure`.
- Dependency wiring belongs in `src/cezzis_com_bootstrapper/app_module.py`.
- Runtime orchestration belongs in `src/cezzis_com_bootstrapper/main.py`.
- Business behavior belongs in `application/concerns/...` using command handlers.
- Cross-cutting behavior belongs in `application/behaviors/...`.
- Configuration models belong in `domain/config/...`.
- Messaging and storage domain models belong in `domain/...`.
- External integrations and service implementations belong in `infrastructure/services/...`.
- Keep the bootstrapper modular by concern: storage, eventing, and messaging should stay independently toggleable through options.

## Environment And Infrastructure

- Local and cluster deployment assets live under `.iac/`.
- Kubernetes manifests for local and cloud-sync environments live under `.iac/k8s-loc/` and `.iac/k8s-cloudsync/`.
- ArgoCD application and image updater manifests live under `.iac/argocd/`.
- When changing runtime configuration, secrets, image names, job behavior, or environment variables, review the matching `.iac/` manifests for drift.
- Treat `.env` and `.env.loc` behavior as part of the local runtime contract when changing configuration loading.
- CI and release behavior are defined in `.github/workflows/cezzis-com-bootstrapper-cicd.yaml`; keep workflow assumptions aligned with packaging and artifact structure.

## Coding Patterns

- Follow the existing command-handler pattern built around Mediatr handlers.
- Keep orchestration in handlers and service abstractions, not in configuration models.
- Register new handlers and services through the existing Injector module pattern in `app_module.py`.
- Preserve feature-flag driven bootstrapping through `BootstrapperOptions` so concerns can be enabled or disabled independently.
- Reuse neighboring concern structure before introducing a new abstraction or package layout.
- Keep changes minimal and local. Do not refactor unrelated areas unless the task requires it.
- Prefer existing libraries and patterns already in the repo over introducing new dependencies or frameworks.

## Infrastructure And Deployment Standards

- Treat `.iac/` manifests as part of the application contract, not as detached deployment files.
- Keep kustomization resources, config maps, secrets references, job manifests, and ArgoCD application definitions aligned.
- When changing container runtime expectations, confirm that `Dockerfile`, workflow artifact packaging, and Kubernetes job manifests still agree.
- Avoid implicit cluster-changing commands such as `kubectl apply` or `kubectl delete` unless the user explicitly asked for execution against a target cluster.

## Testing Standards

- Run validation primarily through `make test`.
- For style-related validation, prefer `make standards`.
- After code changes, run both `make standards` and `make test`, not just one of them.
- Add or update tests when behavior changes.
- New command handlers should usually receive unit tests in `test/unit/` following the style of neighboring tests.
- Keep tests aligned with the implementation's actual configuration and async behavior instead of relying on machine-local assumptions.

## Documentation Standards

- Treat `README.md` as part of the repo contract for developer workflow, infrastructure expectations, and runtime usage.
- When code changes affect supported infrastructure, setup flow, required configuration, local workflow, build or test workflow, or deployment shape, review `README.md` for drift and update it when needed.
- During code review, treat stale or missing `README.md` updates for those changes as a review finding, not an optional follow-up.

## Practical Guidance For Copilot

- Before adding a new concern, inspect the nearest existing concern and follow its structure.
- When changing handlers or services, check for adjacent tests and mirror their style.
- When a `make` target exists for the task, use it instead of inventing a new command.
- If direct Poetry use is necessary, keep it consistent with the repo's existing Poetry-based workflow.
- Prefer ASCII-only edits unless the file already requires Unicode.
- Keep comments sparse and only add them when they clarify non-obvious logic.
- When implementing or reviewing changes that affect developer workflow or runtime behavior, perform a quick `README.md` drift check before finishing.