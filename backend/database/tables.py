from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# Tabellen erstellen
class ToDo(SQLModel, table=True):
    """
    Represents a task or todo item in the system.

    Attributes:
        todo_id: Primary key for the todo item
        name: Short title of the todo item
        description: Detailed description of the task
        deadline: Due date and time for the task
        done: Boolean flag indicating if the task is completed
        topic_id: Foreign key to the Topics table
        status_id: Foreign key to the Status table
        bearbeiter_links: Relationship to workers assigned to this task
        topic: Relationship to the topic category
        status: Relationship to the task status
    """
    todo_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=100)
    deadline: datetime | None = Field(default=None)
    # In MariaDB, boolean is stored as tinyint (0=False, 1=True)
    done : bool | None = Field(default=False)
    topic_id: int = Field(default=None, foreign_key='topics.topic_id')
    status_id: int = Field(default=None, foreign_key='status.status_id')
    # Relationships to other tables
    bearbeiter_links: list["Bearbeiter"] = Relationship(back_populates="todo", sa_relationship_kwargs={"lazy": "joined"})
    topic: "Topics" = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "joined"})  # Uses join instead of multiple selects
    status: "Status" = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "joined"})

class Arbeiter(SQLModel, table=True):
    """
    Represents an employee/worker who can be assigned to tasks.

    Attributes:
        mitarbeiter_id: Primary key for the worker
        name: First name of the worker
        todo_links: Relationship to tasks assigned to this worker
    """
    mitarbeiter_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    # Relationship to todos
    todo_links: list["Bearbeiter"] = Relationship(back_populates="arbeiter")

class Bearbeiter(SQLModel, table=True):
    """
    Join table that creates many-to-many relationship between ToDo and Arbeiter.
    Represents task assignments to workers.

    Attributes:
        todo_id: Part of composite primary key, foreign key to ToDo
        mitarbeiter_id: Part of composite primary key, foreign key to Arbeiter
        todo: Relationship to the todo item
        arbeiter: Relationship to the worker
    """
    todo_id: int = Field(foreign_key="todo.todo_id", primary_key=True)
    mitarbeiter_id: int = Field(foreign_key="arbeiter.mitarbeiter_id", primary_key=True)
    # Relationships to ToDo and Arbeiter
    todo: ToDo = Relationship(back_populates="bearbeiter_links")
    arbeiter: Arbeiter = Relationship(back_populates="todo_links")

class Topics (SQLModel, table=True):
    """
    Represents categories or topics for todo items.

    Attributes:
        topic_id: Primary key for the topic
        name: Name of the topic category
        todos: Relationship to todo items in this category
    """
    topic_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    # Relationship to todos
    todos: list["ToDo"] = Relationship(back_populates="topic")

class Status(SQLModel, table=True):
    """
    Represents the possible status values for todo items.

    Attributes:
        status_id: Primary key for the status
        name: Name of the status (e.g., "not started", "in progress", "completed")
        todos: Relationship to todo items with this status
    """
    status_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=100)
    # Relationship to todos
    todos: list["ToDo"] = Relationship(back_populates="status")
