import asyncio
import base64
import os

import httpx
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableConfig,
)

from giga_agent.agents.meme_agent.config import llm, MemeState
from giga_agent.agents.meme_agent.prompts.ru import IMAGE_PROMPT

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

from giga_agent.generators.image import load_image_gen

semaphore = asyncio.Semaphore(7)


class CensorException(Exception):
    """Запрос отклонён цензурой (HTTP 451)."""

    pass


async def generate_image_async(
    prompt: str,
    width: int,
    height: int,
    token: str,
    client,
    *,
    max_retries: int = 3,
    timeout: float | None = 60.0,
) -> str:
    """
    Асинхронно генерирует изображение в Kandinsky-4.1.

    • Повторяет запрос до `max_retries` раз,
      *кроме* случая HTTP 451 — тогда сразу `CensorException`.
    • Возвращает финальный объект `httpx.Response`
      (успешный либо последний неуспешный).

    :raises CensorException: при коде 451.
    :raises httpx.HTTPStatusError: если достигнут лимит ретраев
                                   и статус остаётся ошибочным (≠2xx, 3xx).
    """
    async with semaphore:
        payload = {
            "mode": "kandinsky-4.1:image",
            # "cache_force_bypass": True,
            "query": prompt,
            "model_params": {
                "width": width,
                "height": height,
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        attempt = 0
        while True:
            attempt += 1
            resp = await client.post(
                "https://gigachat.devices.sberbank.ru/api/v1/image/generate",
                json=payload,
                headers=headers,
            )

            # 451 — сразу исключение без повторных попыток
            if resp.status_code in [451]:
                raise CensorException("Server returned HTTP 451 — access restricted.")

            # Любой успешный статус — возвращаем
            if resp.is_success:
                return base64.b64encode(resp.content).decode("ascii")

            # Неуспех: если исчерпали лимит — поднимаем HTTPStatusError
            if attempt >= max_retries:
                resp.raise_for_status()  # пробросит httpx.HTTPStatusError
            else:
                # Мини-бэкофф, чтобы не бомбить сервер
                await asyncio.sleep(2 ** (attempt - 1))  # 1 с, 2 с …
                continue


def memeify(
    img_bytes: bytes,
    up_text: str,
    down_text: str,
    font_path: str = "impact.ttf",  # путь к шрифту Impact
    font_ratio: float = 0.07,  # высота текста ≈ 10 % от ширины картинки
    stroke: int = 2,  # толщина обводки
    margin_ratio: float = 0.05,  # поля сверху/снизу
) -> bytes:
    """Наносит up_text и down_text на картинку, возвращает bytes."""

    def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
        """Возвращает (w, h) c учётом версии Pillow."""
        if hasattr(draw, "textbbox"):  # Pillow ≥ 8.0, в т.ч. ≥10
            bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        else:  # старые Pillow
            return draw.textsize(text, font=font)  # type: ignore[attr-defined]

    def wrap_lines(draw, text, font, max_width):
        """Разбивает текст на строки так, чтобы каждая влезла в max_width."""
        words = text.upper().split()
        lines, line = [], []
        for word in words:
            test = " ".join(line + [word])
            if draw.textlength(test, font=font) <= max_width:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        if line:
            lines.append(" ".join(line))
        return lines

    # открываем картинку
    im = Image.open(BytesIO(img_bytes)).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)

    # подбираем размер шрифта из ширины картинки
    font_size = int(w * font_ratio)

    font = ImageFont.truetype(os.path.join(__location__, "impact.ttf"), font_size)

    max_width = w - int(w * margin_ratio * 2)

    # --- верхний текст ---
    top_lines = wrap_lines(draw, up_text, font, max_width)
    y = int(h * margin_ratio)
    for line in top_lines:
        line_w, line_h = text_size(draw, line, font=font)
        x = (w - line_w) // 2
        # чёрный контур
        draw.text(
            (x, y),
            line,
            font=font,
            fill="white",
            stroke_width=stroke,
            stroke_fill="black",
        )
        y += line_h + 5  # небольшой интервал между строками

    # --- нижний текст ---
    bottom_lines = wrap_lines(draw, down_text, font, max_width)[
        ::-1
    ]  # рисуем снизу вверх
    y = h - int(h * margin_ratio)
    for line in bottom_lines:
        line_w, line_h = text_size(draw, line, font=font)
        y -= line_h
        x = (w - line_w) // 2
        draw.text(
            (x, y),
            line,
            font=font,
            fill="white",
            stroke_width=stroke,
            stroke_fill="black",
        )
        y -= 5

    # сохраняем в bytes
    out = BytesIO()
    im = im.resize((512, 512), Image.Resampling.LANCZOS)
    im.save(out, format="PNG")
    return out.getvalue()


img_ch = (
    IMAGE_PROMPT
    | llm
    | RunnableParallel({"message": RunnablePassthrough(), "json": JsonOutputParser()})
).with_retry()


async def image_node(state: MemeState, config: RunnableConfig):
    resp = await img_ch.ainvoke(
        {
            "messages": [
                (
                    "user",
                    f"Идея пользователя: '{state['task']}'\n"
                    + state["messages"][-1].content,
                )
            ]
        }
    )
    if config["configurable"].get("print_messages", False):
        resp["message"].pretty_print()
    image_gen = load_image_gen()
    await image_gen.init()
    image_data = await image_gen.generate_image(
        resp["json"]["image"]["description"], 1024, 1024
    )
    image_data = memeify(
        base64.b64decode(image_data),
        state["meme_idea"]["up_text"],
        state["meme_idea"]["down_text"],
        stroke=6,
    )

    return {"meme_image": base64.b64encode(image_data).decode("ascii")}
