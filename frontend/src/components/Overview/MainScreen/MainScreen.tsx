import {useEffect, useState} from "react";
import "./MainScreen.css";
import TopicTabs from "./TopicTabs/TopicTabs";
import OverviewBody from "./OverviewBody/OverviewBody";
import { ToDo } from "../../../schemas/to-do";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDo[]>();
  const [noToDos, setNoToDos] = useState<boolean>(false);
  useEffect(() => {
    console.log("ToDOData: ", toDoData)
  }, [toDoData]);

  return (
    <div id='root'>
      <TopicTabs setToDoData={setToDoData} setNoToDos={setNoToDos} />
      <OverviewBody toDoData={toDoData} />
      {noToDos ? null : null}
    </div>
  );
}
