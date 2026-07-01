import time
import pandas as pd
from nba_api.stats.endpoints import shotchartdetail, commonallplayers, playerindex

SEASON = '2025-26'

_players_cache: list | None = None
_shots_cache: dict[int, pd.DataFrame] = {}


def _height_to_inches(h: str) -> int | None:
    try:
        feet, inches = h.split('-')
        return int(feet) * 12 + int(inches)
    except Exception:
        return None


def get_all_players() -> list[dict]:
    global _players_cache
    if _players_cache is None:
        active = commonallplayers.CommonAllPlayers(
            is_only_current_season=0,
            league_id='00',
            season=SEASON,
        ).get_data_frames()[0]
        active = active[(active['GAMES_PLAYED_FLAG'] == 'Y') & (active['TO_YEAR'] == '2026')]
        active = active[['PERSON_ID', 'DISPLAY_FIRST_LAST']]

        index = playerindex.PlayerIndex(season=SEASON).get_data_frames()[0]
        index = index[['PERSON_ID', 'HEIGHT', 'WEIGHT', 'POSITION', 'DRAFT_NUMBER', 'FROM_YEAR', 'PTS', 'REB', 'AST']].copy()
        index['height_in'] = index['HEIGHT'].apply(_height_to_inches)

        merged = active.merge(index, on='PERSON_ID', how='left')
        merged = merged.sort_values('DISPLAY_FIRST_LAST').reset_index(drop=True)

        _players_cache = [
            {
                'id':         int(r['PERSON_ID']),
                'name':       r['DISPLAY_FIRST_LAST'],
                'height':     r['HEIGHT']    if pd.notna(r['HEIGHT'])    else None,
                'height_in':  int(r['height_in']) if pd.notna(r['height_in']) else None,
                'weight':     int(r['WEIGHT'])    if pd.notna(r['WEIGHT'])    else None,
                'position':   r['POSITION']  if pd.notna(r['POSITION'])  else None,
                'draft_pick': int(r['DRAFT_NUMBER']) if pd.notna(r['DRAFT_NUMBER']) else None,
                'exp':        (2026 - int(r['FROM_YEAR'])) if pd.notna(r['FROM_YEAR']) else None,
                'dnp':        bool(pd.isna(r['PTS']) and pd.isna(r['REB']) and pd.isna(r['AST'])),
            }
            for _, r in merged.iterrows()
        ]
    return _players_cache


def get_shot_data(player_id: int) -> pd.DataFrame:
    if player_id not in _shots_cache:
        time.sleep(1)
        df = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=SEASON,
            season_type_all_star='Regular Season',
            context_measure_simple='FGA',
        ).get_data_frames()[0]
        df['LOC_X_FT'] = df['LOC_X'] / 10
        df['LOC_Y_FT'] = df['LOC_Y'] / 10
        _shots_cache[player_id] = df[df['LOC_Y_FT'] <= 50]
    return _shots_cache[player_id]
