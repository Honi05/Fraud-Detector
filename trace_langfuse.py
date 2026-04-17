import os
import ulid
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langfuse import Langfuse, observe
from langfuse.langchain import CallbackHandler

load_dotenv(".env.py")
load_dotenv(".env")


def main():
    LANGFUSE_PUBLIC_KEY = os.environ["LANGFUSE_PUBLIC_KEY"]
    LANGFUSE_SECRET_KEY = os.environ["LANGFUSE_SECRET_KEY"]
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
    TEAM_NAME = os.getenv("TEAM_NAME", "my_team")

    print("DEBUG PUBLIC:", LANGFUSE_PUBLIC_KEY)
    print("DEBUG HOST:", LANGFUSE_HOST)

    # Initialize Langfuse client (mainly to validate keys)
    _ = Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
    )

    # LangChain callback handler for Langfuse
    handler = CallbackHandler()

    # Unique session id required by the challenge
    session_id = f"{TEAM_NAME}-{ulid.new().str}"

    # LLM via OpenRouter (OpenAI-compatible)
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model="openai/gpt-4.1-mini",
        callbacks=[handler],
    )

    config = {"metadata": {"langfuse_session_id": session_id}}

    @observe(name="trace_test_session", capture_input=True, capture_output=True)
    def run_test_calls():
        questions = [
            "Say 'hello' in one short sentence.",
            "In one sentence, explain what fraud detection is.",
            "Output a number between 0 and 1, like 0.42.",
        ]
        for q in questions:
            _ = llm.invoke(q, config=config)

    run_test_calls()

    print("Finished traced Langfuse session:", session_id)


if __name__ == "__main__":
    main()