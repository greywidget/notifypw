# NotifyPW
Checks various internet sites and notify me via [ntfy](https://ntfy.sh) of anything of interest.

# On PlayWright
When I first encountered a message from Amazon: *Looks like you are a program...*
I foolishly assumed I needed to use PlayWright rather than Requests to access
the site.

I did get it all working, but installing PlayWright (including
running `playwright install --with-deps`) meant that the Docker Image was 2 GB.
Installing just the Chromium Browser (`playwright install --with-deps chromium`)
got the Image down to 1.2 GB.  

I rearranged the `Dockerfile` so that I can use a *cache-busting* `ARG` to control when I want to rebuild from the `git clone` down. If you change the repo you must manually change to `CACHEBUST` value in the `docker-compose.yml` file (don't use a value you've used before).  **Note** Although `docker-compose.yml` is in the repo - you need to update it on the Synology Server in order to get the repo to re-clone so this step needs to be done manually. Use the Synology File Edit application to bump the value.

Note that you must run `docker-compose up -d --build` (i.e. use the `--build`) flag if you want `docker` to check if any image layers need rebuilding.

# Running locally
From `..python_projects\notifypw\notifypw` you can run `python main.py run`

**Note that you will require the scrapers.db file from the Synology Server. Then `git restore` back to the empty one,**
