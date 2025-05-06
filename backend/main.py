from fastapi import HTTPException
from sqlmodel import select
from backend.database.config import create_db_and_tables, create_database_helper
from backend.database.tables import ToDo, Topics, Status, Bearbeiter, Arbeiter
from datetime import datetime
from backend.api.baseModels import CreateToDo, CreateArbeiter, CreateTopicStatus, TopicUpdate, AddArbeiter, ArbeiterUpdate, StatusUpdate, DoneUpdate, DeleteBearbeiterMitarbeiter
from backend.api.helperFunc import create_todo_helper, create_helper, read_todo_helper, change_helper, delete_helper
from backend.api.config import app, SessionDep

##########--Anfragen--##########

##########--Post--##########

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
    # retrun mitarbeiter_id
    create_helper(mitarbeiter, session)
    statemen = select(Arbeiter.mitarbeiter_id)
    result = session.exec(statemen)
    toretrun = {"status": "success", "mitarbeiter_id": str(max(result))}
    return toretrun
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

##########--Get--##########

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
# Aufgabe: Get mitarbeiter-by-name
@app.get("/miarbeiter-by-name")
def read_mitarbeiter_by_name(name:str, session:SessionDep):
    statement = select(Arbeiter).where(Arbeiter.name == name)
    result= session.exec(statement).first()
    if result:
        toretrun = {"mitarbeiter_id": result.mitarbeiter_id, "name": result.name, "lastname": result.lastname, "email": result.email}
        return toretrun
    else:
        raise HTTPException(status_code=404, detail=f"Arbeiter: '{name}' nicht gefunden")

##########--Put--##########

# API Anfragen:
# arbeiter in der bearbeiter liste ändern
@app.put("/change-arbeiter")
def update_arbeiter(new_mitarbeiter: ArbeiterUpdate, session: SessionDep):
    test = 0
    for x in new_mitarbeiter.mitarbeiter_id:
        # im BaseModel von List zu int ändern
        statement = select(Bearbeiter).where((Bearbeiter.todo_id == new_mitarbeiter.todo_id)
                                         & (Bearbeiter.mitarbeiter_id == x))
        y = new_mitarbeiter.new_mitarbeiter_id[test]
        print(y)
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


##########--Delete--##########

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

# change-todos hinzufügen