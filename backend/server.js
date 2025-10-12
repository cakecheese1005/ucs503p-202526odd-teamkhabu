// server.js
import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ status: "Node Server Running ✅" });
});

app.post("/join-trip", async (req, res) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/search-groups", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Error connecting to Flask backend:", err);
    res.status(500).json({ error: "Flask service unavailable" });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 Node server running on port ${PORT}`));
