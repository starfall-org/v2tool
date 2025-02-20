import { drizzle } from "npm:drizzle-orm/libsql";
import { createClient } from "npm:@libsql/client";

const client = createClient({
  url: Deno.env.get("DATABASE_URL"),
  authToken: Deno.env.get("DATABASE_AUTH_TOKEN"),
});

export const db = drizzle(client);
