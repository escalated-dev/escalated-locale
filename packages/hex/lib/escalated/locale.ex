defmodule Escalated.Locale do
  @moduledoc false

  def get_locale_data(locale \\ "en") do
    locale
    |> locale_path()
    |> File.read!()
    |> Jason.decode!()
  end

  def t(key, locale \\ "en", params \\ %{}) do
    value =
      resolve(get_locale_data(locale), key) ||
        resolve(get_locale_data("en"), key)

    if is_binary(value) do
      Enum.reduce(params, value, fn {name, replacement}, current ->
        String.replace(current, "{#{name}}", to_string(replacement))
      end)
    else
      key
    end
  end

  defp resolve(data, key) do
    Enum.reduce_while(String.split(key, "."), data, fn part, current ->
      case current do
        %{} ->
          case Map.fetch(current, part) do
            {:ok, value} -> {:cont, value}
            :error -> {:halt, nil}
          end

        _ ->
          {:halt, nil}
      end
    end)
  end

  defp locale_path(locale) do
    Path.join(:code.priv_dir(:escalated_locale), "locales/#{locale}.json")
  end
end
