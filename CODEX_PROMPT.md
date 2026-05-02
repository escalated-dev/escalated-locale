# Prompt for Codex — bootstrap `escalated-dev/escalated-locale`

Paste this as-is into Codex. The repo already exists at `https://github.com/escalated-dev/escalated-locale` (currently empty except for a stub README and this file). Local clone: `C:\Users\work\escalated\escalated-locale\`.

---

## Context

You are working on the Escalated portfolio: a NestJS reference backend (`escalated-nestjs`), a shared Vue 3 frontend (`escalated`), and 11 framework plugins (Laravel, Rails, Django, Adonis, Symfony, WordPress, Phoenix, Go, Spring, .NET, Filament). Each plugin currently maintains its own translation/locale files in the framework's native i18n format. This causes drift — strings updated in one plugin don't propagate to the others.

The user has decided to centralize translations in a new repo `escalated-dev/escalated-locale` (this repo). The repo will be published as a versioned package to multiple ecosystem registries; each plugin will consume it as a dependency and merge it with its own framework-local overrides at i18n load time.

A separate agent will handle the per-plugin consumption PRs (i18n loader configuration, dep additions, override directories) — **you do not need to touch any plugin repo**. Your job is exclusively to populate this central repo.

## All repos in the portfolio (cloned locally)

```
C:\Users\work\escalated                    # Vue 3 frontend, shared
C:\Users\work\escalated-nestjs             # NestJS reference (canonical backend)
C:\Users\work\escalated-laravel            # Laravel plugin
C:\Users\work\escalated-rails              # Rails plugin
C:\Users\work\escalated-django             # Django plugin
C:\Users\work\escalated-adonis             # AdonisJS plugin
C:\Users\work\escalated-symfony            # Symfony plugin
C:\Users\work\escalated-wordpress          # WordPress plugin
C:\Users\work\escalated-phoenix            # Phoenix plugin
C:\Users\work\escalated-go                 # Go plugin
C:\Users\work\escalated-spring             # Spring Boot plugin
C:\Users\work\escalated-dotnet             # .NET plugin
C:\Users\work\escalated-filament           # Filament (wraps Laravel)
C:\Users\work\escalated-locale             # ← this repo (you work here)
```

The user has helper scripts you should read first to understand the current pattern:
- `C:\Users\work\gen_translations.py`
- `C:\Users\work\gen_all_translations.py`
- `C:\Users\work\gen_nestjs_tr.py`
- `C:\Users\work\gen_go_tr.py`
- `C:\Users\work\gen_nestjs_tr.py`
- Plus any other `gen_*.py` or `*_translations*.py` in `C:\Users\work\`

These suggest some translation codegen already exists. Read each, identify the canonical source they read from, and reuse it.

## Phase 1 — Discovery

Sweep every plugin repo for translation files. Locations vary by framework — check at minimum:

| Framework | Likely locations |
|---|---|
| Vue (escalated) | `src/locales/`, `src/lang/`, `lang/`, `i18n/` (JSON or JS modules, often via `vue-i18n`) |
| NestJS | `src/i18n/{locale}/*.json` (via `nestjs-i18n`) |
| Laravel | `lang/{locale}/*.php`, `lang/{locale}.json` |
| Rails | `config/locales/*.{yml,yaml}` |
| Django | `locale/{lang}/LC_MESSAGES/django.po` |
| AdonisJS | `resources/lang/{locale}/*.{json,yaml}`, `config/i18n.ts` |
| Symfony | `translations/messages.{locale}.{xliff,yaml,php}` |
| WordPress | `languages/*.{pot,po,mo}` |
| Phoenix | `priv/gettext/{locale}/LC_MESSAGES/*.po` |
| Go | `i18n/active.{locale}.{toml,yaml}` or any `translations/`, `locales/` dir |
| Spring | `src/main/resources/messages_{locale}.properties` or `i18n/` |
| .NET | `Resources/*.{resx,resw}` or `locales/*.json` |
| Filament | inherits from Laravel |

For each file found, capture: repo, path, format, locale, key count.

Report a compact inventory before moving on.

## Phase 2 — Canonical format

Convert all discovered translations to a **single canonical JSON format** at `locales/{locale}.json` in this repo. Use nested keys (UI namespace separation) — example structure:

```json
{
  "ticket": {
    "status": {
      "open": "Open",
      "closed": "Closed",
      "pending": "Pending review"
    },
    "actions": {
      "reply": "Reply",
      "assign": "Assign agent"
    }
  },
  "auth": {
    "login": "Sign in",
    "logout": "Sign out"
  },
  "validation": {
    "required": "{field} is required",
    "email": "{field} must be a valid email"
  }
}
```

Required locales (union of what's already supported across plugins, plus `en` as default):
- Determine from the discovery sweep. At minimum produce `en.json`. If multiple plugins ship translations for a locale, **merge** them — last-write-wins is wrong; instead reconcile so the most-recent / most-complete set is canonical. When two plugins disagree on a key's translation, pick the Vue frontend's value (it's the canonical surface) and flag the divergence in `MIGRATION_NOTES.md`.

If a key only exists in one plugin (e.g., a Rails-specific validation message), include it — it's still useful to centralize.

Decide a **key naming convention** and stick to it. Suggest: lowerCamelCase for keys, dot-separated namespaces (`ticket.status.open`).

## Phase 3 — Repo layout

Final layout to produce:

```
escalated-locale/
├── README.md                     # architecture doc (overwrite the stub)
├── CODEX_PROMPT.md               # leave this file in place
├── MIGRATION_NOTES.md            # log divergences, decisions, deprecated keys
├── locales/
│   ├── en.json
│   ├── fr.json
│   ├── es.json
│   └── ...
├── packages/
│   ├── npm/                      # @escalated-dev/locale
│   │   ├── package.json
│   │   ├── index.js              # exports the JSON + a helper t(key, locale, params)
│   │   ├── index.d.ts
│   │   └── README.md
│   ├── composer/                 # escalated-dev/locale
│   │   ├── composer.json
│   │   ├── src/Locale.php        # Composer autoload class wrapping the JSON
│   │   └── README.md
│   ├── rubygems/                 # escalated-locale gem
│   │   ├── escalated-locale.gemspec
│   │   ├── lib/escalated/locale.rb
│   │   └── README.md
│   ├── maven/                    # dev.escalated:escalated-locale
│   │   ├── pom.xml
│   │   ├── src/main/java/dev/escalated/locale/Locale.java
│   │   └── README.md
│   ├── nuget/                    # Escalated.Locale
│   │   ├── Escalated.Locale.csproj
│   │   ├── Locale.cs
│   │   └── README.md
│   ├── hex/                      # :escalated_locale
│   │   ├── mix.exs
│   │   ├── lib/escalated/locale.ex
│   │   └── README.md
│   ├── pypi/                     # escalated-locale (Django)
│   │   ├── pyproject.toml
│   │   ├── escalated_locale/__init__.py
│   │   └── README.md
│   └── go/                       # importable as github.com/escalated-dev/escalated-locale
│       ├── locale.go
│       └── README.md             # Go uses the repo root as the module; this dir is just for the loader
├── scripts/
│   └── sync.{sh|ps1}             # generates per-package embedded JSON copies from /locales
└── .github/workflows/
    ├── ci.yml                    # validate JSON, key parity across locales
    └── publish.yml               # on tag push, run the publish matrix
```

Each per-ecosystem wrapper should:
1. Embed the `locales/*.json` files at build time (copy them in via `scripts/sync.*`)
2. Expose a minimal loader API in that ecosystem's idiom — typically `getLocaleData(locale)` returning the parsed dict, plus optionally a `t(key, locale, params)` helper. Keep the wrapper thin — the per-plugin i18n loader will do the heavy lifting (interpolation, fallback, pluralization). The wrapper just delivers data.

## Phase 4 — Publishing CI

**Handled by a parallel agent.** Workflows under `.github/workflows/` (`publish.yml` + `ci.yml`) and `scripts/sync.{sh,ps1}` are being written separately and may already exist on `main` by the time you reach this phase. **Do not duplicate them.**

Your responsibility for this phase is limited to populating each `packages/{ecosystem}/` directory with:
- A correct, publishable manifest (`package.json`, `composer.json`, `*.gemspec`, `pom.xml`, `*.csproj`, `mix.exs`, `pyproject.toml`/`setup.py`, plus `go.mod`-equivalent — but Go uses the repo root, see below).
- Minimal loader code in that ecosystem's idiom (`getLocaleData(locale)` + optional `t()` helper).
- Embedded `locales/` directory (the sync script either generates this or the manifest declares the JSON files as package data — your call).

Add an additional ecosystem missed in the original layout: `packages/pypi/` for Django (Python), publishable to PyPI as `escalated-locale`.

If `scripts/sync.{sh,ps1}` already exists on `main` when you arrive, use it. If not, write a minimal version that copies `locales/*.json` into each `packages/*/locales/` directory; the CI agent will adapt the workflow to whatever sync scheme you settle on.

When you finish, each `packages/*/` should be in a "would publish cleanly if pushed to a tag" state — the publish workflow is already wired.

Add `.github/workflows/ci.yml` checks (the CI agent likely has these in place already):
1. Lint all JSON files for syntax.
2. Verify key parity: every key in `en.json` must exist in every other locale (warn on missing — don't fail).
3. Run `scripts/sync.*` and verify no diff.

## Phase 5 — Documentation

Overwrite `README.md` with:
- One-paragraph purpose
- Architecture diagram (text-based) showing: central repo → 6 ecosystem packages → consumed by plugins via dep manager
- "How to add a translation" — edit `locales/en.json`, then `scripts/sync.*`, commit, tag a release
- "How to add a locale" — copy `en.json` to `{locale}.json`, translate, sync, commit
- "Override pattern" — explain that plugins layer their own translations on top via the framework's i18n fallback chain
- Package consumption examples for each of the 6 ecosystems (just the import line + 2-3 lines of usage)
- Versioning policy (semver: major = key removal/rename, minor = new keys, patch = string updates)

Write `MIGRATION_NOTES.md` capturing:
- Decisions you made when reconciling divergent translations
- Keys that were deprecated or renamed during consolidation (so plugin agents know what to map)
- Any locales that were partial (and which keys were left in English as fallback)

## Phase 6 — Initial release

1. Commit everything in logical chunks (don't squash into one giant commit — one per phase is fine).
2. Push to `main`.
3. Tag `v0.1.0` and push the tag — this triggers the publish workflow.
4. Verify each ecosystem's package landed (check `npm view`, `packagist.org`, `rubygems.org`, etc.).
5. Open a tracking issue listing any ecosystems that didn't publish (missing secrets, etc.) so the user can configure them.

## Constraints

- **Do not touch any other repo.** Plugin consumption PRs are someone else's job.
- Do not invent translations — use only what's already in the plugins. If the source is incomplete, leave keys in English with a comment.
- The Vue frontend (`escalated`) is the most authoritative source when there's disagreement.
- Don't bypass git hooks. Don't force-push.
- If a publishing pipeline can't be set up cleanly (e.g., Maven Central requires GPG signing infrastructure that's not trivial in CI), document the gap in `MIGRATION_NOTES.md` and skip — the user will configure manually.
- Keep package wrapper code minimal — these are data containers, not feature libraries.
- **Commit and push frequently — do not batch.** After each meaningful step (discovery summary, locales scaffold, npm package, composer package, etc.), commit with a clear message and push to `main`. Don't sit on 50 files of work for a single end-of-task commit. The user explicitly prefers small, frequent commits over large batched ones.

## Report at the end

Output:
- Locales shipped + key count per locale
- Which ecosystem packages built/published successfully and which need manual setup
- v0.1.0 tag SHA
- Any divergence decisions you made (link to `MIGRATION_NOTES.md` sections)
- List of plugin repos and which translation files in each were consolidated (so the next agent knows what to delete or treat as override-only)
