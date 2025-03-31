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
  useEffect(() => {
    setToDoData([
      {
        todo_id: 1,
        name: "Buy milk",
        description: null,
        arbeiter: [{ mitarbeiter_id: 1, name: "Müller", lastname: "Hans" }],
        topic: { topic_id: 1, name: "Sport" },
        status: { status_id: 1, name: "offen" },
      },
      {
        todo_id: 2,
        name: "test22",
        description: "tets_2",
        arbeiter: [{ mitarbeiter_id: 2, name: "Franz", lastname: "Hans" }],
        topic: { topic_id: 1, name: "Sport" },
        status: {
          status_id: 1,
          name: "offen",
        },
      },
    ]);
  });
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
