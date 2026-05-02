package dev.escalated.locale;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public final class Locale {
  private static final ObjectMapper MAPPER = new ObjectMapper();
  private static final Map<String, Map<String, Object>> CACHE = new HashMap<>();

  private Locale() {}

  public static Map<String, Object> getLocaleData(String locale) {
    String effectiveLocale = locale == null || locale.isBlank() ? "en" : locale;
    return CACHE.computeIfAbsent(effectiveLocale, Locale::loadLocale);
  }

  public static String translate(String key, String locale, Map<String, ?> params) {
    Object value = resolve(getLocaleData(locale), key);
    if (!(value instanceof String)) {
      value = resolve(getLocaleData("en"), key);
    }
    if (!(value instanceof String)) {
      return key;
    }

    String text = (String) value;
    if (params != null) {
      for (Map.Entry<String, ?> entry : params.entrySet()) {
        text = text.replace("{" + entry.getKey() + "}", String.valueOf(entry.getValue()));
      }
    }
    return text;
  }

  private static Map<String, Object> loadLocale(String locale) {
    String path = "locales/" + locale + ".json";
    try (InputStream stream = Locale.class.getClassLoader().getResourceAsStream(path)) {
      if (stream == null) {
        throw new IllegalArgumentException("Missing locale: " + locale);
      }
      return MAPPER.readValue(stream, new TypeReference<Map<String, Object>>() {});
    } catch (IOException exception) {
      throw new IllegalStateException("Failed to load locale " + locale, exception);
    }
  }

  @SuppressWarnings("unchecked")
  private static Object resolve(Map<String, Object> data, String key) {
    Object current = data;
    for (String part : key.split("\\.")) {
      if (!(current instanceof Map<?, ?> currentMap) || !currentMap.containsKey(part)) {
        return null;
      }
      current = ((Map<String, Object>) currentMap).get(part);
    }
    return current;
  }
}
