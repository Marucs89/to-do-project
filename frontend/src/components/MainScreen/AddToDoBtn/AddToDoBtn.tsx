import Select from "react-select";
import "./AddToDoBtn.css";
import "uikit";
import { useState } from "react";
import { addWeeks, previousSunday } from "date-fns";
import { AllTopics } from "../../../schemas/topics";
import { AllAssignees } from "../../../schemas/assignees";
import {
  assigneesSelectStyles,
  topicsSelectStyles,
  animatedComponent,
} from "./selectConfig";
import { crateToDoInput, createToDo } from "../../../services/api";

export default function AddToDoBtn({
  allTopics,
  allAssignees,
}: {
  allTopics: AllTopics | undefined;
  allAssignees: AllAssignees | undefined;
}) {
  const [toDoTopic, setToDoTopic] = useState<
    | {
        label: string;
        value: number;
      }
    | undefined
  >();
  const [toDoName, setToDoName] = useState("");
  const [toDoDescription, setToDoDescription] = useState("");
  const [toDoDeadline, setToDoDeadline] = useState<string | undefined>();
  const [toDoAssignees, setToDoAssignees] =
    useState<{ value: number; label: string }[]>();
  const now = new Date();
  const minDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(
    2,
    "0"
  )}-${String(now.getDate()).padStart(2, "0")}`;
  const maxDateObject = addWeeks(previousSunday(now), 4);
  const maxDate = `${maxDateObject.getFullYear()}-${String(
    maxDateObject.getMonth() + 1
  ).padStart(2, "0")}-${String(maxDateObject.getDate()).padStart(2, "0")}`;

  const assigneesOptions = allAssignees?.map((assignee) => {
    return { value: assignee.mitarbeiter_id, label: assignee.name };
  });

  const topicOptions = allTopics?.map((topic) => {
    return { value: topic.topic_id, label: topic.name };
  });

  return (
    <div>
      <button uk-toggle='target: #offCanvas' id='addToDoBtn'>
        Add To Do
      </button>

      <div id='offCanvas' uk-offcanvas='flip: true'>
        <div className='uk-offcanvas-bar myOffCanvas' id='createToDoDiv'>
          <form id='createToDoForm'>
            <h1>Create To Do: </h1>
            <div id='topic'>
              <h2 className='headline'>Topic:</h2>
              <Select
                styles={topicsSelectStyles}
                //@ts-expect-error Bullshits
                options={topicOptions}
                components={animatedComponent}
                onChange={(topic) => {
                  //@ts-expect-error bullshit
                  setToDoTopic(topic);
                }}
              />
            </div>
            <div id='name'>
              <h2 className='headline'>Name:</h2>
              <input
                type='text'
                id='nameInput'
                placeholder='add a Name'
                onChange={({ target: { value: name } }) => {
                  setToDoName(name);
                }}
              />
            </div>
            <div id='description'>
              <h2 className='headline'>Description:</h2>
              <textarea
                id='descriptionInput'
                placeholder='add a description'
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
                min={minDate}
                max={maxDate}
                onChange={({ target: { value: deadline } }) => {
                  setToDoDeadline(deadline);
                }}
              />
            </div>
            <div id='assignees'>
              <h2>Assignee/s:</h2>
              <Select
                styles={assigneesSelectStyles}
                //@ts-expect-error Bullshit
                options={assigneesOptions}
                components={animatedComponent}
                isMulti
                onChange={(assignees) => {
                  //@ts-expect-error Bullshit
                  setToDoAssignees(assignees);
                }}
              />
            </div>
            <div id='submit'>
              <button
                id='submitBtn'
                className='submitBtn'
                onClick={async () => {
                  if (!toDoTopic?.value) {
                    throw new Error("No Topic id is set!!!");
                  }
                  if (!toDoDeadline) {
                    throw new Error("No Deadine is set!!!");
                  }
                  if (!toDoAssignees) {
                    throw new Error("No Assignee/s is/are set!!!");
                  }
                  const assignees = toDoAssignees.map((assignee) => {
                    return assignee.value;
                  });

                  const input: crateToDoInput = {
                    topic_id: toDoTopic?.value,
                    name: toDoName,
                    description: toDoDescription,
                    deadline: toDoDeadline,
                    mitarbeiter_id: assignees,
                    status_id: 1, //open status
                  };
                  await createToDo(input);
                }}
              >
                Create To Do
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
