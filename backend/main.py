from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select
from database import Session, get_session, create_db_and_tables, Hero, Teams, ToDo, Topics

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

@app.post("/teams/")
def create_team(team: Teams, session: SessionDep) -> Teams:
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

# get Anfrage mit query: tagid
@app.get("/todo")
def read_todos(todoid:int, session: SessionDep):
    # Optionale Filterung nach ID
    statement = select(ToDo).where(ToDo.todo_id == todoid)
    todos = session.exec(statement).all()

    # Liste mit erweiterten Informationen erstellen
    result = []
    for todo in todos:
        # Bei Bedarf explizites Laden der verknüpften Daten
        arbeiter_liste = [
            {
                "mitarbeiter_id": link.arbeiter.mitarbeiter_id,
                "name": link.arbeiter.name,
                "lastname": link.arbeiter.lastname
            }
            for link in todo.bearbeiter_links
        ]

        # ToDo mit verknüpften Arbeitern
        todo_dict = {
            "todo_id": todo.todo_id,
            "name": todo.name,
            "details": todo.description,
            "deadline": todo.deadline,
            "arbeiter": arbeiter_liste
        }
        result.append(todo_dict)

    return result

# get anfrage todos-by-topic?topic=1 -> topic table, premade topics später post request
@app.get("/todos-by-topic")
def read_todos_by_topic(topic: str, session: SessionDep):
    statement = select(Topics.topic_id).where(Topics.name == topic)
    topicid = session.exec(statement).all()
    statement = select(ToDo).where(ToDo.topic_id == topicid[0])
    todos = session.exec(statement).all()
    for todo in todos:
        return todo