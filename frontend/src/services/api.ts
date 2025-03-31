import axios from "axios";

const localHostURL = "http://localhost:8000";
export async function getToDoDataForTopic(topic: string) {
  const resp = await axios
    .get(`${localHostURL}/todos-by-topic?topic=${topic}`)
    .catch(() => {
      throw new Error("No data for topic found!");
    });
  return resp.data;
}
