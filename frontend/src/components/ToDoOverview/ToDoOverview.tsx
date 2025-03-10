import { useState } from "react";
import "./ToDoOverview.css";

enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function ToDoOverview() {
  const [topic, setTopic] = useState<Topics>();
  return (
    <div id='root'>
      <div id='tabBar'>
        <button
          onClick={() => {
            setTopic(Topics.Freizeit);
          }}
        >
          Freizeit
        </button>
        <button
          onClick={() => {
            setTopic(Topics.Arbeit);
          }}
        >
          Arbeit
        </button>
        <button
          onClick={() => {
            setTopic(Topics.Schule);
          }}
        >
          Schule
        </button>
        <button
          onClick={() => {
            setTopic(Topics.Sport);
          }}
        >
          Sport
        </button>
      </div>
    </div>
  );
}
