# generate_thapar_dummy_data.py
# Generates realistic dummy CSVs for Thapar RideShare prototype:
# - users.csv (uid,name,gender,email)
# - connections.csv (u1,u2)
# - grps.csv (gid,start,dest,capacity,preference,stops,departure_date,fare)
# - grp_members.csv (gid,uid)
#
# Put this file in your backend folder and run:
#   python generate_thapar_dummy_data.py
#
import random
import csv
import os
from datetime import datetime, timedelta

OUT_DIR = os.path.dirname(__file__) or "."
NUM_USERS = 80
AVG_CONNECTIONS = 4             # average friends per user
NUM_GROUPS = 25
CAPACITY_MIN, CAPACITY_MAX = 3, 6
FEMALE_ONLY_PROB = 0.10
SEED = 42

random.seed(SEED)

# realistic north-indian names for Thapar students
first_m = ["Arjun","Rohit","Karan","Siddharth","Rahul","Vikram","Abhishek","Aman","Manish","Harsh","Rajat","Pranav","Gaurav"]
first_f = ["Ananya","Muskan","Riya","Ishita","Kavya","Simran","Neha","Sanya","Priya","Mitali","Pooja","Tanvi","Mehak"]
last_names = ["Sharma","Verma","Singh","Bansal","Gupta","Kaur","Malhotra","Aggarwal","Chawla","Mehta","Jain"]

# realistic routes / places around Patiala region + NCR
ROUTES = [
    ["Thapar Patiala", "Ambala", "Panipat", "Delhi"],
    ["Thapar Patiala", "Ambala", "Karnal", "Gurgaon"],
    ["Thapar Patiala", "Rajpura", "Ambala", "Yamunanagar"],
    ["Thapar Patiala", "Khanna", "Ludhiana", "Jalandhar", "Amritsar"],
    ["Thapar Patiala", "Barnala", "Bathinda"],
    ["Thapar Patiala", "Rajpura", "Chandigarh"],
    ["Thapar Patiala", "Chandigarh", "Sonipat", "Noida"],
    ["Thapar Patiala", "Ambala", "Panipat", "Faridabad"]
]

def gen_users(n):
    users = []
    for i in range(1, n+1):
        gender = random.choice(["M","F"])
        if gender == "M":
            name = f"{random.choice(first_m)} {random.choice(last_names)}"
        else:
            name = f"{random.choice(first_f)} {random.choice(last_names)}"
        uid = f"U{i:03d}"
        # create a mock college email: u{number}@thapar.edu or name-based
        email = f"{uid.lower()}@thapar.edu"
        users.append({"uid": uid, "name": name, "gender": gender, "email": email})
    return users

def gen_connections(users, avg_deg):
    uid_list = [u["uid"] for u in users]
    edges = set()
    # make a chain to ensure graph connectivity
    for i in range(len(uid_list)-1):
        a, b = uid_list[i], uid_list[i+1]
        edges.add(tuple(sorted((a,b))))
    # add random edges until approx target
    target_edges = int(len(uid_list) * avg_deg / 2)
    while len(edges) < target_edges:
        a, b = random.sample(uid_list, 2)
        if a == b:
            continue
        edges.add(tuple(sorted((a,b))))
    return sorted(list(edges))

def gen_groups(users, num_groups):
    uid_list = [u["uid"] for u in users]
    groups = []
    grp_members = []
    for gi in range(1, num_groups+1):
        gid = f"G{gi:03d}"
        route = random.choice(ROUTES).copy()
        # sometimes shuffle inner stops slightly to vary
        if len(route) > 3 and random.random() < 0.2:
            inner = route[1:-1]
            random.shuffle(inner)
            route = [route[0]] + inner + [route[-1]]
        start = route[0]
        dest = route[-1]
        stops = route[1:-1]
        capacity = random.randint(CAPACITY_MIN, CAPACITY_MAX)
        preference = "FEMALE_ONLY" if random.random() < FEMALE_ONLY_PROB else "ALL"
        # departure_date: random within next 30 days, time between 6:00 and 22:00
        future_days = random.randint(0, 30)
        hour = random.randint(6, 22)
        minute = random.choice([0, 0, 15, 30, 45])
        departure_dt = (datetime.now() + timedelta(days=future_days)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        departure_iso = departure_dt.isoformat()
        # fare approx depending on destination distance (simple heuristic)
        base_fare = 150
        if dest in ["Delhi","Noida","Gurgaon","Faridabad"]:
            fare = base_fare + random.randint(200, 500)
        elif dest in ["Chandigarh","Ludhiana","Amritsar"]:
            fare = base_fare + random.randint(100, 300)
        else:
            fare = base_fare + random.randint(50, 200)
        groups.append({
            "gid": gid,
            "start": start,
            "dest": dest,
            "capacity": capacity,
            "preference": preference,
            "stops": stops,
            "departure_date": departure_iso,
            "fare": fare
        })
        # assign some initial members (up to capacity-1)
        num_members = random.randint(0, max(0, capacity-1))
        members = random.sample(uid_list, num_members)
        for m in members:
            grp_members.append((gid, m))
    return groups, grp_members

def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def main():
    users = gen_users(NUM_USERS)
    edges = gen_connections(users, AVG_CONNECTIONS)
    groups, grp_members = gen_groups(users, NUM_GROUPS)

    users_p = os.path.join(OUT_DIR, "users.csv")
    conn_p = os.path.join(OUT_DIR, "connections.csv")
    grps_p = os.path.join(OUT_DIR, "grps.csv")
    grp_mem_p = os.path.join(OUT_DIR, "grp_members.csv")

    write_csv(users_p, ["uid","name","gender","email"], [(u["uid"], u["name"], u["gender"], u["email"]) for u in users])
    write_csv(conn_p, ["u1","u2"], edges)
    # grps: include stops as pipe-separated string, plus departure_date and fare
    write_csv(grps_p, ["gid","start","dest","capacity","preference","stops","departure_date","fare"],
              [(g["gid"], g["start"], g["dest"], g["capacity"], g["preference"], "|".join(g["stops"]), g["departure_date"], g["fare"]) for g in groups])
    write_csv(grp_mem_p, ["gid","uid"], grp_members)

    print("✅ Dummy data generated in:", OUT_DIR)
    print(f" - users: {len(users)}")
    print(f" - connections (edges): {len(edges)}")
    print(f" - groups: {len(groups)}")
    print(f" - group_members: {len(grp_members)}")

if __name__ == "__main__":
    main()
