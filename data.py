import time
import pandas as pd
from nba_api.stats.endpoints import shotchartdetail, commonallplayers, playerindex

SEASONS = [
    '2025-26', '2024-25', '2023-24', '2022-23', '2021-22',
    '2020-21', '2019-20', '2018-19', '2017-18',
]
CURRENT_SEASON = SEASONS[0]

_players_cache: dict[str, list] = {}
_shots_cache: dict[tuple, pd.DataFrame] = {}


def _height_to_inches(h: str) -> int | None:
    try:
        feet, inches = h.split('-')
        return int(feet) * 12 + int(inches)
    except Exception:
        return None


def get_all_players(season: str = CURRENT_SEASON) -> list[dict]:
    if season in _players_cache:
        return _players_cache[season]

    season_start = season[:4]                    # e.g. '2019' from '2019-20'
    season_end   = str(int(season[:4]) + 1)      # e.g. '2020' from '2019-20'

    active = commonallplayers.CommonAllPlayers(
        is_only_current_season=0,
        league_id='00',
        season=season,
    ).get_data_frames()[0]
    active = active[
        (active['GAMES_PLAYED_FLAG'] == 'Y') &
        (active['FROM_YEAR'] <= season_start) &
        (active['TO_YEAR'] >= season_end)
    ]
    active = active[['PERSON_ID', 'DISPLAY_FIRST_LAST']]

    index = playerindex.PlayerIndex(season=season).get_data_frames()[0]
    index = index[[
        'PERSON_ID', 'HEIGHT', 'WEIGHT', 'POSITION',
        'DRAFT_NUMBER', 'FROM_YEAR', 'PTS', 'REB', 'AST', 'TEAM_ID',
    ]].copy()
    index['height_in'] = index['HEIGHT'].apply(_height_to_inches)

    merged = active.merge(index, on='PERSON_ID', how='left')
    merged = merged.sort_values('DISPLAY_FIRST_LAST').reset_index(drop=True)

    _players_cache[season] = [
        {
            'id':         int(r['PERSON_ID']),
            'name':       r['DISPLAY_FIRST_LAST'],
            'height':     r['HEIGHT']    if pd.notna(r['HEIGHT'])       else None,
            'height_in':  int(r['height_in']) if pd.notna(r['height_in']) else None,
            'weight':     int(r['WEIGHT'])    if pd.notna(r['WEIGHT'])    else None,
            'position':   r['POSITION']  if pd.notna(r['POSITION'])    else None,
            'draft_pick': int(r['DRAFT_NUMBER']) if pd.notna(r['DRAFT_NUMBER']) else None,
            'exp':        (int(season[:4]) + 1 - int(r['FROM_YEAR'])) if pd.notna(r['FROM_YEAR']) else None,
            'team_id':    int(r['TEAM_ID']) if pd.notna(r['TEAM_ID']) and r['TEAM_ID'] != 0 else None,
            'dnp':        season == CURRENT_SEASON and bool(pd.isna(r['PTS']) and pd.isna(r['REB']) and pd.isna(r['AST'])),
        }
        for _, r in merged.iterrows()
    ]
    return _players_cache[season]


def get_shot_data(player_id: int, season: str = CURRENT_SEASON) -> pd.DataFrame:
    key = (player_id, season)
    if key not in _shots_cache:
        time.sleep(1)
        df = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season,
            season_type_all_star='Regular Season',
            context_measure_simple='FGA',
        ).get_data_frames()[0]
        df['LOC_X_FT'] = df['LOC_X'] / 10
        df['LOC_Y_FT'] = df['LOC_Y'] / 10
        _shots_cache[key] = df[df['LOC_Y_FT'] <= 50]
    return _shots_cache[key]
