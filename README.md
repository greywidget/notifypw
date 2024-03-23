# NotifyPW
Checks various internet sites and notify me via [ntfy](https://ntfy.sh) of anything of interest.

# Careful with those line endings
Although I include `Dockerfile`, `pyproject.toml` and `startup.sh` in the repo,
in reality they will need to be created/copied into the directory from which 
you are going to run `docker-compose`.  
I had an issue with `startup.sh` because my `git` on `windows` is set to convert
line endings to `CRLF` and `sh` doesn't like that. I don't really want to change
my `git config` right now, so my solution is to use Synology Text Editor to mod
the file once I've copied/created it on my server.

# On PlayWright
When I first encountered a message from Amazon: *Looks like you are a program...*
I foolishly assumed I needed to use PlayWright rather than Requests to access
the site.

I did get it all working, but installing PlayWright (including
running `playwright install --with-deps`) meant that the Docker Image was 2GB.

Additionally, I'd foolishly created this as a package (see hatch-notify),
which on reflection was not a great idea and gave me issues using 
`python-decouple` that I couldn't resolve, and I ended up adding the TOPIC
directly as an environmental variable.

Here is what the config looked like at that time:
### DockerFile
```
FROM ubuntu:22.04

ENV VIRTUAL_ENV=/opt/venv
ENV TOPIC=blah-blah-blah

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get upgrade -y

RUN apt-get install -y python3.10-venv

# Verify Python installation
RUN python3 --version

WORKDIR /app

COPY ./.env .
COPY ./hatch_notify-0.0.1-py3-none-any.whl .

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --no-cache-dir hatch_notify-0.0.1-py3-none-any.whl

RUN playwright install --with-deps

# Define the command to run your Python script (replace with your script name)
CMD ["notify", "run"]
```

### docker-compose.yml
```
services:
  python:
    build:
      context: .
    ports:
      - "8000:8000"
```
On reflection, that `ports` is odd since I'd have thought it should be 80 if 
anything. Also on the latest version I didn't expose any ports so I'm not sure 
how `requests` can reach outside the container.
