# Releasing `escalated-locale`

A release of `escalated-locale` publishes the same translation data to 7 ecosystem registries plus a GitHub Release. The Go module needs no registry — Go fetches modules directly from a tagged git ref.

## How to release

1. Bump versions in each `packages/{ecosystem}/` manifest if you want them committed (the publish workflow also stamps the version from the tag at publish time, so this is optional).
2. Commit and push to `main`.
3. Tag and push:
   ```
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. The `Publish` workflow runs. Watch it: <https://github.com/escalated-dev/escalated-locale/actions/workflows/publish.yml>
5. Each ecosystem job either publishes or **skips with a clear log line** if its manifest is missing or its secret isn't configured. Skipped ecosystems do **not** fail the workflow — add the missing secret/manifest and re-run, or wait for the next release.
6. The final job creates a GitHub Release for the tag.

## Required secrets

Add these in repo Settings → Secrets and variables → Actions. Each one independently activates one ecosystem; missing secrets cause that ecosystem's job to skip gracefully.

| Ecosystem | Package name | Secrets |
|---|---|---|
| **npm** | `@escalated-dev/locale` | `NPM_TOKEN` (npm auth token with publish scope on `@escalated-dev`) |
| **RubyGems** | `escalated-locale` | `RUBYGEMS_API_KEY` (rubygems.org API key with push permission) |
| **PyPI** | `escalated-locale` | `PYPI_API_TOKEN` (pypi.org project-scoped or user-scoped token) |
| **NuGet** | `Escalated.Locale` | `NUGET_API_KEY` (nuget.org API key) |
| **Hex** | `:escalated_locale` | `HEX_API_KEY` (`mix hex.user key generate`) |
| **Maven Central** | `dev.escalated:escalated-locale` | `MAVEN_USERNAME`, `MAVEN_PASSWORD` (Sonatype OSSRH or Central Portal user token), `MAVEN_GPG_PRIVATE_KEY`, `MAVEN_GPG_PASSPHRASE` (ASCII-armored private key + its passphrase, for signing) |
| **Packagist** | `escalated-dev/locale` | `PACKAGIST_USERNAME`, `PACKAGIST_TOKEN` (optional — Packagist auto-syncs from GitHub if the webhook is set up; these only force an immediate sync) |
| **Go** | `github.com/escalated-dev/escalated-locale` | None — Go modules are tag-based; `git push origin <tag>` is sufficient |

## How a tag becomes a release

```
git tag v0.1.0  ──▶  GitHub Actions: publish.yml triggered
                          │
                          ├── prepare      (extract version, run scripts/sync.sh)
                          │
                          ├── publish-npm        (skip if no NPM_TOKEN or no packages/npm/package.json)
                          ├── publish-rubygems   (skip if no RUBYGEMS_API_KEY or no .gemspec)
                          ├── publish-pypi       (skip if no PYPI_API_TOKEN or no pyproject.toml)
                          ├── publish-nuget      (skip if no NUGET_API_KEY or no .csproj)
                          ├── publish-hex        (skip if no HEX_API_KEY or no mix.exs)
                          ├── publish-maven      (skip if missing any of 4 Maven secrets or no pom.xml)
                          ├── packagist-trigger  (skip if no Packagist creds — webhook covers this)
                          │
                          └── github-release     (always runs after the matrix; creates the release page)
```

Every per-ecosystem job:
1. Runs `scripts/sync.sh` to refresh embedded `locales/*.json` copies inside the package directory.
2. Stamps the package version from the tag (`v0.1.0` → `0.1.0`).
3. Builds and pushes to the registry.

## Ecosystem-specific notes

### npm — `@escalated-dev/locale`
- Token must have publish access to the `@escalated-dev` scope.
- Published as a public package (`--access public`).
- First publish requires `npm access grant` configuration if the scope is restricted.

### RubyGems — `escalated-locale`
- Token created at <https://rubygems.org/profile/edit> (API Keys, scope = "Push rubygem").
- First publish reserves the gem name; subsequent publishes need ownership.

### PyPI — `escalated-locale`
- Use a project-scoped token (created after the first manual upload reserves the name) or an account-scoped token for the first publish.
- TestPyPI is not used by this workflow — first manual publish should go directly to PyPI.

### NuGet — `Escalated.Locale`
- API key from <https://www.nuget.org/account/apikeys>, scope = "Push" + glob `Escalated.*`.

### Hex — `:escalated_locale`
- Generate the API key locally: `mix hex.user key generate --key-name escalated-locale-ci --permission api:write`.

### Maven Central — `dev.escalated:escalated-locale`
- Most setup-heavy ecosystem. Requirements:
  1. Reserve the `dev.escalated` namespace on <https://central.sonatype.com>.
  2. Generate a user token (username + password pair).
  3. Generate a GPG keypair, publish the public key to a key server, paste the **private** key (ASCII-armored) into the `MAVEN_GPG_PRIVATE_KEY` secret along with its passphrase.
  4. The `pom.xml` must declare the `central-publishing-maven-plugin` and a `release` profile that signs and deploys.
- If any of those aren't ready, the job skips. Configure later and re-run or re-tag.

### Packagist — `escalated-dev/locale`
- Submit the repo once at <https://packagist.org/packages/submit>. After that, Packagist auto-syncs from GitHub on every push (via webhook).
- The `packagist-trigger` job is purely a fallback to force an immediate sync — optional.

### Go — `github.com/escalated-dev/escalated-locale`
- Nothing to publish. After the tag is pushed, run `GOPROXY=https://proxy.golang.org go get github.com/escalated-dev/escalated-locale@v0.1.0` to warm the proxy cache (or just wait — first import does it).

## Versioning policy

`escalated-locale` follows semver based on translation-key impact:

- **Patch** (`v0.1.0` → `v0.1.1`) — string updates, typo fixes. Existing keys keep working with same shape.
- **Minor** (`v0.1.0` → `v0.2.0`) — new keys added, no removals/renames. Backward-compatible.
- **Major** (`v0.1.0` → `v1.0.0`) — keys removed, renamed, or restructured. Plugins must update mappings.

Pre-1.0 releases follow the same rules but minor bumps are allowed to be breaking — see https://semver.org/#spec-item-4.
