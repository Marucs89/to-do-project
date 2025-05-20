def read_todo_helper(read_todo:list):
    """
    Convert ToDo objects to a formatted dictionary structure for API responses.

    Parameters:
        read_todo: List of ToDo objects with their related entities

    Returns:
        List of dictionaries containing formatted ToDo data with related information
    """
    result = []
    for todo in read_todo:
        # Extract topic information from a related topic entity
        topic_info = {"topic_id": todo.topic.topic_id, "name": todo.topic.name}

        # Extract status information from a related status entity
        status_info = {"status_id": todo.status.status_id, "name": todo.status.name}

        # Create list of all workers (Arbeiter) associated with this ToDo
        arbeiter_liste = [
            {
                "mitarbeiter_id": link.arbeiter.mitarbeiter_id,
                "name": link.arbeiter.name
            }
            for link in todo.bearbeiter_links  # Process each link in the many-to-many relationship
        ]

        # Build complete ToDo dictionary with all related information
        todo_dict = {
            "todo_id": todo.todo_id,
            "name": todo.name,
            "description": todo.description,
            "deadline": todo.deadline,
            "done": todo.done,
            "arbeiter": arbeiter_liste,  # Include all associated workers
            "topic": topic_info,         # Include topic information
            "status": status_info        # Include status information
        }
        result.append(todo_dict)
    return result