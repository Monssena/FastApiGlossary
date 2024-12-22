from sqlalchemy import Column, Integer, String

from app.db import Base


class Term(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True, nullable=False)
    definition = Column(String)
