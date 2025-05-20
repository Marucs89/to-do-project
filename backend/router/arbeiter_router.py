from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from backend.database.tables import Bearbeiter, Arbeiter
from typing import Annotated
from backend.models.requests import CreateArbeiter, AddArbeiter, ArbeiterUpdate, DeleteArbeiter
from backend.services.create_services import create_helper
from backend.services.change_services import change_helper
from backend.database.config import Session, get_session
from backend.repositories.repository import ArbeiterRepository
from backend.services.delete_services import delete_helper


router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/all-arbeiter")
def all_arbeiter(session: SessionDep):
    return session.exec(select(Arbeiter)).unique().all()


@router.post("/create-arbeiter")
def create_arbeiter(arbeiter_data : CreateArbeiter, session: SessionDep):
    """
    Create one or more new worker entries in the database.

    Args:
        arbeiter_data: Data containing a list of worker names to create
        session: Database session

    Actions:
        1. For each name in the list, create a new worker with that name
        2. Save each worker to the database
        3. Query for each worker's ID after creation
        4. Return success status with all newly created worker IDs
    """
    data_for_return = []
    for arbeiter in arbeiter_data.name:
        mitarbeiter = Arbeiter(name=arbeiter)
        create_helper(mitarbeiter, session)
        result = ArbeiterRepository.get_mitarbeiter_id(session)
        data_for_return.append(result)
    return_data = {"status": "success", "message": "the operation was successful", "data": {"mitarbeiter_id": data_for_return}}
    return return_data

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


@router.delete("/delete-arbeiter")
def delete_arbeiter(arbeiter_ids_to_delete: DeleteArbeiter, session: SessionDep):
    # Delete all worker associations for this todo
    deleted_data:list = []
    for arbeiter_id in arbeiter_ids_to_delete.mitarbeiter_id:
        statement = select(Bearbeiter).where(Bearbeiter.mitarbeiter_id == arbeiter_id)
        delete_helper(statement, session)
        # Delete the todo item itself
        statement = select(Arbeiter).where(Arbeiter.mitarbeiter_id == arbeiter_id)
        data = delete_helper(statement, session)
        deleted_data.append(data)
    return {"status": "success", "message": "oh no I hope you delete the right todo", "data": deleted_data}