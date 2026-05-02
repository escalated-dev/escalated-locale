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
  @{ Path = "packages/go/locales" },
  @{ Path = "packages/pypi/escalated_locale/locales" }
)

foreach ($target in $targets) {
  $absolute = Join-Path $repoRoot $target.Path
  New-Item -ItemType Directory -Force -Path $absolute | Out-Null
  Get-ChildItem -Path $absolute -Filter *.json -File -ErrorAction SilentlyContinue | Remove-Item -Force
  Copy-Item -Path (Join-Path $localesDir "*.json") -Destination $absolute -Force
}

Write-Host "Synchronized locales into package directories."

# Build framework-native artifacts (Rails YAML, Django/WP/Phoenix gettext,
# Symfony YAML, Spring properties). See scripts/build_native_artifacts.py.
$buildScript = Join-Path $PSScriptRoot "build_native_artifacts.py"
$pythonExe = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonExe) {
  $pythonExe = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $pythonExe) {
  throw "sync: python (or python3) is required to build native locale artifacts"
}
& $pythonExe.Source $buildScript
if ($LASTEXITCODE -ne 0) {
  throw "sync: build_native_artifacts.py failed (exit $LASTEXITCODE)"
}
