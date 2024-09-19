from pydantic import BaseModel
from typing import Dict


class MessagePayload(BaseModel):
    recipient: Dict[str, str]
    message: Dict[str, str]
