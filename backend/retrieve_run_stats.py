import json
from pathlib import Path
from itertools import combinations

def locate_folder():
    base = Path.home() / "AppData" / "Roaming" / "SlayTheSpire2" / "steam"

    latest_time = -1
    latest_profile = None
    player_id = None

    for account in base.iterdir():
        if not account.is_dir():
            continue

        for profile in account.iterdir():
            if not profile.is_dir():
                continue

            # check all files inside profile
            save_file = profile / "saves" / "progress.save"

            if save_file.exists():
                mtime = save_file.stat().st_mtime

                if mtime > latest_time:
                    latest_time = mtime
                    latest_profile = profile
                    player_id = account.name

    if latest_profile is None:
        return None, None

    return latest_profile / "saves" / "history", player_id

def analyze_relics(stats, relics_data, win): # retrieve relics data
    for relic in relics_data:
        rid = relic["id"].replace("RELIC.", "")

        if rid in {
            "BURNING_BLOOD", "RING_OF_THE_SNAKE", "CRACKED_CORE", "DIVINE_RIGHT", "BOUND_PHYLACTERY"
        }:
            continue # skip character starter relics

        entry = stats["relics"].setdefault(rid, {
            "acquired": 0,
            "wins": 0,
            "times_picked": 0,
            "times_skipped": 0,
        })

        entry["acquired"] += 1
        if win:
            entry["wins"] += 1

def analyze_starter_relics(stats, starter_data, win): # retrieve starter relic data
    for floor in starter_data:
        for encounter in floor:
            if encounter["map_point_type"] == "ancient":
                if "ancient_choice" in encounter["player_stats"][0]:
                    for starter in encounter["player_stats"][0]["ancient_choice"]:
                        rid = starter["TextKey"]

                        entry = stats["relics"].setdefault(rid, {
                            "acquired": 0,
                            "wins": 0,
                            "times_picked": 0,
                            "times_skipped": 0,
                        })

                        if encounter["player_stats"][0]["relic_choices"][0]["choice"].replace("RELIC.", "") == rid:
                            entry["times_picked"] += 1
                            if win:
                                entry["wins"] += 1
                        else:
                            entry["times_skipped"] += 1

def analyze_encounters(stats, encounters_data): # retrieve encounter data
    for floor in encounters_data:
        for encounter in floor:
            if encounter["map_point_type"] in {"monster", "elite", "boss"}:
                eid = encounter["rooms"][0]["model_id"].replace("ENCOUNTER.", "")
                entry = stats["encounters"].setdefault(eid, {
                    "battles": 0,
                    "wins": 0,
                    "total_hp_lost": 0,
                })

                entry["battles"] += 1
                entry["total_hp_lost"] += encounter["player_stats"][0]["damage_taken"]
                if encounter["player_stats"][0]["current_hp"] != 0:
                    entry["wins"] += 1
                
def analyze_cards(stats, cards_data, win): # retrieve card synergy data
    STARTER_CARDS = { # list of starter cards
        "STRIKE_IRONCLAD", "STRIKE_SILENT", "STRIKE_REGENT", "STRIKE_NECROBINDER", "STRIKE_DEFECT",
        "DEFEND_IRONCLAD", "DEFEND_SILENT", "DEFEND_REGENT", "DEFEND_NECROBINDER", "DEFEND_DEFECT",
        "BASH", "SURVIVOR", "NEUTRALIZE", "VENERATE", "FALLING_STAR", "BODYGUARD", "UNLEASH", "DUALCAST", "ZAP",
    }
    deck = { # remove starter cards from synergy list
        card["id"].replace("CARD.", "")
        for card in cards_data
        if card["id"].replace("CARD.", "") not in STARTER_CARDS
    }

    for c1, c2, in combinations(deck, 2):
        synergy = stats.setdefault("cards", {})

        entry1 = synergy.setdefault(c1, {}).setdefault(c2, {"games": 0, "wins": 0})
        entry2 = synergy.setdefault(c2, {}).setdefault(c1, {"games": 0, "wins": 0})

        entry1["games"] += 1
        entry2["games"] += 1

        if win:
            entry1["wins"] += 1
            entry2["wins"] += 1

def analyze_runs(folder, player_id):
    folder = Path(folder)
    stats = {
        "summary": {
            "total_runs": 0,
            "wins": 0,
            "playtime": 0,
            "killed": {},
            "characters": {
                "IRONCLAD": {
                    "total_runs": 0,
                    "wins": 0,
                },
                "SILENT": {
                    "total_runs": 0,
                    "wins": 0,
                },
                "REGENT": {
                    "total_runs": 0,
                    "wins": 0,
                },
                "NECROBINDER": {
                    "total_runs": 0,
                    "wins": 0,
                },
                "DEFECT": {
                    "total_runs": 0,
                    "wins": 0,
                },
            },
        },

        "cards": {},       # synergies
        "relics": {},      # obtained, wins
        "encounters": {}   # fought, wins, total HP loss
    }

    for run in folder.iterdir():
        if run.suffix != ".run": # ignore backup files
            continue

        with open(run, "r") as f:
            print(run)
            data = json.load(f)

        player_idx = 0 # default index for singleplayer runs
        filtered_map = []
        for i, player in enumerate(data["players"]): # find player index in case of multiplayer run
            if player["id"] == 1: # id of 1 means singleplayer, stop looking for index
                break
            if str(player_id) == str(player["id"]): # multiplayer run, filter floors
                player_idx = i
                for floor in data["map_point_history"]:
                    filtered_floor = []

                    for point in floor:
                        player_stats = [ # keep only this player's stats
                            p for p in point.get("player_stats", [])
                            if str(p.get("player_id")) == str(player_id)
                        ]

                        if player_stats:
                            point = point.copy()  # avoid modifying original
                            point["player_stats"] = player_stats
                            filtered_floor.append(point)

                    if filtered_floor:
                        filtered_map.append(filtered_floor)
                break
        if not filtered_map: # if singleplayer, fall back to default map history
            filtered_map = data["map_point_history"]

        stats["summary"]["playtime"] += round(data["run_time"] / 60, 1) # length of run in minutes
        if data["killed_by_encounter"] != "NONE.NONE": # encounter that killed player
            enc = data["killed_by_encounter"]
            stats["summary"]["killed"][enc] = stats["summary"]["killed"].get(enc, 0) + 1

        stats["summary"]["total_runs"] += 1
        stats["summary"]["characters"][data["players"][player_idx]["character"].replace("CHARACTER.", "")]["total_runs"] += 1
        if data["win"]:
            stats["summary"]["wins"] += 1
            stats["summary"]["characters"][data["players"][player_idx]["character"].replace("CHARACTER.", "")]["wins"] += 1

        analyze_relics(stats, data["players"][player_idx]["relics"], data["win"])
        analyze_starter_relics(stats, filtered_map, data["win"])
        analyze_encounters(stats, filtered_map)
        analyze_cards(stats, data["players"][player_idx]["deck"], data["win"])
        
    with open("data/test/data.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("SUCCESS")

def analyze_all_runs():
    folder, player_id = locate_folder()
    analyze_runs("data/sts history", player_id)

analyze_all_runs()