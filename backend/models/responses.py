from pydantic import BaseModel
from typing import Any

class StandardResponse(BaseModel):
    status: str
    message: str | None
    data: Any | None