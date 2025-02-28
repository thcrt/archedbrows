<div align="center">
  
# archedbrows

### save text and media. browse through your archive.

![UV Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fuv%2Frefs%2Fheads%2Fmain%2Fassets%2Fbadge%2Fv0.json&style=for-the-badge)
![Python Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fthcrt%2Farchedbrows%2Frefs%2Fheads%2Fmain%2F.python-version&query=%24&style=for-the-badge&label=Python)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/thcrt/archedbrows/build.yml?branch=main&style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Farchedbrows%2Fpkgs%2Fcontainer%2Farchedbrows)
![GitHub License](https://img.shields.io/github/license/thcrt/archedbrows?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Farchedbrows%2Fblob%2Fmain%2FLICENSE)
![GitHub Release](https://img.shields.io/github/v/release/thcrt/archedbrows?style=for-the-badge)
![Free Palestine Badge](https://img.shields.io/badge/Free%20-%20Palestine%20-%20red?style=for-the-badge)

![image](https://github.com/user-attachments/assets/83433a31-e690-450d-9e09-08d9df57d533)

</div>

## Installation

### With Docker

Two containers are needed in order to run archedbrows. The `archedbrows-server`
image provides an API, while the `archedbrows-web` image serves a web frontend.
The images published on GHCR have the `-server` and `-web` variants running on
ports `8001` and `8000` respectively.

The backend container stores data in a SQLite database located in the directory
`/app/.venv/var/archedbrows-instance`. To ensure data persists across container
runs, mount a Docker volume at this path.

An example `docker-compose.yml` file might look like this:

```yaml
# docker-compose.yml

services:
  server:
    restart: unless-stopped
    image: archedbrows-server:latest
    volumes:
      - archedbrows_data:/app/.venv/var/archedbrows-instance

  web:
    restart: unless-stopped
    image: archedbrows-web:latest

  reverse-proxy:
    image: caddy:latest
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data

volumes:
  archedbrows_data:
  caddy_data:
```

```Caddy
# Caddyfile
example.com {
	route /api/* {
		uri strip_prefix /api
		reverse_proxy server:8001
	}

	reverse_proxy web:8000
}
```

Of course, if you're running in production, you should replace the `latest` tags
with a pinned version. You may also wish to use a different reverse proxy,
and/or one running in a different Compose stack. The important thing is that
both `archedbrows-server` and `archedbrows-web` are available under the same
domain. Requests under the pattern `/api/*` must be passed to the backend, with
the `/api/` prefix removed, and all other requests to the frontend.

### From source

You'll need [`uv`](https://docs.astral.sh/uv/), used as a package and project
manager.

This project also uses [`task`](https://taskfile.dev/) as a task runner to save
repeated typing on the command-line. You don't technically need to use it, and
you can read `taskfile.yml` to see which commands to run manually, but this
guide assumes you have it installed.

To begin, clone the repository, install dependencies and initialise a database:

```shell
git clone git@github.com:thcrt/archedbrows.git
cd archedbrows
task run-migrations
```

Now you're ready to bring up a development environment:

```shell
task dev
```

Note that the development server is for debugging purposes, and may not be used
in production. To run in production, I strongly recommend Docker, but you can
also do it yourself with:

```shell
task build
task serve
```

This will serve the backend at port `8001` and the frontend at port `8000`. You
can then configure a reverse proxy of your choice to serve external requests.

If you later pull a newer version of the code, you must run migrations. Do that
the same way you initialised the database:

```shell
task run-migrations
```

If you modify the code, please make sure to run linting, formatting and
type-checking, and correct any issues that may arise:

```shell
task check
```

## Upgrading

If you later upgrade the container image to a newer version, you may need to run
migrations.

This can be done with the command:

```shell
uv run flask --app archedbrows db upgrade
```

Or, if you have `task` installed:

```shell
task run-migrations
```

If you're running in Docker, make sure to run it inside the `archedbrows-server`
container. With the container name `server`, this means:

```shell
docker compose exec server flask --app archedbrows db upgrade
```

## Licensing

This project is available under the AGPLv3, available at
[`./LICENSE`](./LICENSE).

It includes the vector graphic "eyebrow" by Harianto, from
<a href="https://thenounproject.com/browse/icons/term/eyebrow/">the Noun
Project</a> (CC BY 3.0).
