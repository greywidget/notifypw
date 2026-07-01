FROM python:3.14-slim

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

WORKDIR /app

# Clone the repository. Force rebuild via CACHEBUST setting if repo changes
ARG CACHEBUST
RUN git clone --branch main --single-branch --depth 1 https://github.com/greywidget/notifypw.git .

# Install the Python dependencies
RUN uv sync --extra dev

# Manually set up path to the venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Chromium with Playwright
RUN playwright install --with-deps chromium

COPY ./.env .

CMD ["python", "notifypw/main.py", "run"]
