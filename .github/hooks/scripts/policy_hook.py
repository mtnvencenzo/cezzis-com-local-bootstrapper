#!/usr/bin/env python3
import json
import re
import sys
from typing import Any


def deep_find(value: Any, target_keys: set[str], found: list[Any]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in target_keys:
                found.append(item)
            deep_find(item, target_keys, found)
    elif isinstance(value, list):
        for item in value:
            deep_find(item, target_keys, found)


def json_out(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload))


raw = sys.stdin.read()

try:
    data = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    data = {}

event_candidates: list[Any] = []
deep_find(data, {"hookEventName", "eventName"}, event_candidates)
event_name = next((str(item) for item in event_candidates if item), "")

tool_candidates: list[Any] = []
deep_find(data, {"toolName", "tool_name", "recipient_name"}, tool_candidates)
tool_name = next((str(item) for item in tool_candidates if item), "")

command_candidates: list[Any] = []
deep_find(data, {"command"}, command_candidates)
commands = [str(item) for item in command_candidates if isinstance(item, str)]
combined_commands = "\n".join(commands)

path_candidates: list[Any] = []
deep_find(data, {"filePath", "path", "filePaths"}, path_candidates)
paths_text = raw + "\n" + "\n".join(str(item) for item in path_candidates)


def pretool_response(reason: str) -> None:
    json_out(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        }
    )


if event_name == "PreToolUse":
    kubectl_mutation = re.search(
        r"(^|\s)kubectl\s+(apply|delete|replace|patch)($|\s)",
        combined_commands,
        re.IGNORECASE,
    )
    argocd_mutation = re.search(
        r"(^|\s)argocd\s+app\s+(create|delete|set|sync)($|\s)",
        combined_commands,
        re.IGNORECASE,
    )

    if kubectl_mutation:
        pretool_response(
            "Cluster-mutating kubectl commands should not run by default. Only proceed if the target cluster is clear and the user explicitly asked for execution."
        )
        sys.exit(0)

    if argocd_mutation:
        pretool_response(
            "ArgoCD app mutations affect deployment state. Confirm the target app and intent before proceeding."
        )
        sys.exit(0)

if event_name == "PostToolUse":
    code_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"src/.*\.py|test/.*\.py", paths_text, re.IGNORECASE
    )
    infra_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.iac/.*\.(yml|yaml)", paths_text, re.IGNORECASE
    )
    workflow_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.github/workflows/.*\.(yml|yaml)", paths_text, re.IGNORECASE
    )

    messages: list[str] = []
    if code_touched:
        messages.append(
            "Code files changed. Before finishing, run both `make standards` and `make test`; they are the repo's required quality gates."
        )
    if infra_touched:
        messages.append(
            "Infrastructure manifests changed. Before finishing, review `.iac/k8s-loc/`, `.iac/k8s-cloudsync/`, and `.iac/argocd/` for environment alignment and referenced resource drift."
        )
    if workflow_touched:
        messages.append(
            "Workflow files changed. Before finishing, confirm the workflow still matches the repo's packaging, Docker, and `.iac/` runtime assumptions."
        )

    if messages:
        json_out({"systemMessage": "\n".join(messages)})
        sys.exit(0)

json_out({})
