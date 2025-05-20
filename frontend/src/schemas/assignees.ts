import z from "zod";

export const AllAssigneesSchema = z
  .object({
    mitarbeiter_id: z.number(),
    name: z.string(),
  })
  .array();

export type AllAssignees = z.infer<typeof AllAssigneesSchema>;
