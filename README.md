# GigaAgent
Универсальный агент.

В данном проекте реализована агентская система с REPL (выполнением кода), tools, внешними инструментами.


<img src="docs/images/schema.png" width=500>

Демо:

<img src="docs/images/demo.gif" width=500>

## Блоки
- **GigaAgent** — агент работающий на LangGraph
- **REPL** — отдельный контейнер, который может выполнять код в jupyter-like среде, написанный LLM
- **ToolServer** — сервер, который исполняет инструменты подключенные к LLM или закрытый код (или код завязанный на секретных env переменных), который мы не хотим шарить пользователю в REPL среде.
- **LLM Tools** — Инструменты (поиск, работа с данными ВК, работа с гитхабом и т.д.)
- **REPL Tools** — *predict_sentiments*, *get_embeddings*, *summarize*. Эти методы завязаны на API GigaChat и мы не хотим, чтобы пользователь в среде REPL, мог получить ключи с доступами к API
- **SubAgents** — под-агенты, выполняющие узко-направленные задачи. (Создание презентаций, Создание лендингов и т.д.)

## Запуск (через Docker)
1. make init_files
2. Заполнить .docker.env в корне проекта
3. make build_graph
4. docker compose up -d
5. Проект запущен на http://localhost:8502

## Локальный запуск
Для локального запуска желательно иметь следующие свободные порты: **2024**, **8811**, **9090**, **9092**, **3000**

Если освободить эти порты нельзя, то поправьте .env переменные и [vite.config.ts](front/vite.config.ts)
1. make init_files
2. Заполнить .env в корне проекта
3. Запуск REPL
   * `cd backend/repl`
   * `uv sync`
   * `make run`
4. Запуск Upload Server на REPL
   * `cd backend/repl`
   * `make run_u`
5. Запуск ToolServer
   * `cd backend/graph`
   * `uv sync`
   * `make run_tool_server`
6. Запуск LangGraph
   * `cd backend/graph`
   * `make run_graph`
7. Запуск frontend
   * `cd front`
   * `make dev`

## Генерация изображений
Агент может генерировать изображения. Э

## Внешние сервисы
GigaAgent подключен к внешним сервисам, поэтому для корректной работы некоторых сценариев нужно получить их API ключи.

Также можно отключить тулы/агентов в файле [config](backend/graph/giga_agent/config.py), если нет возможности получить API ключ какого-либо сервиса.

Для этого посмотрите, какие тулы/агенты зависят от сервиса и закомментируйте их в переменных **TOOLS**/**SERVICE_TOOLS**

Ниже ссылки и инструкции
### Tavily (поиск в интернете)
Тулы/агенты, которые зависят от сервиса: **search**, **get_urls**, **city_explore**

Получить API ключ можно здесь: https://tavily.com/

### GitHub
Тулы/агенты, которые зависят от сервиса: **get_workflow_runs**, **list_pull_requests**, **get_pull_request**

Получить API ключ можно здесь: https://github.com/settings/personal-access-tokens

### VK
Тулы/агенты, которые зависят от сервиса: **vk_get_posts**, **vk_get_comments**, **vk_get_last_comments**

Для работы с ВК нужно создать мини-приложение, здесь: https://dev.vk.com/ru/admin/apps-list.
И получить сервисный API-ключ от приложения.

### 2GIS
Тулы/агенты, которые зависят от сервиса: **city_explore**

В

### SaluteSpeech (синтез голоса)
Тулы/агенты, которые зависят от сервиса: **podcast_generate**

https://developers.sber.ru/portal/products/smartspeech

### OpenWeatherMap (получение погоды)
Тулы/агенты, которые зависят от сервиса: **weather**

https://openweathermap.org/api/one-call-3