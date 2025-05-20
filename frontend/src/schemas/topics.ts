import z from "zod";

export const AllTopicsSchema = z
  .object({
    topic_id: z.number(),
    name: z.string(),
  })
  .array();

export type AllTopics = z.infer<typeof AllTopicsSchema>;
