import { getTopicIdByName } from "../../../global";
import { createToDo } from "../../../services/api";
import type { crateToDoInput } from "../../../services/api";
import { Topics } from "../MainScreen";
import "./AddToDoBtn.css";
import "uikit";

export default function AddToDoBtn({ currentTopic }: { currentTopic: string }) {
  const currentTopicId = getTopicIdByName(currentTopic);
  console.log("Test: ", currentTopicId);
  const now = new Date();
  const input: crateToDoInput = {
    name: "test",
    description: "tessttt",
    mitarbeiter_id: 2,
  };

  const allTopics = ["Freizeit", "Arbeit", "Schule", "Sport"];

  return (
    <div>
      <button uk-toggle='target: #offCanvas' id='addToDoBtn'>
        Add To Do
      </button>

      <div id='offCanvas' uk-offcanvas='flip: true'>
        <div className='uk-offcanvas-bar myOffCanvas' id='createToDoDiv'>
          <form id='createToDoForm'>
            <h1>create a new To Do: </h1>
            <div id='name'>
              <h2>To Do Name:</h2>
              <input type='text' />
            </div>
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
