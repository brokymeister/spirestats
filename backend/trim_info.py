import json

def trim_card_info():
    with open("data/old/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)

    trimmed = []

    for card in cards:
        trimmed.append({
            "id": card.get("id"),
            "name": card.get("name"),
            "cost": card.get("cost"),
            "type": card.get("type"),
            "rarity": card.get("rarity")
        })

    with open("data/info/card_info.json", "w") as f:
        json.dump(trimmed, f, indent=2)

    print("Trimmed card info")

def trim_relic_info():
    with open("data/old/relics.json", "r", encoding="utf-8") as f:
        relics = json.load(f)

    trimmed = []

    for relic in relics:
        trimmed.append({
            "id": relic.get("id"),
            "name": relic.get("name"),
            "rarity": relic.get("rarity")
        })

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

    trimmed = []

    for encounter in encounters:
        trimmed.append({
            "id": encounter.get("id"),
            "name": encounter.get("name"),
            "type": encounter.get("room_type"),
            "act": normalize_act(encounter.get("act"))
        })

    with open("data/info/encounter_info.json", "w") as f:
        json.dump(trimmed, f, indent=2)

    print("Trimmed monster info")

trim_monster_info()