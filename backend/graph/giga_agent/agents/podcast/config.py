from typing import TypedDict, List, Union, Literal

from langchain_core.messages import AnyMessage
from langchain_gigachat import GigaChat

from giga_agent.agents.podcast.schema import ShortDialogue, MediumDialogue

podcast_llm = GigaChat(
    model="GigaChat-2-Max",
    profanity_check=False,
    timeout=120,
    disable_streaming=True,
    top_p=0.1,
    streaming=False,
)


class ConfigSchema(TypedDict):
    save_files: bool


class PodcastState(TypedDict):
    messages: List[AnyMessage]
    use_messages: bool
    url: str
    podcast_text: str
    dialogue: Union[ShortDialogue, MediumDialogue]
    question: str
    tone: Literal["entertaining", "formal"]
    length: Literal["short", "medium"]
    audio: str
    transcript: str
