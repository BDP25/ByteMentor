from langchain_community.llms.ollama import Ollama
import warnings
from logger import LOGGER
import json

warnings.filterwarnings("ignore", category=DeprecationWarning)

def chat_with_model(
    message: str, zhaw_modul: str, model: str = "gemma3:1b"
) -> str | None:
    prompt = prompt = f"""
    Extract exactly **two Q&A pairs** related to the module {zhaw_modul}. 
    1. The first Q&A pair should have a general question on a theoretical concept.
    2. The second should repeat the first question, with {zhaw_modul} included.

    Instructions:
    - Output must be valid JSON: a list of four dictionaries (two Q&A pairs).
    - Do not include a trailing comma after the last item.
    - Keep each question and answer under 30 words.
    - Both questions must focus on a theoretical concept related to {zhaw_modul}.
    - Use double quotes for all keys and values.
    - If no valid theory is found, return: {{"error": "Invalid input format."}}

    Example:
    [
    {{"from": "human", "value": "What is statistical inference?"}},
    {{"from": "gpt", "value": "It refers to drawing conclusions about a population from sample data."}},
    {{"from": "human", "value": "In the module {zhaw_modul}, what is statistical inference?"}},
    {{"from": "gpt", "value": "It refers to drawing conclusions about a population from sample data."}}
    ]

    Input:
    {message}
    """

    try:
        llm = Ollama(model=model)
        response = llm.invoke(prompt)
    except Exception as e:
        LOGGER.info(msg=f"Could not format to Q&A format: {e}")
        return None
    return response

def validata_response(response: str, filename: str) -> dict | None:
    try:
        response = response.strip()
        if response.startswith("```") and response.endswith("```"):
            response = "\n".join(response.split("\n")[1:-1]).strip()

        content = json.loads(response)
    except json.JSONDecodeError as e:
        LOGGER.error(f"Error parsing response for {filename}: {e}")
        return None

    try: 
        for entry in content:
            if not entry.get("from") in ["human", "gpt"] and entry.get("value"):
                LOGGER.error(f"Error invalid from-keys: {filename}")
                return None
        
        is_human = True
        for entry in content:
            if is_human and (entry.get("from") in ["human"]):
                is_human = False
            elif not is_human and (entry.get("from") in ["gpt"]):
                is_human = True
            else:
                LOGGER.error(f"Error Invalid From ordering: {filename}")
                return None
        if not is_human:
            LOGGER.error(f"Error Json did not end on gpt: {filename}")
            return None
        
    except Exception as e:
        LOGGER.error(f"Error {e}")
        return None
    
    LOGGER.info(f"Success {filename} : {content}")
    return content

if __name__ == "__main__":
    test_message = """
    Trees are essential to life on Earth. 
    They absorb carbon dioxide, produce oxygen, and provide shelter for countless species. 
    Some trees, like the bristlecone pine, can live for thousands of years. 
    Trees also prevent soil erosion and influence local climates by providing shade and releasing moisture into the air.
    """

    print(chat_with_model(message=test_message, zhaw_modul="Biology"))
    print(chat_with_model(message=".sa.das.", zhaw_modul="Biology"))
