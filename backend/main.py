from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select
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
# BaseModel
class CreateToDo(BaseModel):
    name: str
    description: str | None = None
    deadline: datetime | None = None
    topic_id: int | None = None
    status_id: int | None = None
    arbeiter_id: int | None = None
class CreateArbeiter(BaseModel):
    name: str
    lastname: str
    email: str | None = None
class CreateTopicStatus(BaseModel):
    name: str
# Helper:
def create_todo_helper(data:CreateToDo):
    create_todos = ToDo(name = data.name, description= data.description, deadline = data.deadline, topic_id = data.topic_id, status_id = data.status_id)
    return create_todos
def create_helper(data, session):
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return {"status":"success"}
    except Exception as e:
        session.rollback()
        raise  HTTPException(status_code=400, detail=f"Fehler beim Erstellen des: {str(e)}")
# API Anfragen:
# ToDo erstellen:
@app.post("/create-todo")
def create_todo(todo_data: CreateToDo, session: SessionDep):
    todo = create_todo_helper(todo_data)
    create_helper(todo, session)
    neuer_bearbeiter = Bearbeiter(todo_id=todo.todo_id, mitarbeiter_id=todo_data.arbeiter_id)
    return create_helper(neuer_bearbeiter, session)
# Arbeiter erstellen:
@app.post("/create-arbeiter")
def create_arbeiter(arbeiter_data : CreateArbeiter, session: SessionDep):
    mitarbeiter = Arbeiter(name=arbeiter_data.name,lastname=arbeiter_data.lastname,email=arbeiter_data.email)
    return create_helper(mitarbeiter, session)
# Topic erstellen:
@app.post("/create-topic")
def create_topic(topic_data: CreateTopicStatus, session: SessionDep):
    topic = Topics(name = topic_data.name)
    return create_helper(topic, session)
# Status erstellen:
@app.post("/create-status")
def create_status(status_data: CreateTopicStatus, session: SessionDep):
    status = Status(name = status_data.name)
    return create_helper(status, session)
# Beispieldaten erstellen:
@app.post("/create-beispieldaten")
def create_beispieldaten(session: SessionDep):
    status = Status(name='Bsp.')
    create_helper(status, session)
    topic = Topics(name='Bsp.')
    create_helper(topic, session)
    arbeiter = Arbeiter(name='Test', lastname='Testing', email='E-Mail')
    create_helper(arbeiter, session)
    todo = ToDo(name='Buy Milk', description = 'at the store', deadline = datetime.now(), topic_id = 1, status_id = 1, arbeiter_id = 1)
    create_helper(todo, session)
    return {"status":"success"}

# Get Anfragen:

# BaseModel:

# Helper:
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

# API Anfragen:
# ToDos anhand der todo_id ausgeben
@app.get("/todos-by-id")
def read_todos(todoid: int, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == todoid)
    todos = session.exec(statement).all()
    if not todos:
        raise HTTPException(status_code=404, detail=f"Todo '{todoid}' nicht gefunden")
    return read_todo_helper(todos)
# ToDos anhand des Topic namen ausgeben
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

# BaseModel:
class ArbeiterUpdate(BaseModel):
    todo_id: int
    mitarbeiter_id: int
    new_mitarbeiter_id: int
class TopicUpdate(BaseModel):
    todo_id: int
    topic_id: int
class StatusUpdate(BaseModel):
    todo_id: int
    status_id: int

# Helper:
def change_helper(session, statement, field_name, new_value):
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"ToDo nicht gefunden")
    attribute = results[0]
    setattr(attribute, field_name, new_value) # update attribute, set new_value, where field_name,
    session.add(attribute)
    session.commit()
    session.refresh(attribute)
    return {"status": "success"}

# API Anfragen:
# arbeiter in der bearbeiter liste ändern
@app.put("/change-arbeiter")
def update_arbeiter(new_mitarbeiter: ArbeiterUpdate, session: SessionDep):
    statement = select(Bearbeiter).where(Bearbeiter.todo_id == new_mitarbeiter.todo_id
                                         and Bearbeiter.mitarbeiter_id == new_mitarbeiter.mitarbeiter_id)
    return  change_helper(session, statement, 'mitarbeiter_id', new_mitarbeiter.new_mitarbeiter_id)
# topic in der todo liste ändern
@app.put("/change-topic")
def update_topic(new_topic: TopicUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_topic.todo_id)
    return change_helper(session, statement, 'topic_id', new_topic.topic_id)
# status in der todo liste ändern
@app.put("/change-status")
def update_status(new_status: StatusUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_status.todo_id)
    return change_helper(session, statement, 'status_id', new_status.status_id)
# Test