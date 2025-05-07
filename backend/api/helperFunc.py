from fastapi import HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status, Arbeiter
from backend.api.baseModels import CreateToDo

##########--Anfragen--##########

###########--Post--##########

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

##########--Get--##########

def read_todo_helper(read_todo:list):
    """
    Convert ToDo objects to a formatted dictionary structure for API responses.

    Parameters:
        read_todo: List of ToDo objects with their related entities

    Returns:
        List of dictionaries containing formatted ToDo data with related information
    """
    result = []
    for todo in read_todo:
        # Extract topic information from a related topic entity
        topic_info = {"topic_id": todo.topic.topic_id, "name": todo.topic.name}

        # Extract status information from a related status entity
        status_info = {"status_id": todo.status.status_id, "name": todo.status.name}

        # Create list of all workers (Arbeiter) associated with this ToDo
        arbeiter_liste = [
            {
                "mitarbeiter_id": link.arbeiter.mitarbeiter_id,
                "name": link.arbeiter.name,
                "lastname": link.arbeiter.lastname,
                "email": link.arbeiter.email
            }
            for link in todo.bearbeiter_links  # Process each link in the many-to-many relationship
        ]

        # Build complete ToDo dictionary with all related information
        todo_dict = {
            "todo_id": todo.todo_id,
            "name": todo.name,
            "description": todo.description,
            "deadline": todo.deadline,
            "done": todo.done,
            "arbeiter": arbeiter_liste,  # Include all associated workers
            "topic": topic_info,         # Include topic information
            "status": status_info        # Include status information
        }
        result.append(todo_dict)
    return result

##########--Put--##########

def change_helper(session, statement, field_name, new_value, test=False, table=None):
    """
    Helper function to update a field in a database record

    Parameters:
        session: Database session
        statement: SELECT query to find the record to update
        field_name: Name of the field/attribute to update
        new_value: Value to set the field to
        test: If True, validate that the new_value exists in the referenced table
        table: Referenced table class to check for value existence

    Returns:
        Dict with a status message on success

    Raises:
        HTTPException: If a record is not found or referenced value doesn't exist
    """
    # Execute the query to find the record(s) to update
    results = session.exec(statement).unique().all()
    if not results:
        raise HTTPException(status_code=404, detail=f"'{field_name}' nicht in liste gefunden")

    # Get the first record from results for updating
    attribute = results[0]

    # If a test flag is set, validate that the new value exists in the specified table
    if test and table:
        # Determine the primary key field name based on the table class
        if table == Arbeiter:
            id_field = "mitarbeiter_id"
        elif table == Topics:
            id_field = "topic_id"
        elif table == Status:
            id_field = "status_id"
        elif table == ToDo:
            id_field = "todo_id"
        else:
            id_field = "id"  # Default ID field name

        # Check if the new value exists in the referenced table
        check_statement = select(table).where(getattr(table, id_field) == new_value)
        existing_item = session.exec(check_statement).first()
        if not existing_item:
            raise HTTPException(status_code=400,
                            detail=f"{field_name}={new_value} existiert nicht in '{table.__name__}'")

    # Update the field with the new value
    setattr(attribute, field_name, new_value)

    # Save changes to the database
    session.add(attribute)
    session.commit()
    session.refresh(attribute)
    return {"status": "success"}

##########--Delete--##########

def delete_helper(statement, session):
    """
    Helper function to delete records based on a SQL query statement.

    Parameters:
        statement: SELECT query to find the record(s) to delete
        session: Database session for executing queries

    Raises:
        HTTPException 404: If no records are found to delete
        HTTPException 400: If any error occurs during a deletion process
    """
    try:
        result = session.exec(statement).unique()
        todelete = result.first()
        if not todelete:
            raise HTTPException(status_code=404, detail=f"Es wurde kein eintrag in der tabelle gefunden")
        session.delete(todelete)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Fehler beim löschen Fehler:'{e}'")