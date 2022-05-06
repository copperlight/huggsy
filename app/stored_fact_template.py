import random

# pylint: disable=line-too-long
FACT_LIST = [
    "foo",
    "bar",
    "baz"
]

# from app.stored_fact_template import random_fact
#
# def skill_random_fact(slack_event: SlackEvent) -> int:
#     """Add this to the lambda_function handler."""
#     return slack_post_message(slack_event, random_fact())


def random_fact() -> str:
    return random.choice(FACT_LIST)
