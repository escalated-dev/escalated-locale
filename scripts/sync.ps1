#!/usr/bin/env pwsh
# Copy locales/*.json into each packages/{ecosystem}/ at the path
# the ecosystem's package manifest expects. Idempotent.

$ErrorActionPreference = 'Stop'

$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$src = Join-Path $root 'locales'

if (-not (Test-Path $src) -or -not (Get-ChildItem -Path $src -Filter '*.json' -ErrorAction SilentlyContinue)) {
  Write-Host 'sync: no JSON files in locales/ - nothing to do'
  exit 0
}

$packagesDir = Join-Path $root 'packages'
if (-not (Test-Path $packagesDir)) {
  Write-Host 'sync: packages/ directory missing - nothing to do'
  exit 0
}

$synced = 0
foreach ($pkgDir in Get-ChildItem -Path $packagesDir -Directory) {
  $pkg = $pkgDir.Name
  switch ($pkg) {
    { $_ -in 'npm','composer','rubygems','nuget','hex','go' } {
      $target = Join-Path $pkgDir.FullName 'locales'
    }
    'maven' {
      $target = Join-Path $pkgDir.FullName 'src/main/resources/locales'
    }
    'pypi' {
      $target = Join-Path $pkgDir.FullName 'escalated_locale/locales'
    }
    default {
      Write-Host "sync: skipping unknown package dir '$pkg'"
      continue
    }
  }

  if (Test-Path $target) { Remove-Item -Recurse -Force $target }
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  Copy-Item -Path (Join-Path $src '*.json') -Destination $target
  Write-Host "sync: $pkg <- locales/"
  $synced++
}

Write-Host "sync: done ($synced package(s))"
