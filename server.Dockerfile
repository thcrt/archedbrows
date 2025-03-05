ARG PYTHON_VERSION="3.13.2"
ARG DEBIAN_VERSION="slim-bullseye"
ARG UV_VERSION="0.6.0"

# Current project version, determined by `hatch-vcs`
ARG PROJECT_VERSION="0.0.0"
# Port to run on
ARG PROJECT_PORT="8001"
# User to run as
ARG PROJECT_USER="1000"

# We need to explicitly define this as a stage in order to copy from it, since `COPY --from` doesn't
# take variables defined in `ARG` 
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# Build stage with source code copied ##############################################################
FROM python:${PYTHON_VERSION}-${DEBIAN_VERSION} AS build
WORKDIR /app

# Workaround to pass the current project version (determined by `hatch-vcs`)
ARG PROJECT_VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${PROJECT_VERSION}

# Enable bytecode compilation
# https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# Use a cache mount for the `uv` cache
# `uv sync` must be run with arguments `--mount=type=cache,target=/opt/uv-cache`
# https://docs.docker.com/build/cache/optimize/#use-cache-mounts
# https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/opt/uv-cache/

# Get `uv` binary, `pyproject.toml` and lockfile
COPY --from=uv /uv /bin/uv
COPY ./uv.lock ./pyproject.toml ./

# Install dependencies (change rarely) without installing project (changes often) 
RUN --mount=type=cache,target=/opt/uv-cache \
    uv sync --frozen --no-dev --no-editable --no-install-project

# Add source code and install project
COPY ./ ./
RUN --mount=type=cache,target=/opt/uv-cache \
    uv sync --frozen --no-dev --no-editable

# Prod run stage without `uv` or source code #######################################################
FROM python:${PYTHON_VERSION}-${DEBIAN_VERSION} AS prod
WORKDIR /app

# `uv` has already built the package, so we don't need to copy the source code here
COPY --from=build /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# Run database migrations
RUN --mount=type=bind,source=./migrations,target=./migrations \
    ["flask", "--app", "archedbrows", "db", "upgrade"]

ARG PROJECT_PORT
ARG PROJECT_VERSION
ARG PROJECT_USER
    
# Run application
USER ${PROJECT_USER}
ENV PORT=${PROJECT_PORT}
CMD waitress-serve --port "$PORT" --call archedbrows:create_app

EXPOSE ${PROJECT_PORT}
LABEL org.opencontainers.image.authors="Theo Court (thcrt) <oss@theocourt.com>"
LABEL org.opencontainers.image.source="https://github.com/thcrt/archedbrows/"
LABEL org.opencontainers.image.version=${PROJECT_VERSION}
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"
LABEL org.opencontainers.image.title="archedbrows (server)"
LABEL org.opencontainers.image.description="save text and media. browse through your archive."
