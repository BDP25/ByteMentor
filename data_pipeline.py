import os
from data_utils.data_extraction import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
)
from data_utils.data_transformation import parse_to_dict
from data_utils.translate import translate_text, detect_language
from data_utils.mongodb import load_to_mongodb, extract_from_mongod
from logger import LOGGER


def scan_and_extract_files(root_dir: str) -> None:
    file_handlers = {
        "pptx": extract_text_from_pptx,
        "docx": extract_text_from_docx,
        "pdf": extract_text_from_pdf,
    }

    for obj in os.listdir(root_dir):
        obj_path = os.path.join(root_dir, obj)

        if os.path.isdir(obj_path):
            scan_and_extract_files(root_dir=obj_path)
            continue

        # Skip if file already is in DB
        if extract_from_mongod(
            query={"filename": obj_path}, collection_name="text_extracted_success"
        ) or extract_from_mongod(
            query={"filename": obj_path}, collection_name="text_extracted_error"
        ):
            continue

        filetype = obj.split(".")[-1].lower()
        if not (handler := file_handlers.get(filetype)):
            continue

        if text := handler(obj_path):
            load_to_mongodb(
                data=parse_to_dict(
                    filename=obj_path, text=text, src_lang=detect_language(text=text)
                ),
                collection_name="text_extracted_success",
            )
        else:
            LOGGER.warning(f"No text for {obj_path} detected.")
            load_to_mongodb(
                data={"filename": obj_path}, collection_name="text_extracted_error"
            )


def translate_data(target_lang: str = "en") -> None:
    LOGGER.info(msg=f"Translating data to {target_lang}")
    data = extract_from_mongod(collection_name="text_extracted_success")
    load_collection_name = f"text_{target_lang}"
    for document in data:
        if extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name,
        ):
            continue

        if not (document_language := document["language"]):
            continue

        if document_language == target_lang:
            document["translated"] = False
        else:
            text = translate_text(
                filename=document["filename"],
                text=document["content"],
                src_lang=document_language,
                dest_lang=target_lang,
            )
            if not text:
                continue

            document["translated"] = True
            document["content"] = text
            document["language"] = target_lang

        load_to_mongodb(document, collection_name=load_collection_name)


# Set to True/False to include/exclude steps in the workflow
extract = False
translate = True
transform_qa = False
transform_training = False
dir_path = r"path"

if __name__ == "__main__":
    if extract:
        LOGGER.info(msg=f"Starting data extraction at directory: {dir_path}")
        scan_and_extract_files(root_dir=dir_path)
    if translate:
        translate_data(target_lang="en")
        translate_data(target_lang="de")
    if transform_qa:
        pass
    if transform_training:
        pass
