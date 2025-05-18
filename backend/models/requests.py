from pydantic import BaseModel
from datetime import datetime


##########--Get--##########

class CreateToDo(BaseModel):
    """
    Model to create a new ToDo item.

    Attributes:
        name: Title of the ToDo
        description: Optional detailed explanation of the task
        deadline: Optional due date/time for the task
        topic_id: Optional reference to a topic category
        status_id: Optional reference to current status
        mitarbeiter_id: List of employee IDs assigned to this task
    """
    name: str
    description: str | None = None
    deadline: datetime | None = None
    topic_id: int | None = None
    status_id: int | None = None
    mitarbeiter_id: list[int] = []

class CreateArbeiter(BaseModel):
    """
    Model to create a new employee/worker.

    Attributes:
        name: First name of the employee
    """
    name: list[str]

class CreateTopic(BaseModel):
    """
    Model to create a new topic category.

    Attributes:
        name: a List of Names to add to the topic
    """
    name: list[str]

class CreateStatus(BaseModel):
    """
    Model to create a new status category.

    Attributes:
        name: Name of the status
    """
    name: str

class AddArbeiter(BaseModel):
    """
    Model to assign employees to an existing ToDo.

    Attributes:
        todo_id: ID of the ToDo to assign employees to
        mitarbeiter_id: List of employee IDs to be assigned
    """
    todo_id: int
    mitarbeiter_id: list[int] = []

##########--Put--##########

class TodoUpdate(BaseModel):
    """
    Model to update an existing ToDo item's basic information.

    Attributes:
        todo_id: ID of the ToDo to be updated
        name: Optional new title for the ToDo
        description: Optional new description
        deadline: Optional new deadline
    """
    todo_id: int
    name: str | None = None
    description: str | None = None
    deadline: datetime | None = None

class ArbeiterUpdate(BaseModel):
    """
    Model to update employee assignments for a ToDo.

    Attributes:
        todo_id: ID of the ToDo to update
        mitarbeiter_id: List of current employee IDs to be updated
        new_mitarbeiter_id: List of new employee IDs to assign
    """
    todo_id: int
    mitarbeiter_id: list[int] = []
    new_mitarbeiter_id: list[int] = []

class TopicUpdate(BaseModel):
    """
    Model to change the topic of a ToDo.

    Attributes:
        todo_id: ID of the ToDo to update
        topic_id: ID of the new topic to assign
    """
    todo_id: int
    topic_id: int

class StatusUpdate(BaseModel):
    """
    Model to change the status of a ToDo.

    Attributes:
        todo_id: ID of the ToDo to update
        status_id: ID of the new status to assign
    """
    todo_id: int
    status_id: int

class DoneUpdate(BaseModel):
    """
    Model to mark a ToDo as done or not done.

    Attributes:
        todo_id: ID of the ToDo to update
        done: Boolean indicating completion status
    """
    todo_id:int
    done: bool

##########--Delete--##########

class DeleteTodo(BaseModel):
    """
    Model to delete a ToDo item.

    Attributes:
        todo_id: ID of the ToDo to delete
    """
    todo_id: int

class DeleteBearbeiterMitarbeiter(BaseModel):
    """
    Model to remove employees from a ToDo's assignment list.

    Attributes:
        todo_id: ID of the ToDo to update
        mitarbeiter_id: List of employee IDs to remove from the ToDo
    """
    todo_id:int
    mitarbeiter_id: list[int] = []

class DeleteArbeiter(BaseModel):
    mitarbeiter_id: list[int]