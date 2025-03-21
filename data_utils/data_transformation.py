from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import re


def detect_language(text: str) -> str | None:
    DetectorFactory.seed = 0
    try:
        language = detect(text)
        return language
    except Exception:
        return None


def translate_text(text: str, src_lang: str, dest_lang: str = "en") -> str | None:
    try:
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        return translated
    except Exception:
        return None


def parse_to_dict(
    filename: str,
    text: str,
) -> dict:
    current_dir = filename.split(r"[\\/]")[0]
    # Keywords is the folder structure. Example: Analysis/3/Lectures/filename -> [Analysis, 3, Lectures]
    keywords = [part for part in re.split(r"[\\/]", current_dir) if part]
    data = {"filename": filename, "Key-Words": keywords, "content": text}
    return data
