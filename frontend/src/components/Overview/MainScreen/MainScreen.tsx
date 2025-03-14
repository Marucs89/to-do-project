import { useState } from "react";
import "./MainScreen.css";
import { getToDoDataForTopic } from "../../../services/api";

enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState();
  const [noToDos, setNoToDos] = useState<boolean>();
  console.log("To Do Data: ", toDoData);
  return (
    <div id='root'>
      <div id='tabBar'>
        <button
          onClick={async () => {
            try {
              const freizeitToDoData = await getToDoDataForTopic(
                Topics.Freizeit
              );
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
    </div>
  );
}
