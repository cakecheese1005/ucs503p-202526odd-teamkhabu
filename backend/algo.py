# algo.py
# CampusRide Matching Algorithm (enhanced)
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta

def _load_csv_safe(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def _normalize_stops_field(stops_field):
    if isinstance(stops_field, list):
        return stops_field
    if pd.isna(stops_field):
        return []
    s = str(stops_field)
    if "|" in s:
        return [p.strip() for p in s.split("|") if p.strip()]
    if "," in s:
        return [p.strip() for p in s.split(",") if p.strip()]
    return [s] if s.strip() else []

def pandas_isnan(x):
    try:
        return pd.isna(x)
    except Exception:
        return False

def parse_iso_datetime(s):
    """Try to parse ISO datetime or date strings. Return datetime or None."""
    if not s or pandas_isnan(s):
        return None
    s = str(s)
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.fromisoformat(s) if "T" in s else datetime.strptime(s, fmt)
        except Exception:
            continue
    # fallback attempt
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def find_matching_groups(
    start_input=None,
    dest_input=None,
    departure_date=None,       # ISO date/datetime string - match groups on same date (or +/- window)
    time_window_minutes=180,   # tolerance for time matching (minutes)
    max_group_size=None,       # filter by group capacity (<=)
    pref_input="ALL",
    user_id=None,
    users_csv="users.csv",
    connections_csv="connections.csv",
    grps_csv="grps.csv",
    grp_members_csv="grp_members.csv",
    top_k=20
):
    """
    Enhanced matching that considers:
    - start, dest, stops inclusion
    - departure_date/time matching (date or datetime with tolerance)
    - group capacity filter (max_group_size)
    - preference (FEMALE_ONLY / ALL)
    Returns groups with seats_left and mutual_count and match_reasons.
    """
    users_df = _load_csv_safe(users_csv)
    conns_df = _load_csv_safe(connections_csv)
    grps_df = _load_csv_safe(grps_csv)
    grp_mem_df = _load_csv_safe(grp_members_csv)

    start_q = (start_input or "").strip().lower()
    dest_q = (dest_input or "").strip().lower()
    pref_q = (pref_input or "ALL").upper()
    uid = user_id

    # build friends set
    friends = set()
    if not conns_df.empty and uid:
        for _, row in conns_df.iterrows():
            a = str(row.get("u1", "")).strip()
            b = str(row.get("u2", "")).strip()
            if a == uid:
                friends.add(b)
            elif b == uid:
                friends.add(a)

    # build member lists
    members_by_gid = defaultdict(list)
    if not grp_mem_df.empty:
        for _, r in grp_mem_df.iterrows():
            gid = str(r.get("gid", "")).strip()
            mid = str(r.get("uid", "")).strip()
            if gid and mid:
                members_by_gid[gid].append(mid)

    # parse requested departure datetime (if provided)
    req_dt = parse_iso_datetime(departure_date) if departure_date else None

    results = []
    if grps_df.empty:
        return []

    for _, r in grps_df.iterrows():
        gid = str(r.get("gid") or r.get("id") or "").strip()
        start = str(r.get("start") or r.get("source") or "").strip()
        dest = str(r.get("dest") or r.get("destination") or "").strip()
        stops = _normalize_stops_field(r.get("stops") or r.get("route") or "")
        # capacity
        cap_val = r.get("capacity") if "capacity" in r else r.get("group_size") if "group_size" in r else r.get("size", 0)
        try:
            capacity = int(cap_val) if not pandas_isnan(cap_val) else 0
        except Exception:
            capacity = 0

        # departure datetime in group (if exists)
        departure_group_dt = parse_iso_datetime(r.get("departure_date") or r.get("departure") or r.get("date_time"))

        # seats_left calculation
        filled = len(members_by_gid.get(gid, []))
        seats_left = max(0, capacity - filled) if capacity > 0 else 0

        preference = str(r.get("preference") or r.get("pref") or "ALL").upper()

        # FILTERS first: capacity (group_size)
        if max_group_size is not None:
            try:
                if capacity > int(max_group_size):
                    # skip groups larger than requested max size
                    continue
            except Exception:
                pass

        # FILTER: preference mismatch
        if pref_q and pref_q != "ALL" and preference != pref_q:
            # if user's requested preference is FEMALE_ONLY but group is ALL, still show.
            # But if group is FEMALE_ONLY and user doesn't match (user gender unknown), we will penalize later.
            pass

        # FILTER: date/time matching if req_dt provided
        if req_dt and departure_group_dt:
            # same date check OR within time_window_minutes
            same_date = req_dt.date() == departure_group_dt.date()
            within_window = abs((departure_group_dt - req_dt).total_seconds()) <= time_window_minutes * 60
            if not (same_date or within_window):
                # skip if not same date/window
                continue

        # compute score and match reasons
        score = 0.0
        reasons = []

        if start_q and start and start_q == start.lower():
            score += 40
            reasons.append("exact_start")
        if dest_q and dest and dest_q == dest.lower():
            score += 40
            reasons.append("exact_dest")

        route_all = [start] + stops + ([dest] if dest else [])
        route_all_lower = [s.lower() for s in route_all if s]
        if start_q and start_q in route_all_lower and "exact_start" not in reasons:
            score += 15
            reasons.append("start_in_route")
        if dest_q and dest_q in route_all_lower and "exact_dest" not in reasons:
            score += 15
            reasons.append("dest_in_route")

        # Date/time proximity increases score
        if req_dt and departure_group_dt:
            diff_minutes = abs((departure_group_dt - req_dt).total_seconds()) / 60
            # closer times get higher bonus
            time_bonus = max(0, (time_window_minutes - diff_minutes) / max(1, time_window_minutes) * 20)
            score += time_bonus
            reasons.append("time_proximity")

        # preference
        if preference == "FEMALE_ONLY":
            # if user provided gender and not female, heavy penalty
            if hasattr(uid, "strip") and uid and uid:  # uid exists, but gender unknown here
                # we'll not exclude automatically unless user gender is provided elsewhere
                score -= 10
                reasons.append("female_only_group")
            else:
                reasons.append("female_only_group")

        # seats left bonus
        score += min(10, seats_left * 2)
        if seats_left > 0:
            reasons.append("seats_available")

        # mutual friends
        mutual = 0
        if uid:
            mutual = sum(1 for m in members_by_gid.get(gid, []) if m in friends)
            score += mutual * 8
            if mutual > 0:
                reasons.append(f"mutual_{mutual}")

        results.append({
            "gid": gid,
            "start": start,
            "dest": dest,
            "stops": stops,
            "departure_date": departure_group_dt.isoformat() if departure_group_dt else None,
            "capacity": capacity,
            "seats_left": seats_left,
            "preference": preference,
            "members": members_by_gid.get(gid, []),
            "mutual_count": mutual,
            "score": round(score, 2),
            "match_reasons": reasons
        })

    # sort and return top_k
    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
    return results_sorted[:top_k]


# quick CLI test
if __name__ == "__main__":
    import json
    out = find_matching_groups(start_input="Thapar Patiala", dest_input="Delhi", departure_date=None, user_id="U001")
    print(json.dumps(out, indent=2))
