# ── Stage 1: build frontend assets ───────────────────────────────────────────
FROM node:24 AS frontend

WORKDIR /build

# Copy manifests first for layer-cache efficiency
COPY package.json package-lock.json ./
RUN npm install

# vite.config.js must be present before `npm run build`
COPY vite.config.js ./
COPY ./static_src/ ./static_src/
COPY ./scripts/ ./scripts/

RUN npm run build

# ── Stage 2: Python / Django runtime ─────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

ARG DBMODULE

RUN useradd -m wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DBMODULE=${DBMODULE} \
    DJANGO_SETTINGS_MODULE=app.settings.base

# Install runtime libraries required by Wagtail/Django and Pillow
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    libwebp7 \
    libmariadb3 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock ./

ENV UV_NO_DEV=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Install build tools, compile wheels, then purge build deps to slim the image
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    pkg-config \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    default-libmysqlclient-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install

RUN --mount=type=cache,target=/root/.cache/uv \
    uv export --locked --no-dev --no-hashes --output-file /tmp/requirements.txt && \
    UV_SYSTEM_PYTHON=1 uv pip install --system -r /tmp/requirements.txt

RUN if [ -n "$DBMODULE" ]; then echo "Installing DB module: $DBMODULE" && $DBMODULE; else echo "No DBMODULE specified"; fi

RUN apt-get purge --yes --quiet \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    default-libmysqlclient-dev \
 && apt-get autoremove --yes --quiet --purge \
 && rm -rf /var/lib/apt/lists/*

# Bring in Vite-built assets from the frontend stage
COPY --from=frontend /build/static_compiled ./static_compiled

RUN chown -R wagtail:wagtail /app

# Copy project source (static_compiled/ excluded via .dockerignore — already copied above)
COPY --chown=wagtail:wagtail . .

RUN python manage.py collectstatic --noinput --clear

USER wagtail

# CMD set -xe; python manage.py migrate --noinput; gunicorn app.wsgi:application
