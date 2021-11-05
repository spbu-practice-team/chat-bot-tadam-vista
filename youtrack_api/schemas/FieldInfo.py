from typing import Any
from pydantic import BaseModel


class FieldInfo(BaseModel):
    name: str
    value: Any
