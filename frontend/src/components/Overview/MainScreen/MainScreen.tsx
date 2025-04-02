import { useEffect, useState } from "react";
import "./MainScreen.css";
import TopicTabs from "./TopicTabs/TopicTabs";
import { ToDos } from "../../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";

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
  }, [toDoData]);

  return (
    <div className='uk-flex'>
      <div className='uk-position-center-left'>
        <TopicTabs setToDoData={setToDoData} setNoToDos={setNoToDos} />
      </div>
      {noToDos ? null : (
        <div className='uk-position-top-center uk-margin-large-top uk-margin-large-left'>
          <ToDoOverviewBody toDos={toDoData} />
        </div>
      )}
    </div>
  );
}
