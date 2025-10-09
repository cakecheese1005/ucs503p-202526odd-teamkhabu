// server.js
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const fetch = require("node-fetch");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const FLASK_HOST = process.env.FLASK_HOST || "http://127.0.0.1:5000";
const PORT = process.env.PORT || 4000;

console.log("Using FLASK_HOST =", FLASK_HOST);

app.get("/", (req, res) => {
  res.json({ message: "🚀 CampusRide Node API is up and running!" });
});

app.get("/groups", async (req, res) => {
  try {
    const response = await fetch(`${FLASK_HOST}/groups`);
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Error fetching groups:", err);
    res.status(500).json({ error: "Failed to fetch groups" });
  }
});

app.post("/recommend", async (req, res) => {
  try {
    const payload = req.body;
    const response = await fetch(`${FLASK_HOST}/find_groups`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Error in /recommend:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.post("/join_group", async (req, res) => {
  try {
    const payload = req.body;
    const response = await fetch(`${FLASK_HOST}/join_group`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Error joining group:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.post("/create_group", async (req, res) => {
  try {
    const payload = req.body;
    const response = await fetch(`${FLASK_HOST}/create_group`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Error creating group:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(PORT, () => console.log(`✅ Node server running on port ${PORT}`));
