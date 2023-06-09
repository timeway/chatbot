from typing import List, Tuple

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, BaseMessage, AIMessage

from . import env


def combine_message(question: str, chat_history: List[Tuple[str, str]]) -> List[BaseMessage]:
    messages: List[BaseMessage] = []
    if chat_history is not None:
        for human_s, ai_s in chat_history:
            messages.append(HumanMessage(content=human_s))
            messages.append(AIMessage(content=ai_s))

    messages.append(HumanMessage(content=question))
    return messages


class LLMHelper:
    def __init__(self, temperature: float = 0.7, max_tokens: int = 800, callbacks: List[BaseCallbackHandler] = None, streaming: bool = False):
        self.llm = AzureChatOpenAI(
            deployment_name=env.OPENAI_ENGINE_DEPLOYMENT_NAME,
            model_name=env.OPENAI_ENGINE_MODEL_NAME,
            openai_api_key=env.OPENAI_API_KEY,
            openai_api_base=env.OPENAI_API_BASE,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
            callbacks=callbacks,
            verbose=True
        )

    def generate_response(self, question: str, chat_history: List[Tuple[str, str]] = None):
        response: BaseMessage = self.llm(messages=combine_message(question, chat_history))
        return response.content
