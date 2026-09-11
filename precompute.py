#!/usr/bin/env python3
"""
Pre-compute zone vectors, cosine similarity, and archetypes for all players
across all available seasons.

Run once (~8 min per season due to NBA API rate limits), then restart the server.

Usage:
    python precompute.py
"""

import json
import numpy as np
from sklearn.preprocessing import normalize

from data import get_all_players, get_shot_data, SEASONS

# ── Zone definitions ────────────────────────────────────────────────────────
ZONE_MAP = {
    ('Restricted Area',        'Center(C)'):           'restricted_area',
    ('In The Paint (Non-RA)',  'Left Side(L)'):         'paint_left',
    ('In The Paint (Non-RA)',  'Center(C)'):            'paint_center',
    ('In The Paint (Non-RA)',  'Right Side(R)'):        'paint_right',
    ('Mid-Range',              'Left Side(L)'):         'midrange_left',
    ('Mid-Range',              'Left Side Center(LC)'): 'midrange_lc',
    ('Mid-Range',              'Center(C)'):            'midrange_center',
    ('Mid-Range',              'Right Side Center(RC)'): 'midrange_rc',
    ('Mid-Range',              'Right Side(R)'):        'midrange_right',
    ('Left Corner 3',          'Left Side(L)'):         'corner3_left',
    ('Right Corner 3',         'Right Side(R)'):        'corner3_right',
    ('Above the Break 3',      'Left Side Center(LC)'): 'ab3_left',
    ('Above the Break 3',      'Center(C)'):            'ab3_center',
    ('Above the Break 3',      'Right Side Center(RC)'): 'ab3_right',
}

ZONE_KEYS = list(dict.fromkeys(ZONE_MAP.values()))
MIN_FGA   = 25


# ── Zone vector ─────────────────────────────────────────────────────────────
def _zone_vector(df):
    if len(df) < MIN_FGA:
        return None
    counts = {k: 0 for k in ZONE_KEYS}
    for _, row in df.iterrows():
        key = ZONE_MAP.get((row['SHOT_ZONE_BASIC'], row['SHOT_ZONE_AREA']))
        if key:
            counts[key] += 1
    total = sum(counts.values()) or 1
    return [counts[k] / total for k in ZONE_KEYS]


# ── Archetype labelling ─────────────────────────────────────────────────────
def _label_archetype(vec):
    z       = dict(zip(ZONE_KEYS, vec))
    ra      = z['restricted_area']
    paint   = ra + z['paint_left'] + z['paint_center'] + z['paint_right']
    mid     = z['midrange_left'] + z['midrange_lc'] + z['midrange_center'] + z['midrange_rc'] + z['midrange_right']
    corner3 = z['corner3_left'] + z['corner3_right']
    above3  = z['ab3_left'] + z['ab3_center'] + z['ab3_right']
    total3  = corner3 + above3

    # RA-dominant (Gobert, Giannis) OR full paint heavy + limited mid (Sengun, AD)
    if ra > 0.52 or (paint > 0.50 and mid < 0.34):  return 'Interior Force'
    # Above-break 3 dominates (Steph, Lillard, Trae)
    if above3 > 0.33:                                return '3PT Volume Shooter'
    # Mid-range is biggest non-paint zone (Shai, DeRozan, KD)
    if mid > above3 and mid > 0.25:                  return 'Mid-Range Maestro'
    # Corner 3s are a significant share (Harris, Green)
    if corner3 > 0.15:                               return 'Corner Sniper'
    # Remaining 3pt-leaning players
    if total3 > 0.38:                                return '3PT Volume Shooter'
    return 'Versatile Scorer'


# ── Per-season processing ────────────────────────────────────────────────────
def _process_season(season: str) -> dict:
    players    = get_all_players(season)
    player_map = {p['id']: p['name'] for p in players}
    print(f'  {len(players)} players on roster')

    vectors = {}
    for i, p in enumerate(players):
        pid = p['id']
        try:
            df  = get_shot_data(pid, season)
            vec = _zone_vector(df)
            status = 'ok' if vec else f'skip (<{MIN_FGA} FGA)'
            if vec:
                vectors[pid] = vec
        except Exception as e:
            status = f'ERROR: {e}'
        print(f'    [{i+1:3}/{len(players)}] {p["name"]:<30} {status}')

    if len(vectors) < 2:
        print(f'  Only {len(vectors)} players with data — skipping')
        return {}

    print(f'  Building similarity for {len(vectors)} players…')
    player_ids  = list(vectors.keys())
    idx_map     = {pid: i for i, pid in enumerate(player_ids)}
    matrix      = np.array([vectors[pid] for pid in player_ids])
    matrix_norm = normalize(matrix, norm='l2')
    sim_matrix  = matrix_norm @ matrix_norm.T

    result = {}
    for pid in player_ids:
        idx  = idx_map[pid]
        sims = sim_matrix[idx]
        ranked = sorted(
            [(player_ids[j], float(sims[j])) for j in range(len(player_ids)) if player_ids[j] != pid],
            key=lambda x: -x[1]
        )[:10]
        result[str(pid)] = {
            'archetype': _label_archetype(vectors[pid]),
            'vector':    [round(v, 4) for v in vectors[pid]],
            'similar':   [
                {'id': sid, 'name': player_map.get(sid, ''), 'score': round(s, 3)}
                for sid, s in ranked
            ],
        }
    return result


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    import sys
    # Optional: python precompute.py 2024-25   (single season, fast test)
    target_seasons = [sys.argv[1]] if len(sys.argv) > 1 else SEASONS

    # Load existing data so a single-season run doesn't wipe other seasons
    out_path = 'similarity_data.json'
    try:
        with open(out_path) as f:
            existing = json.load(f)
        all_seasons = existing.get('seasons', {})
    except (FileNotFoundError, json.JSONDecodeError):
        all_seasons = {}

    for season in target_seasons:
        print(f'\n=== {season} ===')
        season_data = _process_season(season)
        if season_data:
            all_seasons[season] = season_data
            print(f'  Done — {len(season_data)} players saved')

    output = {'zone_keys': ZONE_KEYS, 'seasons': all_seasons}
    with open(out_path, 'w') as f:
        json.dump(output, f)

    total = sum(len(v) for v in all_seasons.values())
    print(f'\nDone — {total} player-seasons across {len(all_seasons)} seasons saved to {out_path}')


if __name__ == '__main__':
    main()
