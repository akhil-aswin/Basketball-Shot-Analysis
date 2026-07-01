from fastapi import APIRouter, HTTPException
from data import get_all_players, get_shot_data
from stats import compute_stats
from chart import shot_chart_svg

router = APIRouter()

_COLORS = {'a': '#ff5c35', 'b': '#00d4ff'}


@router.get('/players')
def players():
    return get_all_players()


@router.get('/shots/{player_id}')
def shots(player_id: int, slot: str = 'a'):
    color = _COLORS.get(slot, _COLORS['a'])
    try:
        df = get_shot_data(player_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {
        'team': df['TEAM_NAME'].iloc[0] if 'TEAM_NAME' in df.columns and len(df) > 0 else '',
        'stats': compute_stats(df),
        'svg': shot_chart_svg(df, color),
    }
