from langchain_gigachat import GigaChat
from langchain_core.output_parsers.json import JsonOutputParser

llm = GigaChat(
    profanity_check=False,
    verify_ssl_certs=False,
    timeout=100000,
    max_tokens=32000,
    model="GigaChat-2-Pro",
)


async def summarize(texts: list[str], addition: str = "") -> str:
    """
    Суммаризирует список текстов

    Args:
        texts: Список текстов на суммаризацию
        addition: На что во время суммаризации стоит обратить внимание
    """
    if addition:
        addition = f"\nОбрати особое внимание на {addition}\n"
    texts = "\n----\n".join(texts)
    return (
        await llm.ainvoke(
            [("system", f"""Суммаризируй текста ниже{addition}\n{texts}""")]
        )
    ).content


async def ask(prompt: str) -> str:
    return (await llm.ainvoke(input=[("system", prompt)])).content


async def ask_structure(prompt: str, json_schema: str) -> dict:
    return parse_partial_json(
        (
            await llm.ainvoke(
                input=[("system", f"{prompt}. Ответь в формате JSON: {json_schema}")]
            )
        ).content
    )


def parse_partial_json(s: str):
    return JsonOutputParser().invoke(s)
