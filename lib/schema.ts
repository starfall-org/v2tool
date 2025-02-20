import { sqliteTable, text } from "npm:drizzle-orm/sqlite-core";
import { integer } from "npm:drizzle-orm/sqlite-core";

export const notes = sqliteTable("notes", {
  title: text("title").primaryKey(),
  auth_id: integer("auth_id", { mode: "number" }).notNull(),
  urls: text("urls").notNull(),
  content: text("content").notNull(),
});

export type Note = typeof notes.$inferSelect;
export type InsertNote = typeof notes.$inferInsert;
