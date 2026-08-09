import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { pool } from "./database";

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
  },
  plugins: [jwt()],
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});
