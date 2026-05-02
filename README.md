# escalated-locale

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

## Override Pattern

Each plugin should load the package locale data first, then layer its own framework-local overrides on top. The plugin remains free to keep framework-specific translations or emergency patches in its own repo; the central package provides the base catalog and fallback chain.

## Packages

### npm

```js
const { getLocaleData, t } = require('@escalated-dev/locale')

const messages = getLocaleData('fr')
const label = t('ticket.subject', 'fr')
```

### Composer

```php
use Escalated\Locale\Locale;

$messages = Locale::getLocaleData('fr');
$label = Locale::translate('ticket.subject', 'fr');
```

### RubyGems

```rb
require "escalated/locale"

messages = Escalated::Locale.get_locale_data("fr")
label = Escalated::Locale.t("ticket.subject", "fr")
```

### Maven

```java
import dev.escalated.locale.Locale;

Map<String, Object> messages = Locale.getLocaleData("fr");
String label = Locale.translate("ticket.subject", "fr", Map.of());
```

### NuGet

```csharp
using Escalated.Locale;

var messages = LocaleData.GetLocaleData("fr");
var label = LocaleData.Translate("ticket.subject", "fr");
```

### Hex

```elixir
messages = Escalated.Locale.get_locale_data("fr")
label = Escalated.Locale.t("ticket.subject", "fr")
```

### PyPI (Python / Django)

```python
from escalated_locale import get_locale_data, get_django_locale_path

messages = get_locale_data("fr")  # returns dict from locales/fr.json

# In Django settings.py, layer this dir into LOCALE_PATHS so
# escalated_locale/locale/<lang>/LC_MESSAGES/django.{po,mo} is picked up
# by gettext.
LOCALE_PATHS = [
    BASE_DIR / "locale",  # project overrides (highest priority)
    str(get_django_locale_path()),
]
```

### Go

```go
import escalatedlocale "github.com/escalated-dev/escalated-locale/packages/go"

messages := escalatedlocale.GetLocaleData("fr")
label, _ := escalatedlocale.Translate("ticket.subject", "fr", nil)
```

## Versioning

Semantic versioning applies to the canonical JSON keys and wrapper APIs:

- Major: key removals, key renames, or breaking wrapper API changes.
- Minor: new keys or new locales.
- Patch: string updates, fallback fixes, and packaging-only changes.
