from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select
from database import Session, get_session, create_db_and_tables, Hero

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# wenn Programm gestartet wird, werden tables erstellt / geladen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

# get Anfrage mit query: tagid
@app.get("/todos/")
def read_todos(tagid: int, session: SessionDep):
    statement = select(Hero).where(Hero.id == tagid)
    results = session.exec(statement)
    for x in results:
        return x

# funktioniert nicht
@app.get("/heroes/team/")
def read_heroes_team(session: SessionDep):
    return Hero.team