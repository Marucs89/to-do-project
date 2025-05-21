import "./TopicTabs.css";
import { getToDoDataForTopic } from "../../../services/api";
import { ToDos } from "../../../schemas/to-do";
import { AllTopics } from "../../../schemas/topics";

export default function TopicTabs({
  setToDoData,
  setTopic,
  allTopics,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDos | undefined>>;
  setTopic: React.Dispatch<React.SetStateAction<AllTopics[0]>>;
  allTopics: AllTopics;
}) {
  return (
    <div id='tabBar'>
      {allTopics.map((topic) => {
        return (
          <button
            className='tabBtn'
            onClick={async () => {
              setTopic(topic);
              const toDoData = await getToDoDataForTopic(topic.name);
              console.log("ToDoData: ", toDoData);
              setToDoData(toDoData);
            }}
          >
            {topic.name}
          </button>
        );
      })}
    </div>
  );
}
