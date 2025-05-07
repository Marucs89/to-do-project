from fastapi import HTTPException
from sqlmodel import select
from backend.database.config import create_db_and_tables, create_database_helper
from backend.database.tables import ToDo, Topics, Status, Bearbeiter, Arbeiter
from datetime import datetime
from backend.api.baseModels import CreateToDo, CreateArbeiter, CreateTopicStatus, TopicUpdate, AddArbeiter, ArbeiterUpdate, StatusUpdate, DoneUpdate, DeleteBearbeiterMitarbeiter, TodoUpdate
from backend.api.helperFunc import create_todo_helper, create_helper, read_todo_helper, change_helper, delete_helper
from backend.api.config import app, SessionDep

##########--Post--##########


@app.post("/create-todo")
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


@app.post("/create-arbeiter")
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
    statemen = select(Arbeiter.mitarbeiter_id)
    result = session.exec(statemen)
    toretrun = {"status": "success", "mitarbeiter_id": str(max(result))}
    return toretrun


@app.post("/create-topic")
def create_topic(topic_data: CreateTopicStatus, session: SessionDep):
    """
    Create a new topic in the database.

    Args:
        topic_data: Data for the new topic (contains name field)
        session: Database session

    Actions:
        1. Create a new topic with the provided name
        2. Save it to the database using create_helper
        3. Return the result of create_helper
    """
    topic = Topics(name = topic_data.name)
    return create_helper(topic, session)


@app.post("/create-status")
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


@app.post("/add-arbeiter")
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
        raise HTTPException(status_code=400, detail=f"Worker is already assigned!")


@app.post("/create-beispieldaten")
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
    statement = select(ToDo.todo_id)
    result = session.exec(statement).unique().all()
    lasttodo = max(result)
    bearbeiter = Bearbeiter(todo_id = lasttodo, mitarbeiter_id = 1)
    create_helper(bearbeiter, session)

    return {"status":"success"}


##########--Get--##########


@app.get("/todos-by-id")
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


@app.get("/todos-by-topic")
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


@app.get("/mitarbeiter-by-name")
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
    statement = select(Arbeiter).where(Arbeiter.name == name)
    result= session.exec(statement).first()
    if result:
        toretrun = {"mitarbeiter_id": result.mitarbeiter_id, "name": result.name, "lastname": result.lastname, "email": result.email}
        return toretrun
    else:
        raise HTTPException(status_code=404, detail=f"Worker: '{name}' not found")


##########--Put--##########


@app.put("/change-todo")
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


@app.put("/change-arbeiter")
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


@app.put("/change-topic")
def update_topic(new_topic: TopicUpdate, session: SessionDep):
    """
    Update the topic of a todo item.

    Args:
        new_topic: Data containing todo_id and new topic_id
        session: Database session

    Actions:
        1. Find the todo item by its ID
        2. Update the topic_id field to the new value
        3. Verify the new topic exists using Topics table
        4. Return the result from change_helper
    """
    statement = select(ToDo).where(ToDo.todo_id == new_topic.todo_id)
    return change_helper(session, statement, 'topic_id', new_topic.topic_id, True, Topics)


@app.put("/change-status")
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


@app.put("/change-done")
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


##########--Delete--##########


# DANGER: This endpoint allows deleting the entire database
# Commented out for safety reasons
@app.delete("/delete-database")
def delete_database(delete:bool):
     if delete:
         create_database_helper(delete)
         yield create_db_and_tables()
         return {"status": "success"}
     return {"status": "failed"}


# DANGER: This endpoint allows deleting todo items
@app.delete("/delete-todo")
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


@app.delete("/delete-bearbeiter-mitarbeiter")
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