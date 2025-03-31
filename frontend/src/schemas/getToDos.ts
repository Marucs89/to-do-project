import z from "zod";

export const GetToDosSchema = z.object({
  todo_id: z.number(),
  name: z.string(),
  description: z.string().nullish(),
  deadline: z.date().nullish(),
  arbeiter: z
    .object({
      mitarbeiter_id: z.number(),
      name: z.string(),
      lastname: z.string(),
      email: z.string(),
    })
    .array(),
  topic: z.object({ topic_id: z.number(), name: z.string() }),
  status: z.object({ status_id: z.number(), name: z.string() }),
});

export type GetToDos = z.infer<typeof GetToDosSchema>;
