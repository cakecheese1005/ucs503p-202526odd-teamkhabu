# algo_service.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import algo
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = "."  # adjust if your CSVs are in different folder
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
GRPS_CSV = os.path.join(DATA_DIR, "grps.csv")
GRP_MEM_CSV = os.path.join(DATA_DIR, "grp_members.csv")
CONNS_CSV = os.path.join(DATA_DIR, "connections.csv")

def load_csvs():
    try:
        users = pd.read_csv(USERS_CSV) if os.path.exists(USERS_CSV) else pd.DataFrame()
        grps = pd.read_csv(GRPS_CSV) if os.path.exists(GRPS_CSV) else pd.DataFrame()
        grp_members = pd.read_csv(GRP_MEM_CSV) if os.path.exists(GRP_MEM_CSV) else pd.DataFrame(columns=["gid","uid"])
        return users, grps, grp_members
    except Exception as e:
        print("⚠️ Could not load CSVs:", e)
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(columns=["gid","uid"])

users_df, groups_df, grp_members_df = load_csvs()

@app.route("/")
def home():
    return jsonify({"message": "🚗 CampusRide Flask API Running on Port 5000!"})

@app.route("/groups", methods=["GET"])
def get_groups():
    try:
        # always reload to pick up external changes
        _, grps, _ = load_csvs()
        return jsonify(grps.fillna("").to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/find_groups", methods=["POST"])
def find_groups():
    """
    Expected JSON:
    {
      "uid": "U001",                   # optional
      "start": "Thapar Patiala",
      "dest": "Delhi",
      "departure_date": "2025-10-12T09:00",   # optional
      "time_window_minutes": 180,
      "max_group_size": 6,
      "pref_input": "ALL"
    }
    """
    try:
        data = request.get_json() or {}
        uid = data.get("uid")
        start = data.get("start", "")
        dest = data.get("dest", "")
        departure_date = data.get("departure_date", None)
        time_window_minutes = data.get("time_window_minutes", 180)
        max_group_size = data.get("max_group_size", None)
        pref_input = data.get("pref_input", "ALL")

        # call algo
        results = algo.find_matching_groups(
            start_input=start,
            dest_input=dest,
            departure_date=departure_date,
            time_window_minutes=int(time_window_minutes) if time_window_minutes else 180,
            max_group_size=int(max_group_size) if max_group_size else None,
            pref_input=pref_input,
            user_id=uid,
            users_csv=USERS_CSV,
            connections_csv=CONNS_CSV,
            grps_csv=GRPS_CSV,
            grp_members_csv=GRP_MEM_CSV,
            top_k=50
        )

        return jsonify({"uid": uid, "recommendations": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/join_group", methods=["POST"])
def join_group():
    try:
        data = request.get_json() or {}
        uid = data.get("uid")
        gid = data.get("gid")
        if not uid or not gid:
            return jsonify({"error": "Missing uid or gid"}), 400

        # reload grp_members
        _, _, grp_members = load_csvs()
        if ((grp_members["uid"] == uid) & (grp_members["gid"] == gid)).any():
            return jsonify({"message": f"User {uid} already in {gid}"}), 200

        new_row = pd.DataFrame([[gid, uid]], columns=["gid", "uid"])
        grp_members = pd.concat([grp_members, new_row], ignore_index=True)
        grp_members.to_csv(GRP_MEM_CSV, index=False)
        return jsonify({"message": f"User {uid} successfully joined {gid}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_group", methods=["POST"])
def create_group():
    """
    Create a new group.
    JSON:
    {
      "creator_uid": "U001",
      "start": "Thapar Patiala",
      "dest": "Delhi",
      "stops": ["Ambala","Panipat"] or "Ambala|Panipat",
      "capacity": 4,
      "preference": "ALL" or "FEMALE_ONLY",
      "departure_date": "2025-10-12T09:00",
      "fare": 250
    }
    """
    try:
        data = request.get_json() or {}
        creator = data.get("creator_uid")
        start = data.get("start", "")
        dest = data.get("dest", "")
        stops = data.get("stops", "")
        if isinstance(stops, list):
            stops_str = "|".join(stops)
        else:
            stops_str = str(stops or "")
        capacity = int(data.get("capacity", 4))
        preference = data.get("preference", "ALL").upper()
        departure_date = data.get("departure_date", None)
        fare = data.get("fare", 0)

        # reload groups
        _, grps, grp_members = load_csvs()
        # generate gid
        existing = set(grps["gid"].astype(str)) if not grps.empty else set()
        next_id = 1
        while f"G{next_id:03d}" in existing:
            next_id += 1
        gid = f"G{next_id:03d}"

        # append new group row
        new_row = {
            "gid": gid,
            "start": start,
            "dest": dest,
            "capacity": capacity,
            "preference": preference,
            "stops": stops_str,
            "departure_date": departure_date,
            "fare": fare
        }
        grps = pd.concat([grps, pd.DataFrame([new_row])], ignore_index=True)
        grps.to_csv(GRPS_CSV, index=False)

        # optionally add creator as member
        if creator:
            grp_members = pd.concat([grp_members, pd.DataFrame([[gid, creator]], columns=["gid", "uid"])], ignore_index=True)
            grp_members.to_csv(GRP_MEM_CSV, index=False)

        return jsonify({"message": "Group created", "gid": gid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
