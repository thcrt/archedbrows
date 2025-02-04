FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

RUN apt-get update
RUN apt-get -y install git

# Enable optimisations for all `uv` commands
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Add binaries from venv to path
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies without installing project
# Since dependencies change less often than project code, this saves rebuild time
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project
    
# Install project itself
ADD --keep-git-dir . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.git,target=.git \
    uv sync --frozen --no-dev

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Let's run this thing
CMD ["waitress-serve", "--call", "archedbrows:create_app"]