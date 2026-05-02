# escalated-locale (PyPI)

Central translation data for the Escalated portfolio, packaged for Python.

## Install

```bash
pip install escalated-locale
```

## Use (generic Python)

```python
from escalated_locale import get_locale_data, available_locales

print(available_locales())  # ['ar', 'de', 'en', ...]
en = get_locale_data("en")
print(en["ticket"]["status"]["open"])  # "Open"
```

## Use (Django)

`escalated-locale` ships gettext artifacts at
`escalated_locale/locale/<lang>/LC_MESSAGES/django.{po,mo}` (when generated as part of the package
build). To consume them, add the directory to your project's `LOCALE_PATHS`:

```python
# settings.py
from escalated_locale import get_django_locale_path

LOCALE_PATHS = [
    BASE_DIR / "locale",            # your project overrides (highest priority)
    str(get_django_locale_path()),  # central source (fallback)
]
```

If you're using `escalated-django`, the plugin exposes a helper that does this composition for you.
See <https://github.com/escalated-dev/escalated-django>.

## Source

The canonical JSON catalogs live at `locales/*.json` in
[`escalated-dev/escalated-locale`](https://github.com/escalated-dev/escalated-locale). This Python
package is generated from those files on every release.
