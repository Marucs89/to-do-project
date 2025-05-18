from sqlmodel import select
from backend.database.tables import ToDo, Topics
from backend.models.requests import CreateTopicStatus, TopicUpdate
from backend.services.change_services import change_helper
from backend.services.create_services import create_helper
from typing import Annotated
from backend.database.config import Session, get_session
from fastapi import APIRouter, Depends

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/create-topic")
def create_topic(topic_data: CreateTopicStatus, session: SessionDep):
    """
    Create a new topic in the database.

    Args:
        topic_data: Data for the new topic (contains name field)
        session: Database session

    Actions:
        1. Create a new topic with the provided name
        2. Save it to the database using create_helper
        3. Return the result of create_helper
    """
    topic = Topics(name = topic_data.name)
    return create_helper(topic, session)


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