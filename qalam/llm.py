from loguru import logger
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from qalam.config import settings


class LLM:
    def __init__(self) -> None:
        logger.info("Initializing OpenAI client...")

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=SecretStr(settings.openai_api_key),
        )

        self.messages = [
            (
                "developer",
                "You are a helpful assistant that answers programming questions and writes good quality code",
            ),
        ]

        logger.info("OpenAI client initialized successfully.")

    def invoke_chat(self, prompt: str) -> str | list[str | dict]:
        self.messages.append(("user", prompt))

        llm_res = self.llm.invoke(self.messages)
        logger.info("LLM response received.")

        response_text = llm_res.content
        logger.info("LLM response text: {}", response_text)

        if isinstance(response_text, str):
            self.messages.append(("assistant", response_text))
        else:
            logger.error("llm response wasn't of type str", response=response_text)

        return response_text
