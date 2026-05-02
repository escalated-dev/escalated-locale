using System.Reflection;
using System.Text.Json;

namespace Escalated.Locale;

public static class LocaleData
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
}
