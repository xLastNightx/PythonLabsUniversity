import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Arc
import numpy as np

def draw_axolotl_face(show=True, save_path=None):
    fig, ax = plt.subplots(figsize=(6,6))

    # Head 
    head = Ellipse((0, 0), width=2.8, height=2.2, facecolor='#FFC1CC', edgecolor='none')  
    ax.add_patch(head)

    # Gills 
    gill_color = '#FF8FA3' 
    # positions for three gills 
    y_offsets = [0.4, 0.0, -0.4]
    widths = [0.7, 0.9, 0.7]   
    heights = [0.35, 0.28, 0.35]  
    angles = [30, 0, -30]  

    left_x = 1.6
    right_x = -1.6
    for i in range(3):
        # left gill
        gill_left = Ellipse((left_x, y_offsets[i]),width=widths[i], height=heights[i], angle=angles[i], facecolor=gill_color, edgecolor='none')
        ax.add_patch(gill_left)

        # right gill 
        gill_right = Ellipse((right_x, y_offsets[i]),width=widths[i], height=heights[i], angle=-angles[i], facecolor=gill_color, edgecolor='none')
        ax.add_patch(gill_right)

    # Eyes 
    eye_radius = 0.15
    ax.add_patch(Circle((-0.6, 0.3), eye_radius, color='black'))
    ax.add_patch(Circle((0.6, 0.3), eye_radius, color='black'))

    # small white on eyes
    ax.add_patch(Circle((-0.53, 0.36), 0.04, color='white'))
    ax.add_patch(Circle((0.67, 0.36), 0.04, color='white'))

    # Smile
    smile = Arc((0, -0.2), width=1.2, height=0.6, theta1=200, theta2=340, linewidth=3, color='black')
    ax.add_patch(smile)

    # Styling
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Аксолотль", fontsize=14)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.close(fig)

if __name__ == "__main__":
    draw_axolotl_face(show=True, save_path=None)
