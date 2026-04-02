import json

def generate_summary_stats(stats): # generate general summary stats json
    summary = stats["summary"]

    # round playtime numbers to one decimal
    summary["playtime"] = round(summary["playtime"], 1)
    for _, character in summary["characters"].items():
        character["playtime"] = round(character["playtime"], 1)

    with open("data/stats/summary_stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("Generated summary stats")

def write_card_stats(stats):
    with open("data/stats/card_stats.json", "r") as f:
        existing = json.load(f)

    for cid, card_stats in stats["cards"].items():
        existing[cid]["synergies"] = card_stats

    with open("data/stats/card_stats.json", "w") as f:
        json.dump(existing, f, indent=2)
    print("Updated card synergy stats")

def write_relic_stats(stats):
    with open("data/stats/relic_stats.json", "r") as f:
        existing = json.load(f)

    for rid, relic_stats in stats["relics"].items():
        # avoid divide by 0 errors
        picked = relic_stats["times_picked"] + relic_stats["times_skipped"]
        pickrate = round(relic_stats["times_picked"] / picked, 3) if picked > 0 else 0 
        winrate = round(relic_stats["wins"] / relic_stats["acquired"], 3) if relic_stats["acquired"] > 0 else 0

        existing[rid] = {
            "times_won": relic_stats["wins"],
            "times_lost": relic_stats["acquired"] - relic_stats["wins"],
            "winrate": winrate,
            "pickrate": pickrate,
            "times_picked": relic_stats["times_picked"],
            "times_skipped": relic_stats["times_skipped"],
        }

    with open("data/stats/relic_stats.json", "w") as f:
        json.dump(existing, f, indent=2)
    print("Updated relic stats")

def write_encounter_stats(stats):
    with open("data/stats/encounter_stats.json", "r") as f:
        existing = json.load(f)

    for eid, enc_stats in stats["encounters"].items():
        winrate = round(enc_stats["wins"] / enc_stats["battles"]) if enc_stats["battles"] > 0 else 0 # avoid divide by 0 error
        existing[eid] = {
            "winrate": winrate,
            "wins": enc_stats["wins"],
            "losses": enc_stats["battles"] - enc_stats["wins"],
            "total_hp_lost": enc_stats["total_hp_lost"],
        }

    with open("data/stats/encounter_stats.json", "w") as f:
        json.dump(existing, f, indent=2)
    print("Updated encounter stats")