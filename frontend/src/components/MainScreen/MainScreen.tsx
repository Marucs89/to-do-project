import { useState } from "react";
import TopicTabs from "./TopicTabs/TopicTabs";
import { ToDos } from "../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";
import "./mainscreen.css";
import AddToDoBtn from "./AddToDoBtn/AddToDoBtn";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDos>();

  return (
    <div id='mainscreen' className='uk-grid uk-child-width-1-4'>
      <div id="leftSideArea">
        <AddToDoBtn />
        <TopicTabs setToDoData={setToDoData} />
      </div>
      <div style={{ paddingLeft: 0 }}>
        <ToDoOverviewBody toDos={toDoData} />
      </div>
    </div>
  );
}
