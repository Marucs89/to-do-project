from sqlmodel import Session, SQLModel, create_engine
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