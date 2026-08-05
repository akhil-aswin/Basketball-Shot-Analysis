from fastapi import APIRouter, HTTPException
from data import get_all_players, get_shot_data, SEASONS, CURRENT_SEASON
from stats import compute_stats
from chart import shot_chart_svg
from similarity import get_archetype, get_similar

router = APIRouter()

_COLORS = {'a': '#FF0F05', 'b': '#0046FF'}


@router.get('/seasons')
def seasons():
    return SEASONS


@router.get('/players')
def players(season: str = CURRENT_SEASON):
    return [
        {**p, 'archetype': get_archetype(p['id'], season)}
        for p in get_all_players(season)
    ]


@router.get('/shots/{player_id}')
def shots(player_id: int, slot: str = 'a', season: str = CURRENT_SEASON):
    color = _COLORS.get(slot, _COLORS['a'])
    try:
        df = get_shot_data(player_id, season)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    team_id = int(df['TEAM_ID'].iloc[0]) if 'TEAM_ID' in df.columns and len(df) > 0 else None

    return {
        'team':      df['TEAM_NAME'].iloc[0] if 'TEAM_NAME' in df.columns and len(df) > 0 else '',
        'team_id':   team_id,
        'stats':     compute_stats(df),
        'svg':       shot_chart_svg(df, color),
        'archetype': get_archetype(player_id, season),
        'similar':   get_similar(player_id, season, n=5),
    }
