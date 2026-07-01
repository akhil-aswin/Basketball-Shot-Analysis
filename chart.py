import io
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Rectangle

_BG = '#08080f'
_COURT_COLOR = (0.45, 0.5, 0.82, 0.75)


def _draw_court(ax, lw=1.5):
    c = _COURT_COLOR
    ax.add_patch(Circle((0, 0), radius=0.75, color=c, fill=False, linewidth=lw))
    ax.plot([-3, 3], [-0.75, -0.75], color=c, linewidth=lw)
    ax.add_patch(Rectangle((-8, -2.5), 16, 19, fill=False, color=c, linewidth=lw))
    for y in (11.0, 14.0):
        ax.plot([-10, -8], [y, y], color=c, linewidth=lw * 0.9)
        ax.plot([8, 10],   [y, y], color=c, linewidth=lw * 0.9)
    ax.add_patch(Arc((0, 16.5), 12, 12, theta1=0,   theta2=180, color=c, linewidth=lw))
    ax.add_patch(Arc((0, 16.5), 12, 12, theta1=180, theta2=360, color=c, linewidth=lw * 0.7, linestyle='dashed'))
    ax.add_patch(Arc((0, 0), 47.5, 47.5, theta1=20.9, theta2=159.1, color=c, linewidth=lw))
    corner_y = 23.75 * np.sin(np.radians(20.9))
    ax.plot([-22, -22], [0, corner_y], color=c, linewidth=lw)
    ax.plot([ 22,  22], [0, corner_y], color=c, linewidth=lw)
    ax.add_patch(Arc((0, 0), 8, 8, theta1=0, theta2=180, color=c, linewidth=lw))


_MAKE_COLOR = '#00e676'
_MISS_COLOR = '#ff3b5c'


_PANEL_BG  = '#0e1117'   # matches --bg-lift in the React panel
_TICK_COLOR = (0.55, 0.58, 0.72, 0.85)


def shot_chart_svg(df, player_color):
    fig, ax = plt.subplots(figsize=(5.5, 5.0), dpi=120)
    fig.patch.set_facecolor(_PANEL_BG)   # outer border — matches the HTML panel
    ax.set_facecolor(_BG)                # inner court — stays dark

    _draw_court(ax)
    ax.add_patch(Circle((0, 0), radius=0.75, color=player_color, fill=False, linewidth=2.2, zorder=4))

    made   = df[df['SHOT_MADE_FLAG'] == 1]
    missed = df[df['SHOT_MADE_FLAG'] == 0]
    dot_kw = dict(s=28, edgecolors='none', linewidths=0, alpha=0.9, zorder=5)
    ax.scatter(missed['LOC_X_FT'], missed['LOC_Y_FT'], c=_MISS_COLOR, **dot_kw)
    ax.scatter(made['LOC_X_FT'],   made['LOC_Y_FT'],   c=_MAKE_COLOR, **dot_kw)

    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 50)

    ax.set_xticks([])
    ax.set_yticks(range(0, 51, 5))
    ax.tick_params(axis='y', colors=_TICK_COLOR, labelsize=6.5, length=3, width=0.6, pad=3)
    for spine in ('top', 'bottom', 'right'):
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_edgecolor(_TICK_COLOR)
    ax.spines['left'].set_linewidth(0.6)
    ax.set_ylabel('Feet', fontsize=7, color=_TICK_COLOR, labelpad=4)

    fig.subplots_adjust(left=0.09, right=0.995, top=0.995, bottom=0.02)

    buf = io.StringIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', facecolor=_PANEL_BG, transparent=False)
    plt.close(fig)

    raw = buf.getvalue()
    svg = raw[raw.index('<svg'):]
    svg = re.sub(r'width="[\d.]+pt"',  'width="100%"',  svg, count=1)
    svg = re.sub(r'height="[\d.]+pt"', 'height="100%"', svg, count=1)
    return svg
