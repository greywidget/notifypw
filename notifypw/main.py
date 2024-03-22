import itertools
import logging
from datetime import date, timedelta
from pathlib import Path
from time import sleep

import keyring
import requests
import typer
from decouple import config
from keyring.errors import NoKeyringError
from schedule.intervals import (
    DAILY,
    EVERY_FIFTEEN_MINUTES,
    NINETY_SIX,
)
from scrapers.scrape import scrape_amazon_ebook, scrape_scorp
from typing_extensions import Annotated

DEFAULT_TAG = "snake"
FIFTEEN_MINUTES = 15 * 60
HEARTBEAT = "white_check_mark"
LOG_FILE = Path(__file__).resolve().parent.parent / "notify.log"

FMT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    filename=LOG_FILE.absolute(),
    level=logging.INFO,
    format=FMT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
segments = itertools.cycle(NINETY_SIX)

app = typer.Typer(add_completion=False, rich_markup_mode="markdown")
scrapers = [(scrape_scorp, "hocho"), (scrape_amazon_ebook, "book")]

try:
    topic = keyring.get_password("ntfy", "topic")
except NoKeyringError:
    topic = config("TOPIC")

url = f"https://ntfy.sh/{topic}"


@app.command()
def publish(
    message: Annotated[str, typer.Argument()],
    priority: Annotated[int, typer.Option(min=1, max=5)] = 5,
    tag: Annotated[str, typer.Option()] = DEFAULT_TAG,
):
    """
    **Publish** a manually entered message
    """

    requests.post(
        url,
        data=message.encode(encoding="utf-8"),
        headers={
            "Priority": str(priority),
            "Tags": tag,
        },
    )


@app.command()
def run():
    """
    **Loop** through event checks
    """
    log = logging.getLogger(__name__)

    last_heartbeat = date.today() - timedelta(days=1)
    while True:
        segment = next(segments)

        for scraper, tag in scrapers:
            if (
                (scraper.__name__ == "scrape_scorp")
                and (segment in EVERY_FIFTEEN_MINUTES)
                or (scraper.__name__ == "scrape_amazon_ebook")
                and (segment in DAILY)
            ):
                if message := scraper():
                    publish(message, tag=tag)

                log.info(f" {segment} | {scraper.__name__} | {tag}")

        if (today := date.today()) > last_heartbeat:
            publish(f"{today}", priority=1, tag=HEARTBEAT)
            last_heartbeat = today

        sleep(FIFTEEN_MINUTES)


if __name__ == "__main__":
    app()