# algo_service.py
from flask import Flask, request, jsonify
from algo import (
    UserGraph,
    load_users,
    load_connections,
    load_groups,
    load_group_members,
    find_matching_groups,
    compute_priority_score
)

app = Flask(__name__)

# --- Load CSVs once at startup ---
graph = UserGraph()
load_users("users.csv", graph)
load_connections("connections.csv", graph)
groups = load_groups("grps.csv")
load_group_members("grp_members.csv", groups)

print("✅ Data loaded successfully from CSVs!")

@app.route("/")
def home():
    return jsonify({"status": "Flask Algo Service Running ✅"})

@app.route("/search-groups", methods=["POST"])
def search_groups():
    try:
        data = request.get_json()
        uid = data["uid"]
        start = data["start"]
        dest = data["dest"]
        pref = data.get("preference", "ALL").upper()
        max_size = int(data.get("max_size", 10))

        if uid not in graph.users:
            return jsonify({"error": "User not found"}), 404

        matches = find_matching_groups(graph, groups, uid, start, dest, max_size, pref)
        if not matches:
            return jsonify({"matches": [], "message": "No matching groups found"}), 200

        scored = []
        for g, seg in matches:
            s = compute_priority_score(g, len(seg), uid, graph)
            scored.append((s, g))
        scored.sort(reverse=True, key=lambda x: x[0])

        output = []
        for _, g in scored:
            output.append({
                "groupId": g.groupId,
                "route": g.full_route(),
                "seats_left": g.seats_left(),
                "capacity": g.capacity,
                "preference": g.preference,
                "members": [
                    {
                        "uid": m,
                        "name": graph.users.get(m, {}).get("name", "Unknown"),
                        "gender": graph.users.get(m, {}).get("gender", "?")
                    } for m in g.members
                ]
            })

        return jsonify({"matches": output}), 200
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
