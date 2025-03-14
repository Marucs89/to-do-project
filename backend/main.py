from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select, insert
from database import Session, get_session, create_db_and_tables,ToDo, Topics, Status, Bearbeiter, Arbeiter
from datetime import datetime
from pydantic import BaseModel
from contextlib import asynccontextmanager

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

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
def read_todo_helper(read_todo:list):
    result = []
    for todo in read_todo:
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
            "topic": topic_info,
            "status": status_info
        }
        result.append(todo_dict)
    return result

# Alle Daten mit einer todo_id ausgeben:
@app.get("/todos-by-id")
def read_todos(todoid:int, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == todoid)
    todos = session.exec(statement).all()
    return read_todo_helper(todos)

# alle Daten eines topic ausgeben mit dem topic namen:
@app.get("/todos-by-topic")
def read_todos_by_topic(topic: str, session: SessionDep):
    statement = select(Topics.topic_id).where(Topics.name == topic)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' nicht gefunden")
    statement = select(ToDo).where(ToDo.topic_id == result)
    todos = session.exec(statement).all()
    return read_todo_helper(todos)

# Put Anfragen:
# die topic_id und/oder status_id eines ToDos ändern:
class TopicStatusUpdate(BaseModel):
    todo_id: int
    topic_id: int | None = None
    status_id: int | None = None


def change_topic_status_helper(session, statement, field_name, new_value):
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"ToDo nicht gefunden")
    todo = results[0]
    setattr(todo, field_name, new_value)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.put("/change-topic-status")
def update_status(new_status: TopicStatusUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_status.todo_id)
    if new_status.status_id is not None:
        change_topic_status_helper(session, statement, 'status_id', new_status.status_id)
    if new_status.topic_id is not None:
        change_topic_status_helper(session, statement, 'topic_id', new_status.topic_id)
    if new_status.status_id is None and new_status.topic_id is None:
        raise HTTPException(status_code=404, detail=f"false input")
    return {"status": "success"}

# Aufgaben:
# arbeiter löschen in der bearbeiter/arbeiter liste einen allgemeinen arbeiter hinzufügen
# http errors hinzufügen