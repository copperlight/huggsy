import json
import logging
from os import environ
from typing import Optional

import requests

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
        return {"statusCode": 204}

    status_code = {"statusCode": 204}

    if slack_event.type in [APP_MENTION, MESSAGE]:
        if "help" in slack_event.text or "tell me more" in slack_event.text:
            status_code = {"statusCode": skill_help(slack_event)}
        if "dad joke" in slack_event.text or "tell me a joke" in slack_event.text:
            status_code = {"statusCode": skill_tell_me_a_joke(slack_event)}
        if "seinfeld" in slack_event.text:
            status_code = {"statusCode": skill_seinfeld(slack_event)}
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


def slack_file_upload(data: dict, thread_ts: Optional[int]) -> int:
    if thread_ts is not None:
        data["thread_ts"] = thread_ts
    r = requests.post(f"{SLACK_BASE_URL}/files.upload", headers=AUTHORIZATION, data=data)
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
    return r.status_code


def skill_help(slack_event: SlackEvent) -> int:
    help_message = "".join([
        "Hi, I'm Huggsy, your penguin pal! ",
        "If you summon me by name, I know how to do a few tricks:\n\n",
        " - `help | tell me more` - Display this message.\n",
        " - `cat` - One cat gif.\n",
        " - `dad joke | tell me a joke` - My best attempt at Dad joke humor.\n",
        " - `seinfeld` - One Seinfeld quote.\n",
        " - `wow | owen` - What does the Owen say?\n",
    ])
    data = {
        "channel": slack_event.channel,
        "text": help_message
    }
    return slack_post_message(data, slack_event.thread_ts)


def skill_cat(slack_event: SlackEvent) -> int:
    """Cat gifs."""
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code

    r = requests.get(r.json()[0]["url"])
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return r.status_code

    data = {
        "channel": slack_event.channel,
        "file": r.content
    }
    return slack_file_upload(data, slack_event.thread_ts)


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
