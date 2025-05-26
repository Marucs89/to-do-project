import { useEffect, useState } from "react";
import TopicTabs from "./TopicTabs/TopicTabs";
import { ToDos } from "../../schemas/to-do";
import ToDoOverviewBody from "./OverviewBody/ToDoOverviewBody/ToDoOverviewBody";
import "./mainscreen.css";
import AddToDoBtn from "./AddToDoBtn/AddToDoBtn";
import { AllTopics } from "../../schemas/topics";
import { AllAssignees } from "../../schemas/assignees";
import { getAllAssignees, getAllTopics } from "../../services/api";

export default function MainScreen() {
  const [toDoData, setToDoData] = useState<ToDos>();
  const [allTopics, setAllTopics] = useState<AllTopics>();
  const [topic, setTopic] = useState<AllTopics[0]>();
  const [allAssignees, setAllAssignees] = useState<AllAssignees>();
  useEffect(() => {
    const fetchTopics = async () => {
      setAllTopics(await getAllTopics());
    };
    const fetchAssignees = async () => {
      setAllAssignees(await getAllAssignees());
    };
    fetchTopics();
    fetchAssignees();
  }, []);

  return (
    <div id='mainscreen'>
      <div id='leftSideArea'>
        <AddToDoBtn allTopics={allTopics} allAssignees={allAssignees} />
        <TopicTabs
          setToDoData={setToDoData}
          allTopics={allTopics}
          topic={topic}
          setTopic={setTopic}
        />
      </div>
      <div id='rightSideArea'>
        <ToDoOverviewBody
          toDos={toDoData}
          allTopics={allTopics}
          allAssignees={allAssignees}
        />
      </div>
    </div>
  );
}
