from typing import TypedDict, Annotated, List

from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import AnyMessage
from langchain_gigachat import GigaChat
from langgraph.graph import add_messages

llm = GigaChat(
    model="GigaChat-2-Max",
    verify_ssl_certs=False,
    profanity_check=False,
    timeout=120,
    disable_streaming=True,
    top_p=0.6,
    streaming=False,
)


class ConfigSchema(TypedDict):
    save_files: bool
    print_messages: bool


class MemeState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    task: str
    meme_idea: dict
    meme_image: str
