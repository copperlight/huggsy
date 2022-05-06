import io
import json
import logging
from os import environ

import requests

from app.dice import roll_dice
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

    if is_bot_response(slack_event):
        # the bot posted a message to its messages tab - don't talk to yourself
        return {"statusCode": 204}

    status_code = {"statusCode": 204}

    if slack_event.type in [APP_MENTION, MESSAGE]:
        if "help" in slack_event.text or "tell me more" in slack_event.text:
            status_code = {"statusCode": skill_help(slack_event)}
        if "cat" in slack_event.text:
            status_code = {"statusCode": skill_cat(slack_event)}
        if "dad joke" in slack_event.text or "tell me a joke" in slack_event.text:
            status_code = {"statusCode": skill_dad_joke(slack_event)}
        if "roll" in slack_event.text:
            status_code = {"statusCode": skill_roll_dice(slack_event)}
        if "wow" in slack_event.text or "owen" in slack_event.text:
            status_code = {"statusCode": skill_wow(slack_event)}

    return status_code


def make_slack_event(body_event: dict) -> SlackEvent:
    return SlackEvent(
        body_event.get("type"),
        body_event.get("channel"),
        body_event.get("text").lower(),
        body_event.get("bot_id"),
        body_event.get("display_as_bot"),
        body_event.get("thread_ts")
    )


def is_bot_response(slack_event: SlackEvent) -> bool:
    if slack_event.bot_id is not None or slack_event.display_as_bot is not None:
        return True
    return False


def log_http_error(r: requests.models.Response) -> bool:
    if not r.ok:
        logger.error("http request failed: status_code=%s text=%s", r.status_code, r.text)
        return True
    return False


def slack_post_message(slack_event: SlackEvent, text: str) -> int:
    data = {"channel": slack_event.channel, "text": text}
    if slack_event.thread_ts is not None:
        data["thread_ts"] = slack_event.thread_ts

    r = requests.post(f"{SLACK_BASE_URL}/chat.postMessage", headers=AUTHORIZATION, data=data)
    log_http_error(r)
    return r.status_code


def slack_file_upload(slack_event: SlackEvent, file: bytes, comment: str) -> int:
    data = {"channels": slack_event.channel, "initial_comment": comment}
    if slack_event.thread_ts is not None:
        data["thread_ts"] = slack_event.thread_ts
    files = {"file": io.BytesIO(file)}

    # pylint: disable=line-too-long
    r = requests.post(f"{SLACK_BASE_URL}/files.upload", headers=AUTHORIZATION, files=files, data=data)
    log_http_error(r)
    return r.status_code


def skill_help(slack_event: SlackEvent) -> int:
    help_message = "".join([
        "Hi, I'm Huggsy, your penguin pal! ",
        "If you summon me by name, I know how to do a few tricks:\n\n",
        " - `help | tell me more` - Display this message. I can be helpful.\n",
        " - `cat` - One cat image. Meow.\n",
        " - `dad joke | tell me a joke` - My best attempt at Dad joke humor.\n",
        " - `roll` - Roll two dice.\n",
        " - `wow | owen` - What does the Owen Wilson say?\n",
    ])

    return slack_post_message(slack_event, help_message)


def skill_cat(slack_event: SlackEvent) -> int:
    """Cat facts and images."""
    r = requests.get("https://catfact.ninja/fact")
    if log_http_error(r):
        return r.status_code
    fact = r.json()["fact"]

    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if log_http_error(r):
        return r.status_code
    image_url = r.json()[0]["url"]

    r = requests.get(image_url)
    if log_http_error(r):
        return r.status_code
    image = r.content

    return slack_file_upload(slack_event, image, fact)


def skill_dad_joke(slack_event: SlackEvent) -> int:
    """The bot might be funny. All Dad jokes, all the time."""
    r = requests.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"})
    if log_http_error(r):
        return r.status_code
    joke = r.json()["joke"]

    return slack_post_message(slack_event, joke)


def skill_roll_dice(slack_event: SlackEvent) -> int:
    """Can the bot gamble? Maybe not. Not quite tabletop ready."""
    return slack_post_message(slack_event, roll_dice())


def skill_wow(slack_event: SlackEvent) -> int:
    """Owen says Wow!"""
    r = requests.get("https://owen-wilson-wow-api.herokuapp.com/wows/random")
    if log_http_error(r):
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
    wow = f"\"{full_line}\" --{character}, {movie}, {year} (wow {current_wow}/{total_wows})\n\n{audio}"

    return slack_post_message(slack_event, wow)
