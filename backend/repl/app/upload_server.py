import io
import mimetypes
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_gigachat import GigaChat
from dotenv import load_dotenv

from PIL import Image

load_dotenv("../../.env")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # кому разрешаем
    allow_credentials=True,  # передавать ли куки/креденшалы
    allow_methods=["*"],  # какие HTTP-методы
    allow_headers=["*"],  # какие заголовки
)

FILES_DIR = os.environ.get("FILES_DIR", "files")
os.makedirs(FILES_DIR, exist_ok=True)

llm = GigaChat(
    profanity_check=False,
    verify_ssl_certs=False,
    timeout=100000,
    max_tokens=32000,
    user=os.getenv("MAIN_GIGACHAT_USER"),
    password=os.getenv("MAIN_GIGACHAT_PASSWORD"),
    credentials=os.getenv("MAIN_GIGACHAT_CREDENTIALS"),
    scope=os.getenv("MAIN_GIGACHAT_SCOPE"),
    base_url=os.getenv("MAIN_GIGACHAT_BASE_URL"),
)

if not Path(FILES_DIR).exists():
    Path(FILES_DIR).mkdir(parents=True, exist_ok=True)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


@app.options("/upload")
def upload_options():
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        path = uniquify(os.path.join(FILES_DIR, file.filename))
        with open(path, "wb") as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        if file.content_type.startswith("image/"):
            image = Image.open(path).convert("RGB")
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            uploaded = llm.upload_file(
                (
                    f"{uuid.uuid4()}.jpg",
                    buf,
                )
            )
            return {"path": path, "file_id": uploaded.id_}
    except Exception as e:
        raise e
    finally:
        file.file.close()

    return {"path": path}


@app.get("/files/{filename}")
def download_file(filename: str):
    # Нормализуем путь и защищаемся от path traversal
    file_path = os.path.normpath(os.path.join(FILES_DIR, filename))
    if not file_path.startswith(FILES_DIR) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Определяем MIME-тип по расширению
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    # Выбираем режим отдачи: inline для image/* и application/pdf, иначе attachment
    if mime_type.startswith("image/") or mime_type == "application/pdf":
        disposition = "inline"
    else:
        disposition = "attachment"

    return FileResponse(
        path=file_path,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'{disposition}; filename="{os.path.basename(file_path)}"'
        },
    )
