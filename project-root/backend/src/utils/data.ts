import { Trip, User } from "../types/trip";

// 🚗 Trips Dataset
export const trips: Trip[] = [
  {
    id: "1",
    creatorId: "u1",
    start: "Thapar",
    destination: "Meerut",
    date: "2025-09-07",
    groupSize: 3,
    members: ["u1"],
    availableSeats: 2,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "2",
    creatorId: "u2",
    start: "Delhi",
    destination: "Chandigarh",
    date: "2025-09-08",
    groupSize: 2,
    members: ["u2", "u3"],
    availableSeats: 0,
    isGirlsOnly: true,
    status: "FULL"
  },
  {
    id: "3",
    creatorId: "u3",
    start: "Thapar",
    destination: "Delhi",
    date: "2025-09-07",
    groupSize: 4,
    members: ["u3", "u4"],
    availableSeats: 2,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "4",
    creatorId: "u4",
    start: "Thapar",
    destination: "Amritsar",
    date: "2025-09-09",
    groupSize: 3,
    members: ["u4"],
    availableSeats: 2,
    isGirlsOnly: true,
    status: "OPEN"
  },
  {
    id: "5",
    creatorId: "u5",
    start: "Patiala",
    destination: "Ludhiana",
    date: "2025-09-07",
    groupSize: 2,
    members: ["u5"],
    availableSeats: 1,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "6",
    creatorId: "u6",
    start: "Thapar",
    destination: "Shimla",
    date: "2025-09-10",
    groupSize: 5,
    members: ["u6", "u7", "u8"],
    availableSeats: 2,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "7",
    creatorId: "u7",
    start: "Thapar",
    destination: "Jaipur",
    date: "2025-09-07",
    groupSize: 4,
    members: ["u7"],
    availableSeats: 3,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "8",
    creatorId: "u8",
    start: "Delhi",
    destination: "Meerut",
    date: "2025-09-08",
    groupSize: 3,
    members: ["u8", "u9"],
    availableSeats: 1,
    isGirlsOnly: true,
    status: "OPEN"
  },
  {
    id: "9",
    creatorId: "u9",
    start: "Chandigarh",
    destination: "Patiala",
    date: "2025-09-09",
    groupSize: 2,
    members: ["u9"],
    availableSeats: 1,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "10",
    creatorId: "u10",
    start: "Thapar",
    destination: "Delhi",
    date: "2025-09-08",
    groupSize: 5,
    members: ["u10", "u11"],
    availableSeats: 3,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "11",
    creatorId: "u11",
    start: "Patiala",
    destination: "Amritsar",
    date: "2025-09-07",
    groupSize: 3,
    members: ["u11", "u12"],
    availableSeats: 1,
    isGirlsOnly: true,
    status: "OPEN"
  },
  {
    id: "12",
    creatorId: "u12",
    start: "Delhi",
    destination: "Shimla",
    date: "2025-09-10",
    groupSize: 4,
    members: ["u12"],
    availableSeats: 3,
    isGirlsOnly: false,
    status: "OPEN"
  },
  {
    id: "13",
    creatorId: "u13",
    start: "Thapar",
    destination: "Ludhiana",
    date: "2025-09-07",
    groupSize: 2,
    members: ["u13", "u14"],
    availableSeats: 0,
    isGirlsOnly: false,
    status: "FULL"
  },
  {
    id: "14",
    creatorId: "u14",
    start: "Jaipur",
    destination: "Delhi",
    date: "2025-09-08",
    groupSize: 3,
    members: ["u14"],
    availableSeats: 2,
    isGirlsOnly: true,
    status: "OPEN"
  },
  {
    id: "15",
    creatorId: "u15",
    start: "Thapar",
    destination: "Chandigarh",
    date: "2025-09-07",
    groupSize: 6,
    members: ["u15", "u16", "u17"],
    availableSeats: 3,
    isGirlsOnly: false,
    status: "OPEN"
  }
];

// 👥 Users Dataset (for mutual connection)
export const users: User[] = [
  {
    id: "u1",
    name: "Alice",
    email: "alice@thapar.edu",
    phone: "1111",
    contacts: ["2222", "3333"] // knows Bob & Charlie
  },
  {
    id: "u2",
    name: "Bob",
    email: "bob@thapar.edu",
    phone: "2222",
    contacts: ["1111"] // knows Alice
  },
  {
    id: "u3",
    name: "Charlie",
    email: "charlie@thapar.edu",
    phone: "3333",
    contacts: ["1111"] // knows Alice
  },
  {
    id: "u4",
    name: "David",
    email: "david@thapar.edu",
    phone: "4444",
    contacts: ["2222"] // knows Bob
  },
  {
    id: "u5",
    name: "Eva",
    email: "eva@thapar.edu",
    phone: "5555",
    contacts: ["3333"] // knows Charlie
  }
];
