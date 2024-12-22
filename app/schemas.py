from pydantic import BaseModel


class TermBase(BaseModel):
    term: str
    definition: str


class TermCreate(TermBase):
    pass


class TermOut(TermBase):
    id: int

    class Config:
        from_attributes = True
