#!/usr/bin/env python3
"""Fetch the live Kalligator OpenAPI schema and apply the docs overlay.

Usage: python3 scripts/sync_openapi.py [--source URL_OR_PATH]

The API owns the routes and types. `api-reference/overlay.json` owns the reader text:
titles, descriptions, servers, and examples. The output is `api-reference/openapi.json`.
"""
import argparse
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OVERLAY = ROOT / "api-reference" / "overlay.json"
OUTPUT = ROOT / "api-reference" / "openapi.json"
DEFAULT_SOURCE = "https://kalligator.com/api/openapi.json"


def load(source):
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=30) as response:
            return json.load(response)
    return json.loads(pathlib.Path(source).read_text())


def apply(spec, overlay):
    missing = []
    spec["info"].update(overlay["info"])
    spec["servers"] = overlay["servers"]
    spec["tags"] = overlay["tags"]
    for key, patch in overlay["operations"].items():
        method, path = key.split(" ", 1)
        operation = spec["paths"].get(path, {}).get(method.lower())
        if operation is None:
            missing.append(key)
            continue
        params = patch.pop("parameters", {})
        body = patch.pop("requestBody", None)
        operation.update(patch)
        for param in operation.get("parameters", []):
            if param["name"] in params:
                param.update(params[param["name"]])
        if body and "requestBody" in operation:
            operation["requestBody"].update(body)
    for name, patch in overlay["schemas"].items():
        schema = spec["components"]["schemas"].get(name)
        if schema is None:
            missing.append(f"schema {name}")
            continue
        for prop, text in patch.pop("properties", {}).items():
            if prop in schema.get("properties", {}):
                schema["properties"][prop]["description"] = text
            else:
                missing.append(f"{name}.{prop}")
        schema.update(patch)
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            if f"{method.upper()} {path}" not in overlay["operations"]:
                missing.append(f"undocumented {method.upper()} {path}")
    return missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    args = parser.parse_args()
    spec = load(args.source)
    overlay = json.loads(OVERLAY.read_text())
    missing = apply(spec, overlay)
    OUTPUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(spec['paths'])} paths)")
    if missing:
        print("Overlay entries that do not match the schema:", *missing, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
