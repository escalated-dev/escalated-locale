#!/usr/bin/env python3
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = REPO_ROOT.parents[1]
PHP = Path(r"C:\Users\work\.config\herd\bin\php.bat")

SOURCE_REPOS = {
    "vue": WORK_ROOT / "escalated",
    "nestjs": WORK_ROOT / "escalated-nestjs",
    "laravel": WORK_ROOT / "escalated-laravel",
    "rails": WORK_ROOT / "escalated-rails",
    "django": WORK_ROOT / "escalated-django",
    "adonis": WORK_ROOT / "escalated-adonis",
    "symfony": WORK_ROOT / "escalated-symfony",
    "wordpress": WORK_ROOT / "escalated-wordpress",
    "phoenix": WORK_ROOT / "escalated-phoenix",
    "go": WORK_ROOT / "escalated-go",
    "spring": WORK_ROOT / "escalated-spring",
    "dotnet": WORK_ROOT / "escalated-dotnet",
    "filament": WORK_ROOT / "escalated-filament",
}

OUTPUT_DIR = REPO_ROOT / "locales"
INVENTORY_PATH = REPO_ROOT / "MIGRATION_NOTES.md"

COMPACT_CLUSTER = ("nestjs", "adonis", "symfony", "phoenix", "go", "spring", "dotnet")
LOCALE_ALIASES = {
    "de-DE": "de",
    "de_DE": "de",
    "es-ES": "es",
    "es_ES": "es",
    "fr-FR": "fr",
    "fr_FR": "fr",
    "it-IT": "it",
    "it_IT": "it",
    "ko-KR": "ko",
    "ko_KR": "ko",
    "nl-NL": "nl",
    "nl_NL": "nl",
    "pl-PL": "pl",
    "pl_PL": "pl",
    "pt_BR": "pt-BR",
    "ru-RU": "ru",
    "ru_RU": "ru",
    "tr-TR": "tr",
    "tr_TR": "tr",
    "zh_CN": "zh-CN",
    "zh-CN": "zh-CN",
}
SOURCE_PRIORITY = {
    "vue": 100,
    "laravel": 90,
    "filament": 85,
    "rails": 80,
    "adonis": 70,
    "nestjs": 65,
    "symfony": 64,
    "phoenix": 63,
    "go": 62,
    "spring": 61,
    "dotnet": 60,
    "django": 40,
    "wordpress": 30,
}


def normalize_locale(locale: str) -> str:
    return LOCALE_ALIASES.get(locale, locale.replace("_", "-"))


def snake_to_camel(text: str) -> str:
    if not text:
        return text
    if re.search(r"[\s\-]", text):
        parts = [p for p in re.split(r"[\s\-]+", text) if p]
        return parts[0][:1].lower() + parts[0][1:] + "".join(p[:1].upper() + p[1:] for p in parts[1:])
    if "_" not in text:
        return text[:1].lower() + text[1:]
    parts = [p for p in text.split("_") if p]
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def canonicalize_key(text: str) -> str:
    text = text.replace("%", " percent ")
    text = re.sub(r"[^A-Za-z0-9]+", " ", text).strip()
    if not text:
        return "value"
    parts = text.split()
    return parts[0].lower() + "".join(p[:1].upper() + p[1:].lower() for p in parts[1:])


def normalize_placeholders(value: str) -> str:
    value = re.sub(r"%\{([A-Za-z0-9_]+)\}", r"{\1}", value)
    value = re.sub(r"%\(([A-Za-z0-9_]+)\)s", r"{\1}", value)
    value = re.sub(r":([A-Za-z0-9_]+)", r"{\1}", value)
    value = re.sub(r"%([0-9]+)\$s", r"{arg\1}", value)
    value = value.replace("%s", "{value}")
    return value


def deep_copy(value):
    return json.loads(json.dumps(value, ensure_ascii=False))


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            out.update(flatten(value, next_prefix))
    else:
        out[prefix] = obj
    return out


def deep_merge(target, incoming):
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = deep_copy(value)


def set_nested(target, path, value):
    node = target
    for part in path[:-1]:
        node = node.setdefault(part, {})
    node[path[-1]] = value


def unflatten(flat):
    out = {}
    for dotted, value in flat.items():
        set_nested(out, dotted.split("."), value)
    return out


def canonicalize_tree(value):
    if isinstance(value, dict):
        return {snake_to_camel(str(key)): canonicalize_tree(child) for key, child in value.items()}
    if isinstance(value, list):
        return [canonicalize_tree(child) for child in value]
    if isinstance(value, str):
        return normalize_placeholders(value)
    return value


def canonicalize_flat_keys(flat):
    output = {}
    for dotted, value in flat.items():
        parts = [snake_to_camel(part) for part in dotted.split(".")]
        output[".".join(parts)] = normalize_placeholders(value) if isinstance(value, str) else value
    return output


def remap_compact_tree(data):
    mapped = {}
    for key, value in flatten(data).items():
        target = key
        if key.startswith("messages.") or key.startswith("message."):
            suffix = key.split(".", 1)[1]
            message_map = {
                "replySent": "ticket.replySent",
                "ticketAssigned": "ticket.assigned",
                "statusUpdated": "ticket.statusUpdated",
                "priorityUpdated": "ticket.priorityUpdated",
                "tagsUpdated": "ticket.tagsUpdated",
                "departmentUpdated": "ticket.departmentUpdated",
                "ticketCreated": "ticket.created",
                "ticketClosed": "ticket.closed",
                "ticketReopened": "ticket.reopened",
                "settingsUpdated": "settings.updated",
                "accessDenied": "common.accessDenied",
                "notFound": "common.notFound",
            }
            target = message_map.get(suffix, key)
        set_nested(mapped, target.split("."), value)
    return mapped


def parse_json_file(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_yaml_file(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_php_file(path: Path):
    code = (
        f"$data = include '{str(path).replace(chr(92), '/')}';"
        "echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);"
    )
    result = subprocess.run([str(PHP), "-r", code], capture_output=True, check=True)
    return json.loads(result.stdout.decode("utf-8", errors="replace"))


def parse_properties_file(path: Path):
    flat = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        match = re.match(r"([^=:\s][^=:]*?)\s*[:=]\s*(.*)$", line)
        if match:
            flat[match.group(1).strip()] = match.group(2)
    return flat


def parse_resx_file(path: Path):
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    flat = {}
    for data in root.findall("data"):
        name = data.attrib.get("name")
        value = data.findtext("value")
        if name and value is not None:
            if "_" in name:
                prefix, rest = name.split("_", 1)
                dotted = f"{prefix.lower()}.{snake_to_camel(rest)}"
            else:
                dotted = snake_to_camel(name)
            flat[dotted] = value
    return flat


def parse_po_entries(path: Path):
    entries = []
    msgid = None
    msgstr = None
    state = None
    comments = []

    def unquote(text: str) -> str:
        return bytes(text, "utf-8").decode("unicode_escape")

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("#"):
            comments.append(stripped)
            continue
        if stripped.startswith("msgid "):
            if msgid is not None and msgid != "":
                entries.append({"msgid": msgid, "msgstr": msgstr or "", "comments": comments})
            msgid = unquote(stripped[6:].strip()[1:-1])
            msgstr = ""
            state = "msgid"
            comments = []
            continue
        if stripped.startswith("msgstr "):
            msgstr = unquote(stripped[7:].strip()[1:-1])
            state = "msgstr"
            continue
        if stripped.startswith('"') and stripped.endswith('"'):
            piece = unquote(stripped[1:-1])
            if state == "msgid":
                msgid += piece
            elif state == "msgstr":
                msgstr += piece
    if msgid is not None and msgid != "":
        entries.append({"msgid": msgid, "msgstr": msgstr or "", "comments": comments})
    return entries


def build_po_key_map(master_entries, namespace):
    key_map = {}
    collisions = defaultdict(int)
    for entry in master_entries:
        msgid = entry["msgid"]
        if not msgid:
            continue
        base = canonicalize_key(msgid)
        collisions[base] += 1
        if collisions[base] == 1:
            key = base
        else:
            digest = hashlib.sha1(msgid.encode("utf-8")).hexdigest()[:6]
            key = f"{base}{digest}"
        key_map[msgid] = f"{namespace}.{key}"
    return key_map


class Builder:
    def __init__(self):
        self.locales = {}
        self.provenance = defaultdict(dict)
        self.conflicts = defaultdict(list)
        self.inventory_rows = []
        self.partial_locales = defaultdict(list)
        self.consolidated_paths = defaultdict(list)

    def ensure_locale(self, locale):
        self.locales.setdefault(locale, {})
        return self.locales[locale]

    def merge_dict(self, locale, repo, source_path, data):
        locale_data = self.ensure_locale(locale)
        for dotted, value in flatten(data).items():
            self._merge_value(locale, repo, source_path, dotted, value)

    def _merge_value(self, locale, repo, source_path, dotted, value):
        current = flatten(self.ensure_locale(locale))
        existing = current.get(dotted)
        provenance = self.provenance[locale].get(dotted)
        if existing is None:
            set_nested(self.locales[locale], dotted.split("."), value)
            self.provenance[locale][dotted] = {"repo": repo, "path": source_path}
            return
        if existing == value:
            return
        current_priority = SOURCE_PRIORITY.get(repo, 0)
        existing_priority = SOURCE_PRIORITY.get(provenance["repo"], 0) if provenance else -1
        if current_priority > existing_priority:
            set_nested(self.locales[locale], dotted.split("."), value)
            self.conflicts[locale].append(
                {
                    "key": dotted,
                    "keptRepo": repo,
                    "replacedRepo": provenance["repo"],
                    "keptValue": value,
                    "replacedValue": existing,
                }
            )
            self.provenance[locale][dotted] = {"repo": repo, "path": source_path}
        else:
            self.conflicts[locale].append(
                {
                    "key": dotted,
                    "keptRepo": provenance["repo"],
                    "replacedRepo": repo,
                    "keptValue": existing,
                    "replacedValue": value,
                }
            )

    def record_inventory(self, repo, path, fmt, locale, key_count):
        self.inventory_rows.append(
            {
                "repo": repo,
                "path": str(path),
                "format": fmt,
                "locale": locale,
                "keyCount": key_count,
            }
        )
        self.consolidated_paths[repo].append(str(path))

    def add_vue(self):
        locale_dir = SOURCE_REPOS["vue"] / "src" / "locales"
        for path in sorted(locale_dir.glob("*.json")):
            if path.name == "index.js":
                continue
            locale = normalize_locale(path.stem)
            data = canonicalize_tree(parse_json_file(path))
            self.record_inventory("vue", path, "json", locale, len(flatten(data)))
            self.merge_dict(locale, "vue", str(path), data)

    def add_laravel(self):
        lang_dir = SOURCE_REPOS["laravel"] / "resources" / "lang"
        for path in sorted(lang_dir.glob("*/*.php")):
            locale = normalize_locale(path.parent.name)
            file_key = snake_to_camel(path.stem)
            data = parse_php_file(path)
            if path.stem in ("messages", "enums"):
                mapped = canonicalize_tree(data)
            else:
                mapped = {file_key: canonicalize_tree(data)}
            self.record_inventory("laravel", path, "php", locale, len(flatten(canonicalize_tree(data))))
            self.merge_dict(locale, "laravel", str(path), mapped)

    def add_rails(self):
        locale_dir = SOURCE_REPOS["rails"] / "config" / "locales"
        for path in sorted(locale_dir.glob("*.yml")):
            locale = normalize_locale(path.stem)
            data = parse_yaml_file(path)
            scoped = data.get(path.stem, {})
            if "escalated" in scoped:
                scoped = scoped["escalated"]
            scoped = canonicalize_tree(scoped)
            self.record_inventory("rails", path, "yaml", locale, len(flatten(scoped)))
            self.merge_dict(locale, "rails", str(path), scoped)

    def add_filament(self):
        locale_dir = SOURCE_REPOS["filament"] / "resources" / "lang"
        for path in sorted(locale_dir.glob("*/*.php")):
            locale = normalize_locale(path.parent.name)
            data = {"filament": canonicalize_tree(parse_php_file(path))}
            self.record_inventory("filament", path, "php", locale, len(flatten(data)))
            self.merge_dict(locale, "filament", str(path), data)

    def add_compact_cluster(self):
        for repo in COMPACT_CLUSTER:
            if repo == "symfony":
                for path in sorted((SOURCE_REPOS[repo] / "translations").glob("messages.*.yaml")):
                    locale = normalize_locale(path.stem.split(".", 1)[1])
                    data = parse_yaml_file(path)
                    scoped = data.get(locale.replace("-", "_"), data.get(locale, data))
                    if "escalated" in scoped:
                        scoped = scoped["escalated"]
                    flat = flatten(scoped)
                    mapped = remap_compact_tree(unflatten(canonicalize_flat_keys(flat)))
                    self.record_inventory(repo, path, "yaml", locale, len(flat))
                    self.merge_dict(locale, repo, str(path), mapped)
            elif repo == "spring":
                for path in sorted((SOURCE_REPOS[repo] / "src" / "main" / "resources").glob("messages_*.properties")):
                    locale = normalize_locale(path.stem.replace("messages_", ""))
                    flat = parse_properties_file(path)
                    mapped = remap_compact_tree(unflatten(canonicalize_flat_keys(flat)))
                    self.record_inventory(repo, path, "properties", locale, len(flat))
                    self.merge_dict(locale, repo, str(path), mapped)
            elif repo == "dotnet":
                for path in sorted((SOURCE_REPOS[repo] / "src" / "Escalated" / "Resources").glob("Messages.*.resx")):
                    locale = normalize_locale(path.stem.replace("Messages.", ""))
                    flat = parse_resx_file(path)
                    mapped = remap_compact_tree(unflatten(canonicalize_flat_keys(flat)))
                    self.record_inventory(repo, path, "resx", locale, len(flat))
                    self.merge_dict(locale, repo, str(path), mapped)
            elif repo == "adonis":
                for path in sorted((SOURCE_REPOS[repo] / "resources" / "lang").glob("*/*.json")):
                    locale = normalize_locale(path.parent.name)
                    data = canonicalize_tree(parse_json_file(path))
                    if "labels" in data:
                        labels = data.pop("labels")
                        deep_merge(data, labels)
                    data = remap_compact_tree(data)
                    self.record_inventory(repo, path, "json", locale, len(flatten(data)))
                    self.merge_dict(locale, repo, str(path), data)
            elif repo == "nestjs":
                for path in sorted((SOURCE_REPOS[repo] / "src" / "i18n").glob("*/*.json")):
                    locale = normalize_locale(path.parent.name)
                    data = remap_compact_tree(canonicalize_tree(parse_json_file(path)))
                    self.record_inventory(repo, path, "json", locale, len(flatten(data)))
                    self.merge_dict(locale, repo, str(path), data)
            else:
                folder = "priv/locales" if repo == "phoenix" else "locales"
                for path in sorted((SOURCE_REPOS[repo] / folder).glob("*.json")):
                    locale = normalize_locale(path.stem)
                    data = remap_compact_tree(canonicalize_tree(parse_json_file(path)))
                    self.record_inventory(repo, path, "json", locale, len(flatten(data)))
                    self.merge_dict(locale, repo, str(path), data)

    def add_django(self):
        english_entries = parse_po_entries(SOURCE_REPOS["django"] / "escalated" / "locale" / "en" / "LC_MESSAGES" / "django.po")
        key_map = build_po_key_map(english_entries, "djangoStrings")
        for path in sorted((SOURCE_REPOS["django"] / "escalated" / "locale").glob("*/LC_MESSAGES/django.po")):
            locale = normalize_locale(path.parent.parent.name)
            entries = {entry["msgid"]: entry["msgstr"] or entry["msgid"] for entry in parse_po_entries(path)}
            data = {}
            for msgid, dotted in key_map.items():
                value = normalize_placeholders(entries.get(msgid, msgid))
                set_nested(data, dotted.split("."), value)
            self.record_inventory("django", path, "po", locale, len(key_map))
            self.merge_dict(locale, "django", str(path), data)

    def add_wordpress(self):
        master_entries = parse_po_entries(SOURCE_REPOS["wordpress"] / "languages" / "escalated.pot")
        key_map = build_po_key_map(master_entries, "wordpressStrings")
        pot_path = SOURCE_REPOS["wordpress"] / "languages" / "escalated.pot"
        master_data = {}
        for msgid, dotted in key_map.items():
            set_nested(master_data, dotted.split("."), normalize_placeholders(msgid))
        self.record_inventory("wordpress", pot_path, "pot", "template", len(key_map))
        self.merge_dict("en", "wordpress", str(pot_path), master_data)
        for path in sorted((SOURCE_REPOS["wordpress"] / "languages").glob("*.po")):
            locale = normalize_locale(path.stem.replace("escalated-", ""))
            entries = {entry["msgid"]: entry["msgstr"] or entry["msgid"] for entry in parse_po_entries(path)}
            data = {}
            for msgid, dotted in key_map.items():
                value = normalize_placeholders(entries.get(msgid, msgid))
                set_nested(data, dotted.split("."), value)
            self.record_inventory("wordpress", path, "po", locale, len(key_map))
            self.merge_dict(locale, "wordpress", str(path), data)

    def backfill_english_aliases(self):
        aliases = {
            "activity.snoozed": "activityType.snoozed",
            "activity.unsnoozed": "activityType.unsnoozed",
            "activity.ticketSplit": "activityType.ticketSplit",
            "common.accessDenied": "middleware.notAuthorized",
            "common.notFound": "middleware.notFound",
        }
        english = flatten(self.locales["en"])
        for target, source in aliases.items():
            if target not in english and source in english:
                set_nested(self.locales["en"], target.split("."), english[source])

    def add_sources(self):
        self.add_vue()
        self.add_laravel()
        self.add_rails()
        self.add_filament()
        self.add_compact_cluster()
        self.add_django()
        self.add_wordpress()
        self.backfill_english_aliases()

    def apply_english_fallbacks(self):
        english_flat = flatten(self.locales["en"])
        for locale, data in self.locales.items():
            if locale == "en":
                continue
            flat = flatten(data)
            missing = sorted(set(english_flat) - set(flat))
            for key in missing:
                set_nested(data, key.split("."), english_flat[key])
            if missing:
                self.partial_locales[locale] = missing

    def write_locales(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        for path in OUTPUT_DIR.glob("*.json"):
            path.unlink()
        counts = {}
        for locale, data in sorted(self.locales.items()):
            path = OUTPUT_DIR / f"{locale}.json"
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            counts[locale] = len(flatten(data))
        return counts

    def write_notes(self, counts):
        repo_summary = {}
        for row in self.inventory_rows:
            summary = repo_summary.setdefault(row["repo"], {"files": 0, "locales": set(), "keys": 0})
            summary["files"] += 1
            summary["locales"].add(row["locale"])
            summary["keys"] += row["keyCount"]
        lines = [
            "# Migration Notes",
            "",
            "## Inventory",
            "",
            "| Repo | Files | Locales | Total Keys |",
            "| --- | ---: | --- | ---: |",
        ]
        for repo in sorted(repo_summary):
            summary = repo_summary[repo]
            locales = ", ".join(sorted(summary["locales"]))
            lines.append(f"| `{repo}` | {summary['files']} | {locales} | {summary['keys']} |")
        lines.extend(
            [
                "",
                "## Canonical Decisions",
                "",
                "- Locale set normalized to `ar`, `de`, `en`, `es`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt-BR`, `ru`, `tr`, and `zh-CN`.",
                "- Placeholder syntax normalized to `{name}` across the canonical JSON files.",
                "- Vue locale values win on conflicting shared keys. Remaining conflicts are resolved by source priority: Laravel, Filament, Rails, compact backend cluster, Django, then WordPress.",
                "- Django gettext strings were consolidated under the `djangoStrings.*` namespace, using deterministic keys derived from the English `msgid` values.",
                "- WordPress gettext strings were consolidated under the `wordpressStrings.*` namespace, using deterministic keys derived from the English POT catalog.",
                "",
                "## Partial Locales",
                "",
            ]
        )
        if self.partial_locales:
            for locale, keys in sorted(self.partial_locales.items()):
                lines.append(f"- `{locale}`: {len(keys)} keys fallback to English.")
        else:
            lines.append("- None.")
        lines.extend(["", "## Divergences", ""])
        divergence_lines = 0
        for locale in sorted(self.conflicts):
            filtered = []
            seen = set()
            for conflict in self.conflicts[locale]:
                if conflict["keptRepo"] == conflict["replacedRepo"]:
                    continue
                sig = (conflict["key"], conflict["keptRepo"], conflict["replacedRepo"], conflict["keptValue"], conflict["replacedValue"])
                if sig in seen:
                    continue
                seen.add(sig)
                filtered.append(conflict)
            if not filtered:
                continue
            lines.append(f"### `{locale}`")
            for conflict in filtered[:25]:
                lines.append(
                    f"- `{conflict['key']}`: kept `{conflict['keptRepo']}` value over `{conflict['replacedRepo']}`."
                )
                divergence_lines += 1
            if len(filtered) > 25:
                lines.append(f"- Additional conflicts omitted: {len(filtered) - 25}.")
            lines.append("")
        if divergence_lines == 0:
            lines.append("- No conflicting keyed values required manual arbitration after namespacing.")
            lines.append("")
        lines.extend(["## Locale Counts", ""])
        for locale, count in sorted(counts.items()):
            lines.append(f"- `{locale}`: {count} keys")
        lines.extend(["", "## Consolidated Sources", ""])
        for repo in sorted(self.consolidated_paths):
            lines.append(f"### `{repo}`")
            for path in sorted(set(self.consolidated_paths[repo])):
                lines.append(f"- `{path}`")
            lines.append("")
        INVENTORY_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    builder = Builder()
    builder.add_sources()
    if "en" not in builder.locales:
        raise RuntimeError("English locale was not discovered.")
    builder.apply_english_fallbacks()
    counts = builder.write_locales()
    builder.write_notes(counts)
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise
