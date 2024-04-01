FROM ubuntu:22.04

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright
RUN pip install --no-cache-dir playwright

# Install Chromium with Playwright
RUN playwright install --with-deps chromium

WORKDIR /app

# Clone the repository. Force rebuild via CACHEBUST setting if repo changes
ARG CACHEBUST
RUN git clone --branch main --single-branch --depth 1 https://github.com/greywidget/notifypw.git .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./.env .

COPY ./startup.sh .

# Set up Docker logging
RUN ln -sf /dev/stdout /app/notify.log

CMD ["./startup.sh"]
