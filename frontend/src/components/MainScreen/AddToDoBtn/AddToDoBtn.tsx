import { getTopicIdByName } from "../../../global";
import { createToDo } from "../../../services/api";
import type { crateToDoInput } from "../../../services/api";
import Select, { StylesConfig } from "react-select";
import makeAnimated from "react-select/animated";
import "./AddToDoBtn.css";
import "uikit";

export default function AddToDoBtn({ currentTopic }: { currentTopic: string }) {
  const animatedComponent = makeAnimated();
  const currentTopicId = getTopicIdByName(currentTopic);
  // const currentAssigneesId = getAssigneesByName();
  console.log("Test: ", currentTopicId);
  const now = new Date();
  const input: crateToDoInput = {
    name: "test",
    description: "tessttt",
    mitarbeiter_id: 2,
  };

  const allTopics = ["Freizeit", "Arbeit", "Schule", "Sport"];
  const assigneesOptions = [
    { value: "Finn", label: "Finn" },
    { value: "Marcel", label: "Marcel" },
    { value: "Jonas", label: "Jonas" },
    { value: "Marcus", label: "Marcus" },
  ];

  type TAssigneesOptions = typeof assigneesOptions;
  const selectStyles: StylesConfig<TAssigneesOptions> = {
    option: () => {
      return { color: "black" };
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
            <h1>create a new To Do: </h1>
            <div id='topic'>
              <h2>To Do Topic:</h2>
              <select name='topics' id='topics'>
                {allTopics.map((topic) => {
                  if (topic === currentTopic) {
                    return (
                      <option value={currentTopic} selected>
                        {currentTopic}
                      </option>
                    );
                  }
                  return <option value={topic}>{topic}</option>;
                })}
              </select>
            </div>
            <div id='name'>
              <h2>To Do Name:</h2>
              <input type='text' />
            </div>
            <div id='description'>
              <h2>To Do Description:</h2>
              <input type='text' />
            </div>
            <div id='assignees'>
              <h2>To Do Assignee/s:</h2>
              <Select
                styles={selectStyles}
                options={assigneesOptions}
                components={animatedComponent}
                isMulti
              />
            </div>
            <button
              type='submit'
              onClick={() => {
                createToDo(input);
              }}
            ></button>
          </form>
        </div>
      </div>
    </div>
  );
}
