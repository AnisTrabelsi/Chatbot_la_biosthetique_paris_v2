# alembic/env.py
import os
from pathlib import Path
from logging.config import fileConfig
from dotenv import load_dotenv

from alembic import context
from sqlalchemy import engine_from_config, pool

# ------- charge .env -------
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, encoding="utf-8")

# ------- URL DB -------
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # <- plus sûr

# Si vous préférez l'import :
# from app.db.session import DATABASE_URL as SQLALCHEMY_DATABASE_URL

config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# reste du fichier inchangé …
