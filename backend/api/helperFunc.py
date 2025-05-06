from fastapi import HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status, Arbeiter
from backend.api.baseModels import CreateToDo

##########--Anfragen--##########

###########--Post--##########

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

##########--Get--##########

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

##########--Put--##########

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

##########--Delete--##########

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