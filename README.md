<div align="center">
  
# archedbrows

### save text and media. browse through your archive.

![UV Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fuv%2Frefs%2Fheads%2Fmain%2Fassets%2Fbadge%2Fv0.json&style=for-the-badge)
![Python Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fthcrt%2Farchedbrows%2Frefs%2Fheads%2Fmain%2F.python-version&query=%24&style=for-the-badge&label=Python)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/thcrt/archedbrows/build.yml?branch=main&style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Farchedbrows%2Fpkgs%2Fcontainer%2Farchedbrows)
![GitHub License](https://img.shields.io/github/license/thcrt/archedbrows?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Farchedbrows%2Fblob%2Fmain%2FLICENSE)
![GitHub Release](https://img.shields.io/github/v/release/thcrt/archedbrows?style=for-the-badge)
![Free Palestine Badge](https://img.shields.io/badge/Free%20-%20Palestine%20-%20red?style=for-the-badge)

</div>

## Installation

### With Docker

Images are published to GHCR with every release. Pull the latest tagged release with `ghcr.io/thcrt/archedbrows:latest`. or a bleeding-edge build from the `main` branch with `ghcr.io/thcrt/archedbrows:main`.

A SQLite database is initialised as part of the build process, located in the container at `/app/src/instance/project.db`. To make data persistent, you should mount `/app/src/instance` to a bind mount or Docker volume. 

The image runs on port `8080` by default, which can be mapped to whichever host port you like. Even better, you can run Caddy, Traefik or Nginx on the same Docker network as a reverse proxy, and hence avoid exposing anything directly to the internet. 

An example command to serve on port `80` and persist data in the Docker volume `abdata` might look like this:

```shell
docker run -p 80:8080 -v abdata:/app/src/instance ghcr.io/thcrt/archedbrows:latest
```

If you later upgrade the container image to a newer version, you must run migrations. Assuming the same Docker volume name, we can do that like so:

```shell
docker run -v abdata:/app/src/instance ghcr.io/thcrt/archedbrows:latest flask --app archedbrows db upgrade
```

### From source

You'll need [`uv`](https://docs.astral.sh/uv/), used as a package and project manager.

This project also uses [`task`](https://taskfile.dev/) as a task runner to save repeated typing on the command-line. You don't technically need to use it, and you can read `taskfile.yml` to see which commands to run manually, but this guide assumes you have it installed.

To begin, clone the repository, install dependencies and initialise a database:

```shell
git clone git@github.com:thcrt/archedbrows.git
cd archedbrows
uv sync
task db -- upgrade
```

Now you're ready to bring up a development environment:

```shell
task dev
```

Note that the development server is for debugging purposes, and may not be used in production. To run in production, I strongly recommend Docker, but you can also do it yourself with:

```shell
uv run waitress-serve --call archedbrows:create_app
```

If you later pull a newer version of the code, you must run migrations. Do that the same way you initialised the database:

```shell
task db -- upgrade
```

If you modify the code, please make sure to run linting, formatting and type-checking, and correct any issues that may arise:

```shell
task check
```

## Licensing

This project is available under the AGPLv3, available at [`./LICENSE`](./LICENSE).

It includes the vector graphic "eyebrow" by Harianto, from <a href="https://thenounproject.com/browse/icons/term/eyebrow/">the Noun Project</a> (CC BY 3.0).
