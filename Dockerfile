# -------------------------
# Étape 1 : build de l’application
# -------------------------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système puis Poetry
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      wget \
 && wget https://install.python-poetry.org -O /tmp/install-poetry.py \
 && python3 /tmp/install-poetry.py --preview \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
 && apt-get purge -y --auto-remove wget

WORKDIR /usr/src/app

# Copier seulement les fichiers de dépendances pour profiter du cache Docker
COPY pyproject.toml poetry.lock* /usr/src/app/

# Installer les dépendances (sans installer le projet lui-même en editable)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# -------------------------
# Étape 2 : image finale
# -------------------------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Créer un utilisateur non-root
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser

WORKDIR /usr/src/app

# Copier l’environnement et les binaire Poetry
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code de l’application
COPY . /usr/src/app

# Passer en user non-root
RUN chown -R appuser:appgroup /usr/src/app
USER appuser

EXPOSE 8000

# Par défaut on démarre l’API (override possible pour Celery dans docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
