import json
import os

_data: dict | None = None


def _load():
    global _data
    if _data is None:
        path = os.path.join(os.path.dirname(__file__), 'similarity_data.json')
        if os.path.exists(path):
            with open(path) as f:
                raw = json.load(f)
            _data = raw.get('seasons', {})
        else:
            _data = {}


def _entry(player_id: int, season: str) -> dict | None:
    _load()
    return _data.get(season, {}).get(str(player_id))


def get_similar(player_id: int, season: str, n: int = 8) -> list[dict]:
    e = _entry(player_id, season)
    return e['similar'][:n] if e else []


def get_archetype(player_id: int, season: str) -> str | None:
    e = _entry(player_id, season)
    return e['archetype'] if e else None


def get_zone_vector(player_id: int, season: str) -> list[float] | None:
    e = _entry(player_id, season)
    return e['vector'] if e else None
