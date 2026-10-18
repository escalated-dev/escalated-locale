using System.Collections.Concurrent;
using System.Collections.Frozen;
using System.Globalization;
using System.Reflection;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Localization;

namespace Escalated.Locale;

/// <summary>
/// Loads embedded Escalated catalogs with parent-culture and English fallback.
/// </summary>
public static partial class LocaleProvider
{
    private const string ResourcePrefix = "Escalated.Locale.locales.";
    private static readonly Assembly CatalogAssembly = typeof(LocaleProvider).Assembly;
    private static readonly FrozenDictionary<string, string> ResourceNames = CatalogAssembly.GetManifestResourceNames()
        .Where(name => name.StartsWith(ResourcePrefix, StringComparison.Ordinal) && name.EndsWith(".json", StringComparison.Ordinal))
        .ToFrozenDictionary(name => name[ResourcePrefix.Length..^5], name => name, StringComparer.OrdinalIgnoreCase);
    private static readonly ConcurrentDictionary<string, Lazy<CatalogData>> Catalogs = new();

    /// <summary>
    /// Returns a caller-owned snapshot of the most specific available catalog.
    /// Nested values retain their existing <see cref="JsonElement"/> representation.
    /// </summary>
    public static Dictionary<string, object?> GetLocaleData(string locale = "en")
    {
        foreach (var candidate in Cultures(locale, includeParents: true))
        {
            if (Catalog(candidate) is { } catalog)
                return catalog.Data.Deserialize<Dictionary<string, object?>>()!;
        }

        throw new InvalidOperationException("Missing embedded English locale catalog.");
    }

    public static string Translate(string key, string locale = "en", Dictionary<string, object?>? parameters = null)
    {
        var value = Lookup(key, locale);
        return value.ResourceNotFound || parameters is null ? value.Value : ReplaceNamed(value.Value, parameters);
    }

    /// <summary>
    /// Creates a localizer for the canonical catalogs. The resource-localizer
    /// arguments are retained for existing reflection-based host integrations.
    /// </summary>
    public static IStringLocalizer CreateLocalizer(string baseName, string location)
        => new EscalatedStringLocalizer();

    private static LocalizedString Lookup(string key, string locale)
    {
        ArgumentNullException.ThrowIfNull(key);
        foreach (var candidate in Cultures(locale, includeParents: true))
        {
            if (Catalog(candidate) is { } catalog && catalog.Strings.TryGetValue(key, out var text))
                return new LocalizedString(key, text, resourceNotFound: false, ResourceNames[candidate]);
        }

        return new LocalizedString(key, key, resourceNotFound: true, ResourcePrefix);
    }

    private static IEnumerable<string> Cultures(string locale, bool includeParents)
    {
        if (string.IsNullOrWhiteSpace(locale))
        {
            yield return "en";
            yield break;
        }

        yield return locale;
        if (!includeParents)
            yield break;

        var includedEnglish = locale.Equals("en", StringComparison.OrdinalIgnoreCase);
        CultureInfo? culture;
        try
        {
            culture = CultureInfo.GetCultureInfo(locale);
        }
        catch (CultureNotFoundException)
        {
            culture = null;
        }

        while (culture is not null && culture.Parent.Name.Length != 0)
        {
            culture = culture.Parent;
            yield return culture.Name;
            includedEnglish |= culture.Name.Equals("en", StringComparison.OrdinalIgnoreCase);
        }

        if (!includedEnglish)
            yield return "en";
    }

    private static CatalogData? Catalog(string locale)
    {
        // The cache is bounded by the embedded resource set, never request input.
        if (!ResourceNames.TryGetValue(locale, out var resource))
            return null;

        return Catalogs.GetOrAdd(resource, name => new Lazy<CatalogData>(() => Load(name))).Value;
    }

    private static CatalogData Load(string resource)
    {
        using var stream = CatalogAssembly.GetManifestResourceStream(resource)
            ?? throw new InvalidOperationException($"Missing embedded locale resource: {resource}");
        using var document = JsonDocument.Parse(stream);
        var strings = new Dictionary<string, string>(StringComparer.Ordinal);
        Flatten(document.RootElement, string.Empty, strings);
        return new CatalogData(document.RootElement.Clone(), strings.ToFrozenDictionary(StringComparer.Ordinal));
    }

    private static void Flatten(JsonElement node, string prefix, Dictionary<string, string> strings)
    {
        foreach (var property in node.EnumerateObject())
        {
            var key = prefix.Length == 0 ? property.Name : $"{prefix}.{property.Name}";
            if (property.Value.ValueKind == JsonValueKind.Object)
                Flatten(property.Value, key, strings);
            else if (property.Value.ValueKind == JsonValueKind.String)
                strings.Add(key, property.Value.GetString()!);
        }
    }

    private static string ReplaceNamed(string template, IReadOnlyDictionary<string, object?> parameters)
        => NamedPlaceholder().Replace(template, match =>
        {
            if (!parameters.TryGetValue(match.Groups["name"].Value, out var value))
                return match.Value;

            var format = match.Groups["format"].Value;
            return value is IFormattable formattable
                ? formattable.ToString(format.Length == 0 ? null : format[1..], CultureInfo.CurrentCulture) ?? string.Empty
                : Convert.ToString(value, CultureInfo.CurrentCulture) ?? string.Empty;
        });

    private static string Format(string key, string template, object[] arguments)
    {
        if (arguments.Length == 1 && arguments[0] is IReadOnlyDictionary<string, object?> parameters && NamedPlaceholder().IsMatch(template))
            return ReplaceNamed(template, parameters);

        // Positional values follow English token order even if a translation
        // reorders the named placeholders.
        var canonical = Catalog("en")!.Strings.TryGetValue(key, out var english) ? english : template;
        var positions = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (Match match in NamedPlaceholder().Matches(canonical))
            positions.TryAdd(match.Groups["name"].Value, positions.Count);

        var composite = NamedPlaceholder().Replace(template, match =>
            positions.TryGetValue(match.Groups["name"].Value, out var position)
                ? "{" + position.ToString(CultureInfo.InvariantCulture) + match.Groups["format"].Value + "}"
                : match.Value);
        return string.Format(CultureInfo.CurrentCulture, composite, arguments);
    }

    [GeneratedRegex(@"(?<!\{)\{(?<name>[A-Za-z_][A-Za-z0-9_]*)(?<format>:[^{}]+)?\}(?!\})", RegexOptions.CultureInvariant)]
    private static partial Regex NamedPlaceholder();

    private sealed record CatalogData(JsonElement Data, FrozenDictionary<string, string> Strings);

    private sealed class EscalatedStringLocalizer : IStringLocalizer
    {
        public LocalizedString this[string name] => Lookup(name, CultureInfo.CurrentUICulture.Name);

        public LocalizedString this[string name, params object[] arguments]
        {
            get
            {
                ArgumentNullException.ThrowIfNull(arguments);
                var raw = this[name];
                var formatted = arguments.Length == 0 ? raw.Value : Format(name, raw.Value, arguments);
                return new LocalizedString(name, formatted, raw.ResourceNotFound, raw.SearchedLocation);
            }
        }

        public IEnumerable<LocalizedString> GetAllStrings(bool includeParentCultures)
        {
            var seen = new HashSet<string>(StringComparer.Ordinal);
            foreach (var candidate in Cultures(CultureInfo.CurrentUICulture.Name, includeParentCultures))
            {
                if (Catalog(candidate) is not { } catalog)
                    continue;

                foreach (var pair in catalog.Strings)
                {
                    if (seen.Add(pair.Key))
                        yield return new LocalizedString(pair.Key, pair.Value, resourceNotFound: false, ResourceNames[candidate]);
                }
            }
        }
    }
}

/// <summary>
/// Backwards-compatible alias for <see cref="LocaleProvider"/>.
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
