#!/usr/bin/env bash
# Copy locales/*.json into each packages/{ecosystem}/ at the path
# the ecosystem's package manifest expects. Idempotent.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/locales"

if [ ! -d "$SRC" ] || ! ls "$SRC"/*.json >/dev/null 2>&1; then
  echo "sync: no JSON files in locales/ — nothing to do"
  exit 0
fi

if [ ! -d "$ROOT/packages" ]; then
  echo "sync: packages/ directory missing — nothing to do"
  exit 0
fi

synced=0
for pkg_dir in "$ROOT/packages"/*/; do
  pkg="$(basename "$pkg_dir")"
  case "$pkg" in
    npm|composer|rubygems|nuget|hex|go)
      target="$pkg_dir/locales"
      ;;
    maven)
      target="$pkg_dir/src/main/resources/locales"
      ;;
    pypi)
      target="$pkg_dir/escalated_locale/locales"
      ;;
    *)
      echo "sync: skipping unknown package dir '$pkg'"
      continue
      ;;
  esac

  rm -rf "$target"
  mkdir -p "$target"
  cp -R "$SRC"/*.json "$target"/
  echo "sync: $pkg ← locales/"
  synced=$((synced + 1))
done

echo "sync: done ($synced package(s))"
