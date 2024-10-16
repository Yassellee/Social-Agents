from pydantic import BaseModel


class OddOrEven(BaseModel):
    parity: str