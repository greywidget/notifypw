FROM ubuntu:22.04

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update \
    && apt-get upgrade -y

# Verify Python installation
RUN python3 --version

WORKDIR /usr/src/app

RUN git clone --branch main --single-branch --depth 1 https://github.com/greywidget/notifypw.git .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

COPY ./.env .

COPY ./startup.sh .

CMD ["./startup.sh"]
