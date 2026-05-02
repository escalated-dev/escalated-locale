<?php

declare(strict_types=1);

namespace Escalated\Locale;

final class Locale
{
    /** @var array<string, array<string, mixed>> */
    private static array $cache = [];

    /** @return array<string, mixed> */
    public static function getLocaleData(string $locale = 'en'): array
    {
        if (!isset(self::$cache[$locale])) {
            $path = dirname(__DIR__).'/locales/'.$locale.'.json';
            self::$cache[$locale] = json_decode((string) file_get_contents($path), true, 512, JSON_THROW_ON_ERROR);
        }

        return self::$cache[$locale];
    }

    /** @param array<string, scalar> $params */
    public static function translate(string $key, string $locale = 'en', array $params = []): string
    {
        $value = self::resolve(self::getLocaleData($locale), $key) ?? self::resolve(self::getLocaleData('en'), $key);
        if (!is_string($value)) {
            return $key;
        }

        foreach ($params as $name => $replacement) {
            $value = str_replace('{'.$name.'}', (string) $replacement, $value);
        }

        return $value;
    }

    /** @param array<string, mixed> $data */
    private static function resolve(array $data, string $key): mixed
    {
        $current = $data;
        foreach (explode('.', $key) as $part) {
            if (!is_array($current) || !array_key_exists($part, $current)) {
                return null;
            }
            $current = $current[$part];
        }

        return $current;
    }
}
