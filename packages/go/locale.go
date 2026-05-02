package locale

import (
	"embed"
	"encoding/json"
	"fmt"
	"strings"
)

//go:embed locales/*.json
var localeFS embed.FS

var cache = map[string]map[string]any{}

func GetLocaleData(locale string) map[string]any {
	effectiveLocale := locale
	if effectiveLocale == "" {
		effectiveLocale = "en"
	}
	if cached, ok := cache[effectiveLocale]; ok {
		return cached
	}
	payload, err := localeFS.ReadFile("locales/" + effectiveLocale + ".json")
	if err != nil {
		panic(err)
	}
	var data map[string]any
	if err := json.Unmarshal(payload, &data); err != nil {
		panic(err)
	}
	cache[effectiveLocale] = data
	return data
}

func Translate(key string, locale string, params map[string]any) (string, bool) {
	value, ok := resolve(GetLocaleData(locale), key)
	if !ok {
		value, ok = resolve(GetLocaleData("en"), key)
	}
	if !ok {
		return key, false
	}
	text, isString := value.(string)
	if !isString {
		return key, false
	}
	for name, replacement := range params {
		text = strings.ReplaceAll(text, "{"+name+"}", fmt.Sprint(replacement))
	}
	return text, true
}

func resolve(data map[string]any, key string) (any, bool) {
	var current any = data
	for _, part := range strings.Split(key, ".") {
		next, ok := current.(map[string]any)
		if !ok {
			return nil, false
		}
		current, ok = next[part]
		if !ok {
			return nil, false
		}
	}
	return current, true
}
