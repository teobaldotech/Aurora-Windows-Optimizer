
import gettext
import os
from unittest.mock import Mock

import pytest

import language


class FakeTranslations:
def init(self):
self.install = Mock()


@pytest.fixture
def fake_translations(monkeypatch):
translations = FakeTranslations()
monkeypatch.setattr(
language.gettext,
"translation",
Mock(return_value=translations),
)
return translations


@pytest.fixture
def reset_language(monkeypatch):
monkeypatch.setattr(language, "curLang", "es")


@pytest.mark.parametrize(
("value", "expected"),
[
("pt-br", "pt_BR"),
("PT-br", "pt_BR"),
("en-us", "en_US"),
("es", "es"),
("fr_FR", "fr_FR"),
("de-DE", "de_DE"),
(" pt-br ", "pt_BR"),
],
)
def test_normalize_language_valid(value, expected):
assert language.normalizeLanguage(value) == expected


@pytest.mark.parametrize(
"value",
[
None,
"",
" ",
"x-western",
"X-UNKNOWN",
],
)
def test_normalize_language_invalid(value):
assert language.normalizeLanguage(value) is None


@pytest.mark.parametrize(
("value", "expected"),
[
("pt", "ptb"),
("en", "eng"),
("es", "esp"),
("fr", "fre_FRA"),
("de", "deu"),
("ja", "jpn"),
("pt-BR", "ptb"),
("en-US", "eng"),
("unknown", "unknown"),
],
)
def test_lang_to_windows_locale(value, expected):
assert language.langToWindowsLocale(value) == expected


def test_lang_to_windows_locale_rejects_non_string():
with pytest.raises(TypeError):
language.langToWindowsLocale(None)


def test_lang_to_windows_locale_rejects_invalid_language():
with pytest.raises(ValueError):
language.langToWindowsLocale("")


def test_get_language_returns_current_language(monkeypatch):
monkeypatch.setattr(language, "curLang", "pt_BR")

assert language.getLanguage() == "pt_BR"


def test_get_available_languages_includes_portuguese(
tmp_path,
monkeypatch,
):
locales_dir = tmp_path / "locales"
locales_dir.mkdir()

monkeypatch.setattr(
language,
"_get_locales_dir",
lambda: str(locales_dir),
)
monkeypatch.setattr(
language,
"getLanguageDescription",
lambda _: None,
)

result = language.getAvailableLanguages()

assert ("pt", "pt") in result
assert ("system", "idioma do sistema") in result


def test_get_available_languages_discovers_translation(
tmp_path,
monkeypatch,
):
locales_dir = tmp_path / "locales"
translation_file = (
locales_dir / "es" / "LC_MESSAGES" / "aurora.mo"
)
translation_file.parent.mkdir(parents=True)
translation_file.touch()

monkeypatch.setattr(
language,
"_get_locales_dir",
lambda: str(locales_dir),
)
monkeypatch.setattr(
language,
"getLanguageDescription",
lambda lang: "Espanhol" if lang == "es" else None,
)

result = language.getAvailableLanguages()

assert ("es", "Espanhol, es") in result
assert ("pt", "pt") in result


def test_get_available_languages_handles_missing_directory(
tmp_path,
monkeypatch,
):
monkeypatch.setattr(
language,
"_get_locales_dir",
lambda: str(tmp_path / "missing"),
)
monkeypatch.setattr(
language,
"getLanguageDescription",
lambda _: None,
)

result = language.getAvailableLanguages()

assert ("pt", "pt") in result
assert ("system", "idioma do sistema") in result


def test_set_language_loads_requested_translation(
monkeypatch,
fake_translations,
reset_language,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(language.locale, "setlocale", Mock())

language.setLanguage("es")

assert language.getLanguage() == "es"
fake_translations.install.assert_called_once()


def test_set_language_uses_portuguese_fallback(
monkeypatch,
reset_language,
):
portuguese = FakeTranslations()
translation_calls = []

def translation_side_effect(
domain,
localedir=None,
languages=None,
fallback=False,
):
translation_calls.append((languages, fallback))

if languages == ["es"]:
raise OSError("Tradução espanhola não encontrada")

if languages == ["pt"]:
return portuguese

if fallback:
return portuguese

raise OSError("Tradução não encontrada")

monkeypatch.setattr(
language.gettext,
"translation",
Mock(side_effect=translation_side_effect),
)
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(language.locale, "setlocale", Mock())

language.setLanguage("es")

assert language.getLanguage() == "pt"
portuguese.install.assert_called_once()
assert (["es"], False) in translation_calls
assert (["pt"], False) in translation_calls


def test_set_language_handles_locale_error(
monkeypatch,
fake_translations,
reset_language,
):
setlocale = Mock(side_effect=language.locale.Error("Locale inválido"))

monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(language.locale, "setlocale", setlocale)

language.setLanguage("pt_BR")

assert language.getLanguage() == "pt_BR"
fake_translations.install.assert_called_once()
assert setlocale.called


def test_set_language_invalid_input_uses_portuguese(
monkeypatch,
fake_translations,
reset_language,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(language.locale, "setlocale", Mock())

language.setLanguage(None)

assert language.getLanguage() == "pt"
fake_translations.install.assert_called_once()


def test_set_language_system_mode(
monkeypatch,
fake_translations,
reset_language,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(
language,
"_get_system_language",
lambda: "pt_BR",
)

language.setLanguage("system")

assert language.getLanguage() == "pt_BR"
fake_translations.install.assert_called_once()


def test_set_language_system_mode_without_system_locale(
monkeypatch,
fake_translations,
reset_language,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(
language,
"_get_system_language",
lambda: "pt",
)

language.setLanguage("system")

assert language.getLanguage() == "pt"
fake_translations.install.assert_called_once()


def test_make_pgettext_returns_message_for_non_gnu_translation():
pgettext = language.makePgettext(object())

assert pgettext("menu", "Open") == "Open"


def test_make_pgettext_uses_context_catalog():
translations = gettext.GNUTranslations.new(
gettext.GNUTranslations
)
translations._catalog = {
"menu\x04Open": "Abrir",
}

pgettext = language.makePgettext(translations)

assert pgettext("menu", "Open") == "Abrir"


def test_make_pgettext_falls_back_to_original_message():
translations = gettext.GNUTranslations.new(
gettext.GNUTranslations
)
translations._catalog = {}

pgettext = language.makePgettext(translations)

assert pgettext("menu", "Missing") == "Missing"


def test_get_language_description_returns_none_on_linux(
monkeypatch,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")

assert language.getLanguageDescription("pt_BR") is None


def test_locale_name_to_windows_lcid_returns_zero_for_invalid_name(
monkeypatch,
):
monkeypatch.setattr(language.platform, "system", lambda: "Linux")
monkeypatch.setattr(language.locale, "windows_locale", {})

assert language.localeNameToWindowsLCID("invalid") == 0


def test_locale_name_to_windows_lcid_rejects_empty_input():
assert language.localeNameToWindowsLCID("") == 0
assert language.localeNameToWindowsLCID(None) == 0 
