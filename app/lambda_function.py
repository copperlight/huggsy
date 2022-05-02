import json
import logging
from os import environ

import requests

from app.slack_event_type import APP_MENTION, MESSAGE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SLACK_BASE_URL = "https://slack.com/api"
AUTHORIZATION = {"Authorization": "Bearer " + environ.get("BOT_USER_OAUTH_TOKEN", "")}


def lambda_handler(event: dict, context: object) -> dict:
    logger.debug("event=%s", event)
    logger.debug("context=%s", context)

    user_agent = event.get("headers").get("User-Agent")

    if not user_agent.startswith("Slackbot 1.0"):
        return {"body": "forbidden", "statusCode": 403}

    body = json.loads(event.get("body"))

    if "challenge" in body:
        # used during the initial setup of a Slack API integration
        return {"body": body.get("challenge"), "statusCode": 200}

    slack_event = body.get("event")
    logger.info("slack_event=%s", slack_event)

    if slack_event.get("type") in [APP_MENTION, MESSAGE]:
        if "bot_id" in slack_event:
            # the bot posted a message to its messages tab - don't talk to yourself
            return {"statusCode": 200}
        if "tell me a joke" in slack_event.get("text").lower():
            # 'text': '<@...........> tell me a joke',
            return {"statusCode": skill_tell_me_a_joke(slack_event)}
        if "wow" in slack_event.get("text").lower():
            # 'text': '<@...........> wow',
            return {"statusCode": skill_wow(slack_event)}

    return {"statusCode": 404}


def slack_post_message(data: dict) -> int:
    r = requests.post(f"{SLACK_BASE_URL}/chat.postMessage", headers=AUTHORIZATION, data=data)
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
    return r.status_code


def skill_tell_me_a_joke(slack_event: dict) -> int:
    """The bot is not funny. Yet."""
    data = {
        "channel": slack_event.get("channel"),
        "text": "No, I'm a bot user. I don't understand jokes."
    }
    return slack_post_message(data)


def skill_wow(slack_event: dict) -> int:
    """Owen says Wow!"""
    r = requests.get("https://owen-wilson-wow-api.herokuapp.com/wows/random")
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code

    random_wow = r.json()[0]
    movie = random_wow['movie']
    year = random_wow['year']
    character = random_wow['character']
    full_line = random_wow['full_line']
    current_wow = random_wow['current_wow_in_movie']
    total_wows = random_wow['total_wows_in_movie']
    audio = random_wow['audio']

    # pylint: disable=line-too-long
    data = {
        "channel": slack_event.get("channel"),
        "text": f"\"{full_line}\" --{character}, {movie}, {year} (wow {current_wow}/{total_wows})\n\n{audio}"
    }
    return slack_post_message(data)
