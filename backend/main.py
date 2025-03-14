from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select, insert
from database import Session, get_session, create_db_and_tables,ToDo, Topics, Status, Bearbeiter
from datetime import datetime

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# wenn Programm gestartet wird, werden tables erstellt / geladen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# get Anfrage mit query: tagid
from pydantic import BaseModel


class ToDoCreate(BaseModel):
    name: str
    description: str | None = None
    deadline: datetime | None = None
    topic_id: int | None = None
    status_id: int | None = None
    arbeiter_id: int | None = None

def create_todo_helper(data:ToDoCreate):
    create_todos = ToDo(name = data.name, description= data.description, deadline = data.deadline, topic_id = data.topic_id, status_id = data.status_id)
    return create_todos

@app.post("/todo")
def create_todo(todo_data: ToDoCreate, session: SessionDep):
    try:
        todo = create_todo_helper(todo_data)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        neuer_bearbeiter = Bearbeiter(todo_id=todo.todo_id, mitarbeiter_id=todo_data.arbeiter_id)
        session.add(neuer_bearbeiter)
        session.commit()
        return {"status": "success", "todo": todo}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Fehler beim Erstellen des ToDos: {str(e)}")
@app.get("/todos-by-id")
def read_todos(todoid:int, session: SessionDep):
    # Optionale Filterung nach ID
    statement = select(ToDo).where(ToDo.todo_id == todoid)
    todos = session.exec(statement).all()

    # Liste mit erweiterten Informationen erstellen
    result = []
    for todo in todos:
        topic_info = {"topic_id": todo.topic.topic_id, "name": todo.topic.name}
        status_info = {"status_id": todo.status.status_id, "name": todo.status.name}
        # Bei Bedarf explizites Laden der verknüpften Daten
        arbeiter_liste = [
            {
                "mitarbeiter_id": link.arbeiter.mitarbeiter_id,
                "name": link.arbeiter.name,
                "lastname": link.arbeiter.lastname,
                "email": link.arbeiter.email
            }
            for link in todo.bearbeiter_links
        ]
        todo_dict = {
            "todo_id": todo.todo_id,
            "name": todo.name,
            "description": todo.description,
            "deadline": todo.deadline,
            "arbeiter": arbeiter_liste,
            "topic": topic_info,
            "status": status_info
        }
        result.append(todo_dict)

    return result

# get anfrage todos-by-topic?topic=1 -> topic table, premade topics später post request
@app.get("/todos-by-topic")
def read_todos_by_topic(topic: str, session: SessionDep):
    # Zuerst die topic_id finden
    statement = select(Topics.topic_id).where(Topics.name == topic)
    result = session.exec(statement).first()

    # Prüfen, ob ein Topic gefunden wurde
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' nicht gefunden")

    topic_id = result

    # Alle ToDos mit diesem Topic laden
    statement = select(ToDo).where(ToDo.topic_id == topic_id)
    todos = session.exec(statement).all()

    # Ergebnisliste erstellen
    result = []
    for todo in todos:
        # Topic und Status als einzelne Dictionaries, nicht als Listen
        topic_info = {"topic_id": todo.topic.topic_id, "name": todo.topic.name}
        status_info = {"status_id": todo.status.status_id, "name": todo.status.name}

        arbeiter_liste = [
            {
                "mitarbeiter_id": link.arbeiter.mitarbeiter_id,
                "name": link.arbeiter.name,
                "lastname": link.arbeiter.lastname,
                "email": link.arbeiter.email
            }
            for link in todo.bearbeiter_links
        ]

        todo_dict = {
            "todo_id": todo.todo_id,
            "name": todo.name,
            "description": todo.description,
            "deadline": todo.deadline,
            "arbeiter": arbeiter_liste,
            "topic": topic_info,  # Einzelnes Dictionary, keine Liste
            "status": status_info  # Einzelnes Dictionary, keine Liste
        }
        result.append(todo_dict)

    return result