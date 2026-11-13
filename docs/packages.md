# Packages

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

var messages = LocaleProvider.GetLocaleData("fr");
var label = LocaleProvider.Translate("nav.admin", "fr-CA");
```

The .NET 8 wrapper embeds all catalogs and falls back through parent cultures
to English. `LocaleData` remains a compatible alias. See the
[NuGet wrapper documentation](../packages/nuget/README.md) for named placeholders,
`IStringLocalizer` integration and source/package validation.

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
