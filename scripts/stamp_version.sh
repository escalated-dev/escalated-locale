#!/usr/bin/env bash
# Patches the version in every ecosystem manifest to match $VERSION.
# Called from the Publish workflow so the tag (e.g. v0.1.8 -> 0.1.8) is the
# single source of truth and ecosystems can't drift out of sync.
#
# Usage: scripts/stamp_version.sh 0.1.8
set -euo pipefail

VERSION="${1:?usage: stamp_version.sh <version>}"

# Resolve to the repo root (one level above this script).
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

echo "Stamping version $VERSION into ecosystem manifests"

# npm — "version": "x.y.z"
sed -i.bak -E "s/(\"version\"[[:space:]]*:[[:space:]]*\")[^\"]+(\")/\1${VERSION}\2/" packages/npm/package.json

# nuget — <Version>x.y.z</Version> (only the package's own Version, not PackageReference Version)
sed -i.bak -E "s|<Version>[^<]+</Version>|<Version>${VERSION}</Version>|" packages/nuget/Escalated.Locale.csproj

# pypi — version = "x.y.z"
sed -i.bak -E "s/^(version[[:space:]]*=[[:space:]]*\")[^\"]+(\")/\1${VERSION}\2/" packages/pypi/pyproject.toml

# maven — first <version>x.y.z</version> only (the project's own; later <version> entries are deps)
# Use awk to replace only the first occurrence to avoid touching dependency versions.
awk -v v="$VERSION" '
  /<version>[^<]+<\/version>/ && !done {
    sub(/<version>[^<]+<\/version>/, "<version>" v "</version>")
    done = 1
  }
  { print }
' packages/maven/pom.xml > packages/maven/pom.xml.tmp && mv packages/maven/pom.xml.tmp packages/maven/pom.xml

# rubygems — spec.version = "x.y.z"
sed -i.bak -E "s/(spec\.version[[:space:]]*=[[:space:]]*\")[^\"]+(\")/\1${VERSION}\2/" packages/rubygems/escalated-locale.gemspec

# hex — version: "x.y.z"
sed -i.bak -E "s/(version:[[:space:]]*\")[^\"]+(\")/\1${VERSION}\2/" packages/hex/mix.exs

# Cleanup sed backup files.
find packages -name '*.bak' -type f -delete

echo "Done. Updated versions:"
grep -E "(\"version\"|<Version>|^version |spec\.version|version: |<version>0)" \
  packages/npm/package.json \
  packages/nuget/Escalated.Locale.csproj \
  packages/pypi/pyproject.toml \
  packages/maven/pom.xml \
  packages/rubygems/escalated-locale.gemspec \
  packages/hex/mix.exs \
  | grep -v 'PackageReference\|jackson\|central-publishing\|setuptools' \
  || true
