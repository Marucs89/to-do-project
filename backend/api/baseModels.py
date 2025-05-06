from pydantic import BaseModel
from datetime import datetime

##########--Anfragen--##########

##########--Get--##########

class CreateToDo(BaseModel):
    name: str
    description: str | None = None
    deadline: datetime | None = None
    topic_id: int | None = None
    status_id: int | None = None
    mitarbeiter_id: list[int] = int
class CreateArbeiter(BaseModel):
    name: str
    lastname: str
    email: str | None = None
class CreateTopicStatus(BaseModel):
    name: str
class AddArbeiter(BaseModel):
    todo_id: int
    mitarbeiter_id: list[int] = int

##########--Put--##########

class ArbeiterUpdate(BaseModel):
    todo_id: int
    mitarbeiter_id: list[int] = int
    new_mitarbeiter_id: list[int] = int
class TopicUpdate(BaseModel):
    todo_id: int
    topic_id: int
class StatusUpdate(BaseModel):
    todo_id: int
    status_id: int
class DoneUpdate(BaseModel):
    todo_id:int
    done: bool

##########--Delete--##########

class DeleteTodo(BaseModel):
    todo_id: int
class DeleteBearbeiterMitarbeiter(BaseModel):
    todo_id:int
    mitarbeiter_id: list[int] = int