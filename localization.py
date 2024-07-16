import json


def get_message(key: str, language: str, **kwargs) -> str:
    with open(f"localization/{language}.json", encoding="utf-8") as f:
        localization = json.load(f)
    if key not in localization:
        return "NONE"
    return localization.get(key).format(**kwargs)