#!/usr/bin/env python3
"""Build framework-native locale artifacts from canonical locales/*.json.

Pure stdlib. Linux + Windows compatible. Run from anywhere.

Outputs (paths relative to repo root):
  - packages/rubygems/locales/{locale}.yml                                  (Rails I18n)
  - packages/pypi/escalated_locale/locale/{lang}/LC_MESSAGES/django.po+mo   (Django gettext)
  - packages/composer/translations/messages.{locale}.yaml                   (Symfony)
  - packages/composer/languages/escalated-{locale}.po+mo                    (WordPress)
  - packages/hex/priv/gettext/{locale}/LC_MESSAGES/escalated.po             (Phoenix gettext)
  - packages/maven/src/main/resources/META-INF/escalated/locale/messages_{locale}.properties  (Spring)

For .mo compilation, attempts msgfmt first; falls back to a pure-Python encoder.
"""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, Iterator, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = REPO_ROOT / "locales"

# Map BCP-47-ish locale (en, pt-BR, zh-CN) -> language tag used by gettext dirs.
# gettext directories conventionally use ll_CC with underscore. For Django and
# WordPress, language directory keys differ; keep the mapping flexible.
GETTEXT_LANG_MAP = {
    "en": "en",
    "ar": "ar",
    "de": "de",
    "es": "es",
    "fr": "fr",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "nl": "nl",
    "pl": "pl",
    "pt-BR": "pt_BR",
    "ru": "ru",
    "tr": "tr",
    "zh-CN": "zh_CN",
}

# WordPress uses locale codes like en_US, pt_BR, zh_CN. Map our short codes.
WP_LOCALE_MAP = {
    "en": "en_US",
    "ar": "ar",
    "de": "de_DE",
    "es": "es_ES",
    "fr": "fr_FR",
    "it": "it_IT",
    "ja": "ja",
    "ko": "ko_KR",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "pt-BR": "pt_BR",
    "ru": "ru_RU",
    "tr": "tr_TR",
    "zh-CN": "zh_CN",
}


# ----------------------------------------------------------------------------
# Loading + flattening
# ----------------------------------------------------------------------------

def load_locale(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(data: Dict[str, object], prefix: str = "") -> Iterator[Tuple[str, str]]:
    """Walk nested dict and yield (dot.path, leaf_value_as_str) pairs.

    Skips list values (locale data is dict-of-strings only). Non-string leaves
    are coerced to their JSON representation as a defensive fallback.
    """
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            yield from flatten(value, path)
        elif isinstance(value, str):
            yield path, value
        else:
            # Defensive: coerce to JSON repr so caller never sees a non-str.
            yield path, json.dumps(value, ensure_ascii=False)


# ----------------------------------------------------------------------------
# Output writers
# ----------------------------------------------------------------------------

def yaml_quote(s: str) -> str:
    """Quote a string for YAML scalar use. Always emits double-quoted form,
    safe for any content including colons, leading dashes, numerics, etc."""
    escaped = (
        s.replace("\\", "\\\\")
         .replace("\"", "\\\"")
         .replace("\n", "\\n")
         .replace("\r", "\\r")
         .replace("\t", "\\t")
    )
    return f"\"{escaped}\""


def write_nested_yaml(data: Dict[str, object], indent: int, out: list) -> None:
    """Write nested dict as YAML. `data` may have str leaves."""
    pad = "  " * indent
    for key, value in data.items():
        # YAML key: bare if it's a simple identifier, else quote.
        if key.replace("_", "").replace("-", "").isalnum():
            yaml_key = key
        else:
            yaml_key = yaml_quote(key)
        if isinstance(value, dict):
            out.append(f"{pad}{yaml_key}:")
            write_nested_yaml(value, indent + 1, out)
        elif isinstance(value, str):
            out.append(f"{pad}{yaml_key}: {yaml_quote(value)}")
        else:
            out.append(f"{pad}{yaml_key}: {yaml_quote(json.dumps(value, ensure_ascii=False))}")


def emit_rails_yaml(locale: str, data: Dict[str, object], out_dir: Path) -> Path:
    """Rails I18n YAML: top-level key = locale, then nested tree."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{locale}.yml"
    lines = [f"{locale}:"]
    write_nested_yaml(data, 1, lines)
    lines.append("")  # trailing newline
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def emit_symfony_yaml(locale: str, data: Dict[str, object], out_dir: Path) -> Path:
    """Symfony YAML translation: nested tree at top level (no locale key)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"messages.{locale}.yaml"
    lines: list = []
    write_nested_yaml(data, 0, lines)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def properties_escape_key(s: str) -> str:
    out = []
    for ch in s:
        if ch in (" ", "=", ":", "\\"):
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "".join(out)


def properties_escape_value(s: str) -> str:
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "".join(out)


def emit_spring_properties(locale: str, en_pairs: Iterable[Tuple[str, str]],
                           loc_pairs_map: Dict[str, str], out_dir: Path) -> Path:
    """Java properties file with flat dot.keys.

    Uses English keys as the source of truth (same set every locale). Falls
    back to English when a localized value is missing.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"messages_{locale}.properties"
    lines = [
        "# Auto-generated by scripts/build_native_artifacts.py — do not edit",
        f"# locale: {locale}",
        "",
    ]
    for key, en_value in en_pairs:
        value = loc_pairs_map.get(key, en_value)
        lines.append(f"{properties_escape_key(key)}={properties_escape_value(value)}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ----------------------------------------------------------------------------
# gettext PO + MO
# ----------------------------------------------------------------------------

def po_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
         .replace("\"", "\\\"")
         .replace("\n", "\\n")
         .replace("\t", "\\t")
    )


def write_po(path: Path, locale: str, domain: str,
             entries: Iterable[Tuple[str, str]]) -> None:
    """Write a gettext PO file.

    entries: iterable of (msgid, msgstr) pairs. msgid is the dot.path key.
    The English source string is included as a `#.` reference comment so
    translators see context.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '# Escalated locale catalog — auto-generated, do not edit manually.',
        f'# locale: {locale}, domain: {domain}',
        'msgid ""',
        'msgstr ""',
        '"Project-Id-Version: escalated-locale 0.1.0\\n"',
        f'"Language: {locale}\\n"',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: 8bit\\n"',
        '',
    ]
    for msgid, msgstr in entries:
        lines.append(f'msgid "{po_escape(msgid)}"')
        lines.append(f'msgstr "{po_escape(msgstr)}"')
        lines.append('')
    path.write_text("\n".join(lines), encoding="utf-8")


def encode_mo(messages: Dict[str, str]) -> bytes:
    """Encode a dict of msgid -> msgstr as a gettext .mo file.

    Format reference: https://www.gnu.org/software/gettext/manual/html_node/MO-Files.html
    The empty msgid carries the metadata header (Content-Type etc.).
    """
    # Always include the metadata header at empty key.
    if "" not in messages:
        messages = dict(messages)
        messages[""] = (
            "Project-Id-Version: escalated-locale 0.1.0\n"
            "MIME-Version: 1.0\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: 8bit\n"
        )

    # Sort by msgid (required by spec for hash-table lookup; safe even if
    # we don't emit a hash table).
    keys = sorted(messages.keys())
    n = len(keys)

    # Build encoded id and str blobs concatenated with NUL separators between
    # entries (spec requires each string to be NUL-terminated; we'll write
    # offsets pointing at start, length being the byte length excluding NUL).
    ids_data = b""
    strs_data = b""
    offsets = []
    for k in keys:
        msgid_b = k.encode("utf-8")
        msgstr_b = messages[k].encode("utf-8")
        offsets.append((len(ids_data), len(msgid_b), len(strs_data), len(msgstr_b)))
        ids_data += msgid_b + b"\x00"
        strs_data += msgstr_b + b"\x00"

    # Header is 7 * 4 bytes = 28 bytes. After the header we put two tables
    # (n entries x 2 ints each = 8 bytes per entry).
    header_size = 7 * 4
    ids_table_offset = header_size
    strs_table_offset = ids_table_offset + n * 8
    ids_blob_offset = strs_table_offset + n * 8
    strs_blob_offset = ids_blob_offset + len(ids_data)

    # Build tables.
    ids_table = b""
    strs_table = b""
    for id_off, id_len, str_off, str_len in offsets:
        ids_table += struct.pack("<II", id_len, ids_blob_offset + id_off)
        strs_table += struct.pack("<II", str_len, strs_blob_offset + str_off)

    # Header: magic, version, n_strings, ids_table_offset, strs_table_offset,
    # hash_table_size (0 = no hash table), hash_table_offset (0).
    header = struct.pack(
        "<IIIIIII",
        0x950412DE,        # magic (little-endian)
        0,                 # version
        n,                 # number of strings
        ids_table_offset,
        strs_table_offset,
        0,                 # hash table size
        0,                 # hash table offset
    )

    return header + ids_table + strs_table + ids_data + strs_data


def compile_mo(po_path: Path, mo_path: Path,
               messages: Dict[str, str]) -> str:
    """Compile a .mo from messages. Returns 'msgfmt' or 'python'.

    Tries msgfmt first (system gettext-tools). Falls back to in-Python encoder.
    """
    msgfmt = shutil.which("msgfmt")
    if msgfmt:
        try:
            subprocess.run(
                [msgfmt, "-o", str(mo_path), str(po_path)],
                check=True,
                capture_output=True,
            )
            return "msgfmt"
        except (subprocess.CalledProcessError, OSError):
            pass  # fall through to Python encoder

    mo_path.parent.mkdir(parents=True, exist_ok=True)
    mo_path.write_bytes(encode_mo(messages))
    return "python"


# ----------------------------------------------------------------------------
# Entry-point logic per gap
# ----------------------------------------------------------------------------

def collect_locales() -> Dict[str, Dict[str, object]]:
    return {
        p.stem: load_locale(p)
        for p in sorted(LOCALES_DIR.glob("*.json"))
    }


def main() -> int:
    if not LOCALES_DIR.exists():
        print(f"locales/ missing at {LOCALES_DIR}", file=sys.stderr)
        return 1

    locales = collect_locales()
    if "en" not in locales:
        print("locales/en.json missing — required as English source", file=sys.stderr)
        return 1

    en_pairs_list = list(flatten(locales["en"]))
    en_pairs_map = dict(en_pairs_list)

    # Output dirs (relative to REPO_ROOT).
    rails_dir = REPO_ROOT / "packages" / "rubygems" / "locales"
    symfony_dir = REPO_ROOT / "packages" / "composer" / "translations"
    spring_dir = (
        REPO_ROOT / "packages" / "maven" / "src" / "main" / "resources"
        / "META-INF" / "escalated" / "locale"
    )
    pypi_locale_root = REPO_ROOT / "packages" / "pypi" / "escalated_locale" / "locale"
    wp_dir = REPO_ROOT / "packages" / "composer" / "languages"
    phoenix_root = REPO_ROOT / "packages" / "hex" / "priv" / "gettext"

    # Clean stale outputs we own *without* touching JSON files copied by sync.
    # rails_dir is shared with sync (which copies *.json there); only remove .yml.
    if rails_dir.exists():
        for p in rails_dir.glob("*.yml"):
            p.unlink()
    # The other dirs are exclusively ours; safe to wipe entirely.
    for d in (symfony_dir, spring_dir, pypi_locale_root, wp_dir, phoenix_root):
        if d.exists():
            shutil.rmtree(d)

    mo_methods = set()

    for locale, data in locales.items():
        loc_pairs_map = dict(flatten(data))

        # Rails YAML (nested under locale key).
        emit_rails_yaml(locale, data, rails_dir)

        # Symfony YAML (nested, no locale top-key).
        emit_symfony_yaml(locale, data, symfony_dir)

        # Spring properties (flat dot keys).
        emit_spring_properties(locale, en_pairs_list, loc_pairs_map, spring_dir)

        # PO entries: msgid is the dot.path key, msgstr is the localized value
        # (fall back to English so every key has *some* string).
        po_entries = [
            (key, loc_pairs_map.get(key, en_value))
            for key, en_value in en_pairs_list
        ]
        po_messages_for_mo = {key: msgstr for key, msgstr in po_entries}

        # Django: po + mo at packages/pypi/escalated_locale/locale/{lang}/LC_MESSAGES/django.{po,mo}
        django_lang = GETTEXT_LANG_MAP.get(locale, locale)
        django_po = pypi_locale_root / django_lang / "LC_MESSAGES" / "django.po"
        django_mo = django_po.with_suffix(".mo")
        write_po(django_po, locale, "django", po_entries)
        mo_methods.add(compile_mo(django_po, django_mo, po_messages_for_mo))

        # Phoenix: po only at packages/hex/priv/gettext/{locale}/LC_MESSAGES/escalated.po
        phoenix_lang = GETTEXT_LANG_MAP.get(locale, locale)
        phoenix_po = phoenix_root / phoenix_lang / "LC_MESSAGES" / "escalated.po"
        write_po(phoenix_po, locale, "escalated", po_entries)

        # WordPress: po + mo at packages/composer/languages/escalated-{wp_locale}.{po,mo}
        wp_locale = WP_LOCALE_MAP.get(locale, locale)
        wp_po = wp_dir / f"escalated-{wp_locale}.po"
        wp_mo = wp_po.with_suffix(".mo")
        write_po(wp_po, locale, "escalated", po_entries)
        mo_methods.add(compile_mo(wp_po, wp_mo, po_messages_for_mo))

    print(f"Built native artifacts for {len(locales)} locales.")
    print(f"  Rails YAML       -> {rails_dir.relative_to(REPO_ROOT)}/<locale>.yml")
    print(f"  Symfony YAML     -> {symfony_dir.relative_to(REPO_ROOT)}/messages.<locale>.yaml")
    print(f"  Spring props     -> {spring_dir.relative_to(REPO_ROOT)}/messages_<locale>.properties")
    print(f"  Django po+mo     -> {pypi_locale_root.relative_to(REPO_ROOT)}/<lang>/LC_MESSAGES/django.{{po,mo}}")
    print(f"  WordPress po+mo  -> {wp_dir.relative_to(REPO_ROOT)}/escalated-<wp_locale>.{{po,mo}}")
    print(f"  Phoenix po       -> {phoenix_root.relative_to(REPO_ROOT)}/<locale>/LC_MESSAGES/escalated.po")
    print(f"  .mo compiler(s)  -> {', '.join(sorted(mo_methods)) or '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
