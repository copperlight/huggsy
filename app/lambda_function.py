import json
import logging
from os import environ

import requests

from .slack_event_type import APP_MENTION

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SLACK_BASE_URL = "https://slack.com/api"
AUTHORIZATION = {"Authorization": "Bearer " + environ["BOT_USER_OAUTH_TOKEN"]}


def skill_challenge_response(event):
    """Used during the initial setup of a Slack API integration."""
    event_body = event.get("body")
    slack_event = json.loads(event_body)
    challenge_answer = slack_event.get("challenge")

    return {
        "statusCode": 200,
        "body": challenge_answer
    }


def lambda_handler(event, context):
    logger.debug("event=%s", event)
    logger.debug("context=%s", context)

    user_agent = event.get("multiValueHeaders").get("User-Agent")[0]

    if not user_agent.startswith("Slackbot 1.0"):
        return {"statusCode": 403}

    slack_event = json.loads(event.get("body")).get("event")

    if slack_event.get("type") == APP_MENTION:
        if "tell me a joke" in slack_event.get("text").lower():
            r = requests.post(
                f"{SLACK_BASE_URL}/chat.postMessage",
                headers=AUTHORIZATION,
                data={
                    "channel": slack_event.get("channel"),
                    "text": "No, I'm a bot user. I don't understand jokes."
                }
            )
            if not r.ok:
                logger.error("request failed status_code=%s text=%s", r.status_code, r.text)

    return {"statusCode": 200}
