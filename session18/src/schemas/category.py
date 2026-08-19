from pydantic import BaseModel
from typing import Optional


class CreateCategory(BaseModel):
    name: str
