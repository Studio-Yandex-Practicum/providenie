from typing import Dict
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> Dict[str, str]:
    """Возвращает приветственное сообщение в формате JSON."""
    return {"message": "Здравствуйте, API работает!"}
