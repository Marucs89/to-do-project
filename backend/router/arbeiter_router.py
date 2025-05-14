from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from backend.database.tables import Bearbeiter, Arbeiter
from typing import Annotated
from backend.api.requests import CreateArbeiter, AddArbeiter, ArbeiterUpdate
from backend.api.helperFunc import create_helper, change_helper
from backend.database.config import Session, get_session
from backend.repositories.repository import ArbeiterRepository


router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/create-arbeiter")
def create_arbeiter(arbeiter_data : CreateArbeiter, session: SessionDep):
    """
    Create a new worker entry in the database.

    Args:
        arbeiter_data: Data for the new worker
        session: Database session

    Actions:
        1. Create a new worker with name, lastname and email
        2. Save it to the database
        3. Query for all worker IDs to find the highest (newest)
        4. Return success status with the newly created worker ID
    """
    mitarbeiter = Arbeiter(name=arbeiter_data.name,lastname=arbeiter_data.lastname,email=arbeiter_data.email)
    create_helper(mitarbeiter, session)
    result = ArbeiterRepository.get_mitarbeiter_id(session)
    toretrun = {"status": "success", "mitarbeiter_id": result}
    return toretrun

@router.post("/add-arbeiter")
def add_arbeiter(to_add: AddArbeiter, session: SessionDep):
    """
    Add one or more workers to a todo item.

    Args:
        to_add: Contains todo_id and a list of worker IDs to add
        session: Database session

    Actions:
        1. Query for existing workers assigned to this todo
        2. If workers can be added, create new Bearbeiter entries for each worker
        3. Return success status or error if worker is already assigned
    """
    result = ArbeiterRepository.post_mitarbeiter(session, to_add)
    if result:
        for x in to_add.mitarbeiter_id:
            add = Bearbeiter(todo_id = to_add.todo_id, mitarbeiter_id = x)
            create_helper(add, session)
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail=f"Worker is already assigned!")


@router.get("/mitarbeiter-by-name")
def read_mitarbeiter_by_name(name:str, session:SessionDep):
    """
    Retrieve a worker by their name.

    Args:
        name: The name of the worker to search for
        session: Database session

    Actions:
        1. Query the database for a worker with the specified name
        2. If found, return the worker's details (ID, name, lastname, email)
        3. If not found, raise a 404 error
    """
    result= ArbeiterRepository.get_mitarbeiter(session, name)
    if result:
        toretrun = {"mitarbeiter_id": result.mitarbeiter_id, "name": result.name, "lastname": result.lastname, "email": result.email}
        return toretrun
    else:
        raise HTTPException(status_code=404, detail=f"Worker: '{name}' not found")


@router.put("/change-arbeiter")
def update_arbeiter(new_mitarbeiter: ArbeiterUpdate, session: SessionDep):
    """
    Update worker assignments for a todo item.

    Args:
        new_mitarbeiter: Data containing todo_id, current worker IDs, and new worker IDs
        session: Database session

    Actions:
        1. Iterate through each worker ID in the input list
        2. Find the corresponding worker assignment (Bearbeiter) record
        3. Replace the current worker ID with the new worker ID
        4. Return success status when all updates are complete
    """
    index = 0
    for current_worker_id in new_mitarbeiter.mitarbeiter_id:
        statement = select(Bearbeiter).where((Bearbeiter.todo_id == new_mitarbeiter.todo_id)
                                         & (Bearbeiter.mitarbeiter_id == current_worker_id))
        new_worker_id = new_mitarbeiter.new_mitarbeiter_id[index]
        index += 1
        change_helper(session, statement, 'mitarbeiter_id', new_worker_id, True, Arbeiter)
    return {"status": "success"}