#!/usr/bin/env python3
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = REPO_ROOT / "locales"


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            out.update(flatten(value, next_prefix))
    else:
        out[prefix] = obj
    return out


def main():
    locale_files = sorted(LOCALES_DIR.glob("*.json"))
    if not locale_files:
        raise RuntimeError("No locale files found.")
    locales = {}
    for path in locale_files:
        locales[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    english_keys = set(flatten(locales["en"]))
    warnings = []
    for locale, data in sorted(locales.items()):
        if locale == "en":
            continue
        keys = set(flatten(data))
        missing = sorted(english_keys - keys)
        if missing:
            warnings.append(f"{locale}: missing {len(missing)} keys compared to en")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("All locales match English key parity.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
