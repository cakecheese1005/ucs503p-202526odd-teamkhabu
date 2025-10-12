# algo.py
import csv
from collections import defaultdict, deque

# ------------------- USER GRAPH -------------------
class UserGraph:
    def __init__(self):
        self.users = {}
        self.connections = defaultdict(set)

    def add_user(self, uid, name, gender):
        self.users[uid] = {"name": name, "gender": gender}

    def add_connection(self, u1, u2):
        self.connections[u1].add(u2)
        self.connections[u2].add(u1)

    def get_connections(self, uid, max_depth=3):
        degree_map = {1: set(), 2: set(), 3: set()}
        if uid not in self.users:
            return degree_map
        visited = {uid}
        q = deque([(uid, 0)])
        while q:
            node, depth = q.popleft()
            if depth == max_depth: continue
            for nbr in self.connections[node]:
                if nbr not in visited:
                    visited.add(nbr)
                    q.append((nbr, depth + 1))
                    if 1 <= depth + 1 <= 3:
                        degree_map[depth + 1].add(nbr)
        return degree_map


# ------------------- GROUP CLASS -------------------
class Group:
    def __init__(self, gid, start, dest, stops, capacity, preference="ALL"):
        self.groupId = gid
        self.start = start
        self.dest = dest
        self.stops = stops
        self.capacity = capacity
        self.preference = preference
        self.members = []

    def full(self): return len(self.members) >= self.capacity
    def seats_left(self): return max(0, self.capacity - len(self.members))
    def full_route(self): return [self.start] + self.stops + [self.dest]

    def route_segment_between(self, user_start, user_dest):
        route = self.full_route()
        try:
            i, j = route.index(user_start), route.index(user_dest)
            return route[i:j+1] if i < j else None
        except ValueError:
            return None

    def add_member(self, uid):
        if uid not in self.members:
            self.members.append(uid)


# ------------------- LOAD HELPERS -------------------
def load_users(path, graph):
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 3: continue
            uid, name, gender = row[0].strip(), row[1].strip(), row[2].strip().upper()
            graph.add_user(uid, name, gender)


def load_connections(path, graph):
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 2: continue
            u1, u2 = row[0].strip(), row[1].strip()
            if u1 and u2:
                graph.add_connection(u1, u2)


def load_groups(path):
    groups = {}
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 6: continue
            gid = row[0].strip()
            start = row[1].strip()
            dest = row[2].strip()
            capacity = int(row[3].strip())
            preference = row[4].strip().upper()
            stops = [s.strip() for s in row[5].split("|") if s.strip()]
            groups[gid] = Group(gid, start, dest, stops, capacity, preference)
    return groups


def load_group_members(path, groups):
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 2: continue
            gid, uid = row[0].strip(), row[1].strip()
            if gid in groups:
                groups[gid].add_member(uid)


# ------------------- MATCHING + PRIORITY -------------------
def find_matching_groups(graph, groups, user_id, start_input, dest_input, max_group_size, pref_input):
    matching = []
    for gid, g in groups.items():
        if g.full(): continue
        if g.capacity > max_group_size: continue
        if pref_input == "FEMALE_ONLY" and g.preference != "FEMALE_ONLY": continue
        user_gender = graph.users.get(user_id, {}).get("gender")
        if g.preference == "FEMALE_ONLY" and user_gender != "F": continue
        seg = g.route_segment_between(start_input, dest_input)
        if seg: matching.append((g, seg))
    return matching


def compute_priority_score(group, seg_len, user_id, graph):
    score = 0
    deg_map = graph.get_connections(user_id)
    fill_ratio = len(group.members) / group.capacity if group.capacity else 0
    score += 100 * (1 - abs(0.6 - fill_ratio))
    mutuals = sum(1 for m in group.members if m in deg_map[1])
    score += 300 * min(1, mutuals / 3)
    score += 50 * seg_len
    user = graph.users[user_id]
    if group.preference == "FEMALE_ONLY" and user["gender"] == "F":
        score += 200
    if group.capacity <= 4:
        score += 50
    return score
