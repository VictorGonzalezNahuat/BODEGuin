import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from core.config import DB_TARGET

# from app.routes import usuarios, tarifas, turnos

app = FastAPI(
    title="Sistema de Inventarios",
    description="API para gestión de inventarios",
    version="0.1.0",
)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name, str(default)).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _env_list(name: str, default_csv: str) -> list[str]:
    raw = os.getenv(name, default_csv)
    return [item.strip() for item in raw.split(",") if item.strip()]


cors_allow_origins = _env_list("CORS_ALLOW_ORIGINS", "http://localhost:4200")
cors_allow_credentials = _env_bool("CORS_ALLOW_CREDENTIALS", False)




# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "API de BODEGuin funcionando correctamente"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "Estoy vivo!🐧 *Sonidos de pinguino*"}

@app.get("/db-test")
def db_test():
    with engine.connect():
        pass
    return {"db": "Conectado :)", "target": DB_TARGET}
