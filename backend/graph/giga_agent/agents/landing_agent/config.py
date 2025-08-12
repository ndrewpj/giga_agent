from operator import add
from typing import TypedDict, Annotated, List, Dict

from langchain_core.messages import AnyMessage
from langchain_gigachat import GigaChat
from langgraph.graph import add_messages

llm = GigaChat(
    model="GigaChat-2-Max",
    profanity_check=False,
    timeout=120,
    disable_streaming=True,
    top_p=0.3,
    streaming=False,
)


class ConfigSchema(TypedDict):
    save_files: bool
    print_messages: bool


class LandingState(TypedDict):
    task: str
    agent_messages: Annotated[list[AnyMessage], add_messages]
    plan: str
    plan_messages: Annotated[list[AnyMessage], add_messages]
    image_messages: Annotated[list[AnyMessage], add_messages]
    image_plan_loaded: bool
    coder_messages: Annotated[list[AnyMessage], add_messages]
    coder_plan_loaded: bool
    images: Annotated[List[str], add]
    images_base_64: Dict[str, str]
    html: str
    done: str
