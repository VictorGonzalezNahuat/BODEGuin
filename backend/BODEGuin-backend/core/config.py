import json
import os
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.json"


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value

_load_dotenv(BASE_DIR / ".env")

def _get_required_env(key: str) -> str:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise ValueError(f"{key} no esta configurada en variables de entorno")
    return value.strip()


db_target = os.getenv("DB_TARGET", "local").strip().lower()
if db_target not in {"local", "cloud"}:
    raise ValueError("DB_TARGET debe ser 'local' o 'cloud'")

DB_TARGET = db_target

prefix = "LOCAL_DB" if db_target == "local" else "CLOUD_DB"

db_user = _get_required_env(f"{prefix}_USER")
db_password = _get_required_env(f"{prefix}_PASSWORD")
db_host = _get_required_env(f"{prefix}_HOST")
db_name = _get_required_env(f"{prefix}_NAME")
db_port = os.getenv(f"{prefix}_PORT", "5432").strip()
db_sslmode = os.getenv(f"{prefix}_SSLMODE", "").strip()

encoded_user = quote_plus(db_user)
encoded_password = quote_plus(db_password)

DATABASE_URL = (
    f"postgresql+psycopg2://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
)

if db_sslmode:
    DATABASE_URL = f"{DATABASE_URL}?sslmode={db_sslmode}"

