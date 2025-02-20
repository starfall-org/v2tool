import { Hono, Context } from "jsr:@hono/hono";
import { eq } from "npm:drizzle-orm";
import { db } from "./lib/db.ts";
import { notes } from "./lib/schema.ts";
import { processes } from "./lib/tool.ts";

const app = new Hono();

app.get("/", (c: Context) => {
  return c.text("V2Tool");
});

app.get("/get/:note", async (c: Context) => {
  const note = c.req.param("note");
  const { uuid, sni, tag } = c.req.query();

  try {
    const content = await db
      .select()
      .from(notes)
      .where(eq(notes.title, note))
      .get();
    if (!content) {
      throw new Error("Note not found");
    }
    const listLinks = content.content.split("\n");
    const links = processes(listLinks, uuid, sni, tag);
    const encodedLinks = btoa(links.join("\n"));
    return new Response(encodedLinks, {
      headers: { "Content-Type": "text/plain" },
    });
  } catch (e) {
    return c.json(
      {
        status: "failed",
        message: e instanceof Error ? e.message : String(e),
      },
      404
    );
  }
});

export default app;
