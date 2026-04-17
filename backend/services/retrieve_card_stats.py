import json
from pathlib import Path
from retrieve_run_stats import locate_folder

card_stats_path = "data/stats/card_stats.json"

def update_stats():
    folder, _ = locate_folder()
    temp = Path(folder)
    data_path = temp.parent / "progress.save"

    with open(data_path, "r") as f: # open progress.save
        new_data = json.load(f)

    with open(card_stats_path, "r") as f: # open existing card stats file
        existing = json.load(f)

    for card in new_data["card_stats"]:
        picked = card["times_picked"] 
        skipped = card["times_skipped"]
        won = card["times_won"]
        lost = card["times_lost"]

        pick_rate = round(picked / (picked + skipped) if (picked + skipped) > 0 else 0, 3)
        win_rate = round(won / (won + lost) if (won + lost) > 0 else 0, 3)
        card_id = card["id"].replace("CARD.", "")

        existing[card_id] = {
            "pickrate": pick_rate,
            "winrate": win_rate,
            "times_picked": picked,
            "times_skipped": skipped,
            "synergies": existing[card_id]["synergies"]
        }

    with open(card_stats_path, "w") as f: # update card stats file
        json.dump(existing, f, indent=2)

    print("Updated card stats")

def sort_cards(cards, amount, by="win_rate"): # sort cards by certain metric (winrate/pickrate)
    filtered = [
        c for c in cards
        if c["times_picked"] >= 1
    ]
    return sorted(filtered, key=lambda x: x[by], reverse=True)[:amount]

update_stats()