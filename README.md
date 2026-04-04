# remote-devcontainer-util

Personal scripts for working with devcontainers on a remote development environment, like my Ubuntu server running on Digital Ocean. The primary goal here is to make it easier to code on my iPad :-) 

## Dependencies

- **Python 3** — all scripts are Python 3 and use only the standard library (no `pip install` required)
- **Docker** — with the `docker compose` plugin (not the legacy `docker-compose` binary)

## Setup

**1. Clone this repo**

Personally I like for it to live right in my home directory.

```sh
git clone git@github.com:tylerpaige/remote-devcontainer-util.git
```

**2. (Optional) Make the command available as `devcontainer`**

Add the scripts to your `PATH` by appending the following to your `~/.bashrc` or `~/.zshrc` or what have you. If you cloned the repo into your home directory, that would look like this:

```sh
export PATH="$HOME/devcontainer:$PATH"
```

Then reload your shell or open a new window.

## Commands

| Command | Description |
|---|---|
| `devcontainer start <project>` | Build and start a devcontainer |
| `devcontainer exec <project>` | Open a shell in the running container |
| `devcontainer stop <project>` | Stop the container (preserves it for restart) |
| `devcontainer down <project> [--rmi]` | Remove the container; `--rmi` also removes the image |

## Typical workflow

```sh
devcontainer start ~/code/my-project   # first time, or after a down
devcontainer exec  ~/code/my-project   # get a shell
devcontainer stop  ~/code/my-project   # done for the day
devcontainer start ~/code/my-project   # pick up tomorrow (fast, no rebuild)
```

## Supported devcontainer configurations

Each project needs a `.devcontainer/` directory with at least one of:

- `devcontainer.json` with an `"image"` key — runs that image directly
- `devcontainer.json` with a `"build"` key (or a bare `Dockerfile`) — builds the image first
- `devcontainer.json` with a `"dockerComposeFile"` key — delegates to docker-compose

The container name is taken from the `"name"` field in `devcontainer.json`, falling back to
the project directory name. It is sanitized to a docker-safe slug (e.g. `"My Project"` →
`"my-project"`).

## Rebuilding after Dockerfile or dependency changes

`devcontainer-start` is intentionally lazy — it reuses an existing container or image rather
than rebuilding on every invocation. To force a rebuild, tear down first:

```sh
devcontainer down --rmi ~/code/my-project
devcontainer start ~/code/my-project
```

`--rmi` removes the built image so the next start rebuilds from scratch. Omit it to reuse
the image but recreate the container (rarely needed).

For docker-compose projects, to bust the layer cache too:

```sh
devcontainer down --rmi ~/code/my-project
cd ~/code/my-project/.devcontainer
docker compose -p my-project build --no-cache
devcontainer start ~/code/my-project
```
