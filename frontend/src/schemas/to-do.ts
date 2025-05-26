import z from "zod";

export const ToDoSchema = z
  .object({
    todo_id: z.number(),
    name: z.string(),
    description: z.string(),
    deadline: z.string(),
    arbeiter: z
      .object({
        mitarbeiter_id: z.number(),
        name: z.string(),
      })
      .array(),
    topic: z.object({ topic_id: z.number(), name: z.string() }),
    status: z.object({ status_id: z.number(), name: z.string() }),
  })
  .array();

export type ToDos = z.infer<typeof ToDoSchema>;
