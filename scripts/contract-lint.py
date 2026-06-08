#!/usr/bin/env python3
"""Lightweight contract lint for the orchestrator master repo.

This is v0 guardrail lint. It enforces stable cross-project constraints and
prints warnings for known Sprint 0 gaps that are tracked in feature_list.json.
Full OpenAPI/schema semantic consistency remains S0-36.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"

EXPECTED_OPENAPI = "3.1.0"
EXPECTED_SERVER_URL = "/api"
EXPECTED_PROVIDER_COUNT = 12

KNOWN_MISSING = {
    "contracts/openapi/chapter.yaml": "S0-09",
    "contracts/openapi/outline.yaml": "S0-10",
    "contracts/ai/routing-rules.yaml": "S0-14",
    "contracts/schemas/user.json": "S0-18",
}


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def print(self) -> None:
        for warning in self.warnings:
            print(f"WARN: {warning}")
        for error in self.errors:
            print(f"ERROR: {error}", file=sys.stderr)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_yaml(path: Path, reporter: Reporter) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - lint must explain file failures
        reporter.error(f"{rel(path)} cannot be parsed as YAML: {exc}")
        return None


def load_json(path: Path, reporter: Reporter) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - lint must explain file failures
        reporter.error(f"{rel(path)} cannot be parsed as JSON: {exc}")
        return None


def assert_required_paths(reporter: Reporter) -> None:
    required_existing = [
        CONTRACTS / "openapi" / "auth.yaml",
        CONTRACTS / "openapi" / "project.yaml",
        CONTRACTS / "openapi" / "ai.yaml",
        CONTRACTS / "schemas" / "project.json",
        CONTRACTS / "schemas" / "chapter.json",
        CONTRACTS / "schemas" / "outline.json",
        CONTRACTS / "ai" / "providers.json",
        CONTRACTS / "events" / "ai-stream.ts",
    ]
    for path in required_existing:
        if not path.exists():
            reporter.error(f"required contract file is missing: {rel(path)}")

    for path_text, task_id in KNOWN_MISSING.items():
        path = ROOT / path_text
        if not path.exists():
            reporter.warn(f"known Sprint 0 gap ({task_id}): {path_text} is missing")


def lint_openapi(reporter: Reporter) -> None:
    openapi_dir = CONTRACTS / "openapi"
    for path in sorted(openapi_dir.glob("*.yaml")):
        document = load_yaml(path, reporter)
        if not isinstance(document, dict):
            reporter.error(f"{rel(path)} must contain a YAML object")
            continue

        version = document.get("openapi")
        if version != EXPECTED_OPENAPI:
            reporter.error(f"{rel(path)} openapi must be {EXPECTED_OPENAPI}, got {version!r}")

        servers_text = json.dumps(document.get("servers", []), ensure_ascii=False)
        paths_text = json.dumps(document.get("paths", {}), ensure_ascii=False)
        if "/api/v1" in servers_text or "/api/v1" in paths_text:
            reporter.error(f"{rel(path)} servers/paths must not reference /api/v1")

        servers = document.get("servers")
        if not isinstance(servers, list) or not servers:
            reporter.error(f"{rel(path)} must define servers with url {EXPECTED_SERVER_URL}")
            continue

        urls = [server.get("url") for server in servers if isinstance(server, dict)]
        if EXPECTED_SERVER_URL not in urls:
            reporter.error(f"{rel(path)} servers must include url {EXPECTED_SERVER_URL}")

        paths = document.get("paths")
        if not isinstance(paths, dict) or not paths:
            reporter.error(f"{rel(path)} must define at least one path")


def lint_schemas(reporter: Reporter) -> None:
    schema_dir = CONTRACTS / "schemas"
    for path in sorted(schema_dir.rglob("*.json")):
        document = load_json(path, reporter)
        if not isinstance(document, dict):
            reporter.error(f"{rel(path)} must contain a JSON object")
            continue

        schema_url = document.get("$schema")
        if path.name != "providers.json" and schema_url != "https://json-schema.org/draft/2020-12/schema":
            reporter.error(f"{rel(path)} must use JSON Schema draft 2020-12")

        if document.get("type") != "object":
            reporter.error(f"{rel(path)} root type must be object")

        properties = document.get("properties")
        definitions = document.get("definitions") or document.get("$defs")
        if not isinstance(properties, dict) and not isinstance(definitions, dict):
            reporter.error(f"{rel(path)} must define properties, definitions, or $defs")


def lint_ai_providers(reporter: Reporter) -> None:
    path = CONTRACTS / "ai" / "providers.json"
    document = load_json(path, reporter)
    if not isinstance(document, dict):
        reporter.error(f"{rel(path)} must contain a JSON object")
        return

    providers = document.get("providers")
    if not isinstance(providers, list):
        reporter.error(f"{rel(path)} providers must be an array")
        return

    if len(providers) != EXPECTED_PROVIDER_COUNT:
        reporter.error(f"{rel(path)} must define {EXPECTED_PROVIDER_COUNT} providers, got {len(providers)}")

    keys: list[str] = []
    defaults = 0
    for provider in providers:
        if not isinstance(provider, dict):
            reporter.error(f"{rel(path)} provider entries must be objects")
            continue

        key = provider.get("key")
        if not isinstance(key, str) or not key:
            reporter.error(f"{rel(path)} provider key must be a non-empty string")
        else:
            keys.append(key)

        models = provider.get("models")
        if not isinstance(models, list) or not models:
            reporter.error(f"{rel(path)} provider {key!r} must define non-empty models")

        if provider.get("isDefault") is True:
            defaults += 1

    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    for key in duplicates:
        reporter.error(f"{rel(path)} duplicate provider key: {key}")

    if defaults != 1:
        reporter.error(f"{rel(path)} must define exactly one isDefault provider, got {defaults}")


def main() -> int:
    reporter = Reporter()
    assert_required_paths(reporter)
    lint_openapi(reporter)
    lint_schemas(reporter)
    lint_ai_providers(reporter)

    reporter.print()
    if reporter.errors:
        print(f"contract-lint failed: {len(reporter.errors)} error(s)", file=sys.stderr)
        return 1

    print("contract-lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
