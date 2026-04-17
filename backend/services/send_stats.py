import json

def get_general_stats():
    with open("../data/stats/summary_stats.json") as f:
        return json.load(f)
    
def get_card_stats():
    with open("../data/stats/card_stats.json") as f:
        return json.load(f)

def get_relic_stats():
    with open("../data/stats/relic_stats.json") as f:
        return json.load(f)
    
def get_encounter_stats():
    with open("../data/stats/encounter_stats.json") as f:
        return json.load(f)