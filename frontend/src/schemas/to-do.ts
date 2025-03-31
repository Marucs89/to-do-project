import z from "zod";

export const ToDoSchema = z.object({
  todo_id: z.number(),
  name: z.string(),
  description: z.string().nullish(),
  deadline: z.date().nullish().optional(),
  arbeiter: z
    .object({
      mitarbeiter_id: z.number(),
      name: z.string(),
      lastname: z.string(),
      email: z.string().nullish(),
    })
    .array(),
  topic: z.object({ topic_id: z.number(), name: z.string() }),
  status: z.object({ status_id: z.number(), name: z.string() }),
});

export type ToDo = z.infer<typeof ToDoSchema>;
