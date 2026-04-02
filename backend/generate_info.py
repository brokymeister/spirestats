import json

def trim_card_info():
    with open("data/old/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)

    trimmed = {}

    for card in cards:
        trimmed[card.get("id")] = {
            "name": card.get("name"),
            "cost": card.get("cost"),
            "type": card.get("type"),
            "rarity": card.get("rarity")
        }

    with open("data/info/card_info.json", "w") as f:
        json.dump(trimmed, f, indent=2)

    print("Trimmed card info")

def trim_relic_info():
    with open("data/old/relics.json", "r", encoding="utf-8") as f:
        relics = json.load(f)

    trimmed = {}

    for relic in relics:
        trimmed[relic.get("id")] = {
            "name": relic.get("name"),
            "rarity": relic.get("rarity")
        }

    with open("data/info/relic_info.json", "w") as f:
        json.dump(trimmed, f, indent=2)
    
    print("Trimmed relic info")

def normalize_act(value):
    if not value:
        return None
    value = value.strip()

    if value.startswith("Act 1") or value == "Underdocks":
        return 1
    elif value.startswith("Act 2"):
        return 2
    elif value.startswith("Act 3"):
        return 3
    
    return value

def trim_monster_info():
    with open("data/old/encounters.json", "r", encoding="utf-8") as f:
        encounters = json.load(f)

    trimmed = {}

    for encounter in encounters:
        trimmed[encounter.get("id")] = {
            "name": encounter.get("name"),
            "type": encounter.get("room_type"),
            "act": normalize_act(encounter.get("act"))
        }

    with open("data/info/encounter_info.json", "w") as f:
        json.dump(trimmed, f, indent=2)

    print("Trimmed monster info")

def generate_card_stats():
    with open("data/info/card_info.json", "r") as f:
        cards = json.load(f)

    results = {}

    for card in cards:
        results[card] = {
            "pick_rate": None,
            "win_rate": None,
            "times_picked": None,
            "times_skipped": None
        }

    with open("data/stats/card_stats.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Generated card stats json")

def generate_relic_stats():
    with open("data/info/relic_info.json", "r") as f:
        relics = json.load(f)

    results = {}
    
    for relic in relics:
        results[relic] = {
            "times_won": None,
            "times_lost": None,
            "winrate": None,
            "pickrate": None,
            "times_picked": None,
            "times_skipped": None
        }

    with open("data/stats/relic_stats.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Generated relics stats json")

def generate_encounter_stats():
    with open("data/info/encounter_info.json", "r") as f:
        encounters = json.load(f)

    results = {}

    for encounter in encounters:
        results[encounter] = {
            "winrate": None,
            "wins": None,
            "losses": None,
            "total_hp_loss": None,
        }

    with open("data/stats/encounter_stats.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Generated encounter info json")

trim_card_info()
trim_relic_info()
trim_monster_info()

generate_card_stats()
generate_relic_stats()
generate_encounter_stats()