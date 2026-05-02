defmodule EscalatedLocale.MixProject do
  use Mix.Project

  def project do
    [
      app: :escalated_locale,
      version: "0.1.0",
      elixir: "~> 1.16",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      package: package(),
      description: "Canonical Escalated locale bundle for Elixir consumers"
    ]
  end

  def application do
    [extra_applications: [:logger]]
  end

  defp deps do
    [{:jason, "~> 1.4"}]
  end

  defp package do
    [
      licenses: ["MIT"],
      files: ["lib", "mix.exs", "README.md", "priv/locales", "priv/gettext"]
    ]
  end
end
