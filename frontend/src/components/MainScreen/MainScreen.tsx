import { useState } from "react";
import TopicTabs from "./TopicTabs/TopicTabs";
import { ToDos } from "../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";
import "./mainscreen.css";
import AddToDoBtn from "./AddToDoBtn/AddToDoBtn";
import { AllTopics } from "../../schemas/topics";
import { AllAssignees } from "../../schemas/assignees";

//after implementation of datafetching of topics => deprecated
export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDos>();
  const [topic, setTopic] = useState<AllTopics[0]>({
    name: "Freizeit",
    topic_id: 1,
  });

  //TODO: fetch all Mitarbeiter and Topic and store dem in a usestate + delete default useState value
  const [allTopics, setAllTopics] = useState<AllTopics>([
    { topic_id: 1, name: "Freizeit" },
    { topic_id: 2, name: "Arbeit" },
    { topic_id: 3, name: "Schule" },
    { topic_id: 4, name: "Sport" },
  ]);

  const [allAssignees, setAllAssignees] = useState<AllAssignees>([
    { mitarbeiter_id: 1, name: "Marcus" },
    { mitarbeiter_id: 2, name: "Marcel" },
    { mitarbeiter_id: 3, name: "Finn" },
    { mitarbeiter_id: 4, name: "Jonas" },
  ]);

  return (
    <div id='mainscreen'>
      <div id='leftSideArea'>
        <AddToDoBtn allTopics={allTopics} allAssignees={allAssignees} />
        <TopicTabs
          setToDoData={setToDoData}
          setTopic={setTopic}
          allTopics={allTopics}
        />
      </div>
      <div id='rightSideArea'>
        <ToDoOverviewBody toDos={toDoData} />
      </div>
    </div>
  );
}
