<p align="center">
  <a href="https://escalated.dev"><img src="https://raw.githubusercontent.com/escalated-dev/escalated/main/docs/assets/readme/logo.png" width="56" height="56" alt="Escalated"></a>
</p>

<h1 align="center">Escalated Locale</h1>

<p align="center">Translations for every Escalated backend, from one source.</p>

<p align="center">
  <a href="https://escalated.dev"><b>Website</b></a> ·
  <a href="https://escalated.dev/docs"><b>Docs</b></a> ·
  <a href="https://escalated.dev/cloud"><b>Cloud</b></a> ·
  <a href="https://github.com/escalated-dev/escalated-locale/releases"><b>Releases</b></a>
</p>

This repo keeps the canonical translation catalogues for all 14 Escalated locales and republishes them as npm, Composer, RubyGems, PyPI, Maven, NuGet, Hex and Go packages. It's for Escalated maintainers and translators; your app gets these strings through its Escalated package.

## Usage

```js
const { getLocaleData, t } = require('@escalated-dev/locale')

const label = t('ticket.subject', 'fr')
```

## Learn more

- [Architecture, overrides, conventions and versioning](docs/architecture.md)
- [Adding a translation or a locale](docs/adding-translations.md)
- [Using each package: npm, Composer, RubyGems, Maven, NuGet, Hex, PyPI, Go](docs/packages.md)
- [Releasing](RELEASE.md)
- [Escalated docs](https://escalated.dev/docs)
- [Escalated](https://github.com/escalated-dev/escalated), the main repo

## License

MIT. Copyright (c) 2026 Escalated.dev. See [LICENSE](LICENSE).
