from enum import Enum
from pydantic import BaseModel
from typing import List


class OddOrEven(BaseModel):
    parity: str