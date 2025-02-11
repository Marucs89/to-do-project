from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine
import pymysql
# Tabel erstellen
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    age: int | None = Field(default=None, index=True)
    secret_name: str = Field(max_length=100)

# mariadb definieren
mariadb_url = f"mariadb+pymysql://root:@localhost:3306/herodb"
engine = create_engine(mariadb_url)
# funktion um db und tables zu erstellen
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# sql connection wird etabliert
def get_session():
    with Session(engine) as session:
        yield session