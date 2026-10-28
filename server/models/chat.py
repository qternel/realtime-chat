from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class Message(BaseModel):
    username: Annotated[str, Field(min_length=1)]
    text: Annotated[str, Field(min_length=1)]
    sent_at: datetime


class MessagePayload(BaseModel):
    message: Message
