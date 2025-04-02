import re
from logger import LOGGER


def parse_to_dict(filename: str, text: str, src_lang: str | None) -> dict:
    filename_shortend = re.split(r"[\\/]Module[\\/]", filename, maxsplit=1)[1]
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
        msg=f"Parse to dict of file: {filename} with keywords: {keywords} complete."
    )
    return data
