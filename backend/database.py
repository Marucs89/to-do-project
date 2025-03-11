from sqlmodel import Field, Relationship, Session, SQLModel, create_engine
from datetime import datetime

# Tabellen erstellen
class Teams(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    headquarters: str = Field(max_length=100)
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    age: int | None = Field(default=None, index=True)
    secret_name: str = Field(max_length=100)
    team_id: int | None = Field(default=None, foreign_key="teams.id")
    team: Teams | None = Relationship(back_populates="heroes")

class ToDo(SQLModel, table=True):
    todo_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=100)
    deadline: datetime | None = Field(default=None)
    topic_id: int | None = Field(default=None, foreign_key='topics.topic_id')
    # Ein kann mehrere Bearbeiter-Einträge haben
    bearbeiter_links: list["Bearbeiter"] = Relationship(back_populates="todo")
    # Ein gehört zu einem Topic
    topic_links: list["Topics"] = Relationship(back_populates="todos_links")

class Arbeiter(SQLModel, table=True):
    mitarbeiter_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    contact: str | None = Field(max_length=100)
    # Ein Arbeiter kann mehreren Bearbeiter-Einträgen zugeordnet sein
    todo_links: list["Bearbeiter"] = Relationship(back_populates="arbeiter")

class Bearbeiter(SQLModel, table=True):
    # Zusammengesetzter Primärschlüssel, der auf die richtigen IDs verweist
    todo_id: int = Field(foreign_key="todo.todo_id", primary_key=True)
    mitarbeiter_id: int = Field(foreign_key="arbeiter.mitarbeiter_id", primary_key=True)
    # Jeder Bearbeiter-Eintrag gehört zu einem ToDo und einem Arbeiter
    todo: ToDo = Relationship(back_populates="bearbeiter_links")
    arbeiter: Arbeiter = Relationship(back_populates="todo_links")

class Topics (SQLModel, table=True):
    topic_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    todos_links: list["ToDo"] = Relationship(back_populates="topic_links")

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