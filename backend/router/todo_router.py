from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Bearbeiter
from backend.api.baseModels import CreateToDo, DoneUpdate, TodoUpdate
from backend.api.helperFunc import create_todo_helper, create_helper, read_todo_helper, change_helper, delete_helper
from typing import Annotated
from backend.database.config import Session, get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/create-todo")
def create_todo(todo_data: CreateToDo, session: SessionDep):
    """
    Create a new todo item and associate it with workers.

    Args:
        todo_data: Data for the new todo item
        session: Database session

    Actions:
        1. Create a new todo item
        2. Save it to the database
        3. Associate each worker from the list with the new todo
        4. Return success status
    """
    todo = create_todo_helper(todo_data)
    create_helper(todo, session)
    for x in todo_data.mitarbeiter_id:  # Associate each worker with the todo
        neuer_bearbeiter = Bearbeiter(todo_id=todo.todo_id, mitarbeiter_id=x)
        create_helper(neuer_bearbeiter, session)
    return {"status":"success"}


@router.get("/todos-by-id")
def read_todos(todoid: int, session: SessionDep):
    """
    Retrieve a specific todo item by its ID.

    Args:
        todoid: The ID of the todo item to retrieve
        session: Database session

    Actions:
        1. Query the database for the todo with the specified ID
        2. If not found, raise a 404 error
        3. If found, process and return the todo data
    """
    statement = select(ToDo).where(ToDo.todo_id == todoid)
    todos = session.exec(statement).unique().all()
    if not todos:
        raise HTTPException(status_code=404, detail=f"Todo '{todoid}' nicht gefunden")
    return read_todo_helper(todos)

@router.get("/todos-by-topic")
def read_todos_by_topic(topic: str, session: SessionDep):
    """
    Retrieve all todo items with a specific topic.

    Args:
        topic: The name of the topic to filter by
        session: Database session

    Actions:
        1. Query the database to find the topic ID for the given topic name
        2. If topic not found, raise a 404 error
        3. Query for all todos associated with that topic ID
        4. If no todos found with that topic, raise a 404 error
        5. Process and return the todo data
    """
    statement = select(Topics.topic_id).where(Topics.name == topic)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' nicht in der todo liste gefunden")
    statement = select(ToDo).where(ToDo.topic_id == result)
    todos = session.exec(statement).unique().all()
    if not todos:
        raise HTTPException(status_code=404, detail=f"'{topic}' nicht in todo liste gefunden")
    return read_todo_helper(todos)


@router.put("/change-todo")
def update_todo(new_todo: TodoUpdate, session: SessionDep):
    """
    Update a todo item with new values.

    Args:
        new_todo: Data containing todo_id and fields to update
        session: Database session

    Actions:
        1. Find the todo item by its ID
        2. Update only the fields that contain values (name, description, deadline)
        3. Skip updating fields that are empty

    Returns:
        A success status message
    """
    statement = select(ToDo).where(new_todo.todo_id == ToDo.todo_id)
    if new_todo.name:
        change_helper(session, statement, 'name', new_todo.name)
    if new_todo.description:
        change_helper(session, statement, "description", new_todo.description)
    if new_todo.deadline:
        change_helper(session, statement, "deadline", new_todo.deadline)
    return {"status": "success"}

@router.put("/change-done")
def update_done(new_done: DoneUpdate, session: SessionDep):
    """
    Update the completion status of a todo item.

    Args:
        new_done: Data containing todo_id and new done status
        session: Database session

    Actions:
        1. Find the todo item by its ID
        2. Update the done field to the new value
        3. Return the result from change_helper
    """
    statement = select(ToDo).where(ToDo.todo_id == new_done.todo_id)
    return change_helper(session, statement, 'done', new_done.done)


# DANGER: This endpoint allows deleting todo items
@router.delete("/delete-todo")
def delete_todo(todo_id: int, session:SessionDep):
    """
    Delete a todo item and its worker associations.

    Args:
        todo_id: The ID of the todo item to delete
        session: Database session

    Actions:
        1. First delete all worker associations (Bearbeiter) for this todo
        2. Then delete the actual todo item itself
        3. Return success status
    """
    # Delete all worker associations for this todo
    statement = select(Bearbeiter).where(Bearbeiter.todo_id == todo_id)
    delete_helper(statement, session)
    # Delete the todo item itself
    statement = select(ToDo).where(ToDo.todo_id == todo_id)
    delete_helper(statement, session)
    return {"status": "success"}