export const Config = {
  FILE_SERVER: "http://127.0.0.1:9090/",
};

export const TOOL_MAP = {
  lean_canvas: "Агент по созданию Lean Canvas",
  python: "Код-интерпретатор",
  search: "Поиск",
  shell: "Командная строка",
  vk_get_posts: "Получение постов (ВК)",
  ask_about_image: "Анализ изображения",
  vk_get_comments: "Получение комментариев к посту (ВК)",
  vk_get_last_comments: "Получение последних комментариев (ВК)",
  get_workflow_runs: "Получение CI Runs (GitHub)",
  get_cve_for_package: "Получение CVE для пакета",
  get_pull_request: "Получение PR (GitHub)",
  list_pull_requests: "Получение списка PR (GitHub)",
  weather: "Получение погоды",
  create_landing: "Создание веб-страницы",
  podcast_generate: "Генерация подкаста",
  debates: "Дебаты агентов",
  generate_presentation: "Генерация презентации",
  create_meme: "Агент Мемов",
  get_urls: "Скачивание ссылок",
  city_explore: "Исследователь города",
  gen_image: "Генерация изображения",
};

export const PROGRESS_AGENTS = {
  lean_canvas: {
    "1_customer_segments": "Определяет целевых клиентов",
    "2_problem": "Определяет проблему",
    "3_unique_value_proposition": "Определяет уникальное предложение",
    "3.1_check_unique": "Определяет уникальное предложение",
    "4_solution": "Предлагает решение проблем",
    "5_channels": "Находит каналы привлечения",
    "6_revenue_streams": "Планирует заработок",
    "7_cost_structure": "Определяет затраты",
    "8_key_metrics": "Определяет ключевые метрики",
    "9_unfair_advantage": "Находит преимущество",
    get_feedback: "Находит преимущество",
  },
  create_landing: {
    plan: "Создание плана страницы",
    image: "Генерация изображений",
    coder: "Создание кода страницы",
  },
  podcast_generate: {
    __start__: "Скачивание контента страницы",
    download: "Анализ переписки",
    summarize_messages: "Генерация сюжета подкаста",
    script: "Генерация аудио",
    audio_gen: "Генерация аудио",
  },
  generate_presentation: {
    __start__: "Создание плана",
    plan_node: "Генерация изображений",
    image: "Генерация слайдов",
    slides_node: "Генерация слайдов",
  },
  create_meme: {
    __start__: "Генерация идеи",
    text: "Генерация изображения",
    image: "Генерация изображения",
  },
  city_explore: {
    __start__: "Поиск достопримечательностей",
    attractions_node: "Поиск отелей",
    hotels_node: "Поиск лучших ресторанов / кафе",
    food_node: "Поиск лучших ресторанов / кафе",
  },
};

export const TIME_TO_NEXT_TASK = 15;
