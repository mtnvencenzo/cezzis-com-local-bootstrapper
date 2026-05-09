---
name: Infrastructure Manifest Instructions
description: "Use when writing or reviewing Kubernetes, kustomization, or ArgoCD manifests under .iac for this repo. Covers environment alignment, image/runtime contract consistency, and safe validation guidance."
applyTo: ".iac/**/*.{yml,yaml}"
---

# Infrastructure Manifest Instructions

- Keep `.iac/k8s-loc/`, `.iac/k8s-cloudsync/`, and `.iac/argocd/` aligned when the runtime contract changes.
- Treat manifest changes as part of the bootstrapper contract, especially image names, config maps, secrets references, environment variables, and job execution behavior.
- When changing image names, tags, or packaging expectations, review `.github/workflows/cezzis-com-bootstrapper-cicd.yaml` and `Dockerfile` for consistency.
- Keep kustomization resources synchronized with the manifests they reference.
- Keep ArgoCD application and image updater manifests aligned with the environment-specific kustomize overlays they target.
- Avoid unrelated manifest cleanup or large reformatting passes.
- Do not run `kubectl apply` or `kubectl delete` against a real cluster unless the user explicitly asked for cluster execution and the target is clear.
- Prefer review-level validation such as checking resource references and generated image/runtime assumptions before considering the work complete.