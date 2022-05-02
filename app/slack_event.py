from dataclasses import dataclass
from typing import Optional

APP_MENTION = "app_mention"
MESSAGE = "message"


@dataclass
class SlackEvent:
    type: str
    channel: str
    text: str
    bot_id: Optional[str]
    thread_ts: Optional[int]
