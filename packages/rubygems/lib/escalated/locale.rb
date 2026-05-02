require "json"

module Escalated
  module Locale
    module_function

    CACHE = {}

    def get_locale_data(locale = "en")
      CACHE[locale] ||= JSON.parse(File.read(File.expand_path("../../locales/#{locale}.json", __dir__)))
    end

    def t(key, locale = "en", params = {})
      value = resolve(get_locale_data(locale), key) || resolve(get_locale_data("en"), key)
      return key unless value.is_a?(String)

      params.reduce(value) do |current, (name, replacement)|
        current.gsub("{#{name}}", replacement.to_s)
      end
    end

    def resolve(data, key)
      key.split(".").reduce(data) do |current, part|
        return nil unless current.is_a?(Hash)

        current[part]
      end
    end
  end
end
