import axios from "axios";
import { ToDoSchema } from "../schemas/to-do";
import { AllTopicsSchema } from "../schemas/topics";
import { AllAssigneesSchema } from "../schemas/assignees";

const localHostURL = "http://localhost:8000";

export interface crateToDoInput {
  name: string;
  description: string;
  topic_id: number;
  status_id: number;
  mitarbeiter_id: number[];
  deadline: string;
}

export type updateToDoInput = Omit<crateToDoInput, "mitarbeiter_id"> & {
  todo_id: number;
};

export type changeArbeiterInput = {
  todo_id: number;
  mitarbeiter_id: number[];
  new_mitarbeiter_id: number[];
};

export type deleteToDoInput = number;

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
  const resp = await axios
    .get(`${localHostURL}/all-topics`)
    .catch((error: unknown) => {
      console.log("Error: ", error);
    });
  console.log("All topics: ", resp?.data);
  return resp?.data ? AllTopicsSchema.parse(resp?.data) : [];
}

export async function getAllAssignees() {
  const resp = await axios
    .get(`${localHostURL}/all-arbeiter`)
    .catch((error: unknown) => {
      console.log("Error: ", error);
    });
  console.log("All assignees: ", resp?.data);
  return resp?.data ? AllAssigneesSchema.parse(resp?.data) : [];
}

export async function updateToDo(input: updateToDoInput) {
  let successful = true;
  await axios
    .put(`${localHostURL}/change-todo`, input)
    .catch((error: unknown) => {
      console.log("Error: ", error);
      successful = false;
    });
  return { successful };
}

export async function updateToDoAssignees(input: changeArbeiterInput) {
  let successful = true;
  await axios
    .put(`${localHostURL}/change-arbeiter`, input)
    .catch((error: unknown) => {
      console.log("Error: ", error);
      successful = false;
    });
  return { successful };
}

export async function deleteToDo(todo_id: deleteToDoInput) {
  let successful = true;
  await axios
    .delete(`${localHostURL}/delete-todo?todo_id=${todo_id}`)
    .catch((error: unknown) => {
      console.log("Error: ", error);
      successful = false;
    });
  return { successful };
}
