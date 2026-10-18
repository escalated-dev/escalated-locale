# Escalated.Locale

.NET wrapper for the canonical Escalated locale JSON bundle.

Targets .NET 8. All 14 catalogs are embedded in the assembly; consumers do not
need to copy JSON files into their application.

```csharp
using Escalated.Locale;

var label = LocaleProvider.Translate("nav.admin", "fr-CA"); // Administration
var message = LocaleProvider.Translate("bulk.updated", "fr", new()
{
    ["count"] = 3,
});
```

Lookups try the requested culture, its parents, and then English. Locale names
are case insensitive. Empty, unsupported or malformed locale names fall back
to English. Missing keys and object-valued namespaces return the key itself.
Named `{count}` placeholders are replaced once, so replacement values are not
treated as further templates. Unprovided placeholders remain intact.

`GetLocaleData(locale)` returns a caller-owned dictionary for the most specific
available catalog. Nested JSON values remain `JsonElement` instances. Mutating
the returned dictionary does not change future translations. `LocaleData`
remains an alias for all three `LocaleProvider` methods.

## IStringLocalizer integration

```csharp
using System.Globalization;
using Escalated.Locale;

CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo("fr-CA");
var localizer = LocaleProvider.CreateLocalizer("Host.Resources", "Host.Assembly");
var label = localizer["nav.admin"];
var message = localizer["bulk.updated", 3];
```

The factory arguments preserve the standard resource-localizer signature for
existing host integrations; this provider always uses its embedded catalogs.
The localizer reads `CurrentUICulture` for each request and formats values with
`CurrentCulture`. Pass one `Dictionary<string, object?>` for named values, or
positional arguments in the order of distinct placeholders in the English
message. With no arguments, the original template is returned.

`GetAllStrings(true)` merges the requested culture, parents and English with
the most specific value winning. `GetAllStrings(false)` returns only the
exact catalog, so a regional culture without its own file yields no strings.
The invariant culture uses English. Only string leaves are enumerated, and
`ResourceNotFound` is true only when no catalog contains the requested key.

## Validation

From the repository root, with .NET SDK 8 and Python 3:

```sh
python scripts/test_nuget.py
```

This audits all dependencies, checks every shipped translation and named
message through the public API, packs an unpublished test artifact, and repeats
the contracts in a fresh package-only consumer. CI runs this on Linux and Windows.
