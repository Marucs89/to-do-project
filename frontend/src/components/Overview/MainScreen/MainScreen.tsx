import { useState } from "react";
import "./MainScreen.css";
import TopicTabs from "./TopicTabs/TopicTabs";
import OverviewBody from "./OverviewBody/OverviewBody";
import { ToDo } from "../../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDo[]>();
  const [noToDos, setNoToDos] = useState<boolean>(false);

  return (
    <div id='root'>
      <TopicTabs setToDoData={setToDoData} setNoToDos={setNoToDos} />
      <ToDoOverviewBody></ToDoOverviewBody>
      <OverviewBody toDoData={toDoData} />
      {noToDos ? null : null}
    </div>
  );
}
