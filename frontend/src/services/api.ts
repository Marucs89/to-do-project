import axios from "axios";
import { ToDoSchema } from "../schemas/to-do";

const localHostURL = "http://localhost:8000";
export async function getToDoDataForTopic(topic: string) {
  const resp = await axios
    .get(`${localHostURL}/todos-by-topic?topic=${topic}`)
    .catch((error: unknown) => {
      console.log("Error: ", error);
      throw new Error("No data for topic found!");
    });
  console.log("Raw Data: ", resp.data);
  return ToDoSchema.parse(resp.data);
}
