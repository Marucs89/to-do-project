from sqlmodel import select
from backend.database.config import create_db_and_tables, create_database_helper
from backend.database.tables import ToDo, Topics, Status, Bearbeiter, Arbeiter
from datetime import datetime
from backend.api.helperFunc import create_helper
from typing import Annotated
from backend.database.config import Session, get_session
from fastapi import APIRouter, Depends
from backend.repositories.repository import MiscRepository

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]



@router.post("/create-beispieldaten")
def create_beispieldaten(session: SessionDep):
    """
    Create sample data for the application.

    Args:
        session: Database session

    Creates:
        - Three status entries (not started, in progress, completed)
        - Four topic entries (Leisure, Work, School, Sports)
        - One test worker
        - One sample todo item connected to the worker
    """
    # Create three status entries
    status = Status(name = 'noch nicht begonnen')  # not started
    create_helper(status, session)
    status = Status(name = 'in Arbeit.')  # in progress
    create_helper(status, session)
    status = Status(name = 'fertig')  # completed
    create_helper(status, session)

    # Create four topic entries
    topic = Topics(name = 'Freizeit')  # Leisure
    create_helper(topic, session)
    topic = Topics(name = 'Arbeit')  # Work
    create_helper(topic, session)
    topic = Topics(name = 'Schule')  # School
    create_helper(topic, session)
    topic = Topics(name = 'Sport')  # Sports
    create_helper(topic, session)

    # Create a test worker
    arbeiter = Arbeiter(name = 'Test', lastname = 'Testing', email = 'E-Mail')
    create_helper(arbeiter, session)

    # Create a sample todo item
    todo = ToDo(name = 'Buy Milk', description = 'at the store', deadline = datetime.now(), topic_id = 1, status_id = 1, arbeiter_id = 1)
    create_helper(todo, session)

    # Get the ID of the created todo and connect it with the worker
    result = MiscRepository.get_todoid(session)
    lasttodo = max(result)
    bearbeiter = Bearbeiter(todo_id = lasttodo, mitarbeiter_id = 1)
    create_helper(bearbeiter, session)

    return {"status":"success"}


# DANGER: This endpoint allows deleting the entire database
# Commented out for safety reasons
@router.delete("/delete-database")
def delete_database(delete:bool):
     if delete:
         create_database_helper(delete)
         yield create_db_and_tables()
         return {"status": "success"}
     return {"status": "failed"}