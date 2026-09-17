"""
Monokuma bot — one-shot script for GitHub Actions.
Sends ONE announcement (morning or evening) and exits.
Trigger which one via the TIME_OF_DAY environment variable ("morning" or "evening").
"""

import os
import sys

import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TIME_OF_DAY = os.environ.get("TIME_OF_DAY", "morning")

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "monokuma.jpg")

MORNING_CAPTION = (
    "Good morning, everyone! It is now 7 a.m. and nighttime is officially over! "
    "Time to rise and shine! Get ready to greet another beee-yutiful day!"
)

EVENING_CAPTION = (
    "Mm, ahem, this is a school announcement. It is now 10 p.m. As such, it is "
    "officially nighttime. Soon the doors to the dining hall will be locked, and "
    "entry at that point is strictly prohibited. Okay then...sweet dreams, "
    "everyone! Good night, sleep tight, don't let the bed bugs bite."
)


def main():
    if TIME_OF_DAY == "morning":
        caption = MORNING_CAPTION
    elif TIME_OF_DAY == "evening":
        caption = EVENING_CAPTION
    else:
        print(f"Unknown TIME_OF_DAY: {TIME_OF_DAY}")
        sys.exit(1)

    if not os.path.isfile(IMAGE_PATH):
        print(f"Image not found at {IMAGE_PATH}")
        sys.exit(1)

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(IMAGE_PATH, "rb") as photo:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": photo},
            timeout=30,
        )

    if response.ok:
        print(f"Sent {TIME_OF_DAY} announcement successfully.")
    else:
        print(f"Failed to send: {response.status_code} {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
