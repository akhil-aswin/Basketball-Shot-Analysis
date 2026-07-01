import os
import re

from chart import shot_chart_svg
from stats import bar_widths, compute_stats, get_initials

_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compare.html')
_SEASON_LABEL = '2025–26'

_PLAYER_A_COLOR = '#c9a84c'
_PLAYER_B_COLOR = '#7ab3e0'


def _substitutions(name1, s1, name2, s2):
    fg_a,  fg_b  = bar_widths(s1['fg'],  s2['fg'])
    tp_a,  tp_b  = bar_widths(s1['3p'],  s2['3p'])
    fga_a, fga_b = bar_widths(s1['fga'], s2['fga'])
    ppp_a, ppp_b = bar_widths(s1['ppp'], s2['ppp'])

    return {
        '{{ playerAName }}':     name1,
        '{{ playerAInitials }}': get_initials(name1),
        '{{ playerAMeta }}':     f"{s1['team']} · {_SEASON_LABEL}",
        '{{ playerAFG }}':       str(s1['fg']),
        '{{ playerA3P }}':       str(s1['3p']),
        '{{ playerAPPP }}':      str(s1['ppp']),
        '{{ playerAFGA }}':      str(s1['fga']),
        '{{ playerBName }}':     name2,
        '{{ playerBInitials }}': get_initials(name2),
        '{{ playerBMeta }}':     f"{s2['team']} · {_SEASON_LABEL}",
        '{{ playerBFG }}':       str(s2['fg']),
        '{{ playerB3P }}':       str(s2['3p']),
        '{{ playerBPPP }}':      str(s2['ppp']),
        '{{ playerBFGA }}':      str(s2['fga']),
        '{{ barAFG }}':          str(fg_a),
        '{{ barBFG }}':          str(fg_b),
        '{{ barA3P }}':          str(tp_a),
        '{{ barB3P }}':          str(tp_b),
        '{{ barAFGA }}':         str(fga_a),
        '{{ barBFGA }}':         str(fga_b),
        '{{ barAPPP }}':         str(ppp_a),
        '{{ barBPPP }}':         str(ppp_b),
    }


def render_compare_card(df1, name1, df2, name2):
    """Return a self-contained HTML string for the compare card."""
    with open(_TEMPLATE) as f:
        html = f.read()

    html = re.sub(r'<svg[\s\S]*?</svg>', shot_chart_svg(df1, _PLAYER_A_COLOR), html, count=1)
    html = re.sub(r'<svg[\s\S]*?</svg>', shot_chart_svg(df2, _PLAYER_B_COLOR), html, count=1)

    s1, s2 = compute_stats(df1), compute_stats(df2)
    for placeholder, value in _substitutions(name1, s1, name2, s2).items():
        html = html.replace(placeholder, value)

    return html
