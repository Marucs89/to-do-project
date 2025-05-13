from fastapi import HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status, Arbeiter


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