import { Router } from "express";
import { trips, users } from "../utils/data";

const router = Router();

// Helper: find user by ID
const findUserById = (userId: string) => users.find((u) => u.id === userId);

// Helper: get mutual connections between user and trip members
const getMutualConnections = (userId: string, memberIds: string[]) => {
  const user = findUserById(userId);
  if (!user) return [];

  // map trip members to phones
  const memberContacts = memberIds
    .map((id) => findUserById(id)?.phone)
    .filter(Boolean) as string[];

  // intersection: user.contacts ∩ memberContacts
  const mutuals = memberContacts.filter((phone) =>
    user.contacts.includes(phone)
  );

  // return mutual user names
  return users
    .filter((u) => mutuals.includes(u.phone))
    .map((u) => u.name);
};

// 🔍 POST /search trips
router.post("/search", (req, res) => {
  const { start, destination, date, seats, girlsOnly, userId } = req.body;

  if (!start || !destination) {
    return res.status(400).json({ error: "Start and destination are required" });
  }

  // Filter trips based on start, destination (including intermediate stops) and status
  let results = trips.filter((t) =>
  t.start.toLowerCase().includes(start.toLowerCase()) &&
  (
    t.destination.toLowerCase().includes(destination.toLowerCase()) ||
    (t.intermediateStops?.some(stop =>
      stop.toLowerCase().includes(destination.toLowerCase())
    ) ?? false)
  ) &&
  t.status === "OPEN"
);


  // 📅 Date filter (optional, ±1 day tolerance)
  if (date) {
    const searchDate = new Date(date);

    results = results.filter((t) => {
      const tripDate = new Date(t.date);
      const diffDays = Math.abs(
        (tripDate.getTime() - searchDate.getTime()) / (1000 * 60 * 60 * 24)
      );
      return diffDays <= 1; // same day or ±1 day
    });
  }

  // 💺 Seats filter (optional)
  if (seats) {
    results = results.filter((t) => t.availableSeats >= seats);
  }

  // 👭 Girls-only filter (optional)
  if (girlsOnly) {
    results = results.filter((t) => t.isGirlsOnly === true);
  }

  // 🤝 Add mutual connections (if userId provided)
  const finalResults = results.map((trip) => {
    if (!userId) return trip; // skip if no logged-in user

    const mutuals = getMutualConnections(userId, trip.members);
    return {
      ...trip,
      mutuals, // e.g. ["Alice", "Bob"]
    };
  });

  res.json(finalResults);
});

export default router;
