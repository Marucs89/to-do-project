from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from backend.database.tables import Bearbeiter
from backend.api.baseModels import DeleteBearbeiterMitarbeiter
from backend.api.helperFunc import delete_helper
from typing import Annotated
from backend.database.config import Session, get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@router.delete("/delete-bearbeiter-mitarbeiter")
def delete_bearbeiter_mitarbeiter(to_delete: DeleteBearbeiterMitarbeiter, session: SessionDep):
    """
    Delete a worker association from a todo item.

    Args:
        to_delete: Object containing todo_id and mitarbeiter_id (worker ID) to remove
        session: Database session

    Actions:
        1. Query all worker associations for the specified todo
        2. Check if there's more than one worker assigned
        3. If only one worker is assigned, reject the delete operation
        4. If multiple workers are assigned, delete the specified association

    Returns:
        Success status if the worker was removed from the todo

    Raises:
        HTTPException: If attempting to delete the only worker from a todo
    """
    statement = select(Bearbeiter).where(Bearbeiter.todo_id == to_delete.todo_id)
    result: list = session.exec(statement).unique().all()
    if len(result) < 2:
        raise HTTPException(status_code=400, detail="Es gibt nur einen Mitarbeiter für das ToDo!")
    else:
        statement = select(Bearbeiter).where((Bearbeiter.todo_id == to_delete.todo_id)
                                             & (Bearbeiter.mitarbeiter_id == to_delete.mitarbeiter_id))
        delete_helper(statement, session)
        return {"status": "success"}