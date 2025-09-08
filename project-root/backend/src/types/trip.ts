export interface Trip {
  id: string;                         // unique ID
  creatorId: string;                  // who created the trip
  start: string;                      // e.g., TIET, Patiala
  destination: string;                // e.g., Chandigarh
  date: string;                       // legacy (can keep for backward compatibility)
  //startDateTime: Date;                // 🆕 full start date + time
  groupSize: number;                  // total seats
  members: string[];                  // joined member IDs
  availableSeats: number;             // seats left
  isGirlsOnly: boolean;               // restrict visibility to female users
  status: "OPEN" | "FULL" | "CANCELLED";

  // 🆕 Intermediate stops like trains
  intermediateStops?: string[];

  // 🆕 Detailed user info (gender required for filtering)
  users: { id: string; gender: "male" | "female" }[];


}

// 👤 User interface (for mutual connections)
export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  contacts: string[]; // list of emails/phones from their contact book
}
