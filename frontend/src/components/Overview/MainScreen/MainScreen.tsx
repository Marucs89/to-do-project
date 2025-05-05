import { useEffect, useState } from "react";
import TopicTabs from "./TopicTabs/TopicTabs";
import { ToDos } from "../../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";
import "./mainscreen.css";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDos>();
  const [noToDos, setNoToDos] = useState<boolean>(false);
  useEffect(() => {
    console.log("ToDOData: ", toDoData);
    console.log("No To Dos: ", noToDos);
  }, [toDoData]);

  return (
    <div id='mainscreen' className='uk-grid uk-child-width-1-4'>
      <div>
        <TopicTabs setToDoData={setToDoData} setNoToDos={setNoToDos} />
      </div>
      {
        <div style={{ paddingLeft: 0 }}>
          <ToDoOverviewBody toDos={toDoData} noToDos={noToDos} />
        </div>
      }
    </div>
  );
}
