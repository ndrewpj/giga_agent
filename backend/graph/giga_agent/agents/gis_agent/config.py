from typing import TypedDict, List

from langchain_gigachat import GigaChat

from giga_agent.agents.gis_agent.utils.gis_client import Location, Attraction, Point

llm = GigaChat(
    model="GigaChat-2-Max",
    verify_ssl_certs=False,
    profanity_check=False,
    timeout=120,
    disable_streaming=True,
    top_p=0.4,
    streaming=False,
)


class ConfigSchema(TypedDict):
    fetch_descriptions: bool
    print_messages: bool


class MapState(TypedDict):
    city_name: str
    city_point: Point
    hotels: List[Location]
    food: List[Location]
    attractions: List[Attraction]
