import random

# pylint: disable=line-too-long
FACT_LIST = [
    "foo",
    "bar",
    "baz"
]


# def skill_random_fact(slack_event: SlackEvent) -> int:
#     """Add this to the lambda_function handler."""
#     data = {
#         "channel": slack_event.channel,
#         "text": random_fact()
#     }
#     return slack_post_message(data, slack_event.thread_ts)


def random_fact() -> str:
    return random.choice(FACT_LIST)
