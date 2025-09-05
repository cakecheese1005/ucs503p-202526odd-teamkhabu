const express = require("express");
const cors = require("cors");
const pool = require("./db");

const app = express();
app.use(cors());
app.use(express.json());

// Health check
app.get("/", (req, res) => {
  res.send("🚀 RideShare Backend Running!");
});

// Example: Get all users
app.get("/users", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM users");
    res.json(result.rows);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// Example: Add user
app.post("/users", async (req, res) => {
  try {
    const { name, email, year, roll_no } = req.body;
    const result = await pool.query(
      "INSERT INTO users (name, email, year, roll_no) VALUES ($1, $2, $3, $4) RETURNING *",
      [name, email, year, roll_no]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});

