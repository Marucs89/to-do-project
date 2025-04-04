from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select
from database import Session, get_session, create_db_and_tables,ToDo, Topics, Status, Bearbeiter, Arbeiter, create_database_helper
from datetime import datetime
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

# Access-Control-Allow-Origin
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Post Anfragen:
# BaseModel
class CreateToDo(BaseModel):
    name: str
    description: str | None = None
    deadline: datetime | None = None
    topic_id: int | None = None
    status_id: int | None = None
    mitarbeiter_id: list[int] = int
class CreateArbeiter(BaseModel):
    name: str
    lastname: str
    email: str | None = None
class CreateTopicStatus(BaseModel):
    name: str
class AddArbeiter(BaseModel):
    todo_id: int
    mitarbeiter_id: list[int] = int
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
        raise  HTTPException(status_code=400, detail=f"Fehler beim Erstellen: {str(e)}")
# API Anfragen:
# ToDo erstellen:
@app.post("/create-todo")
def create_todo(todo_data: CreateToDo, session: SessionDep):
    todo = create_todo_helper(todo_data)
    create_helper(todo, session)
    for x in todo_data.mitarbeiter_id: #<class 'database.Bearbeiter'>
        neuer_bearbeiter = Bearbeiter(todo_id=todo.todo_id, mitarbeiter_id=x)
        create_helper(neuer_bearbeiter, session)
    return {"status":"success"}
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
# arbeiter zu einem ToDo hinzufügen
@app.post("/add-arbeiter")
def add_arbeiter(to_add: AddArbeiter, session: SessionDep):
    statement = select(Bearbeiter).where(
    Bearbeiter.todo_id == to_add.todo_id,
                Bearbeiter.mitarbeiter_id != to_add.mitarbeiter_id
    )
    result = session.exec(statement)
    if result:
        for x in to_add.mitarbeiter_id:
            add = Bearbeiter(todo_id = to_add.todo_id, mitarbeiter_id = x)
            create_helper(add, session)
        return {"status": "success"}
    else:
        raise HTTPException (status_code=400, detail=f"mitarbeiter ist schon vorhanden!")
# Beispieldaten erstellen:
@app.post("/create-beispieldaten")
def create_beispieldaten(session: SessionDep):
    status = Status(name = 'noch nicht begonnen')
    create_helper(status, session)
    status = Status(name = 'in Arbeit.')
    create_helper(status, session)
    status =Status(name = 'fertig')
    create_helper(status, session)
    topic = Topics(name = 'Freizeit')
    create_helper(topic, session)
    topic = Topics(name = 'Arbeit')
    create_helper(topic, session)
    topic = Topics(name = 'Schule')
    create_helper(topic, session)
    topic = Topics(name = 'Sport')
    create_helper(topic, session)
    arbeiter = Arbeiter(name = 'Test', lastname = 'Testing', email = 'E-Mail')
    create_helper(arbeiter, session)
    todo = ToDo(name = 'Buy Milk', description = 'at the store', deadline = datetime.now(), topic_id = 1, status_id = 1, arbeiter_id = 1)
    create_helper(todo, session)
    statement = select(ToDo.todo_id)
    result = session.exec(statement).unique().all()
    lasttodo = max(result)
    bearbeiter = Bearbeiter(todo_id = lasttodo, mitarbeiter_id = 1)
    create_helper(bearbeiter, session)
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
            "done": todo.done,
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
    todos = session.exec(statement).unique().all()
    if not todos:
        raise HTTPException(status_code=404, detail=f"Todo '{todoid}' nicht gefunden")
    return read_todo_helper(todos)
# ToDos anhand des Topic namen ausgeben
@app.get("/todos-by-topic")
def read_todos_by_topic(topic: str, session: SessionDep):
    statement = select(Topics.topic_id).where(Topics.name == topic)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' nicht in der todo liste gefunden")
    statement = select(ToDo).where(ToDo.topic_id == result)
    todos = session.exec(statement).unique().all()
    if not todos:
        raise HTTPException(status_code=404, detail=f"'{topic}' nicht in todo liste gefunden")
    return read_todo_helper(todos)

# Put Anfragen:

# BaseModel:
class ArbeiterUpdate(BaseModel):
    todo_id: int
    mitarbeiter_id: list[int] = int
    new_mitarbeiter_id: list[int] = int
class TopicUpdate(BaseModel):
    todo_id: int
    topic_id: int
class StatusUpdate(BaseModel):
    todo_id: int
    status_id: int
class DoneUpdate(BaseModel):
    todo_id:int
    done: bool

# Helper:
def change_helper(session, statement, field_name, new_value, test=False, table=None):
    results = session.exec(statement).unique().all()
    if not results:
        raise HTTPException(status_code=404, detail=f"'{field_name}' nicht in liste gefunden")
    attribute = results[0]
    if test and table:
        if table == Arbeiter:
            id_field = "mitarbeiter_id"
        elif table == Topics:
            id_field = "topic_id"
        elif table == Status:
            id_field = "status_id"
        else:
            id_field = "id"
        check_statement = select(table).where(getattr(table, id_field) == new_value) # SELECT * FROM table_name WHERE id_field = value
        existing_item = session.exec(check_statement).first()
        if not existing_item:
            raise HTTPException(status_code=400,
                                detail=f"{field_name}={new_value} existiert nicht in '{table.__name__}'")
    setattr(attribute, field_name, new_value) # UPDATE table_name SET field_name = new_value WHERE primary_key_column = primary_key_value
    session.add(attribute)
    session.commit()
    session.refresh(attribute)
    return {"status": "success"}

# API Anfragen:
# arbeiter in der bearbeiter liste ändern
@app.put("/change-arbeiter")
def update_arbeiter(new_mitarbeiter: ArbeiterUpdate, session: SessionDep):
    test = 0
    for x in new_mitarbeiter.mitarbeiter_id:
        statement = select(Bearbeiter).where((Bearbeiter.todo_id == new_mitarbeiter.todo_id)
                                         & (Bearbeiter.mitarbeiter_id == x))
        y = new_mitarbeiter.new_mitarbeiter_id[test]
        test += 1
        change_helper(session, statement, 'mitarbeiter_id', y, True, Arbeiter)
    return {"status": "success"}
# 1. for loop führt aus -> 2. for loop darf nur die erste sache ausführen: for x in new_mitarbeiter.new_mitarbeiter_id.first() -> del new_mitarbeiter.new_mitarbeiter_id[1] -> break

# topic in der todo liste ändern
@app.put("/change-topic")
def update_topic(new_topic: TopicUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_topic.todo_id)
    return change_helper(session, statement, 'topic_id', new_topic.topic_id, True, Topics)
# status in der todo liste ändern
@app.put("/change-status")
def update_status(new_status: StatusUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_status.todo_id)
    return change_helper(session, statement, 'status_id', new_status.status_id, True, Status)
# done in der todo lsite ändern
@app.put("/change-done")
def update_done(new_done: DoneUpdate, session: SessionDep):
    statement = select(ToDo).where(ToDo.todo_id == new_done.todo_id)
    return change_helper(session, statement, 'done', new_done.done)


# DELETE Anfragen:
# Base Model:
class DeleteTodo(BaseModel):
    todo_id: int
class DeleteBearbeiterMitarbeiter(BaseModel):
    todo_id:int
    mitarbeiter_id: list[int] = int
# Helper:
def delete_helper(statement, session):
    try:
        result = session.exec(statement).unique()
        todelete = result.first()
        if not todelete:
            raise HTTPException(status_code=404, detail=f"Es wurde kein eintrag in der tabelle gefunden")
        for x in todelete:
            session.delete(todelete)
            session.commit()
    except Exception as e:
        session.rollback()
        raise  HTTPException(status_code=400, detail=f"Fehler beim löschen Fehler:'{e}'")
# API Anfragen:
# die ganze database wird gelöscht und neu erstellt inklusive tables
@app.delete("/delete-database")
def delete_database(delete:bool):
    if delete:
        create_database_helper(delete)
        yield create_db_and_tables()
        return {"status": "success"}
    return {"status": "failed"}

# delete todo
@app.delete("/delete-todo")
def delete_todo(todo_id: int, session:SessionDep):
    # delete from ToDo where ToDo.todo_id == todo_id
    statement = select(Bearbeiter).where(Bearbeiter.todo_id == todo_id)
    delete_helper(statement, session)
    statement = select(ToDo).where(ToDo.todo_id == todo_id)
    delete_helper(statement, session)
    return {"status": "success"}
# delete mitarbeiter von Bearbeiter wenn es über zwei gibt
@app.delete("/delete-bearbeiter-mitarbeiter")
def delete_bearbeiter_mitarbeiter(to_delete: DeleteBearbeiterMitarbeiter, session: SessionDep):
    statement = select(Bearbeiter).where(Bearbeiter.todo_id == to_delete.todo_id)
    result: list = session.exec(statement).unique().all()
    if len(result) < 2:
        raise HTTPException(status_code=400, detail="Es gibt nur einen Mitarbeiter für das ToDo!")
    else:
        statement = select(Bearbeiter).where((Bearbeiter.todo_id == to_delete.todo_id)
                                             & (Bearbeiter.mitarbeiter_id == to_delete.mitarbeiter_id))
        delete_helper(statement, session)
        return {"status": "success"}