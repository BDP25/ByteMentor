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
    """
    available_languages = argostranslate.translate.get_installed_languages()
    if (
        src_lang not in available_languages or dest_lang not in available_languages
    ):  # download if language does not exist
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == src_lang and x.to_code == dest_lang,
                available_packages,
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())

    try:
        translation = argostranslate.translate.translate(text, src_lang, dest_lang)
        return translation
    except Exception:
        return None


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


def parse_to_dict(filename: str, text: str, src_lang: str | None) -> dict:
    filename_shortend = re.split(r"[\\/]Module[\\/]", filename, maxsplit=1)[1]
    print(filename_shortend)
    # Keywords is the folder structure. Example: Analysis/3/Lectures/filename -> [Analysis, 3, Lectures]
    keywords = [
        part
        for part in re.split(r"[\\/]", filename_shortend.split(r"[\\/]")[0])
        if part
    ]
    data = {
        "filename": filename,
        "Key-Words": keywords,
        "language": src_lang,
        "content": text,
    }
    LOGGER.info(
        f"Parse to dict of file: {filename} with keywords: {keywords} complete."
    )
    return data
