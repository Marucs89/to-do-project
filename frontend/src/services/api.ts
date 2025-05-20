import axios from "axios";
import { ToDoSchema } from "../schemas/to-do";

const localHostURL = "http://localhost:8000";

export interface crateToDoInput {
  name: string;
  description: string;
  topic_id: number;
  status_id: number;
  mitarbeiter_id: number[];
  deadline: string;
}

export async function getToDoDataForTopic(topic: string) {
  const resp = await axios
    .get(`${localHostURL}/todos-by-topic?topic=${topic}`)
    .catch((error: unknown) => {
      console.log("Error: ", error);
    });
  console.log("Raw Data: ", resp?.data);
  console.log("data: ", resp?.data);
  return resp?.data ? ToDoSchema.parse(resp?.data) : [];
}

export async function createToDo(input: crateToDoInput) {
  let successful = true;
  await axios
    .post(`${localHostURL}/create-todo`, input)
    .catch((error: unknown) => {
      console.log("Error: ", error);
      successful = false;
    });
  return { successful };
}

//TODO: get all topics
export async function getAllTopics() {
  return;
}

export async function getAllUsers() {
  return;
}
