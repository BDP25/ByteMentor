from langchain_community.llms.ollama import Ollama
import warnings
from logger import LOGGER

warnings.filterwarnings("ignore", category=DeprecationWarning)


def chat_with_model(
    message: str, zhaw_modul: str, model: str = "gemma3:1b", promt: str = str
) -> str | None:
    prompt = f"""
    You are given a text.  
    Your task is to transform it into a list wiht JSON-like dialogue format between 'human' and 'gpt'.

    Instructions:
    - The output must be a list of dictionary-like entries with 'from' (either 'human' or 'gpt') and 'value' (the text).
    - The structure should represent a natural input/output (question/answer) conversation, where the 'human' is asking questions (like a bachelor student in Data Science) and the 'gpt' is providing answers (like a teacher in {zhaw_modul}).
    - Keep the Questions and Answers simple, professional (less than 30 words).
    - Do **not** invent or add information.
    - If the input message is invalid or cannot be structured into a dialogue, return:  
      {{'error': 'Invalid input format.'}}

    Output Example:
    [
    {{'from': 'human', 'value': 'Tree spirit, can you teach me about trees?'}},
    {{'from': 'gpt', 'value': 'Of course! Trees breathe life into the world, offer shade, fruit, and shelter.'}},
    {{'from': 'human', 'value': 'What\'s your favorite tree?'}},
    {{'from': 'gpt', 'value': 'The oak! It\'s tall, sturdy, and full of history.'}}]

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


if __name__ == "__main__":
    test_message = """
    Trees are essential to life on Earth. 
    They absorb carbon dioxide, produce oxygen, and provide shelter for countless species. 
    Some trees, like the bristlecone pine, can live for thousands of years. 
    Trees also prevent soil erosion and influence local climates by providing shade and releasing moisture into the air.
    """

    print(chat_with_model(message=test_message, zhaw_modul="Biology"))
    print(chat_with_model(message=".sa.das.", zhaw_modul="Biology"))
