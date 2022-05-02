import json
import logging
from os import environ
from typing import Optional

import requests

from app.evil_overlord import random_evil_overlord
from app.jeff_dean import random_jeff_dean
from app.skippys_list import random_skippy
from app.slack_event import APP_MENTION, MESSAGE, SlackEvent

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

    body_event = body.get("event")
    logger.info("body_event=%s", body_event)
    slack_event = make_slack_event(body_event)

    if slack_event.bot_id is not None:
        # the bot posted a message to its messages tab - don't talk to yourself
        return {"statusCode": 200}

    status_code = {"statusCode": 404}

    if slack_event.type in [APP_MENTION, MESSAGE]:
        if "help" in slack_event.text or "tell me more" in slack_event.text:
            status_code = {"statusCode": skill_help(slack_event)}
        if "chuck norris" in slack_event.text:
            status_code = {"statusCode": skill_chuck_norris(slack_event)}
        if "dad joke" in slack_event.text or "tell me a joke" in slack_event.text:
            status_code = {"statusCode": skill_tell_me_a_joke(slack_event)}
        if "evil overlord" in slack_event.text:
            status_code = {"statusCode": skill_evil_overlord(slack_event)}
        if "jeff dean" in slack_event.text:
            status_code = {"statusCode": skill_jeff_dean(slack_event)}
        if "seinfeld" in slack_event.text:
            status_code = {"statusCode": skill_seinfeld(slack_event)}
        if "skippy" in slack_event.text:
            status_code = {"statusCode": skill_skippy(slack_event)}
        if "wow" in slack_event.text or "owen" in slack_event.text:
            status_code = {"statusCode": skill_wow(slack_event)}

    return status_code


def make_slack_event(body_event: dict) -> SlackEvent:
    return SlackEvent(
        body_event.get("type"),
        body_event.get("channel"),
        body_event.get("text").lower(),
        body_event.get("bot_id"),
        body_event.get("thread_ts")
    )


def slack_post_message(data: dict, thread_ts: Optional[int]) -> int:
    if thread_ts is not None:
        data["thread_ts"] = thread_ts
    r = requests.post(f"{SLACK_BASE_URL}/chat.postMessage", headers=AUTHORIZATION, data=data)
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
    return r.status_code


def skill_help(slack_event: SlackEvent) -> int:
    help_message = "".join([
        "Hi, I'm Huggsy, your penguin pal! ",
        "If you summon me by name, I know how to do a few tricks:\n\n",
        " - `help | tell me more` - Display this message.\n",
        " - `chuck norris` - One Chuck Norris fact.\n",
        " - `dad joke | tell me a joke` - My best attempt at Dad joke humor.\n",
        " - `evil overlord` - One of the top 100 things to do, if you become an Evil Overlord.\n",
        " - `jeff dean` - One Jeff Dean fact.\n",
        " - `seinfeld` - One Seinfeld quote.\n",
        " - `skippy` - One of the 213 things Skippy is no longer allowed to do in the US Army.\n",
        " - `wow | owen` - What does the Owen say?\n",
    ])
    data = {
        "channel": slack_event.channel,
        "text": help_message
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_chuck_norris(slack_event: SlackEvent) -> int:
    """Chuck Norris facts."""
    r = requests.get("https://api.chucknorris.io/jokes/random")
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code
    data = {
        "channel": slack_event.channel,
        "text": r.json()["value"]
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_evil_overlord(slack_event: SlackEvent) -> int:
    """One of the Top 100 Things I'd Do, If I Ever Became An Evil Overlord."""
    data = {
        "channel": slack_event.channel,
        "text": random_evil_overlord()
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_jeff_dean(slack_event: SlackEvent) -> int:
    """Jeff Dean facts."""
    data = {
        "channel": slack_event.channel,
        "text": random_jeff_dean()
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_seinfeld(slack_event: SlackEvent) -> int:
    """Seinfeld quotes."""
    r = requests.get("https://seinfeld-quotes.herokuapp.com/random")
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code

    seinfeld = r.json()
    quote = seinfeld["quote"]
    character = seinfeld["author"]
    season = seinfeld["season"]
    episode = seinfeld["episode"]

    data = {
        "channel": slack_event.channel,
        "text": f"\"{quote}\" --{character}, S{season}E{episode}"
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_skippy(slack_event: SlackEvent) -> int:
    """One of 213 Things Skippy is No Longer Allowed to Do in the US Army."""
    data = {
        "channel": slack_event.channel,
        "text": random_skippy()
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_tell_me_a_joke(slack_event: SlackEvent) -> int:
    """The bot might be funny. All Dad jokes, all the time."""
    r = requests.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"})
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code
    data = {
        "channel": slack_event.channel,
        "text": r.json()["joke"]
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_wow(slack_event: SlackEvent) -> int:
    """Owen says Wow!"""
    r = requests.get("https://owen-wilson-wow-api.herokuapp.com/wows/random")
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code

    random_wow = r.json()[0]
    movie = random_wow["movie"]
    year = random_wow["year"]
    character = random_wow["character"]
    full_line = random_wow["full_line"]
    current_wow = random_wow["current_wow_in_movie"]
    total_wows = random_wow["total_wows_in_movie"]
    audio = random_wow["audio"]

    # pylint: disable=line-too-long
    data = {
        "channel": slack_event.channel,
        "text": f"\"{full_line}\" --{character}, {movie}, {year} (wow {current_wow}/{total_wows})\n\n{audio}"
    }
    return slack_post_message(data, slack_event.thread_ts)
