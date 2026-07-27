import json
import os
import random

_tarot_data = None


def _load_tarot_data():
    global _tarot_data
    if _tarot_data is None:
        project_root = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(project_root, "data", "json", "tarot.json")
        with open(json_path, "r", encoding="utf-8") as f:
            _tarot_data = json.load(f)
    return _tarot_data


def get_random_cards(count: int = 3) -> list[str]:
    tarot_data = _load_tarot_data()
    keys = list(tarot_data.keys())
    if count <= 0:
        return []
    if count > len(keys):
        count = len(keys)
    return random.sample(keys, count)


def get_card_meanings(card_keys: list[str]) -> list[dict]:
    tarot_data = _load_tarot_data()
    result = []
    for key in card_keys:
        if key in tarot_data:
            result.append({
                "key": key,
                "描述": tarot_data[key]["描述"],
                "关键字": tarot_data[key]["关键字"]
            })
        else:
            result.append({
                "key": key,
                "描述": "",
                "关键字": []
            })
    return result