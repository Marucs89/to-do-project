from sqlmodel import Field, Relationship, Session, SQLModel, create_engine
from datetime import datetime
import pymysql

def create_database_helper(delete:bool):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=''
    )

    # Cursor-Objekt erstellen
    cursor = connection.cursor()

    # Datenbank erstellen, falls sie nicht existiert
    # cursor.execute("DROP DATABASE tododb") # Bestehende Datenbank löschen nur nutzen, wenn neue Attribute hinzugefügt werden
    if delete:
        cursor.execute("DROP DATABASE tododb")
    cursor.execute("CREATE DATABASE IF NOT EXISTS tododb")

    # Verbindung schließen
    cursor.close()
    connection.close()


create_database_helper(delete = False)

# Tabellen erstellen
class ToDo(SQLModel, table=True):
    todo_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=100)
    deadline: datetime | None = Field(default=None)
    # Es gibt in Mariadb kein boolean weswegen der Datentyp in der Tabelle ein tinyint ist, dementsprechend ist 0 = False und 1 = True, der default value ist immer False also muss beim Erstellen des ToDos nicht darüber nachgedacht werden.
    done : bool | None = Field(default=False)
    topic_id: int = Field(default=None, foreign_key='topics.topic_id')
    status_id: int = Field(default=None, foreign_key='status.status_id')
    # Beziehungen zu anderen Tabellen
    bearbeiter_links: list["Bearbeiter"] = Relationship(back_populates="todo", sa_relationship_kwargs={"lazy": "joined"})
    topic: "Topics" = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "joined"}) # bei der abfrage wird immer join genutzt und nicht 4 mal select
    status: "Status" = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "joined"})

class Arbeiter(SQLModel, table=True):
    mitarbeiter_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    email: str | None = Field(max_length=100)
    # Beziehung zu ToDos
    todo_links: list["Bearbeiter"] = Relationship(back_populates="arbeiter")

class Bearbeiter(SQLModel, table=True):
    todo_id: int = Field(foreign_key="todo.todo_id", primary_key=True)
    mitarbeiter_id: int = Field(foreign_key="arbeiter.mitarbeiter_id", primary_key=True)
    # Beziehungen zu ToDo und Arbeiter
    todo: ToDo = Relationship(back_populates="bearbeiter_links")
    arbeiter: Arbeiter = Relationship(back_populates="todo_links")

class Topics (SQLModel, table=True):
    topic_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    # Beziehung zu ToDos
    todos: list["ToDo"] = Relationship(back_populates="topic")

class Status(SQLModel, table=True):
    status_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=100)
    # Beziehung zu ToDos
    todos: list["ToDo"] = Relationship(back_populates="status")

# MariaDB Verbindungs-URL
mariadb_url = f"mariadb+pymysql://root:@localhost:3306/tododb"
engine = create_engine(mariadb_url)

# Funktion zum Erstellen der Tabellen
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # Tabellen neu erstellen

# Funktion zum Erstellen einer SQL-Session
def get_session():
    with Session(engine) as session:
        yield session