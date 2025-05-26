import { useEffect } from "react";
import { ToDos } from "../../../schemas/to-do";
import { AllTopics } from "../../../schemas/topics";
import { getToDoDataForTopic } from "../../../services/api";
import "./TopicTabs.css";

export default function TopicTabs({
  setToDoData,
  allTopics,
  topic,
  setTopic,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDos | undefined>>;
  allTopics: AllTopics | undefined;
  topic: AllTopics[0] | undefined;
  setTopic: React.Dispatch<
    React.SetStateAction<
      | {
          name: string;
          topic_id: number;
        }
      | undefined
    >
  >;
}) {
  useEffect(() => {
    if (!allTopics) return;
    setTopic(allTopics[0]);
    const initActiveTabBtn = document.getElementById(
      "topic-tab-" + String(allTopics[0].topic_id)
    );
    initActiveTabBtn?.classList.add("active");
    initActiveTabBtn?.click();
  }, [allTopics]);

  return (
    <div id='tabBar'>
      {allTopics?.map((currentTopic) => {
        return (
          <button
            className='tabBtn'
            id={"topic-tab-" + String(currentTopic.topic_id)}
            key={"topic-tab-" + String(currentTopic.topic_id)}
            onClick={async () => {
              const toDoData = await getToDoDataForTopic(currentTopic.name);
              const prevTabBtn = document.getElementById(
                "topic-tab-" + String(topic?.topic_id ?? "")
              );
              const currentTabBtn = document.getElementById(
                "topic-tab-" + String(currentTopic.topic_id)
              );
              prevTabBtn?.classList.remove("active");
              currentTabBtn?.classList.add("active");
              setTopic(currentTopic);
              setToDoData(toDoData);
            }}
          >
            {currentTopic.name}
          </button>
        );
      })}
    </div>
  );
}
