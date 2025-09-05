// Existing Trip interface
export interface Trip {
  id: string;
  creatorId: string;
  start: string;
  destination: string;
  date: string;
  groupSize: number;        // total seats
  members: string[];        // joined members (user IDs)
  availableSeats: number;   // left seats
  isGirlsOnly: boolean;
  status: "OPEN" | "FULL" | "CANCELLED";
}

// 👤 New User interface (for mutual connection feature)
export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  contacts: string[]; // list of emails/phones from their contact book
}
