# Adding translations

## How To Add A Translation

1. Update the source translation in the portfolio repo, or edit `locales/en.json` directly if the central package is now the canonical owner.
2. Run `python scripts/build_locales.py` (regenerates the canonical JSON from upstream sources, if needed).
3. Run the sync script: `bash scripts/sync.sh` (Linux/macOS/git-bash) or `pwsh ./scripts/sync.ps1` (Windows). Both write the same outputs — JSON copies into each `packages/*/` plus framework-native artifacts (Rails YAML, Django/WP gettext, Symfony YAML, Spring properties, Phoenix .po) via `scripts/build_native_artifacts.py`.
4. Commit the locale changes and the synced package copies.
5. Tag a release when the bundle is ready to publish.

## How To Add A Locale

1. Copy `locales/en.json` to `locales/{locale}.json`.
2. Translate the values.
3. Run `bash scripts/sync.sh` (or `pwsh ./scripts/sync.ps1`).
4. Commit the new locale and synced package copies.
