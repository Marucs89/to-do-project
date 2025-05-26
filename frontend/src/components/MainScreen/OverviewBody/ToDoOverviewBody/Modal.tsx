import { useEffect, useState } from "react";
import Select from "react-select";
import { status_ids } from "../../../../global";
import { AllAssignees } from "../../../../schemas/assignees";
import { ToDos } from "../../../../schemas/to-do";
import { AllTopics } from "../../../../schemas/topics";
import {
  deleteToDo,
  updateToDo,
  updateToDoInput,
} from "../../../../services/api";
import {
  animatedComponent,
  assigneesSelectStyles,
} from "../../AddToDoBtn/selectConfig";
import "./ToDoOverviewBody.css";

export default function Modal({
  toDo,
  allTopics,
  allAssignees,
}: {
  toDo: ToDos[0];
  allTopics: AllTopics | undefined;
  allAssignees: AllAssignees | undefined;
}) {
  const [toDoTopic, setToDoTopic] = useState<{
    name: string;
    topic_id: number;
  }>(toDo.topic);
  const currentDeadlineDate = new Date(toDo.deadline);
  const formattedToDoDeadline = `${currentDeadlineDate.getFullYear()}-${String(
    currentDeadlineDate.getMonth() + 1
  ).padStart(2, "0")}-${String(currentDeadlineDate.getDate()).padStart(
    2,
    "0"
  )}`;

  const [toDoDeadline, setToDoDeadline] = useState<string>(
    formattedToDoDeadline
  );
  const [toDoName, setToDoName] = useState(toDo.name);

  const [toDoDescription, setToDoDescription] = useState(toDo.description);

  const [toDoAssignees, setToDoAssignees] = useState(
    toDo.arbeiter.map((assignee) => {
      return { label: assignee.name, value: assignee.mitarbeiter_id };
    })
  );

  const [toDoStatus, setToDoStatus] = useState(toDo.status);

  useEffect(() => {
    setToDoName(toDo.name);
    setToDoAssignees(
      toDo.arbeiter.map((assignee) => ({
        label: assignee.name,
        value: assignee.mitarbeiter_id,
      }))
    );
    setToDoDeadline(formattedToDoDeadline);
    setToDoDescription(toDo.description);
    setToDoTopic(toDo.topic);
    setToDoStatus(toDo.status);
  }, [toDo.todo_id]);

  const now = new Date();
  const currentDate = `${now.getFullYear()}-${String(
    now.getMonth() + 1
  ).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;

  const assigneesOptions = allAssignees?.map((assignee) => {
    return { value: assignee.mitarbeiter_id, label: assignee.name };
  });

  const handleClose = () => {
    setToDoName(toDo.name);
    setToDoAssignees(
      toDo.arbeiter.map((assignee) => ({
        label: assignee.name,
        value: assignee.mitarbeiter_id,
      }))
    );
    setToDoDeadline(formattedToDoDeadline);
    setToDoDescription(toDo.description);
    setToDoTopic(toDo.topic);
    setToDoStatus(toDo.status);
    const modalDialog = document.getElementById(
      `modal-${toDo.todo_id}`
    ) as HTMLDialogElement;
    modalDialog.close();
  };

  const handleDelete = async () => {
    await deleteToDo(toDo.todo_id);
    const modalDialog = document.getElementById(
      `modal-${toDo.todo_id}`
    ) as HTMLDialogElement;
    modalDialog.close();
    const topicTabElement = document.getElementById(
      "topic-tab-" + String(toDo.topic.topic_id)
    );
    topicTabElement?.click();
  };

  return (
    <dialog id={`modal-${toDo.todo_id}`} className='modalDialog'>
      <div id='modalCloseBtnForm'>
        <button id='modalCloseBtn' onClick={handleClose}>
          X
        </button>
      </div>
      <div id='modalContent'>
        <div id='name'>
          <h2 className='headline'>Name:</h2>
          <input
            type='text'
            id='nameInput'
            style={{ width: "50%" }}
            placeholder={toDo.name}
            value={toDoName}
            onChange={({ target: { value: name } }) => {
              setToDoName(name);
            }}
          />
        </div>
        <div id='topic'>
          <h2 className='headline'>Topic:</h2>
          <select
            id='topicSelect'
            value={toDoTopic.name}
            onChange={(event) => {
              setToDoTopic(() => {
                return (
                  allTopics?.find((topic) => {
                    return topic.name === event.target.value;
                  }) ?? { name: "", topic_id: 1 }
                );
              });
            }}
          >
            {allTopics
              ?.map((topic) => {
                if (topic.topic_id === toDo.topic.topic_id)
                  return <option>{topic.name}</option>;
              })
              .concat(
                allTopics?.map((topic) => {
                  if (topic.topic_id === toDo.topic.topic_id) return;
                  return <option>{topic.name}</option>;
                })
              )}
          </select>
        </div>

        <div id='description'>
          <h2 className='headline'>Description:</h2>
          <textarea
            placeholder={toDoDescription}
            value={toDoDescription}
            style={{
              width: "55%",
              height: "4rem",
              padding: "3%",
              fontFamily: "arial",
              resize: "none",
            }}
            onChange={({ target: { value: description } }) => {
              setToDoDescription(description);
            }}
          ></textarea>
        </div>
        <div id='date'>
          <h2 className='headline'>Deadline</h2>
          <input
            type='date'
            id='dateInput'
            value={toDoDeadline}
            min={currentDate}
            defaultValue={toDoDeadline}
            style={{ height: "1.5rem", width: "39%" }}
            onChange={({ target: { value: deadline } }) => {
              setToDoDeadline(deadline);
            }}
          />
        </div>
        <div id='assigneesAndStatus'>
          <div id='assignees'>
            <h2
              className='headline'
              style={{ marginBottom: "4%", fontSize: "28px" }}
            >
              Assignee/s:
            </h2>
            <Select
              isMulti
              //@ts-expect-error Bullshit
              styles={assigneesSelectStyles}
              options={assigneesOptions}
              value={toDoAssignees}
              components={animatedComponent}
              defaultValue={toDoAssignees}
              onChange={(assignees) => {
                //@ts-expect-error Bullshit
                toDoAssignees = assignees;
                // setToDoAssignees(assignee s);
              }}
            ></Select>
          </div>
          <div id='status'>
            <h2 className='headline' style={{ marginBottom: "6%" }}>
              Status
            </h2>
            <select
              id='statusSelect'
              value={toDoStatus.name}
              onChange={(event) => {
                setToDoStatus(() => {
                  return (
                    status_ids?.find((status) => {
                      return status.name === event.target.value;
                    }) ?? { name: "", status_id: 1 }
                  );
                });
              }}
            >
              {status_ids
                .map((status) => {
                  if (status.status_id === toDo.status.status_id)
                    return <option>{status.name}</option>;
                })
                .concat(
                  status_ids.map((status) => {
                    if (status.status_id === toDo.status.status_id) return;
                    return <option>{status.name}</option>;
                  })
                )}
            </select>
          </div>
        </div>
        <div id='submitAndDelete' style={{ width: "100%" }}>
          <div id='submit' style={{ width: "100%" }}>
            <button
              id='submitBtn'
              className='submitBtn'
              onClick={async () => {
                //TODO: handle assignees change!
                // const assignees = toDoAssignees.map((assignee) => {
                //   return assignee.value;
                // });

                const toDoinput: updateToDoInput = {
                  todo_id: toDo.todo_id,
                  topic_id: toDoTopic.topic_id,
                  name: toDoName,
                  description: toDoDescription,
                  deadline: toDoDeadline,
                  status_id: toDoStatus.status_id,
                };
                await updateToDo(toDoinput);

                const modalDialog = document.getElementById(
                  `modal-${toDo.todo_id}`
                ) as HTMLDialogElement;

                const topicTabElement = document.getElementById(
                  "topic-tab-" + String(toDo.topic.topic_id)
                );

                modalDialog.close();
                topicTabElement?.click();
              }}
            >
              Update To Do
            </button>
          </div>
          <div id='delete' style={{ width: "90%", marginBottom: "7%" }}>
            <button id='deleteBtn' className='submitBtn' onClick={handleDelete}>
              Delete
            </button>
          </div>
        </div>
      </div>
    </dialog>
  );
}
