import os
from pathlib import Path
from dotenv import load_dotenv


def load_project_env(filename: str = ".env", override: bool = False) -> None:
    explicit = os.getenv("ENV_PATH")
    if explicit and Path(explicit).is_file():
        load_dotenv(explicit, override=override)
        return

    here = Path(__file__).resolve()
    for p in [here.parent, *here.parents]:
        candidate = p / filename
        if candidate.is_file():
            load_dotenv(candidate, override=override)
            return
