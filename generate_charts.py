"""
generate_charts.py
──────────────────
Offline utility: generates two shot-chart SVGs and prints them for
manual pasting into compare.html.

Usage
─────
1. Populate shots_a / shots_b with (LOC_X, LOC_Y, made?) tuples.
   LOC_X / LOC_Y use NBA API units (10ths of feet, basket = origin).
2. Run: python generate_charts.py
3. Copy each SVG block into the matching slot in compare.html.
"""

import pandas as pd
from chart import shot_chart_svg

GOLD = '#c9a84c'
BLUE = '#7ab3e0'


def _to_df(shots):
    """Convert (LOC_X, LOC_Y, made?) tuples to the DataFrame shape expected by shot_chart_svg."""
    rows = [{'LOC_X': x, 'LOC_Y': y, 'SHOT_MADE_FLAG': int(made)} for x, y, made in shots]
    df = pd.DataFrame(rows)
    df['LOC_X_FT'] = df['LOC_X'] / 10
    df['LOC_Y_FT'] = df['LOC_Y'] / 10
    return df


# ── paste your shot data here ──────────────────────────────────────────
shots_a = [
    # (LOC_X,  LOC_Y,  made?)
    ( 220,  -40,  True),
    ( 180,  200,  True),
    (   0,   30,  True),
    (   0,   30,  True),
    (   0,   30, False),
    (-220,  -40, False),
]

shots_b = [
    (-220,  -40,  True),
    (-180,  200,  True),
    (   0,  250,  True),
    (   0,  250,  True),
    (   0,   30,  True),
    ( 220,  -40, False),
]
# ───────────────────────────────────────────────────────────────────────


if __name__ == '__main__':
    sep = '─' * 60
    for label, shots, color in [
        ('PLAYER A', shots_a, GOLD),
        ('PLAYER B', shots_b, BLUE),
    ]:
        print(sep)
        print(f'{label} — paste into the matching <svg> slot in compare.html')
        print(sep)
        print(shot_chart_svg(_to_df(shots), color))
        print()
