$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$localesDir = Join-Path $repoRoot "locales"

$targets = @(
  @{ Path = "packages/npm/locales" },
  @{ Path = "packages/composer/locales" },
  @{ Path = "packages/rubygems/locales" },
  @{ Path = "packages/maven/src/main/resources/locales" },
  @{ Path = "packages/nuget/locales" },
  @{ Path = "packages/hex/priv/locales" },
  @{ Path = "packages/go/locales" }
)

foreach ($target in $targets) {
  $absolute = Join-Path $repoRoot $target.Path
  New-Item -ItemType Directory -Force -Path $absolute | Out-Null
  Get-ChildItem -Path $absolute -Filter *.json -File -ErrorAction SilentlyContinue | Remove-Item -Force
  Copy-Item -Path (Join-Path $localesDir "*.json") -Destination $absolute -Force
}

Write-Host "Synchronized locales into package directories."
