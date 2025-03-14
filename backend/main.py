from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select, insert
from database import Session, get_session, create_db_and_tables,ToDo, Topics, Status, Bearbeiter, Arbeiter
from datetime import datetime
from pydantic import BaseModel

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# wenn Programm gestartet wird, werden tables erstellt / geladen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Post Anfragen:
# Ein ToDo erstellen:
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

@app.post("/create-todo")
def create_todo(todo_data: ToDoCreate, session: SessionDep):
    try:
        todo = create_todo_helper(todo_data)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        neuer_bearbeiter = Bearbeiter(todo_id=todo.todo_id, mitarbeiter_id=todo_data.arbeiter_id)
        session.add(neuer_bearbeiter)
        session.commit()
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Fehler beim Erstellen des ToDos: {str(e)}")

# Ein Arbeiter erstellen:
class CreateArbeiter(BaseModel):
    name: str
    lastname: str
    email: str | None = None
@app.post("/create-arbeiter")
def create_arbeiter(arbeiter_data : CreateArbeiter, session: SessionDep):
    try:
        mitarbeiter = Arbeiter(
            name=arbeiter_data.name,
            lastname=arbeiter_data.lastname,
            email=arbeiter_data.email
        )
        session.add(mitarbeiter)
        session.commit()
        session.refresh(mitarbeiter)
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Fehler beim Erstellen des Arbeiter: {str(e)}")

# Ein Topic erstellen:
class CreateTopic(BaseModel):
    name: str
@app.post("/create-topic")
def create_topic(topic_data: CreateTopic, session: SessionDep):
    try:
        topic = Topics(name=topic_data.name)
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return {"status":"success"}
    except Exception as e:
        session.rollback()
        raise  HTTPException(status_code=400, detail=f"Fehler beim Erstellen des Topics: {str(e)}")

# Get Anfragen:
# Alle Daten mit einer todo_id ausgeben:
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

# alle Daten eines topic ausgeben mit dem topic namen:
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

# Put Anfragen:
# die topic_id und/oder status_id eines ToDos ändern:
class StatusTopicUpdate(BaseModel):
    todo_id: int
    topic_id: int | None = None
    status_id: int | None = None
@app.put("/change-topic-status")
def update_status(new_status: StatusTopicUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_status.todo_id)
    if new_status.status_id is not None:
        results = session.exec(statement).all()
        change_todo = results[0]
        change_todo.status_id = new_status.status_id
        session.add(change_todo)
        session.commit()
        session.refresh(change_todo)
    if new_status.topic_id is not None:
        results = session.exec(statement).all()
        change_topic = results[0]
        change_topic.topic_id = new_status.topic_id
        session.add(change_topic)
        session.commit()
        session.refresh(change_topic)
    else:
        raise HTTPException(status_code=404, detail=f"false input")
    return {"status": "success"}

# Aufgaben:
# arbeiter löschen in der bearbeiter/arbeiter liste einen allgemeinen arbeiter hinzufügen
# http errors hinzufügen