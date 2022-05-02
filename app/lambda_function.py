import json
import logging
from os import environ

import requests

from app.slack_event_type import APP_MENTION, MESSAGE
from app.skippys_list import random_skippy

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

    if "bot_id" in slack_event:
        # the bot posted a message to its messages tab - don't talk to yourself
        return {"statusCode": 200}

    status_code = {"statusCode": 404}

    if slack_event.get("type") in [APP_MENTION, MESSAGE]:
        lowercase_text = slack_event.get("text").lower()
        if "help" in lowercase_text:
            status_code = {"statusCode": skill_help(slack_event)}
        if "skippy" in lowercase_text:
            status_code = {"statusCode": skill_skippy(slack_event)}
        if "tell me a joke" in lowercase_text:
            status_code = {"statusCode": skill_tell_me_a_joke(slack_event)}
        if "wow" in lowercase_text:
            status_code = {"statusCode": skill_wow(slack_event)}

    return status_code


def slack_post_message(data: dict) -> int:
    r = requests.post(f"{SLACK_BASE_URL}/chat.postMessage", headers=AUTHORIZATION, data=data)
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
    return r.status_code


def skill_help(slack_event: dict) -> int:
    help_message = "".join([
        "Hi, I'm Huggsy, your penguin pal! ",
        "If you summon me by name, I know how to do a few tricks:\n\n",
        " - 'help' - Display this message.\n",
        " - 'tell me a joke' - My best attempt at Dad joke humor.\n",
        " - 'wow' - What does the Owen say?\n",
        " - 'skippy' - One of the things Skippy is no longer allowed to do.",
    ])
    data = {
        "channel": slack_event.get("channel"),
        "text": help_message
    }
    return slack_post_message(data)


def skill_skippy(slack_event: dict) -> int:
    data = {
        "channel": slack_event.get("channel"),
        "text": random_skippy()
    }
    return slack_post_message(data)


def skill_tell_me_a_joke(slack_event: dict) -> int:
    """The bot might be funny. All Dad jokes, all the time."""
    r = requests.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"})
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code
    data = {
        "channel": slack_event.get("channel"),
        "text": r.json()["joke"]
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
