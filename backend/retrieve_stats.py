import json
import os

data_path = "data/progress.save"
stats_path = "data/card_stats.json"

def generate_card_info():
    with open(stats_path, "r") as f:
        cards = json.load(f)

    card_info = []

    for card in cards:
        card_id = card["id"]

        card_info.append({
            "id": card_id,
            "rarity": "",
            "cost": -1,
            "type": "",
            "color": ""
        })

    with open("data/card_info.json", "w") as f:
        json.dump(card_info, f, indent=2)

def update_stats():
    with open(data_path, "r") as f:
        new_data = json.load(f)

    results = []

    for card in new_data["card_stats"]:
        picked = card["times_picked"] 
        skipped = card["times_skipped"]
        won = card["times_won"]
        lost = card["times_lost"]

        pick_rate = round(picked / (picked + skipped) if (picked + skipped) > 0 else 0, 3)
        win_rate = round(won / (won + lost) if (won + lost) > 0 else 0, 3)

        results.append({
            "id": card["id"].replace("CARD.", ""),
            "pick_rate": pick_rate,
            "win_rate": win_rate,
            "times_picked": picked,
        })

    with open("data/card_stats.json", "w") as f:
        json.dump(results, f, indent=2)

    return results
    
generate_card_info()
card_stats = update_stats()

def sort_cards(cards, amount, by="win_rate"): # sort cards by certain metric (winrate/pickrate)
    filtered = [
        c for c in cards
        if c["times_picked"] >= 1
    ]
    return sorted(filtered, key=lambda x: x[by], reverse=True)[:amount]

print(json.dumps(sort_cards(card_stats, 5, "pick_rate"), indent=2))