from fastapi import HTTPException
from sqlmodel import select
from backend.database.tables import ToDo, Topics, Status, Arbeiter
from backend.api.requests import CreateToDo


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