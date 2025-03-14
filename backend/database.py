from sqlmodel import Field, Relationship, Session, SQLModel, create_engine
from datetime import datetime

# Tabellen erstellen
class ToDo(SQLModel, table=True):
    todo_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=100)
    deadline: datetime | None = Field(default=None)
    topic_id: int = Field(default=None, foreign_key='topics.topic_id')
    status_id: int = Field(default=None, foreign_key='status.status_id')
    # Beziehungen
    bearbeiter_links: list["Bearbeiter"] = Relationship(back_populates="todo")
    topic: "Topics" = Relationship(back_populates="todos")
    status: "Status" = Relationship(back_populates="todos")

class Arbeiter(SQLModel, table=True):
    mitarbeiter_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    email: str | None = Field(max_length=100)
    todo_links: list["Bearbeiter"] = Relationship(back_populates="arbeiter")

class Bearbeiter(SQLModel, table=True):
    todo_id: int = Field(foreign_key="todo.todo_id", primary_key=True)
    mitarbeiter_id: int = Field(foreign_key="arbeiter.mitarbeiter_id", primary_key=True)
    todo: ToDo = Relationship(back_populates="bearbeiter_links")
    arbeiter: Arbeiter = Relationship(back_populates="todo_links")

class Topics (SQLModel, table=True):
    topic_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    todos: list["ToDo"] = Relationship(back_populates="topic")

class Status(SQLModel, table=True):
    status_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=100)
    todos: list["ToDo"] = Relationship(back_populates="status")

#mariadb_url = f"mariadb+pymysql://if0_38298610:ToDoProjekt2025@sql300.infinityfree.com/if0_38298610_todoprojekt"
mariadb_url = f"mariadb+pymysql://root:@localhost:3306/herodb"
engine = create_engine(mariadb_url)

# funktion tables zu erstellen / laden
def create_db_and_tables():
#    SQLModel.metadata.drop_all(engine)  # Bestehende Tabellen löschen nur nutzen wenn neue Attribute hinzugefügt werden
    SQLModel.metadata.create_all(engine)  # Tabellen neu erstellen

# sql connection wird etabliert
def get_session():
    with Session(engine) as session:
        yield session