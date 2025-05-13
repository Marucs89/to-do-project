from fastapi import HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status, Arbeiter
from backend.api.requests import CreateToDo


def create_todo_helper(data:CreateToDo):
    """
    Creates a ToDo object from the provided CreateToDo data model.

    Parameters:
        data: CreateToDo model containing the todo item details

    Returns:
        ToDo: A new ToDo database object ready to be added to the session
    """
    create_todos = ToDo(name=data.name, description=data.description, deadline=data.deadline,
                        topic_id=data.topic_id, status_id=data.status_id)
    return create_todos

def create_helper(data, session):
    """
    Adds an object to the database and handles the transaction.

    Parameters:
        data: The database model object to be added (ToDo, Arbeiter, etc.)
        session: Database session for executing the transaction

    Returns:
        Dict with success status on successful addition

    Raises:
        HTTPException: If database transaction fails with error details
    """
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return {"status":"success"}
    except Exception as e:
        session.rollback()
        raise  HTTPException(status_code=400, detail=f"Fehler beim Erstellen: {str(e)}")