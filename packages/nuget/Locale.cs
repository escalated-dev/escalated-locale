using System.Reflection;
using System.Text.Json;
using Microsoft.Extensions.Localization;

namespace Escalated.Locale;

/// <summary>
/// Canonical locale provider for Escalated. Loads locales/*.json embedded
/// resources on demand, caches per-locale dictionaries, and exposes lookup
/// helpers used by host-framework plugins.
/// </summary>
public static class LocaleProvider
{
    private static readonly Dictionary<string, Dictionary<string, object?>> Cache = new();

    public static Dictionary<string, object?> GetLocaleData(string locale = "en")
    {
        var effectiveLocale = string.IsNullOrWhiteSpace(locale) ? "en" : locale;
        if (!Cache.TryGetValue(effectiveLocale, out var data))
        {
            var streamName = $"Escalated.Locale.locales.{effectiveLocale}.json";
            using var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(streamName)
                ?? throw new InvalidOperationException($"Missing locale resource: {effectiveLocale}");
            data = JsonSerializer.Deserialize<Dictionary<string, object?>>(stream)
                ?? throw new InvalidOperationException($"Invalid locale resource: {effectiveLocale}");
            Cache[effectiveLocale] = data;
        }

        return data;
    }

    public static string Translate(string key, string locale = "en", Dictionary<string, object?>? parameters = null)
    {
        var value = Resolve(GetLocaleData(locale), key) ?? Resolve(GetLocaleData("en"), key);
        if (value is not string text)
        {
            return key;
        }

        if (parameters is null)
        {
            return text;
        }

        foreach (var pair in parameters)
        {
            text = text.Replace("{" + pair.Key + "}", Convert.ToString(pair.Value));
        }

        return text;
    }

    /// <summary>
    /// Build an <see cref="IStringLocalizer"/> backed by the canonical Escalated
    /// locale catalog. The <paramref name="baseName"/> and <paramref name="location"/>
    /// arguments mirror the standard .NET resource-localizer signature; they are
    /// accepted for compatibility with reflection-based callers (e.g. the
    /// escalated-dotnet host plugin) but are not used for resource resolution —
    /// the canonical Escalated locale data is always consulted.
    /// </summary>
    public static IStringLocalizer CreateLocalizer(string baseName, string location)
    {
        return new EscalatedStringLocalizer(baseName, location);
    }

    private static object? Resolve(Dictionary<string, object?> data, string key)
    {
        object? current = data;
        foreach (var part in key.Split('.'))
        {
            if (current is JsonElement element && element.ValueKind == JsonValueKind.Object)
            {
                if (!element.TryGetProperty(part, out current))
                {
                    return null;
                }
                continue;
            }

            if (current is Dictionary<string, object?> dictionary && dictionary.TryGetValue(part, out current))
            {
                continue;
            }

            return null;
        }

        return current is JsonElement finalElement && finalElement.ValueKind == JsonValueKind.String
            ? finalElement.GetString()
            : current;
    }

    private sealed class EscalatedStringLocalizer : IStringLocalizer
    {
        private readonly string _baseName;
        private readonly string _location;

        public EscalatedStringLocalizer(string baseName, string location)
        {
            _baseName = baseName;
            _location = location;
        }

        public LocalizedString this[string name]
        {
            get
            {
                var locale = System.Globalization.CultureInfo.CurrentUICulture.Name;
                var translated = Translate(name, NormalizeLocale(locale));
                var resourceNotFound = translated == name && Resolve(GetLocaleData(NormalizeLocale(locale)), name) is null;
                return new LocalizedString(name, translated, resourceNotFound);
            }
        }

        public LocalizedString this[string name, params object[] arguments]
        {
            get
            {
                var raw = this[name];
                var formatted = arguments.Length == 0 ? raw.Value : string.Format(raw.Value, arguments);
                return new LocalizedString(name, formatted, raw.ResourceNotFound);
            }
        }

        public IEnumerable<LocalizedString> GetAllStrings(bool includeParentCultures)
        {
            var locale = NormalizeLocale(System.Globalization.CultureInfo.CurrentUICulture.Name);
            foreach (var pair in Flatten(GetLocaleData(locale), prefix: ""))
            {
                yield return new LocalizedString(pair.Key, pair.Value, resourceNotFound: false);
            }
        }

        private static string NormalizeLocale(string locale)
        {
            if (string.IsNullOrWhiteSpace(locale))
            {
                return "en";
            }
            // .NET CultureInfo names use hyphens (e.g. "pt-BR") which match our
            // locales/*.json filenames directly.
            return locale;
        }

        private static IEnumerable<KeyValuePair<string, string>> Flatten(Dictionary<string, object?> data, string prefix)
        {
            foreach (var pair in data)
            {
                var path = string.IsNullOrEmpty(prefix) ? pair.Key : $"{prefix}.{pair.Key}";
                switch (pair.Value)
                {
                    case Dictionary<string, object?> nested:
                        foreach (var inner in Flatten(nested, path))
                        {
                            yield return inner;
                        }
                        break;
                    case JsonElement element when element.ValueKind == JsonValueKind.Object:
                        var asDict = JsonSerializer.Deserialize<Dictionary<string, object?>>(element.GetRawText());
                        if (asDict is not null)
                        {
                            foreach (var inner in Flatten(asDict, path))
                            {
                                yield return inner;
                            }
                        }
                        break;
                    case JsonElement leaf when leaf.ValueKind == JsonValueKind.String:
                        yield return new KeyValuePair<string, string>(path, leaf.GetString() ?? string.Empty);
                        break;
                    case string s:
                        yield return new KeyValuePair<string, string>(path, s);
                        break;
                }
            }
        }
    }
}

/// <summary>
/// Backwards-compatible alias for <see cref="LocaleProvider"/>. Pre-existing
/// consumers that referenced <c>Escalated.Locale.LocaleData</c> continue to
/// work without code changes; new callers should prefer
/// <see cref="LocaleProvider"/> directly.
/// </summary>
public static class LocaleData
{
    public static Dictionary<string, object?> GetLocaleData(string locale = "en")
        => LocaleProvider.GetLocaleData(locale);

    public static string Translate(string key, string locale = "en", Dictionary<string, object?>? parameters = null)
        => LocaleProvider.Translate(key, locale, parameters);

    public static IStringLocalizer CreateLocalizer(string baseName, string location)
        => LocaleProvider.CreateLocalizer(baseName, location);
}
