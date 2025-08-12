import json

from langchain_core.messages import AIMessage, ToolMessage, HumanMessage

FEW_SHOTS_ORIGINAL = [
    HumanMessage(
        content="""<task>Вычисли 10-ое число фибоначи</task> Активно планируй и следуй своему плану! Действуй по простым шагам!
Следующий шаг:"""
    ),
    AIMessage(
        content="""<thinking>
Сначала вычислим числа Фибоначчи до десятого числа, используя простой рекурсивный подход или итерационный метод. Итерации предпочтительнее из-за лучшей производительности.
</thinking>
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibonacci(9))  # Так как индекс начинается с 0, 10-е число будет иметь индекс 9
```
""",
        tool_calls=[dict(name="python", args={}, id="123")],
    ),
    ToolMessage(
        tool_call_id="123",
        content=json.dumps(
            {
                "message": 'Результат выполнения: "34". Не забудь, что пользователь не видит этот результат, поэтому если нужно перепиши его.\nПроверь результат выполнения. Твой следующий шаг: ',
                "file_ids": [],
                "is_exception": False,
            },
            ensure_ascii=False,
        ),
    ),
    AIMessage(
        content="<thinking>\nВ результате работы кода, я получил результат 34. Теперь мне нужно вывести его пользователю\n</thinking>\n10-ое число Фибоначчи равно **34**."
    ),
    HumanMessage(
        """<task>Кто выиграл евро-2024?</task> Активно планируй и следуй своему плану! Действуй по простым шагам!
Следующий шаг:"""
    ),
    AIMessage(
        content="""<thinking>
Евро-2024 – это футбольный турнир, который проходит каждые четыре года среди европейских национальных сборных команд. Учитывая дату проведения турнира, которая обычно приходится на лето четных лет, Евро-2024 скорее всего проходил летом 2024 года. Поскольку текущая дата – июнь 2025 года, результаты турнира должны были стать известны ранее.

Чтобы ответить на вопрос, кто выиграл Евро-2024, я могу воспользоваться поиском информации в интернет-ресурсах, где традиционно публикуются итоги крупных спортивных событий. Для поиска информации я использую инструмент `search`.
</thinking>

План:
1. Найти победителя Евро-2024 через поиск.

Начну выполнение плана с первого пункта.
""",
        tool_calls=[
            dict(name="search", args={"queries": ["Победитель Евро-2024"]}, id="123")
        ],
    ),
    ToolMessage(
        tool_call_id="123",
        content=json.dumps(
            {
                "data": [
                    {
                        "query": "Победитель Евро-2024",
                        "follow_up_questions": None,
                        "answer": None,
                        "images": [],
                        "results": [
                            {
                                "title": "Евро-2024 - кто победил на чемпионате Европы - 24 канал Спорт",
                                "url": "https://sport.24tv.ua/ru/evro-2024-kto-pobedil-chempionate-evropy_n2596866",
                                "content": "Победитель Евро 2024 определился в финале между сборными Испании и Англии. Какая сборная выиграла чемпионат Европы 2024 в противостоянии Испания - Англия узнайте на сайте 24 Канал Спорт.",
                                "score": 0.902481,
                                "raw_content": None,
                            },
                            {
                                "title": "Испания - Победитель Евро-2024 - Спорт.ua",
                                "url": "https://sport.ua/news/693801-ispaniya-pobeditel-evro-2024",
                                "content": "Испания - победитель Евро-2024 В финале подопечные де ла Фуэнте переиграли Англию 14 июля 2024, 23:55 | Обновлено 16 июля 2024, 19:52",
                                "score": 0.84918517,
                                "raw_content": None,
                            },
                            {
                                "title": "Досье Победителей Евро-2024 | Uefa Euro 2024",
                                "url": "https://www.uefa.com/euro2024/news/028f-1b4e6c936ec4-43c850dd0239-1000--досье-п/",
                                "content": "Испания. Лучший результат на ЕВРО: победитель (1964, 2008, 2012, 2024) Предыдущие финалы на ЕВРО: 1964 (победа над СССР",
                                "score": 0.82186085,
                                "raw_content": None,
                            },
                            {
                                "title": "UEFA Euro 2024 - Wikipedia",
                                "url": "https://en.wikipedia.org/wiki/UEFA_Euro_2024",
                                "content": "It was the third time that European Championship matches were played on German territory, and the second time in reunified Germany, as West Germany hosted the 1988 tournament, and four matches of the multi-national Euro 2020 were played in Munich. Munich, the site of the first game of UEFA Euro 2024, was also a host city at the multi-national UEFA Euro 2020 tournament, hosting four matches (three involving Germany) in front of a greatly reduced number of spectators due to COVID-19 restrictions. UEFA announced the tournament schedule on 10 May 2022, which included kick-off times only for the opening match, semi-finals, and final. On 20 July 2024, after an open vote on the official Euro 2024 website, UEFA announced that Turkish defender Mert Müldür's group stage goal against Georgia had been chosen as the fans' goal of the tournament.",
                                "score": 0.54855317,
                                "raw_content": None,
                            },
                            {
                                "title": "Финал чемпионата Европы по футболу 2024 — Википедия",
                                "url": "https://ru.wikipedia.org/wiki/Финал_чемпионата_Европы_по_футболу_2024",
                                "content": "Финал чемпионата Европы по футболу 2024 — футбольный матч, завершивший чемпионат Европы 2024 года.Стал 17-м финалом в истории чемпионатов Европы, футбольного турнира, проводимого каждые четыре года среди национальных",
                                "score": 0.3929895,
                                "raw_content": None,
                            },
                        ],
                        "response_time": 2.49,
                    }
                ],
                "message": "Результат функции сохранен в переменную `function_results[0]['data']` ",
            },
            ensure_ascii=False,
        ),
    ),
    AIMessage(
        content="""<thinking>
Результаты поиска показывают, что победителем Евро-2024 стала сборная Испании. Эта информация подтверждается несколькими источниками, включая сайт Sport.ua и УЕФА. Таким образом, ответ на вопрос очевиден.
</thinking>

Победителем Евро-2024 стала сборная **Испании**, победившая сборную Англии в финале."""
    ),
    HumanMessage(
        content="Ок, супер! Забудь теперь нашу переписку ранее, я готов приступать к следующей задаче"
    ),
    AIMessage(
        content="""<thinking>
Пользователь попросил меня забыть переписку выше и приступить к новой задаче.
</thinking>

Ок, я готов к новой задаче!"""
    ),
]


FEW_SHOTS_UPDATED = [
    HumanMessage(
        content="""<task>Вычисли 10-ое число фибоначи</task> Активно планируй и следуй своему плану! Действуй по простым шагам!
Следующий шаг:"""
    ),
    AIMessage(
        content="""<thinking>
Сначала вычислим числа Фибоначчи до десятого числа, используя простой рекурсивный подход или итерационный метод. Итерации предпочтительнее из-за лучшей производительности.
</thinking>
""",
        tool_calls=[
            dict(
                name="python",
                args={
                    "code": """def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibonacci(9))  # Так как индекс начинается с 0, 10-е число будет иметь индекс 9"""
                },
                id="123",
            )
        ],
    ),
    ToolMessage(
        tool_call_id="123",
        content=json.dumps(
            {
                "message": 'Результат выполнения: "34". Не забудь, что пользователь не видит этот результат, поэтому если нужно перепиши его.\nПроверь результат выполнения. Твой следующий шаг: ',
                "file_ids": [],
                "is_exception": False,
            },
            ensure_ascii=False,
        ),
    ),
    AIMessage(
        content="<thinking>\nВ результате работы кода, я получил результат 34. Теперь мне нужно вывести его пользователю\n</thinking>\n10-ое число Фибоначчи равно **34**."
    ),
    HumanMessage(
        """<task>Кто выиграл евро-2024?</task> Активно планируй и следуй своему плану! Действуй по простым шагам!
Следующий шаг:"""
    ),
    AIMessage(
        content="""<thinking>
Евро-2024 – это футбольный турнир, который проходит каждые четыре года среди европейских национальных сборных команд. Учитывая дату проведения турнира, которая обычно приходится на лето четных лет, Евро-2024 скорее всего проходил летом 2024 года. Поскольку текущая дата – июнь 2025 года, результаты турнира должны были стать известны ранее.

Чтобы ответить на вопрос, кто выиграл Евро-2024, я могу воспользоваться поиском информации в интернет-ресурсах, где традиционно публикуются итоги крупных спортивных событий. Для поиска информации я использую инструмент `search`.
</thinking>

План:
1. Найти победителя Евро-2024 через поиск.

Начну выполнение плана с первого пункта.
""",
        tool_calls=[
            dict(name="search", args={"queries": ["Победитель Евро-2024"]}, id="123")
        ],
    ),
    ToolMessage(
        tool_call_id="123",
        content=json.dumps(
            {
                "data": [
                    {
                        "query": "Победитель Евро-2024",
                        "follow_up_questions": None,
                        "answer": None,
                        "images": [],
                        "results": [
                            {
                                "title": "Евро-2024 - кто победил на чемпионате Европы - 24 канал Спорт",
                                "url": "https://sport.24tv.ua/ru/evro-2024-kto-pobedil-chempionate-evropy_n2596866",
                                "content": "Победитель Евро 2024 определился в финале между сборными Испании и Англии. Какая сборная выиграла чемпионат Европы 2024 в противостоянии Испания - Англия узнайте на сайте 24 Канал Спорт.",
                                "score": 0.902481,
                                "raw_content": None,
                            },
                            {
                                "title": "Испания - Победитель Евро-2024 - Спорт.ua",
                                "url": "https://sport.ua/news/693801-ispaniya-pobeditel-evro-2024",
                                "content": "Испания - победитель Евро-2024 В финале подопечные де ла Фуэнте переиграли Англию 14 июля 2024, 23:55 | Обновлено 16 июля 2024, 19:52",
                                "score": 0.84918517,
                                "raw_content": None,
                            },
                            {
                                "title": "Досье Победителей Евро-2024 | Uefa Euro 2024",
                                "url": "https://www.uefa.com/euro2024/news/028f-1b4e6c936ec4-43c850dd0239-1000--досье-п/",
                                "content": "Испания. Лучший результат на ЕВРО: победитель (1964, 2008, 2012, 2024) Предыдущие финалы на ЕВРО: 1964 (победа над СССР",
                                "score": 0.82186085,
                                "raw_content": None,
                            },
                            {
                                "title": "UEFA Euro 2024 - Wikipedia",
                                "url": "https://en.wikipedia.org/wiki/UEFA_Euro_2024",
                                "content": "It was the third time that European Championship matches were played on German territory, and the second time in reunified Germany, as West Germany hosted the 1988 tournament, and four matches of the multi-national Euro 2020 were played in Munich. Munich, the site of the first game of UEFA Euro 2024, was also a host city at the multi-national UEFA Euro 2020 tournament, hosting four matches (three involving Germany) in front of a greatly reduced number of spectators due to COVID-19 restrictions. UEFA announced the tournament schedule on 10 May 2022, which included kick-off times only for the opening match, semi-finals, and final. On 20 July 2024, after an open vote on the official Euro 2024 website, UEFA announced that Turkish defender Mert Müldür's group stage goal against Georgia had been chosen as the fans' goal of the tournament.",
                                "score": 0.54855317,
                                "raw_content": None,
                            },
                            {
                                "title": "Финал чемпионата Европы по футболу 2024 — Википедия",
                                "url": "https://ru.wikipedia.org/wiki/Финал_чемпионата_Европы_по_футболу_2024",
                                "content": "Финал чемпионата Европы по футболу 2024 — футбольный матч, завершивший чемпионат Европы 2024 года.Стал 17-м финалом в истории чемпионатов Европы, футбольного турнира, проводимого каждые четыре года среди национальных",
                                "score": 0.3929895,
                                "raw_content": None,
                            },
                        ],
                        "response_time": 2.49,
                    }
                ],
                "message": "Результат функции сохранен в переменную `function_results[0]['data']` ",
            },
            ensure_ascii=False,
        ),
    ),
    AIMessage(
        content="""<thinking>
Результаты поиска показывают, что победителем Евро-2024 стала сборная Испании. Эта информация подтверждается несколькими источниками, включая сайт Sport.ua и УЕФА. Таким образом, ответ на вопрос очевиден.
</thinking>

Победителем Евро-2024 стала сборная **Испании**, победившая сборную Англии в финале."""
    ),
    HumanMessage(
        content="Ок, супер! Забудь теперь нашу переписку ранее, я готов приступать к следующей задаче"
    ),
    AIMessage(
        content="""<thinking>
Пользователь попросил меня забыть переписку выше и приступить к новой задаче.
</thinking>

Ок, я готов к новой задаче!"""
    ),
]
