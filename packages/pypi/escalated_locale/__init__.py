"""Central translation data for the Escalated portfolio.

This package ships JSON locale catalogs and (when generated) Django gettext
artifacts. Plugins layer their own framework-local overrides on top.

Typical use (any Python project)::

    from escalated_locale import get_locale_data

    en = get_locale_data("en")
    open_label = en["ticket"]["status"]["open"]

For Django, point ``LOCALE_PATHS`` at :func:`get_django_locale_path` so the
package's ``locale/<lang>/LC_MESSAGES/django.mo`` files (when present) are
picked up by Django's gettext machinery.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

__all__ = [
    "get_locale_data",
    "available_locales",
    "get_locale_path",
    "get_django_locale_path",
]

_PACKAGE_DIR = Path(__file__).resolve().parent
_LOCALES_DIR = _PACKAGE_DIR / "locales"
_DJANGO_LOCALE_DIR = _PACKAGE_DIR / "locale"


def get_locale_path() -> Path:
    """Directory containing ``{locale}.json`` files."""
    return _LOCALES_DIR


def get_django_locale_path() -> Path:
    """Directory matching Django's ``LOCALE_PATHS`` layout (``<lang>/LC_MESSAGES/django.mo``).

    The directory may be empty if the package was built without a gettext
    compilation step. Django gracefully tolerates an empty locale dir.
    """
    return _DJANGO_LOCALE_DIR


@lru_cache(maxsize=None)
def get_locale_data(locale: str) -> dict[str, Any]:
    """Return the parsed JSON catalog for ``locale``.

    Raises FileNotFoundError if the locale is not shipped.
    """
    path = _LOCALES_DIR / f"{locale}.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"locale '{locale}' not found in escalated-locale "
            f"(looked for {path})"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def available_locales() -> list[str]:
    """Sorted list of locales shipped in this package."""
    if not _LOCALES_DIR.is_dir():
        return []
    return sorted(p.stem for p in _LOCALES_DIR.glob("*.json"))
