import "./TopicTabs.css";
import { getToDoDataForTopic } from "../../../services/api";
import { Topics } from "../MainScreen";
import { ToDos } from "../../../schemas/to-do";

export default function TopicTabs({
  setToDoData,
  setTopic,
}: {
  setToDoData: React.Dispatch<React.SetStateAction<ToDos | undefined>>;
  setTopic: React.Dispatch<React.SetStateAction<string>>;
}) {
  return (
    <div id='tabBar'>
      <button
        className='tabBtn'
        onClick={async () => {
          setTopic(Topics.Freizeit);
          const freizeitToDoData = await getToDoDataForTopic(Topics.Freizeit);
          setToDoData(freizeitToDoData);
        }}
      >
        Freizeit
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          setTopic(Topics.Arbeit);
          const arbeitToDoData = await getToDoDataForTopic(Topics.Arbeit);
          setToDoData(arbeitToDoData);
        }}
      >
        Arbeit
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          setTopic(Topics.Schule);
          const schulToDoData = await getToDoDataForTopic(Topics.Schule);
          setToDoData(schulToDoData);
        }}
      >
        Schule
      </button>
      <button
        className='tabBtn'
        onClick={async () => {
          setTopic(Topics.Sport);
          const sportToDoData = await getToDoDataForTopic(Topics.Sport);
          setToDoData(sportToDoData);
        }}
      >
        Sport
      </button>
    </div>
  );
}
