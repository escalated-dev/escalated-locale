using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;
using Escalated.Locale;
using Microsoft.Extensions.Localization;

var catalogs = Directory.GetFiles(Path.Combine(AppContext.BaseDirectory, "catalogs"), "*.json")
    .ToDictionary(path => Path.GetFileNameWithoutExtension(path), ReadCatalog, StringComparer.OrdinalIgnoreCase);
var localizer = LocaleProvider.CreateLocalizer("Any.Host.Resource", "Any.Host.Assembly");
var checks = new List<(string Name, Action Run)>();
var placeholder = new Regex(@"(?<!\{)\{(?<name>[A-Za-z_][A-Za-z0-9_]*)\}(?!\})", RegexOptions.CultureInvariant);
var failures = 0;
var formattedMessages = 0;

foreach (var (locale, expected) in catalogs)
{
    checks.Add(($"catalog/{locale}", () => WithCulture(locale, () =>
    {
        var exported = FlattenDictionary(LocaleProvider.GetLocaleData(locale));
        var all = localizer.GetAllStrings(includeParentCultures: false).ToArray();
        Equal(expected.Count, all.Length, "exact-culture enumeration count");
        Equal(all.Length, all.Select(value => value.Name).Distinct(StringComparer.Ordinal).Count(), "unique keys");
        foreach (var (key, text) in expected)
        {
            Equal(text, LocaleProvider.Translate(key, locale), key);
            Equal(text, LocaleData.Translate(key, locale), $"alias/{key}");
            Equal(text, exported[key], $"data/{key}");
            var localized = localizer[key];
            Equal(text, localized.Value, $"localizer/{key}");
            Equal(false, localized.ResourceNotFound, $"found/{key}");
            Equal(text, all.Single(value => value.Name == key).Value, $"enumeration/{key}");

            var names = placeholder.Matches(text).Select(match => match.Groups["name"].Value).Distinct().ToArray();
            if (names.Length == 0)
                continue;

            var parameters = names.ToDictionary(name => name, name => (object?)$"VALUE_{name}");
            var formatted = text;
            foreach (var name in names)
                formatted = formatted.Replace("{" + name + "}", (string)parameters[name]!, StringComparison.Ordinal);
            Equal(formatted, LocaleProvider.Translate(key, locale, parameters), $"named provider/{key}");
            Equal(formatted, localizer[key, parameters].Value, $"named localizer/{key}");

            var canonicalNames = placeholder.Matches(catalogs["en"][key])
                .Select(match => match.Groups["name"].Value).Distinct().ToArray();
            Equal(formatted, localizer[key, canonicalNames.Select(name => parameters[name]!).ToArray()].Value,
                $"positional localizer/{key}");
            formattedMessages++;
        }
    })));
}

foreach (var (requested, expected) in new[] { ("fr-CA", "fr"), ("de-AT", "de"), ("cs-CZ", "en"), ("en-GB", "en"), ("PT-br", "pt-BR"), ("", "en") })
{
    checks.Add(($"fallback/{requested}", () => WithCulture(requested, () =>
    {
        Equal(catalogs[expected]["nav.admin"], LocaleProvider.Translate("nav.admin", requested), "provider fallback");
        Equal(catalogs[expected]["nav.admin"], localizer["nav.admin"].Value, "localizer fallback");
        Equal(false, localizer["nav.admin"].ResourceNotFound, "fallback is found");
        Equal(catalogs[expected]["nav.admin"], FlattenDictionary(LocaleData.GetLocaleData(requested))["nav.admin"], "data fallback");
        var all = localizer.GetAllStrings(includeParentCultures: true).ToArray();
        Equal(catalogs["en"].Count, all.Length, "merged fallback count");
        Equal(catalogs[expected]["nav.admin"], all.Single(value => value.Name == "nav.admin").Value, "first locale wins");
    })));
}

checks.Add(("exact-only enumeration", () => WithCulture("fr-CA", () =>
    Equal(0, localizer.GetAllStrings(includeParentCultures: false).Count(), "no parent catalog requested"))));
checks.Add(("unsupported exact-only enumeration", () => WithCulture("cs-CZ", () =>
    Equal(0, localizer.GetAllStrings(includeParentCultures: false).Count(), "no unsupported catalog"))));
checks.Add(("missing and non-string keys", () => WithCulture("fr-CA", () =>
{
    foreach (var name in new[] { "missing.translation", "nav", "nav.admin.child" })
    {
        Equal(name, LocaleProvider.Translate(name, "fr-CA"), "provider missing");
        Equal(name, localizer[name].Value, "localizer missing");
        Equal(true, localizer[name].ResourceNotFound, "missing flag");
    }
    Equal("missing.{count}", LocaleProvider.Translate("missing.{count}", "fr-CA", new() { ["count"] = 3 }), "missing provider key is preserved");
})));
checks.Add(("malformed locale", () =>
    Equal(catalogs["en"]["nav.admin"], LocaleProvider.Translate("nav.admin", "../../not-a-locale"), "embedded-only fallback")));
checks.Add(("mutable data cannot poison translations", () =>
{
    var data = LocaleProvider.GetLocaleData("fr");
    var original = data["nav"];
    try
    {
        data["nav"] = new Dictionary<string, object?> { ["admin"] = "POISONED" };
        Equal(catalogs["fr"]["nav.admin"], LocaleData.Translate("nav.admin", "fr"), "cache remains private");
        Equal(catalogs["fr"]["nav.admin"], FlattenDictionary(LocaleProvider.GetLocaleData("fr"))["nav.admin"], "fresh data snapshot");
    }
    finally
    {
        data["nav"] = original;
    }
}));
checks.Add(("named values are replaced once", () => WithCulture("en", () =>
{
    var parameters = new Dictionary<string, object?> { ["reference"] = "{subject}", ["subject"] = "Final" };
    const string expected = "[{subject}] New Ticket: Final";
    Equal(expected, LocaleProvider.Translate("notifications.newTicket.subject", "en", parameters), "provider non-recursive replacement");
    Equal(expected, localizer["notifications.newTicket.subject", parameters].Value, "localizer non-recursive replacement");
    Equal("[{reference}] New Ticket: Final", localizer["notifications.newTicket.subject",
        new Dictionary<string, object?> { ["subject"] = "Final" }].Value, "unprovided token preserved");
})));
checks.Add(("format culture is independent of UI culture", () => WithCulture("fr-CA", () =>
{
    CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("en-US");
    var template = catalogs["fr"]["bulk.updated"];
    var expected = template.Replace("{count}", "1.5", StringComparison.Ordinal);
    Equal(expected, localizer["bulk.updated", 1.5m].Value, "positional numeric culture");
    Equal(expected, LocaleProvider.Translate("bulk.updated", "fr-CA", new() { ["count"] = 1.5m }), "named numeric culture");
})));
checks.Add(("alias factory", () => WithCulture("fr", () =>
    Equal(catalogs["fr"]["nav.admin"], LocaleData.CreateLocalizer("Ignored", "Ignored")["nav.admin"].Value, "backwards-compatible factory"))));
checks.Insert(0, ("parallel request cultures with cold caches", () => Parallel.For(0, 256, index =>
{
    var locale = catalogs.Keys.ElementAt(index % catalogs.Count);
    WithCulture(locale, () =>
    {
        for (var iteration = 0; iteration < 10; iteration++)
        {
            Equal(catalogs[locale]["nav.admin"], localizer["nav.admin"].Value, "per-request locale");
            Equal(catalogs[locale]["nav.admin"], LocaleProvider.Translate("nav.admin", locale), "parallel provider");
        }
    });
})));

foreach (var (name, run) in checks)
{
    try
    {
        run();
        Console.WriteLine($"PASS {name}");
    }
    catch (Exception exception)
    {
        failures++;
        Console.Error.WriteLine($"FAIL {name}: {exception.Message}");
    }
}
Console.WriteLine($"LOCALE_CONTRACTS: checks={checks.Count}, failed={failures}, catalogs={catalogs.Count}, formatted_messages={formattedMessages}");
return failures == 0 ? 0 : 1;

static void Equal<T>(T expected, T actual, string context)
{
    if (!EqualityComparer<T>.Default.Equals(expected, actual))
        throw new InvalidOperationException($"{context}: expected '{expected}', got '{actual}'");
}

static void WithCulture(string locale, Action action)
{
    var originalCulture = CultureInfo.CurrentCulture;
    var originalUiCulture = CultureInfo.CurrentUICulture;
    try
    {
        CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo(locale);
        CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo(locale);
        action();
    }
    finally
    {
        CultureInfo.CurrentCulture = originalCulture;
        CultureInfo.CurrentUICulture = originalUiCulture;
    }
}

static Dictionary<string, string> ReadCatalog(string file)
{
    using var document = JsonDocument.Parse(File.ReadAllText(file));
    var result = new Dictionary<string, string>(StringComparer.Ordinal);
    Flatten(document.RootElement, "", result);
    return result;
}

static Dictionary<string, string> FlattenDictionary(Dictionary<string, object?> data)
{
    using var document = JsonDocument.Parse(JsonSerializer.Serialize(data));
    var result = new Dictionary<string, string>(StringComparer.Ordinal);
    Flatten(document.RootElement, "", result);
    return result;
}

static void Flatten(JsonElement element, string prefix, Dictionary<string, string> result)
{
    foreach (var property in element.EnumerateObject())
    {
        var name = prefix.Length == 0 ? property.Name : $"{prefix}.{property.Name}";
        if (property.Value.ValueKind == JsonValueKind.Object)
            Flatten(property.Value, name, result);
        else if (property.Value.ValueKind == JsonValueKind.String)
            result.Add(name, property.Value.GetString()!);
    }
}
