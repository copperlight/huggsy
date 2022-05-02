import unittest

from app.lambda_function import lambda_handler
from .mock_events import SLACK_CHALLENGE_EVENT
from .mock_events import SLACK_MESSAGE_EVENT


class LambdaFunctionTest(unittest.TestCase):

    def test_accept_known_user_agent(self):
        result = lambda_handler(SLACK_MESSAGE_EVENT, {})
        self.assertEqual({"statusCode": 200}, result)

    def test_reject_unknown_user_agent(self):
        event = SLACK_MESSAGE_EVENT
        event["headers"]["User-Agent"] = "Mozilla/5.0"
        result = lambda_handler(event, {})
        self.assertEqual({"body": "forbidden", "statusCode": 403}, result)

    def test_skill_challenge_response(self):
        result = lambda_handler(SLACK_CHALLENGE_EVENT, {})
        self.assertEqual({"body": "challenge_response", "statusCode": 200}, result)
