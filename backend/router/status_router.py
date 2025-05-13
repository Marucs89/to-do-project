from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status
from backend.api.baseModels import CreateTopicStatus, StatusUpdate
from backend.api.helperFunc import create_helper, change_helper
from typing import Annotated
from backend.database.config import Session, get_session
from fastapi import APIRouter, Depends

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/create-status")
def create_status(status_data: CreateTopicStatus, session: SessionDep):
    """
    Create a new status in the database.

    Args:
        status_data: Data for the new status (contains name field)
        session: Database session

    Actions:
        1. Create a new status with the provided name
        2. Save it to the database using create_helper
        3. Return the result of create_helper
    """
    status = Status(name = status_data.name)
    return create_helper(status, session)


@router.put("/change-status")
def update_status(new_status: StatusUpdate, session: SessionDep):
    """
    Update the status of a todo item.

    Args:
        new_status: Data containing todo_id and new status_id
        session: Database session

    Actions:
        1. Find the todo item by its ID
        2. Update the status_id field to the new value
        3. Verify the new status exists using Status table
        4. Return the result from change_helper
    """
    statement = select(ToDo).where(ToDo.todo_id == new_status.todo_id)
    return change_helper(session, statement, 'status_id', new_status.status_id, True, Status)