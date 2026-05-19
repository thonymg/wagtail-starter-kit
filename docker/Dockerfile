# syntax=docker/dockerfile:1.7

# ── Stage 1: frontend assets (Vite + Tailwind + image optimisation) ───────────
FROM node:24-alpine AS frontend

WORKDIR /build

# Layer-cache: install deps before copying source
COPY package.json package-lock.json vite.config.js ./
RUN npm ci

COPY static_src/ ./static_src/
COPY scripts/ ./scripts/

RUN npm run build


# ── Stage 2: Python dependency builder ───────────────────────────────────────
# Compiles wheels for native extensions (Pillow, psycopg2, mysqlclient…)
# Nothing from this stage goes into the final image except /app/.venv
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS python-builder

# Build-time libs for native extensions
RUN apk add --no-cache \
    build-base \
    pkgconf \
    postgresql-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    libwebp-dev \
    mariadb-dev

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Optional extras: "postgres" | "mysql" — passed from compose build args
ARG EXTRAS=""

# Install deps into .venv without installing the project itself.
# Bind-mounting the lock files avoids copying them into the layer.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-install-project \
    ${EXTRAS:+--extra $EXTRAS}


# ── Stage 3: runtime ──────────────────────────────────────────────────────────
FROM python:3.13-alpine AS runtime

# Runtime-only shared libraries — no compilers, no headers
RUN apk add --no-cache \
    libpq \
    libjpeg-turbo \
    zlib \
    libwebp \
    mariadb-connector-c

RUN adduser -D wagtail

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Activate the uv-managed venv without sourcing it
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=app.settings.base

WORKDIR /app

# Copy the compiled venv from builder (Python + all deps, no build tools)
COPY --from=python-builder /app/.venv /app/.venv

# Copy the Vite-built frontend assets from the frontend stage
COPY --from=frontend /build/static_compiled ./static_compiled

# Project source (static_compiled/ excluded by .dockerignore)
COPY . .

# collectstatic requires a valid SECRET_KEY — supply a build-time placeholder
# (never used at runtime; runtime value comes from .env / environment)
ARG DJANGO_SECRET_KEY="build-time-placeholder-not-used-at-runtime"
RUN DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    python manage.py collectstatic --noinput --clear \
    && chown -R wagtail:wagtail /app

USER wagtail

EXPOSE 8000

# Daphne: production-grade ASGI server
# Override CMD or set DAPHNE_ARGS env var to customise (e.g. --proxy-headers)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "app.asgi:application"]
