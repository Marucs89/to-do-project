from sqlmodel import select
from backend.database.tables import ToDo


class TodoRepository:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id: int):
        statement = select(ToDo).where(ToDo.todo_id == id)
        result = self.exec(statement)
        return result.unique().all()