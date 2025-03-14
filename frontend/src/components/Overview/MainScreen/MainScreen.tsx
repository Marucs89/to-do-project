import { useState } from "react";
import "./MainScreen.css";
import { getToDoDataForTopic } from "../../../services/api";
import TopicTabs from "./TopicTabs/TopicTabs";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  //TODO: Data Schema definieren
  const [toDoData, setToDoData] = useState();
  const [noToDos, setNoToDos] = useState(false);
  console.log("To Do Data: ", toDoData);
  return (
    <div id='root'>
      <TopicTabs setToDoData={setToDoData} setNoToDos={setNoToDos} />
      
    </div>
  );
}
