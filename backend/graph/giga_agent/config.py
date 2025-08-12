import os
from operator import add
from typing import TypedDict, Annotated, List

from langchain_core.messages import AnyMessage
from langchain_gigachat import GigaChat
from langgraph.graph import add_messages

from giga_agent.repl_tools.llm import summarize
from giga_agent.repl_tools.sentiment import predict_sentiments, get_embeddings
from giga_agent.tools.another import (
    search,
    ask_about_image,
    generate_image,
)
from giga_agent.tools.github import (
    get_workflow_runs,
    list_pull_requests,
    get_pull_request,
)
from giga_agent.tools.repl import shell
from giga_agent.tools.scraper import get_urls
from giga_agent.tools.vk import vk_get_posts, vk_get_comments, vk_get_last_comments
from giga_agent.tools.weather import weather

from giga_agent.agents.landing_agent.graph import create_landing
from giga_agent.agents.lean_canvas import lean_canvas
from giga_agent.agents.meme_agent.graph import create_meme
from giga_agent.agents.podcast.graph import podcast_generate
from giga_agent.agents.presentation_agent.graph import generate_presentation
from giga_agent.agents.gis_agent.graph import city_explore
from giga_agent.utils.env import load_project_env

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_project_env()


class AgentState(TypedDict):  # noqa: D101
    messages: Annotated[list[AnyMessage], add_messages]
    file_ids: Annotated[List[str], add]
    kernel_id: str
    tool_call_index: int
    tools: list


llm = GigaChat(
    model="GigaChat-2-Max",
    profanity_check=False,
    verify_ssl_certs=False,
    timeout=os.getenv("MAIN_GIGACHAT_TIMEOUT", 70),
    max_tokens=1280000,
    user=os.getenv("MAIN_GIGACHAT_USER"),
    password=os.getenv("MAIN_GIGACHAT_PASSWORD"),
    credentials=os.getenv("MAIN_GIGACHAT_CREDENTIALS"),
    scope=os.getenv("MAIN_GIGACHAT_SCOPE"),
    base_url=os.getenv("MAIN_GIGACHAT_BASE_URL"),
    top_p=os.getenv("MAIN_GIGACHAT_TOP_P", 0.5),
)

if os.getenv("REPL_FROM_MESSAGE", "1") == "1":
    from giga_agent.tools.repl.message_tool import python
else:
    from giga_agent.tools.repl.args_tool import python


MCP_CONFIG = {}

SERVICE_TOOLS = [
    weather,
    # VK TOOLS
    vk_get_posts,
    vk_get_comments,
    vk_get_last_comments,
    # GITHUB TOOLS
    get_workflow_runs,
    list_pull_requests,
    get_pull_request,
]

AGENTS = [
    lean_canvas,
    create_landing,
    podcast_generate,
    generate_presentation,
    create_meme,
    get_urls,
    search,
]

if os.getenv("TWOGIS_TOKEN"):
    AGENTS += [city_explore]

TOOLS = (
    [
        # REPL
        python,
        shell,
        # SEARCH TOOLS
        get_urls,
        search,
        ask_about_image,
        generate_image,
    ]
    + AGENTS
    + SERVICE_TOOLS
)

REPL_TOOLS = [predict_sentiments, summarize, get_embeddings]

AGENT_MAP = {agent.name: agent for agent in AGENTS}
