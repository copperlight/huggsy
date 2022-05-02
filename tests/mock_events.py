import copy
import json

SLACK_BASE_EVENT = {
    'resource': '/huggsy',
    'path': '/huggsy',
    'httpMethod': 'POST',
    'headers': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'application/json',
        'User-Agent': 'Slackbot 1.0',
    },
    'multiValueHeaders': {
        'Accept': ['*/*'],
        'Accept-Encoding': ['gzip,deflate'],
        'Content-Type': ['application/json'],
        'User-Agent': ['Slackbot 1.0'],
    },
    'queryStringParameters': None,
    'multiValueQueryStringParameters': None,
    'pathParameters': None,
    'stageVariables': None,
    'requestContext': {
        'resourcePath': '/huggsy',
        'httpMethod': 'POST',
        'path': '/default/huggsy',
        'protocol': 'HTTP/1.1',
        'stage': 'default',
    },
    'body': '',
    'isBase64Encoded': False
}


SLACK_APP_MENTION_EVENT = copy.deepcopy(SLACK_BASE_EVENT)
SLACK_APP_MENTION_EVENT_BODY = {
    "event": {
        "type": "app_mention",
        "text": "<@abc123> tell me a joke",
        "channel": "ghi789"
    }
}
SLACK_APP_MENTION_EVENT['body'] = json.dumps(SLACK_APP_MENTION_EVENT_BODY)


SLACK_BOT_MESSAGE_EVENT = copy.deepcopy(SLACK_BASE_EVENT)
SLACK_BOT_MESSAGE_EVENT_BODY = {
    "event": {
        "type": "message",
        "text": "tell me a joke",
        "channel": "abc123"
    }
}
SLACK_BOT_MESSAGE_EVENT['body'] = json.dumps(SLACK_BOT_MESSAGE_EVENT_BODY)


SLACK_CHALLENGE_EVENT = copy.deepcopy(SLACK_BASE_EVENT)
SLACK_CHALLENGE_EVENT_BODY = {"challenge": "challenge_response"}
SLACK_CHALLENGE_EVENT['body'] = json.dumps(SLACK_CHALLENGE_EVENT_BODY)


SLACK_MESSAGE_EVENT = copy.deepcopy(SLACK_BASE_EVENT)
SLACK_MESSAGE_EVENT_BODY = {
    "event": {
        "type": "message",
        "text": "tell me a joke",
        "channel": "abc123"
    }
}
SLACK_MESSAGE_EVENT['body'] = json.dumps(SLACK_MESSAGE_EVENT_BODY)
