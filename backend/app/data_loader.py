"""Loads and serves the 4 JSON data files used by the RAG pipeline."""

import json
import os
from typing import Any, Optional

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_json(filename: str) -> Any:
    path = os.path.join(_DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load all data once at import time
_typologies_data: list[dict] = _load_json("player_typologies.json")["player_typologies"]
_abuse_flavors_data: list[dict] = _load_json("flavours_of_abuse.json")
_trauma_data: list[dict] = _load_json("trauma.json")
_vulnerability_data: list[dict] = _load_json("vulnerability_types.json")


def get_all_typologies() -> list[dict]:
    return _typologies_data


def get_typology_by_name(name: str) -> Optional[dict]:
    """Case-insensitive lookup of a single player typology."""
    for t in _typologies_data:
        if t.get("name", "").lower() == name.lower():
            return t
    return None


def get_all_abuse_flavors() -> list[dict]:
    return _abuse_flavors_data


def get_all_trauma_types() -> list[dict]:
    return _trauma_data


def get_all_vulnerability_types() -> list[dict]:
    return _vulnerability_data
