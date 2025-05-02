import os
from data_utils.extraction import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
)
from data_utils.transform import parse_to_dict
from data_utils.translate import translate_text, detect_language
from data_utils.mongodb import load_to_mongodb, extract_from_mongod
from logger import LOGGER
from data_utils.ollama_llm import chat_with_model
import json


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
    load_collection_name_succes = f"translated_{target_lang}_success"
    load_collection_name_error = f"translated_{target_lang}_error"
    for document in data:
        if extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name_succes,
        ) or extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name_error,
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
                load_to_mongodb(document, collection_name=load_collection_name_error)
                continue

            document["translated"] = True
            document["content"] = text
            document["language"] = target_lang

        load_to_mongodb(document, collection_name=load_collection_name_succes)


def transform_into_qa_format() -> None:
    LOGGER.info(msg="Transforming data to QA format")
    data = extract_from_mongod(collection_name="translated_en_success")

    load_collection_name_succes = "Q&A_format_success"
    load_collection_name_error = "Q&A_format_error"

    for document in data:
        keywords_exclude = [
            "abgaben",
            "lab",
            "labs",
            "labs-20230223",
            "praktikum",
            "pratikum",
            "probe_pruefung",
            "lösung serie",
            "sep",
            "graded_lab",
            "exercises",
            "exercise",
            "uebung",
        ]
        if any(kw.lower() in keywords_exclude for kw in document["Key-Words"]):
            continue

        if extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name_succes,
        ) or extract_from_mongod(
            query={"filename": document["filename"]},
            collection_name=load_collection_name_error,
        ):
            continue

        content_qa = []
        zhaw_module = document["Key-Words"][0]
        paragraphs = [
            "\n".join(document["content"].split("\n")[i : i + 4]).strip()
            for i in range(0, len(document["content"].split("\n")), 4)
        ]

        if not paragraphs:
            LOGGER.warning(f"No paragraphs for {document['filename']} detected.")
            load_to_mongodb(document, collection_name=load_collection_name_error)
            continue

        LOGGER.info(msg=f"Transforming {document['filename']} to Q&A format")
        for i, paragraph in enumerate(paragraphs):
            print(f"Processing paragraph {i + 1}/{len(paragraphs)}")
            if not paragraph:
                continue

            if not (
                response := chat_with_model(message=paragraph, zhaw_modul=zhaw_module)
            ):
                continue

            try:
                response = response.strip()
                if response.startswith("```") and response.endswith("```"):
                    response = "\n".join(response.split("\n")[1:-1]).strip()

                content = json.loads(response)
            except json.JSONDecodeError as e:
                LOGGER.error(f"Error parsing response for {document['filename']}: {e}")
                continue

            for entry in content:
                if entry.get("from") in ["human", "gpt"] and entry.get("value"):
                    content_qa.append(entry)

        if not content_qa:
            load_to_mongodb(document, collection_name=load_collection_name_error)
        else:
            document["content"] = content_qa
            load_to_mongodb(document, collection_name=load_collection_name_succes)


# Set to True/False to include/exclude steps in the workflow
extract = False
translate = False
transform_qa = True
transform_training = False
dir_path = r"C:\Users\damia\OneDrive\Documents\Studium_Weiterbildung\ZHAW_Zuercher_Hochschuele_fuer_angewandte_Wissenschaften\Bachlor_Data_Science\Module"

if __name__ == "__main__":
    if extract:
        LOGGER.info(msg=f"Starting data extraction at directory: {dir_path}")
        scan_and_extract_files(root_dir=dir_path)
    if translate:
        translate_data(target_lang="en")
    if transform_qa:
        transform_into_qa_format()
    if transform_training:
        pass
