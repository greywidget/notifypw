import keyring
import requests
import typer
from decouple import config
from keyring.errors import NoKeyringError
from typing_extensions import Annotated


def main(
    message: str,
    priority: Annotated[int, typer.Option(min=1, max=5)] = 3,
):
    """
    Examples of Publishing Parameters.
    Notice that Tags is a CSV string.
    Tags which match an emoji short code https://docs.ntfy.sh/emojis/ get
    converted to emojis and prepended to the Title or Message.
    Tags that don't match, will be listed below the notification.
    """

    try:
        topic = keyring.get_password("ntfy", "topic")
    except NoKeyringError:
        topic = config("TOPIC")

    url = f"https://ntfy.sh/{topic}"

    requests.post(
        url,
        data=message.encode(encoding="utf-8"),
        headers={
            "Title": "Greywidget Notifications",
            "Priority": str(priority),
            "Tags": "snake,octopus,Amazon,Price Change",
        },
    )


if __name__ == "__main__":
    typer.run(main)
