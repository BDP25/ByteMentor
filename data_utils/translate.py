from googletrans import Translator
import argostranslate.package
import argostranslate.translate
from langdetect import detect, DetectorFactory
import re
from logger import LOGGER


def detect_language(text: str) -> str | None:
    DetectorFactory.seed = 0
    try:
        language = detect(text)
        return language
    except Exception:
        return None


def translate_googletrans(
    text: str, src_lang: str, dest_lang: str = "en"
) -> str | None:
    """
    Translate via googletrans library
    """
    try:
        translator = Translator()
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception:
        return None


def translate_argostranslate(
    text: str, src_lang: str, dest_lang: str = "en"
) -> str | None:
    """
    Translating via Argos Translate uses pre-trained offline neural models.
    Split the text into sentences and translate each sentence separately for faster translations.
    """
    try:
        available_languages = argostranslate.translate.get_installed_languages()
        if src_lang not in available_languages or dest_lang not in available_languages:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == src_lang and x.to_code == dest_lang,
                    available_packages,
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())
    except Exception:
        LOGGER.warning("Argos Translate package installation failed.")
        return None

    translations = []
    sentences = re.split(r"(?<=[.!?]) +", text)
    for _, sentence in enumerate(sentences):
        try:
            translation = argostranslate.translate.translate(
                sentence, src_lang, dest_lang
            )
            translations.append(translation)
        except Exception:
            continue

    translated_text = " ".join(translations).strip()
    return translated_text or None


def translate_text(
    filename: str, text: str, src_lang: str, dest_lang: str = "en"
) -> str | None:
    """
    Translates text using different methodes until one returns a result or no more methodes are available
    """
    LOGGER.info(msg=f"Translating file: {filename}, from {src_lang} to {dest_lang}")

    if translated_text := translate_argostranslate(
        text=text, src_lang=src_lang, dest_lang=dest_lang
    ):
        return translated_text

    if translated_text := translate_googletrans(
        text=text, src_lang=src_lang, dest_lang=dest_lang
    ):
        return translated_text

    return None
