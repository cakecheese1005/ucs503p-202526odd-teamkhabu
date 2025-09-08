import express, { Application, Request, Response } from "express";
import dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";

// Routes
import tripRoutes from "./routes/trips";

dotenv.config();

const app: Application = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan("dev"));
app.use(express.json());

// Health check
app.get("/", (req: Request, res: Response) => {
  res.send("🚀 Backend is running with date-only trips!");
});

// Trip routes (use date-only format: YYYY-MM-DD)
app.use("/api/trips", tripRoutes);

// Server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
