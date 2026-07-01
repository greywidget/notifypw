# NotifyPW
Checks various internet sites and notify me via [ntfy](https://ntfy.sh) of anything of interest.

## Upgrading with uv
- I updated the `.python-version` file by running `uv python pin 3.14`.
- I manually updated the `requires-python` constraint in `pyproject.toml`, I don't think anything auto updates that by design.
- I ran `uv lock --upgrade` to recompute the lockfile. Note that this will respect constraints in `pyproject.toml` so one way to manage that is to specify (for example) `package>=1.2,<2` so that you can upgrade but stay below the next major version.
- I ran `uv sync` to update the `venv`.
- This could have been done in one step with `uv sync --upgrade`
- Note that since `playwright` is an optional dev dependency, I needed to sync with `uv sync --all-extras`
- Additionally I needed to run the `playwright` local install: `playwright install --with-deps chromium`. This installed:
    - Chrome for Testing
    - FFmpeg
    - Chrome Headless Shell
    - Winldd

# On PlayWright
When I first encountered a message from Amazon: *Looks like you are a program...*
I foolishly assumed I needed to use PlayWright rather than Requests to access
the site.

I did get it all working, but installing PlayWright (including
running `playwright install --with-deps`) meant that the Docker Image was 2 GB.
Installing just the Chromium Browser (`playwright install --with-deps chromium`)
got the Image down to 1.2 GB.  

**I think my original comment below is not quite correct**
- I agree that everything above the `ARG CACHEBUST` should be preserved from the cache.
- To rebuild from below that, (`git clone ... down`) you can pass a unique `CACHEBUST` value into the build:
- `docker compose build --build-arg CACHEBUST=$(date +%s)`
- `docker compose up -d`

*I think this isn't quite right, see above*
I rearranged the `Dockerfile` so that I can use a *cache-busting* `ARG` to control when I want to rebuild from the `git clone` down. If you change the repo you must manually change to `CACHEBUST` value in the `docker-compose.yml` file (don't use a value you've used before).  **Note** Although `docker-compose.yml` is in the repo - you need to update it on the Synology Server in order to get the repo to re-clone so this step needs to be done manually. Use the Synology File Edit application to bump the value.

Note that you must run `docker-compose up -d --build` (i.e. use the `--build`) flag if you want `docker` to check if any image layers need rebuilding.
*End of dodgy comment*

# Running locally
From `..python_projects\notifypw\notifypw` you can run `python main.py run`

**Note that you will require the scrapers.db file from the Synology Server. Then `git restore` back to the empty one,**
