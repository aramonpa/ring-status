from pydantic import BaseModel
from typing import Literal

class TrackStatusResponse(BaseModel):
    response: Literal["ok", "error"]
    status: Literal["Open", "Closed", "Unknown"]
    img_url: str
