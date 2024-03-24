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
running `playwright install --with-deps`) meant that the Docker Image was 2 GB.
Installing just the Chromium Browser (`playwright install --with-deps chromium`)
got the Image down to 1.2 GB

Additionally, I'd foolishly created this as a package (see hatch-notify),
which on reflection was not a great idea and gave me issues using 
`python-decouple` that I couldn't resolve, and I ended up adding the TOPIC
directly as an environmental variable.
