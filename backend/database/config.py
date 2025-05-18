from sqlmodel import Session, SQLModel, create_engine
import pymysql

def create_database_helper(delete:bool):
    """
    Creates or resets the database based on the delete parameter.

    Args:
        delete: Boolean flag - if True, drops an existing database before creating a new one
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=''
    )

    # Create cursor object to execute SQL commands
    cursor = connection.cursor()

    # Database operations
    # If delete=True, drop the existing database
    if delete:
        cursor.execute("DROP DATABASE tododb")
    # Create a database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS tododb")

    # Close connections
    cursor.close()
    connection.close()


# Initialize a database on a module load (without deleting existing data)
create_database_helper(delete = False)

# Configure MariaDB connection URL
mariadb_url = f"mariadb+pymysql://root:@localhost:3306/tododb"
engine = create_engine(mariadb_url)

def create_db_and_tables():
    """
    Creates all tables defined in SQLModel metadata.
    Uses the database schema definitions from the model classes.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Creates and yields a database session.
    Used as a dependency in FastAPI endpoints.
    Session is automatically closed after use.
    """
    with Session(engine) as session:
        yield session