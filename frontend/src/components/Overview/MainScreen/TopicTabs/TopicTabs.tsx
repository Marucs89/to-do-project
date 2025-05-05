import "./TopicTabs.css";
import { getToDoDataForTopic } from "../../../../services/api";
import { Topics } from "../MainScreen";
import { ToDos } from "../../../../schemas/to-do";

export default function TopicTabs({
  setToDoData,
  setNoToDos,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDos | undefined>>;
  setNoToDos: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  return (
    <div id='tabBar'>
      <button
        onClick={async () => {
          try {
            const freizeitToDoData = await getToDoDataForTopic(Topics.Freizeit);
            setToDoData(freizeitToDoData);
            setNoToDos(false);
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
          try {
            const arbeitToDoData = await getToDoDataForTopic(Topics.Arbeit);
            setToDoData(arbeitToDoData);
            setNoToDos(false);
          } catch (err: unknown) {
            if (err === "No data for topic found!") {
              setNoToDos(true);
            }
            console.log("ERROR: ", err);
          }
        }}
      >
        Arbeit
      </button>
      <button
        onClick={async () => {
          try {
            const schulToDoData = await getToDoDataForTopic(Topics.Schule);
            setToDoData(schulToDoData);
            setNoToDos(false);
          } catch (err: unknown) {
            if (err === "No data for topic found!") {
              setNoToDos(true);
            }
          }
        }}
      >
        Schule
      </button>
      <button
        onClick={async () => {
          try {
            const sportToDoData = await getToDoDataForTopic(Topics.Sport);
            setToDoData(sportToDoData);
            setNoToDos(false);
          } catch (err: unknown) {
            if (err === "No data for topic found!") {
              setNoToDos(true);
            }
            console.log("ERROR: ", err);
          }
        }}
      >
        Sport
      </button>
    </div>
  );
}
