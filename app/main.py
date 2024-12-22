from fastapi import FastAPI, HTTPException, Depends
from typing import List

from app.db import SessionLocal, get_db, Base, engine
from app.initial_terms import INITIAL_TERMS
from app.models import Term
from app.schemas import TermOut, TermCreate

app = FastAPI()


def init_db():
    Base.metadata.create_all(bind=engine)


def db_init_terms():
    db = SessionLocal()
    try:
        for term_data in INITIAL_TERMS:
            term = db.query(Term).filter(Term.term == term_data["term"]).first()
            if not term:
                db.add(Term(**term_data))
        db.commit()
    finally:
        db.close()

init_db()
db_init_terms()

# Получение всех терминов
@app.get("/terms", response_model=List[TermOut])
def get_terms(db: SessionLocal = Depends(get_db)):
    terms = db.query(Term).all()
    return terms


# Получение термина по названию
@app.get("/terms/{term}", response_model=TermOut)
def get_term(term: str, db: SessionLocal = Depends(get_db)):
    term_obj = db.query(Term).filter(Term.term == term).first()

    if not term_obj:
        raise HTTPException(status_code=404, detail="Термин не найден")

    return term_obj


# Добавление нового термина
@app.post("/terms", response_model=TermOut)
def create_term(term: TermCreate, db: SessionLocal = Depends(get_db)):
    existing_term = db.query(Term).filter(Term.term == term.term).first()

    if existing_term:
        raise HTTPException(status_code=400, detail="Термин уже существует")

    new_term = Term(term=term.term, definition=term.definition)
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term


# Обновление термина
@app.put("/terms/{term}", response_model=TermOut)
def update_term(term: str, term_data: TermCreate, db: SessionLocal = Depends(get_db)):
    term_obj = db.query(Term).filter(Term.term == term).first()

    if not term_obj:
        raise HTTPException(status_code=404, detail="Термин не найден")

    term_obj.term = term_data.term
    term_obj.definition = term_data.definition
    db.commit()
    db.refresh(term_obj)
    return term_obj


@app.delete("/terms/{term}", response_model=dict)
def delete_term(term: str, db: SessionLocal = Depends(get_db)):
    term_obj = db.query(Term).filter(Term.term == term).first()

    if not term_obj:
        raise HTTPException(status_code=404, detail="Термин не найден")

    db.delete(term_obj)
    db.commit()
    return {"message": "Термин удалён"}
