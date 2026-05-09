---
name: add-bootstrapper-concern
description: 'Add or change a bootstrapper concern using this repo''s existing Mediatr, Injector, Pydantic Settings, service abstraction, and infrastructure-manifest patterns. Use for new bootstrapping concerns, handler changes, option changes, DI wiring, runtime orchestration updates, tests, and matching .iac updates.'
argument-hint: 'Describe the concern to add or change, the affected service or infrastructure, whether new configuration is needed, and whether .iac manifests or workflow changes are required.'
user-invocable: true
---

# Add Bootstrapper Concern

Use this skill when adding or changing a bootstrapper feature slice in this repo.

This skill is for changes that span one or more of the following:
- command and handler updates under `src/cezzis_com_bootstrapper/application/concerns/`
- configuration changes under `src/cezzis_com_bootstrapper/domain/config/`
- dependency wiring in `src/cezzis_com_bootstrapper/app_module.py`
- runtime orchestration in `src/cezzis_com_bootstrapper/main.py`
- service interfaces and implementations under `src/cezzis_com_bootstrapper/infrastructure/services/`
- tests under `test/unit/`
- matching `.iac/` manifest changes when runtime expectations, config, or deployment shape change

## When To Use

Use this skill for:
- a new bootstrapping concern such as another storage, messaging, or eventing dependency
- a change to how an existing concern is configured or executed
- a new settings model or environment-driven feature flag
- a new service abstraction or implementation used by a handler
- a runtime change that also needs Kubernetes, ArgoCD, Docker, or workflow updates

## Repository-Specific Rules

- Prefer the `makefile` for validation and primary workflows.
- Use `make test` for the main test run.
- Use `make standards` for linting and formatting.
- Use direct `poetry` commands only when there is no matching `make` target or the task explicitly requires Poetry.
- Keep runtime orchestration in `main.py` thin and focused on startup plus concern dispatch.
- Put concern logic in handlers and services, not in `main.py`.
- Register new handlers, options, and services in `src/cezzis_com_bootstrapper/app_module.py`.
- Keep concern toggles explicit through settings in `domain/config/`.
- When runtime behavior, image assumptions, secrets, or environment variables change, review `.iac/` manifests and CI workflow files for drift.
- When the change affects developer workflow or supported infrastructure, review `README.md` for drift and update it if needed.

## Delivery Procedure

### 1. Anchor On A Neighboring Concern

Start from the nearest existing concern that matches the requested behavior.

Good reference surfaces in this repo include:
- RabbitMQ under `application/concerns/messaging/`
- Kafka under `application/concerns/eventing/`
- Blob Storage under `application/concerns/storage/`

Do not invent a new structure if the repo already has a matching concern pattern.

### 2. Decide The Minimal Slice

Identify whether the change needs:
- a new or updated command and handler
- a new or updated options model
- service interface or implementation changes
- dependency wiring in `app_module.py`
- startup orchestration updates in `main.py`
- test changes under `test/unit/`
- `.iac/` manifest updates
- `README.md` updates

Prefer the smallest slice that fully implements the behavior.

### 3. Implement In Repo Order

For a typical concern change, apply changes in this order:

1. domain configuration or service interface prerequisites
2. command and handler changes under `application/concerns/`
3. service implementation changes under `infrastructure/services/`
4. dependency registration in `app_module.py`
5. runtime orchestration in `main.py` if startup flow changes
6. unit tests under `test/unit/`
7. `.iac/` manifest, Docker, or workflow updates when runtime expectations changed
8. `README.md` updates when behavior or workflow documentation changed

### 4. Handler And Runtime Expectations

When editing handlers and startup flow:
- keep handlers focused on one concern
- keep `main.py` responsible for sequencing enabled concerns, not implementing their details
- preserve structured configuration loading through settings models
- keep service-specific logic behind interfaces where the repo already does so

### 5. Infrastructure Alignment

If the change affects deployment or execution:
- review `.iac/k8s-loc/` and `.iac/k8s-cloudsync/` for matching environment variable, config map, and job changes
- review `.iac/argocd/` manifests if ArgoCD targets or sync inputs changed
- review `.github/workflows/cezzis-com-bootstrapper-cicd.yaml` and `Dockerfile` if build or image behavior changed

### 6. Tests And Validation

For changed behavior:
- add or update unit tests under `test/unit/`
- mirror the style of nearby tests and concern handlers
- run `make standards`
- run `make test`

## Review Checklist

Before finishing, verify:
- the change matches an existing repo pattern instead of introducing a new architecture
- `app_module.py` contains any needed wiring
- `main.py` remains a thin orchestrator
- settings live in `domain/config/` when new configuration is introduced
- tests were added at the same boundary as neighboring concerns
- `.iac/`, workflow, or Docker files were updated when the runtime contract changed
- `README.md` was reviewed for drift when behavior or workflow changed

## Expected Output Quality

The final implementation should feel like it was added by the same team that wrote the surrounding code:
- same handler structure
- same Injector wiring style
- same option-loading approach
- same infrastructure alignment
- same validation workflow