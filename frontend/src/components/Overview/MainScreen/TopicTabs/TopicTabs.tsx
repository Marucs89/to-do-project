import "./TopicTabs.css";
import { getToDoDataForTopic } from "../../../../services/api";
import { Topics } from "../MainScreen";
import { ToDo } from "../../../../schemas/to-do";
import { useEffect } from "react";

export default function TopicTabs({
  setToDoData,
  setNoToDos,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDo[] | undefined>>;
  setNoToDos: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  return (
    <div id='tabBar'>
      <button
        onClick={async () => {
          try {
            const freizeitToDoData = await getToDoDataForTopic(Topics.Freizeit);
            setToDoData(freizeitToDoData);
          } catch (err: unknown) {
            if (err === "No data for topic found!") {
              setNoToDos(true);
            }
            console.log("ERROR: ", err);
          }
        }}
      >
        Freizeit
      </button>
      <button
        onClick={async () => {
          const arbeitToDoData = await getToDoDataForTopic(Topics.Arbeit);
          setToDoData(arbeitToDoData);
        }}
      >
        Arbeit
      </button>
      <button
        onClick={async () => {
          const schuleToDoData = await getToDoDataForTopic(Topics.Schule);
          setToDoData(schuleToDoData);
        }}
      >
        Schule
      </button>
      <button
        onClick={async () => {
          const sportToDoData = await getToDoDataForTopic(Topics.Sport);
          setToDoData(sportToDoData);
        }}
      >
        Sport
      </button>
    </div>
  );
}
