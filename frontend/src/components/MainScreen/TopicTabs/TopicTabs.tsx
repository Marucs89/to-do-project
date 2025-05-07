import "./TopicTabs.css";
import { getToDoDataForTopic } from "../../../services/api";
import { Topics } from "../MainScreen";
import { ToDos } from "../../../schemas/to-do";

export default function TopicTabs({
  setToDoData,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDos | undefined>>;
}) {
  

  return (
    <div id='tabBar'>
      <button
        className='tabBtn'
        onClick={async () => {
          const freizeitToDoData = await getToDoDataForTopic(Topics.Freizeit);
          setToDoData(freizeitToDoData);
        }}
      >
        Freizeit
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          const arbeitToDoData = await getToDoDataForTopic(Topics.Arbeit);
          setToDoData(arbeitToDoData);
        }}
      >
        Arbeit
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          const schulToDoData = await getToDoDataForTopic(Topics.Schule);
          setToDoData(schulToDoData);
        }}
      >
        Schule
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          const sportToDoData = await getToDoDataForTopic(Topics.Sport);
          setToDoData(sportToDoData);
        }}
      >
        Sport
      </button>
    </div>
  );
}
