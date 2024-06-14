
from manim import *
import numpy as np

class PolarCoordinates(Scene):
    def construct(self):
        # Create both Cartesian and polar planes
        plane = PolarPlane(azimuth_units='degrees', radius_max=3).add_coordinates()
        # Define a point in polar coordinates (r, theta)
        r, theta = 2, 45  # 45 degrees and radius 2
        point_polar = plane.polar_to_point(r, theta * DEGREES)
        # Plot the point
        dot_polar = Dot(point_polar, color=GREEN)
        label_polar = MathTex('2\text{ at } 45^\circ').next_to(dot_polar, RIGHT)
        # Conversion to Cartesian coordinates
        x, y = r * np.cos(theta * DEGREES), r * np.sin(theta * DEGREES)
        label_cartesian = MathTex(f'({x:.2f}, {y:.2f})').next_to(dot_polar, DOWN)
        # Visualize the point and its coordinates
        self.play(Create(plane), run_time=1)
        self.play(FadeIn(dot_polar, scale=0.5), Write(label_polar))
        self.wait(1)
        self.play(Write(label_cartesian))
        self.wait(2)


