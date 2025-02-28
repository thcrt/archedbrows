ARG NODE_VERSION="23.8.0"
ARG ALPINE_VERSION="3.21"

# Current project version, determined by `hatch-vcs`
ARG PROJECT_VERSION="0.0.0"
# Port to run on
ARG PROJECT_PORT="8000"
# User to run as
ARG PROJECT_USER="1000"

# Base stage with variables defined, `pnpm-lock.yaml` copied and `pnpm` installed ##################
FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV NODE_ENV=production
WORKDIR /app

RUN ["corepack", "enable", "pnpm"]
COPY ./pnpm-lock.yaml ./

# Dependencies needed for build stage (dev dependencies included) ##################################
FROM base AS build-deps
RUN ["pnpm", "fetch"]
COPY ./package.json ./
RUN ["pnpm", "install", "--offline"]

# Build stage ######################################################################################
FROM base AS build
COPY --from=build-deps /app/node_modules ./node_modules
COPY ./ ./
RUN ["pnpm", "run", "build"]

# Dependencies needed to run built project in prod (dev dependencies excluded) #####################
FROM base AS prod-deps
RUN ["pnpm", "fetch", "--prod"]
COPY ./package.json ./
RUN ["pnpm", "install", "--offline", "--prod"]

# Prod run stage ###################################################################################
FROM base AS prod
COPY --from=build /app/build ./build
COPY --from=prod-deps /app/node_modules ./node_modules
COPY ./package.json ./

ARG PROJECT_USER
ARG PROJECT_VERSION
ARG PROJECT_PORT

USER ${PROJECT_USER}
ENV PORT=${PROJECT_PORT}
CMD ["pnpm", "start"]

EXPOSE ${PROJECT_PORT}
LABEL org.opencontainers.image.authors="Theo Court (thcrt) <oss@theocourt.com>"
LABEL org.opencontainers.image.source="https://github.com/thcrt/archedbrows/"
LABEL org.opencontainers.image.version=${PROJECT_VERSION}
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"
LABEL org.opencontainers.image.title="archedbrows (web)"
LABEL org.opencontainers.image.description="save text and media. browse through your archive."
