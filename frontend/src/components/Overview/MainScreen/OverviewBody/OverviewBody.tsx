import "./OverviewBody.css";
import { ToDo } from "../../../../schemas/to-do";

export enum Topics {
  Freizeit = "Freizeit",
  Arbeit = "Arbeit",
  Schule = "Schule",
  Sport = "Sport",
}

export default function OverviewBody({ toDoData }: { toDoData: ToDo[] | undefined }) {
  console.log("To Do Data: ", toDoData);
  return <div id='overviewBody'>
    
  </div>;
}
