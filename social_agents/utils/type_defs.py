from pydantic import BaseModel


class OddOrEven(BaseModel):
    parity: str

class EvacuationDiscussion(BaseModel):
    content: str
    make_decision: bool
    decision: str