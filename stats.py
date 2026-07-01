def get_initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper()


def compute_stats(df):
    total = len(df)
    if total == 0:
        return {'fg': 0.0, '3p': 0.0, 'ppp': 0.0, 'fga': 0, 'team': ''}

    made       = df[df['SHOT_MADE_FLAG'] == 1]
    three_att  = df[df['SHOT_TYPE'] == '3PT Field Goal']
    three_made = three_att[three_att['SHOT_MADE_FLAG'] == 1]
    two_made   = made[made['SHOT_TYPE'] == '2PT Field Goal']

    return {
        'fg':   round(len(made) / total * 100, 1),
        '3p':   round(len(three_made) / len(three_att) * 100, 1) if len(three_att) > 0 else 0.0,
        'ppp':  round((len(two_made) * 2 + len(three_made) * 3) / total, 2),
        'fga':  total,
        'team': df['TEAM_NAME'].iloc[0] if 'TEAM_NAME' in df.columns else '',
    }


def bar_widths(a, b, max_px=56):
    """Scale two values to comparative bar widths capped at *max_px*."""
    mx = max(float(a), float(b), 1e-9)
    return round(max_px * a / mx), round(max_px * b / mx)
