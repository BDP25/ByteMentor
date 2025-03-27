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
from logger import LOGGER


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
        if filetype not in {"pptx", "docx", "pdf"}:
            continue

        if filetype == "pptx":
            text = extract_text_from_pptx(pptx_path=obj_path)
        elif filetype == "docx":
            text = extract_text_from_docx(docx_path=obj_path)
        elif filetype == "pdf":
            text = extract_text_from_pdf(pdf_path=obj_path)

        if text:
            load_to_mongodb(
                data=parse_to_dict(
                    filename=obj_path, text=text, src_lang=detect_language(text=text)
                ),
                collection_name="text_extracted",
            )
        else:
            LOGGER.warning(f"No text for {obj_path} detected.")


def translate_data(target_lang: str = "en") -> None:
    data = extract_from_mongod(collection_name="text_extracted")
    load_collection_name = f"translated_{target_lang}"
    for document in data:
        if extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name,
        ):
            continue

        document_language = document["language"]
        text = None
        if (document_language != target_lang) and document_language:
            text = translate_text(
                filename=document["filename"],
                text=document["content"],
                src_lang=document_language,
                dest_lang=target_lang,
            )
        if text:
            document["content"] = text
            document["language"] = target_lang
            document["translated"] = True
        else:
            document["translated"] = False
        load_to_mongodb(document, collection_name=load_collection_name)


# Set to True/False to include/exclude steps in the workflow
extract = False
translate = True
transform = False
dir_path = r"root_path"

if __name__ == "__main__":
    if extract:
        scan_and_extract_files(root_dir=dir_path)
    if translate:
        translate_data()
    if transform:
        pass
