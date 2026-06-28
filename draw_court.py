from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np

def draw_court(ax):
    basket = Circle((0, 0), radius=0.75, color='black', fill=False, linewidth=1.5)
    ax.add_patch(basket)
    ax.plot([-3, 3], [-0.75, -0.75], color='black', linewidth=1.5)
    paint = Rectangle((-8, -2.5), 16, 19, fill=False, color='black', linewidth=1.5)
    ax.add_patch(paint)
    ft_circle_top = Arc((0, 16.5), 12, 12, angle=0, theta1=0, theta2=180, color='black', linewidth=1.5)
    ft_circle_bottom = Arc((0, 16.5), 12, 12, angle=0, theta1=180, theta2=360, color='black', linewidth=1.5, linestyle='dashed')
    ax.add_patch(ft_circle_top)
    ax.add_patch(ft_circle_bottom)
    three_arc = Arc((0, 0), 47.5, 47.5, angle=0, theta1=20.9, theta2=159.1, color='black', linewidth=1.5)
    ax.add_patch(three_arc)
    corner_y = 23.75 * np.sin(np.radians(20.9))
    ax.plot([-22, -22], [0, corner_y], color='black', linewidth=1.5)
    ax.plot([22, 22], [0, corner_y], color='black', linewidth=1.5)
    restricted = Arc((0, 0), 8, 8, angle=0, theta1=0, theta2=180, color='black', linewidth=1.5)
    ax.add_patch(restricted)


