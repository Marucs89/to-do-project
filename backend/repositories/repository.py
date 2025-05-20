from sqlmodel import select
from backend.database.tables import ToDo, Topics, Bearbeiter, Arbeiter
from backend.models.requests import DeleteBearbeiterMitarbeiter, AddArbeiter


class TodoRepository:
    """
    Repository class for handling ToDo items in the database.
    """
    def get_by_id(self, todoid: int):
        """
        Retrieve a ToDo item by its ID.

        Parameters:
            todoid: The ID of the ToDo item to retrieve

        Returns:
            List of ToDo items matching the ID
        """
        statement = select(ToDo).where(ToDo.todo_id == todoid)
        result = self.exec(statement)
        return result.unique().all()

    def get_by_topic(self, topicName: str):
        """
        Find a topic ID by its name.

        Parameters:
            topicName: The name of the topic to search for

        Returns:
            The topic ID if found, otherwise None
        """
        statement = select(Topics.topic_id).where(Topics.name == topicName)
        result = self.exec(statement)
        return result.first()

    def get_by_topicid(self, topicid: int):
        statement = select(Topics.topic_id).where(Topics.topic_id == topicid)
        result = self.exec(statement)
        return result.first()

    def get_todo_by_topicid(self, topic_id: int):
        statement = select(ToDo).where(ToDo.topic_id == topic_id)
        result = self.exec(statement)
        return result.unique().all()
    

class BearbeiterRepository():
    """
    Repository class for managing worker assignments to ToDo items.
    """
    def delete_mitarbeiter(self, to_delete: DeleteBearbeiterMitarbeiter):
        """
        Get all worker assignments for a specific ToDo that should be deleted.

        Parameters:
            to_delete: Object containing the ToDo ID and worker IDs to remove

        Returns:
            List of worker assignments for the ToDo
        """
        statement = select(Bearbeiter).where(Bearbeiter.todo_id == to_delete.todo_id)
        result: list = self.exec(statement)
        return result.unique().all()


class ArbeiterRepository():
    """
    Repository class for managing workers/employees.
    """
    def get_mitarbeiter(self, mitarbeiterName: str):
        """
        Find a worker by their name.

        Parameters:
            mitarbeiterName: The name of the worker to search for

        Returns:
            The worker object if found, otherwise None
        """
        statement = select(Arbeiter).where(Arbeiter.name == mitarbeiterName)
        result = self.exec(statement)
        return result.first()

    def post_mitarbeiter(self, mitarbeiterData: AddArbeiter):
        """
        Find worker assignments for a ToDo that don't include a specific worker.

        Parameters:
            mitarbeiterData: Object containing ToDo ID and worker ID to check

        Returns:
            Query result of worker assignments
        """
        statement = select(Bearbeiter).where(
            Bearbeiter.todo_id == mitarbeiterData.todo_id,
            Bearbeiter.mitarbeiter_id != mitarbeiterData.mitarbeiter_id
        )
        result = self.exec(statement)
        return result

    def get_mitarbeiter_id(self):
        """
        Get the highest worker ID in the database.

        Returns:
            String representation of the maximum worker ID
        """
        statemen = select(Arbeiter.mitarbeiter_id)
        result = self.exec(statemen)
        return str(max(result))


class MiscRepository():
    """
    Repository class for miscellaneous database operations.
    """
    def get_todoid(self):
        """
        Get all ToDo IDs from the database.

        Returns:
            List of all ToDo IDs
        """
        statement = select(ToDo.todo_id)
        result = self.exec(statement)
        return result.unique().all()