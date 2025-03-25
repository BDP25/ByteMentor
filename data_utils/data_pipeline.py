import os
from data_utils.data_extraction import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
)
from data_utils.data_transformation import (
    translate_text,
    parse_to_dict,
    detect_language,
)
from data_utils.mongodb import load_to_mongodb, extract_from_mongod


def scan_and_extract_files(root_dir: str) -> None:
    for obj in os.listdir(root_dir):
        obj_path = os.path.join(root_dir, obj)

        if os.path.isdir(obj_path):
            scan_and_extract_files(root_dir=obj_path)
            continue

        # Skip if file already is in DB
        if extract_from_mongod(
            query={"filename": obj_path}, collection_name="text_extracted"
        ):
            continue

        filetype = obj.split(".")[-1].lower()
        text = None

        if filetype == "pptx":
            text = extract_text_from_pptx(pptx_path=obj_path)
        elif filetype == "docx":
            text = extract_text_from_docx(docs_path=obj_path)
        elif filetype == "pdf":
            text = extract_text_from_pdf(pdf_path=obj_path)

        if text:
            target_lang = "en"
            if (text_lang := detect_language(text=text)) != target_lang:
                text = translate_text(
                    text=text, src_lang=text_lang, dest_lang=target_lang
                )

        if text:
            load_to_mongodb(
                data=parse_to_dict(filename=obj, text=text), collection="text_extracted"
            )


# Set to True/False to include/exclude steps in the workflow
extract = False
transform = False
dir_path = "dir_path"

if __name__ == "__main__":
    if extract:
        scan_and_extract_files(root_dir=dir_path)
    if transform:
        pass
