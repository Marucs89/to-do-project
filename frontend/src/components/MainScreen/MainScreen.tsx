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
  const [topic, setTopic] = useState<string>("");

  return (
    <div id='mainscreen'>
      <div id='leftSideArea'>
        <AddToDoBtn currentTopic={topic} />
        <TopicTabs setToDoData={setToDoData} setTopic={setTopic} />
      </div>
      <div id='rightSideArea'>
        <ToDoOverviewBody toDos={toDoData} />
      </div>
    </div>
  );
}
