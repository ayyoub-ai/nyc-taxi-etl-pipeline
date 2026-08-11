# Étape 1 : On utilise une image officielle légère de Python
FROM python:3.12-slim AS builder

# On installe uv dans l'image de construction
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# On copie les fichiers de dépendances d'abord (pour le cache Docker)
COPY pyproject.toml uv.lock ./

# On installe les dépendances dans un environnement virtuel
RUN uv sync --frozen --no-dev

# Étape 2 : L'image finale (plus petite)
FROM python:3.12-slim

WORKDIR /app

# On copie l'environnement virtuel depuis l'étape builder
COPY --from=builder /app/.venv /app/.venv

# On ajoute le venv au PATH pour pouvoir utiliser les commandes
ENV PATH="/app/.venv/bin:$PATH"

# On copie notre script d'ingestion
COPY ingest_data.py .

# Commande par défaut quand le conteneur démarre
ENTRYPOINT ["python", "ingest_data.py"]