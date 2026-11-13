# Architecture

`escalated-locale` is the central source of truth for Escalated translations. It consolidates locale catalogs from the Vue frontend and the framework plugins into a single canonical `locales/{locale}.json` set, then republishes that data through thin ecosystem-specific packages.

## Architecture

```text
portfolio source repos
  -> escalated-locale/locales/*.json
     -> npm package        (@escalated-dev/locale)
     -> Composer package   (escalated-dev/locale)
     -> RubyGem            (escalated-locale)
     -> PyPI package       (escalated-locale)
     -> Maven package      (dev.escalated:escalated-locale)
     -> NuGet package      (Escalated.Locale)
     -> Hex package        (:escalated_locale)
     -> Go module          (github.com/escalated-dev/escalated-locale/packages/go)
        -> consumed by framework plugins
           -> merged with repo-local overrides at app boot
```

## Override Pattern

Each plugin should load the package locale data first, then layer its own framework-local overrides on top. The plugin remains free to keep framework-specific translations or emergency patches in its own repo; the central package provides the base catalog and fallback chain.

## Conventions

- **Locale set**: `ar`, `de`, `en`, `es`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt-BR`, `ru`, `tr`, `zh-CN`. New locales are added by copying `en.json`.
- **Placeholder syntax**: `{name}` (curly-brace named tokens, e.g. `"Welcome {firstName}"`). The wrapper `t()` helpers interpolate these.
- **Key naming**: lowerCamelCase with dot-separated namespaces (e.g. `ticket.status.open`).
- **Conflict resolution** (when the same key appeared in multiple source repos with divergent values): Vue frontend wins, then Laravel, Filament, Rails, the compact backend cluster, Django, and WordPress in that order.
- **Gettext namespaces**: Django strings live under `djangoStrings.*` and WordPress strings under `wordpressStrings.*`, keyed deterministically from the English `msgid`.
- **Missing translations**: a key absent from a non-English locale falls back to the English value (no empty strings shipped).

## Versioning

Semantic versioning applies to the canonical JSON keys and wrapper APIs:

- Major: key removals, key renames, or breaking wrapper API changes.
- Minor: new keys or new locales.
- Patch: string updates, fallback fixes, and packaging-only changes.
