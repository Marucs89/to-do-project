import { getTopicIdByName } from "../../../global";
import { createToDo } from "../../../services/api";
import type { crateToDoInput } from "../../../services/api";
import Select, { StylesConfig } from "react-select";
import makeAnimated from "react-select/animated";
import "./AddToDoBtn.css";
import "uikit";
import { useState } from "react";
import { addWeeks, previousSunday } from "date-fns";

export default function AddToDoBtn({ currentTopic }: { currentTopic: string }) {
  const animatedComponent = makeAnimated();

  // const currentAssigneesId = getAssigneesByName();
  const [toDoDate, setToDoDate] = useState<string | undefined>();
  const now = new Date();

  const minDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(
    2,
    "0"
  )}-${String(now.getDate()).padStart(2, "0")}`;
  const maxDateObject = addWeeks(previousSunday(now), 4);
  const maxDate = `${maxDateObject.getFullYear()}-${String(
    maxDateObject.getMonth() + 1
  ).padStart(2, "0")}-${String(maxDateObject.getDate()).padStart(2, "0")}`;

  const input: crateToDoInput = {
    name: "test",
    description: "tessttt",
    mitarbeiter_id: 2,
  };

  let currentTopicIndex = 0;

  const allTopics = ["Freizeit", "Arbeit", "Schule", "Sport"];
  const assigneesOptions = [
    { value: "Finn", label: "Finn" },
    { value: "Marcel", label: "Marcel" },
    { value: "Jonas", label: "Jonas" },
    { value: "Marcus", label: "Marcus" },
  ];

  type TAssigneesOptions = typeof assigneesOptions;
  const assigneesSelectStyles: StylesConfig<TAssigneesOptions> = {
    control: (styles) => {
      return {
        ...styles,
        width: "250px",
        ":hover": { cursor: "pointer" },
      };
    },
    option: (styles) => {
      return {
        ...styles,
        color: "black",
        cursor: "pointer",
        justifySelf: "center",
      };
    },
  };

  const topicOptions = allTopics.map((topic, i) => {
    if (topic === currentTopic) currentTopicIndex = i;
    return { value: topic, label: topic };
  });

  type TTopicOptiones = typeof topicOptions;

  const topicsSelectStyles: StylesConfig<TTopicOptiones> = {
    control: (styles) => {
      return { ...styles, width: "11rem", ":hover": { cursor: "pointer" } };
    },
    option: (styles) => {
      return {
        ...styles,
        color: "black",
        cursor: "pointer",
        justifySelf: "center",
      };
    },
  };

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
                //@ts-expect-error Bullshit
                styles={topicsSelectStyles}
                options={topicOptions}
                components={animatedComponent}
                defaultValue={topicOptions[currentTopicIndex]}
                onChange={(event) => {
                  console.log("event: ", event);
                  const currentTopicId = getTopicIdByName(currentTopic);
                }}
              />
            </div>
            <div id='name'>
              <h2 className='headline'>Name:</h2>
              <input type='text' id='nameInput' placeholder='add an Name' />
            </div>
            <div id='description'>
              <h2 className='headline'>Description:</h2>
              <textarea
                id='descriptionInput'
                placeholder='add an description'
              ></textarea>
            </div>
            <div id='date'>
              <h2 className='headline'>Date</h2>

              <input
                type='date'
                id='dateInput'
                min={minDate}
                max={maxDate}
                onChange={({ target: { value } }) => {
                  console.log("date: ", value);
                  setToDoDate(value);
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
              />
            </div>
            <div id='submit'>
              <button
                id='submitBtn'
                className='submitBtn'
                type='submit'
                onClick={() => {
                  createToDo(input);
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
