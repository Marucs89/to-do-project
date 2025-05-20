from sqlmodel import select
from backend.database.tables import ToDo, Topics, Bearbeiter
from backend.models.requests import CreateTopic, TopicUpdate
from backend.services.change_services import change_helper
from backend.services.create_services import create_helper
from typing import Annotated
from backend.database.config import Session, get_session
from fastapi import APIRouter, Depends
from backend.services.delete_services import delete_helper
from sqlalchemy import not_

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/all-topics")
def all_topics(session:SessionDep):
    return session.exec(select(Topics)).unique().all()

@router.post("/create-topic")
def create_topic(topic_data: CreateTopic, session: SessionDep):
    """
    Synchronize topics in the database with the provided list of topic names.

    Args:
        topic_data: Data containing a list of topic names to retain
        session: Database session

    Actions:
        1. Find all topics not in the provided list of names
        2. For each topic to be removed:
           - Find all ToDo items associated with the topic
           - Delete all worker assignments (Bearbeiter) for these ToDos
           - Delete the ToDo items
        3. Delete the topics not in the provided list
        4. Create new topics for any names that don't already exist in the database
        5. Return success status
    """
    # Find all topics that are not in the provided topic list
    topic_statement = select(Topics).where(not_(Topics.name.in_(topic_data.name)))
    topic_result = session.exec(topic_statement).unique().all()

    for y in topic_result:
        todo_statement = select(ToDo).where(ToDo.topic_id == y.topic_id)
        todo_result = session.exec(todo_statement).unique().all()

        for x in todo_result:
            bearbeiter_statement = select(Bearbeiter).where(Bearbeiter.todo_id == x.todo_id)
            delete_helper(bearbeiter_statement, session)

        if todo_result:
            delete_helper(todo_statement, session)

    delete_helper(topic_statement, session)

    # Create the Topics

    statement = select(Topics.name)
    result = session.exec(statement).unique().all()

    existing_names = [topic_name for topic_name in result]

    # Find new names that don't exist in the database
    new_names = [name for name in topic_data.name if name not in existing_names]

    for data in new_names:
        topic = Topics(name = data)
        create_helper(topic, session)
    return {"status: success"}


@router.put("/change-topic")
def update_topic(new_topic: TopicUpdate, session: SessionDep):
    """
    Update the topic of a todo item.

    Args:
        new_topic: Data containing todo_id and new topic_id
        session: Database session

    Actions:
        1. Find the todo item by its ID
        2. Update the topic_id field to the new value
        3. Verify the new topic exists using Topics table
        4. Return the result from change_helper
    """
    statement = select(ToDo).where(ToDo.todo_id == new_topic.todo_id)
    return change_helper(session, statement, 'topic_id', new_topic.topic_id, True, Topics)