import os
import subprocess

def generate_manim_code(prompt):
    # Dictionary containing prompt keywords and corresponding Manim code examples
    examples = {
    "permutation":"""
from manim import *

class PermutationsScene(Scene):
    def construct(self):
        # Create the title text
        title = Text('Permutations of ABC').scale(0.9)
        
        # Write the title text to the scene
        self.play(Write(title))
        self.wait(1)
        
        # Move the title text to the top edge of the scene
        self.play(title.animate.to_edge(UP))
        
        # Create and display the initial item text
        items = Text('ABC').scale(1.2)
        self.play(Write(items))
        self.wait(1)
        
        # Define the permutations of 'ABC'
        permutations = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
        
        # Create a group of Text objects for each permutation
        perm_texts = VGroup(*[Text(perm).scale(0.8) for perm in permutations]).arrange_in_grid(rows=2, cols=3, buff=1)
        
        # Transform the initial items text into the grid of permutations
        self.play(Transform(items, perm_texts))
        self.wait(2)
        
        # Create and display the total count of permutations
        count_text = Text(f'Total permutations = {len(permutations)}').scale(0.8).to_edge(DOWN)
        self.play(Write(count_text))
        self.wait(2)
        
        # Create and display the mathematical explanation of permutations
        explanation_text = MathTex(r'P(n) = n! = 3! = 6').to_edge(DOWN)
        self.play(ReplacementTransform(count_text, explanation_text))
        self.wait(2)
""",
      "binomial": """
from manim import *

class BinomialTheoremScene(Scene):
    def construct(self):
        # Create and write the title
        title = Text('Binomial Theorem: (a + b)^2').scale(0.9)
        self.play(Write(title))
        self.wait(1)
        
        # Move the title to the upper edge of the screen
        self.play(title.animate.to_edge(UP))
        
        # Display the expansion formula of (a+b)^2
        expansion_formula = MathTex('(a + b)^2 = a^2 + 2ab + b^2')
        self.play(Write(expansion_formula))
        self.wait(1)
        
        # Create and arrange Pascal's Triangle below the expansion formula
        pascals_triangle = VGroup(
            MathTex('1'),
            MathTex('1\\quad 1'),
            MathTex('1\\quad 2\\quad 1'),
            MathTex('1\\quad 3\\quad 3\\quad 1')
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(expansion_formula, DOWN, buff=0.5)
        
        # Slightly adjust the position of the last row for better alignment
        pascals_triangle[-1].shift(UP * 0.2)
        self.play(Write(pascals_triangle))
        self.wait(1)
        
        # Highlight the third row of Pascal's Triangle
        highlight = SurroundingRectangle(pascals_triangle[2], color=YELLOW)
        self.play(Create(highlight))
        self.wait(2)
        
        # Display an explanatory text regarding coefficients
        explanation_text = Text("Coefficients come from Pascal's Triangle", font_size=24).next_to(pascals_triangle, DOWN)
        self.play(Write(explanation_text))
        self.wait(2)
""",
        "plot": """
from manim import *
import numpy as np

class Surface3DPlot(ThreeDScene):
    def construct(self):
        # Create axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 1, 0.5]
        )

        # Define the surface function z = sin(x) * cos(y)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            color=BLUE
        )

        # Set up the camera orientation
        self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
        self.add(axes)
        self.play(Create(surface))
        self.begin_ambient_camera_rotation(rate=0.2)  # Optional: Rotate the camera
        self.wait(4)
""",
        "graph": """
from manim import *

class GraphMultipleFunctions(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 9, 1],
            axis_config={'color': BLUE}
        )

        # Function y = x
        linear_function = axes.plot(lambda x: x, color=GREEN)
        linear_label = MathTex('y = x').next_to(linear_function, UP+LEFT)

        # Function y = x^2
        quadratic_function = axes.plot(lambda x: x**2, color=RED)
        quadratic_label = MathTex('y = x^2').next_to(quadratic_function.get_top(), UP)

        # Add all elements to the scene
        self.add(axes, linear_function, quadratic_function, linear_label, quadratic_label)
        self.play(Create(linear_function), Create(quadratic_function), Write(linear_label), Write(quadratic_label))
        self.wait(1)
""",
 "derivative": """
from manim import *

class DerivativeVisualization(Scene):
    def get_tangent_line(self, axes, x_value, graph, dx=0.01, color=ORANGE):
        x_left = x_value - dx
        y_left = graph.underlying_function(x_left)
        left_point = axes.c2p(x_left, y_left)
        x_right = x_value + dx
        y_right = graph.underlying_function(x_right)
        right_point = axes.c2p(x_right, y_right)
        return Line(left_point, right_point, color=color)

    def construct(self):
        title = Text('Visualization of the Derivative', font_size=24).to_edge(UP)
        self.play(Write(title))
        axes = Axes(x_range=[-3, 3, 1], y_range=[-5, 5, 1], axis_config={'include_numbers': True}, tips=True)
        graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2, 2])
        graph_label = axes.get_graph_label(graph, label='y = x^2').next_to(graph, UR, buff=0.5)
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)
        x_value = 1
        point_of_interest = axes.input_to_graph_point(x_value, graph)
        dot = Dot(point=point_of_interest, color=RED)
        dot_label = MathTex(f'x={x_value}', color=RED).next_to(dot, UP+RIGHT)
        tangent_line = always_redraw(lambda: self.get_tangent_line(axes, x_value, graph, dx=0.01, color=ORANGE))
        self.play(FadeIn(dot), Write(dot_label))
        self.play(Create(tangent_line))
        self.wait(2)
        slope = 2 * x_value
        slope_text = MathTex('Slope =', f'{slope}', color=ORANGE).to_corner(DL)
        self.play(Write(slope_text))
        self.wait(2)
        for new_x in [-1.5, 0, 1.5]:
            new_point = axes.input_to_graph_point(new_x, graph)
            new_slope = 2 * new_x
            new_slope_text = MathTex('Slope =', f'{new_slope:.2f}', color=ORANGE)
            self.play(dot.animate.move_to(new_point), Transform(dot_label, MathTex(f'x={new_x:.1f}', color=RED).next_to(dot, UP+RIGHT)), Transform(slope_text, new_slope_text))
            self.wait(1)
        conclusion_text = Text('The slope of the tangent line represents the derivative at that point.', font_size=20, color=BLUE).to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(3)

""",
 "molecular": """
from manim import *

class MolecularOrbitalVisualization(Scene):
    def construct(self):
        title = Text('Molecular Orbital Formation in H2', font_size=24).to_edge(UP)
        self.play(Write(title))
        left_orbital = Circle(color=RED, fill_opacity=0.5).shift(LEFT * 2)
        right_orbital = Circle(color=BLUE, fill_opacity=0.5).shift(RIGHT * 2)
        orbitals_label = Text('Atomic Orbitals (1s)', color=WHITE, font_size=17).next_to(left_orbital, UP, buff=0.5)
        self.play(Create(left_orbital), Create(right_orbital), Write(orbitals_label))
        self.wait(1)
        bonding_orbital = left_orbital.copy().set_color(GREEN).move_to(ORIGIN).scale(1.2)
        antibonding_orbital = right_orbital.copy().set_color(RED).move_to(ORIGIN).scale(1.2)
        bonding_label = Text('Bonding Orbital (σ)', font_size=14).next_to(bonding_orbital, UP)
        antibonding_label = Text('Antibonding Orbital (σ*)', font_size=15).next_to(antibonding_orbital, DOWN)
        self.play(Transform(left_orbital, bonding_orbital), Transform(right_orbital, antibonding_orbital))
        self.play(Write(bonding_label), Write(antibonding_label))
        self.wait(2)
        explanation_text = Text("Bonding orbitals result from constructive interference", font_size=24).next_to(bonding_orbital, DOWN)

        self.play(Write(explanation_text))
        self.wait(3)

""",
 "ecosystem": """
from manim import *
BROWN = '#8B4513'

class EcosystemFoodWeb(Scene):
    def construct(self):
        title = Text('Ecosystem Food Web Complexity', font_size=24).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        plants = Circle(color=GREEN, fill_opacity=1).shift(DOWN * 2)
        plants_label = Text('Plants', color=WHITE, font_size=18).move_to(plants.get_center())
        herbivores = Circle(color=BLUE, fill_opacity=1).shift(LEFT * 2)
        herbivores_label = Text('Herbivores', color=WHITE, font_size=18).move_to(herbivores.get_center())
        carnivores = Circle(color=RED, fill_opacity=1).shift(RIGHT * 2)
        carnivores_label = Text('Carnivores', color=WHITE, font_size=18).move_to(carnivores.get_center())
        decomposers = Circle(color=BROWN, fill_opacity=1).shift(UP * 2)
        decomposers_label = Text('Decomposers', color=WHITE, font_size=18).move_to(decomposers.get_center())
        self.play(Create(plants), Write(plants_label))
        self.play(Create(herbivores), Write(herbivores_label))
        self.play(Create(carnivores), Write(carnivores_label))
        self.play(Create(decomposers), Write(decomposers_label))
        self.wait(2)
        interaction_texts = VGroup(Text('Energy Flow').scale(0.7).next_to(plants, RIGHT), Text('Predation').scale(0.7).next_to(herbivores, UP), Text('Decomposition').scale(0.7).next_to(decomposers, LEFT))
        self.play(*[Write(text) for text in interaction_texts])
        self.wait(2)
        conclusion_text = Text('Understanding Food Webs', font_size=20).next_to(title, DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)

""",
 "neural ": """
from manim import *
BROWN = '#8B4513'

class EcosystemFoodWeb(Scene):
    def construct(self):
        title = Text('Ecosystem Food Web Complexity', font_size=24).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        plants = Circle(color=GREEN, fill_opacity=1).shift(DOWN * 2)
        plants_label = Text('Plants', color=WHITE, font_size=18).move_to(plants.get_center())
        herbivores = Circle(color=BLUE, fill_opacity=1).shift(LEFT * 2)
        herbivores_label = Text('Herbivores', color=WHITE, font_size=18).move_to(herbivores.get_center())
        carnivores = Circle(color=RED, fill_opacity=1).shift(RIGHT * 2)
        carnivores_label = Text('Carnivores', color=WHITE, font_size=18).move_to(carnivores.get_center())
        decomposers = Circle(color=BROWN, fill_opacity=1).shift(UP * 2)
        decomposers_label = Text('Decomposers', color=WHITE, font_size=18).move_to(decomposers.get_center())
        self.play(Create(plants), Write(plants_label))
        self.play(Create(herbivores), Write(herbivores_label))
        self.play(Create(carnivores), Write(carnivores_label))
        self.play(Create(decomposers), Write(decomposers_label))
        self.wait(2)
        interaction_texts = VGroup(Text('Energy Flow').scale(0.7).next_to(plants, RIGHT), Text('Predation').scale(0.7).next_to(herbivores, UP), Text('Decomposition').scale(0.7).next_to(decomposers, LEFT))
        self.play(*[Write(text) for text in interaction_texts])
        self.wait(2)
        conclusion_text = Text('Understanding Food Webs', font_size=20).next_to(title, DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)

""",
 "fourier": """
from manim import *
import numpy as np

class FourierSeriesDecomposition(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 10, 1], y_range=[-2, 2, 1], x_length=10, y_length=3, axis_config={'color': BLUE})
        def fourier_series(x, n_terms=5):
            s = 0
            for n in range(1, n_terms + 1):
                s += (np.sin((2 * n - 1) * x)) / (2 * n - 1)
            return 4 / np.pi * s
        square_wave = axes.plot(lambda x: fourier_series(x * PI), color=RED, x_range=[0, 10])
        square_wave_label = MathTex('f(x) = \\sum_{n=1}^{\\infty} \\frac{4}{\\pi} \\frac{\\sin((2n-1)x)}{2n-1}').next_to(axes, UP)
        components = VGroup()
        label_group = VGroup()
        for n in range(1, 6):
            component = axes.plot(lambda x: 4 / np.pi * np.sin((2 * n - 1) * x * PI) / (2 * n - 1), color=random_bright_color(), x_range=[0, 10])
            label = MathTex(f'4/\\pi \\cdot \\sin({2*n-1}x)/{2*n-1}').scale(0.7)
            components.add(component)
            label_group.add(label)
        label_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(axes, DOWN, buff=0.1)
        self.play(Create(axes))
        self.play(Create(square_wave), Write(square_wave_label))
        self.wait(2)
        for component, label in zip(components, label_group):
            self.play(Create(component))
            self.play(Write(label))
            self.wait(0.5)
        addition_label = MathTex('Sum of first 5 components approximates f(x)').to_edge(UP)
        self.play(Transform(square_wave_label, addition_label))
        self.wait(2)
        self.play(FadeOut(components), FadeOut(label_group), FadeIn(square_wave), ReplacementTransform(addition_label, square_wave_label))
        self.wait(2)

""",
 "combinations": """
from manim import *

class CombinationsScene(Scene):
    def construct(self):
        title = Text('Combinations of ABC taken 2 at a time').scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        combinations = ['AB', 'AC', 'BC']
        combo_texts = VGroup(*[Text(combo).scale(0.9) for combo in combinations]).arrange_in_grid(rows=1, cols=3, buff=1)
        self.play(Write(combo_texts))
        self.wait(2)
        count_text = Text(f'Total combinations = {len(combinations)}').scale(0.8).to_edge(DOWN)
        self.play(Write(count_text))
        self.wait(2)
        explanation_text = MathTex(r'C(n, k) = \binom{n}{k} = \binom{3}{2} = 3').to_edge(DOWN)
        self.play(ReplacementTransform(count_text, explanation_text))
        self.wait(2)

""",
 "second": """
from manim import *
import numpy as np
from scipy.integrate import odeint

class SecondOrderDE(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 10], y_range=[-2, 2], axis_config={'include_tip': True})
        def system(state, t):
            u, v = state
            return [v, -u]
        initial_conditions = [0, 1]
        t = np.linspace(0, 10, 400)
        sol = odeint(system, initial_conditions, t)
        u, v = sol.T
        solution = axes.plot_line_graph(t, u, add_vertex_dots=False, line_color=GREEN)
        equation_label = MathTex(r'\frac{d^2y}{dx^2} + y = 0').to_edge(UP)
        initial_condition_label = MathTex(r'y(0) = 0, \quad y^\prime(0) = 1').next_to(equation_label, DOWN)
        self.play(Create(axes))
        self.play(Create(solution), Write(equation_label), Write(initial_condition_label))
        self.wait(2)

""",
    "simple": """
from manim import *
import numpy as np
from scipy.integrate import odeint

class SimpleDE(Scene):
    def construct(self):
        # Define axes
        axes = Axes(x_range=[0, 5], y_range=[0, 10], axis_config={'include_tip': True})
        # Define the differential equation dy/dx = y
        def diff_eq(y, x):
            return y
        # Initial condition
        y0 = 1
        # Range for x values
        x = np.linspace(0, 5, 400)
        # Solve the differential equation
        y = odeint(diff_eq, y0, x)
        y = np.array(y).flatten()  # Flatten the solution array
        # Create the graph of the solution
        solution = axes.plot_line_graph(x, y, add_vertex_dots=False, line_color=BLUE)
        # Add labels
        solution_label = MathTex('\\frac{dy}{dx} = y', '\\quad y(0) = 1').to_edge(UP)
        # Show everything
        self.play(Create(axes))
        self.play(Create(solution), Write(solution_label))
        self.wait(2)    

""",
    "improper": """
from manim import *

class ImproperIntegral(Scene):
    def construct(self):
        # Define axes
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 1.5, 0.5], axis_config={'include_tip': True, 'include_numbers': True})
        # Define a function that approaches 0 as x approaches infinity
        func = axes.plot(lambda x: 1 / (x + 1), color=BLUE, x_range=[0.01, 9])
        # Highlight the area under the curve to infinity (simulated to a large number)
        area = axes.get_area(func, x_range=[1, 9], color=BLUE, opacity=0.3)
        # Labels and annotations
        func_label = MathTex('y = \\frac{1}{x+1}').next_to(func, RIGHT)
        integral_label = MathTex('\\int_1^\\infty \\frac{1}{x+1} \\, dx').to_edge(UP)
        # Show the elements
        self.play(Create(axes), Create(func))
        self.play(Write(func_label))
        self.play(FadeIn(area, scale=0.5))
        self.play(Write(integral_label))
        self.wait(2)
        # Extend the area animation towards infinity (simulation)
        self.play(area.animate.scale(1.5, about_point=axes.c2p(9, 0)))
        self.wait(2)

""",
"volume": """
from manim import *
import numpy as np

class VolumeOfRevolution(ThreeDScene):
    def construct(self):
        # Define axes
        axes = ThreeDAxes(x_range=[0, 3, 1], y_range=[0, 3, 1], z_range=[0, 3, 1], x_length=5, y_length=5, z_length=5)
        # Define a function
        func = lambda x: np.sqrt(x) + 1
        curve = ParametricFunction(lambda t: axes.c2p(t, func(t), 0), t_range=[0, 3], color=BLUE)
        # Create a revolved surface
        surface = Surface(lambda u, v: axes.c2p(u, func(u) * np.cos(v), func(u) * np.sin(v)), u_range=[0, 3], v_range=[0, TAU], checkerboard_colors=[BLUE_D, BLUE_E])
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, curve)
        self.play(Create(surface))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)

""",
"polar": """
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
        label_polar = MathTex('2\\text{ at } 45^\\circ').next_to(dot_polar, RIGHT)
        # Conversion to Cartesian coordinates
        x, y = r * np.cos(theta * DEGREES), r * np.sin(theta * DEGREES)
        label_cartesian = MathTex(f'({x:.2f}, {y:.2f})').next_to(dot_polar, DOWN)
        # Visualize the point and its coordinates
        self.play(Create(plane), run_time=1)
        self.play(FadeIn(dot_polar, scale=0.5), Write(label_polar))
        self.wait(1)
        self.play(Write(label_cartesian))
        self.wait(2)


""",
"argand": """
from manim import *

class ComplexNumberVisual(Scene):
    def construct(self):
        # Create the Argand plane
        plane = ComplexPlane(axis_config={'stroke_color': WHITE}).add_coordinates()
        # Define a complex number
        z = complex(2, 1)
        dot = Dot(plane.n2p(z), color=YELLOW)
        label = MathTex('2+1i').next_to(dot, UP)
        # Visualize the complex number
        self.play(Create(plane), run_time=1)
        self.play(FadeIn(dot, scale=0.5), Write(label))
        self.wait(1)
        # Show its conjugate
        z_conj = complex(2, -1)
        dot_conj = Dot(plane.n2p(z_conj), color=RED)
        label_conj = MathTex('2-1i').next_to(dot_conj, DOWN)
        self.play(FadeIn(dot_conj, scale=0.5), Write(label_conj))
        self.wait(1)
        # Connect with a line to show symmetry
        line = Line(dot.get_center(), dot_conj.get_center(), color=BLUE)
        self.play(Create(line))
        self.wait(1)

""",
"hexagon": """
from manim import *

class HexagonConstruction(Scene):
    def construct(self):
        # Center point
        center = Dot()
        # Initial circle
        circle = Circle(radius=2)
        circle.move_to(center)

        # Points for hexagon
        points = [circle.point_at_angle(i * PI / 3) for i in range(6)]
        hexagon = Polygon(*points, color=BLUE)

        # Construction animation
        self.play(Create(center))
        self.play(Create(circle))
        self.play(Create(hexagon))
        self.wait(1)

        # Label vertices
        labels = VGroup(*[Text(f"P{i+1}").next_to(points[i], DOWN, buff=0.1) for i in range(6)])
        self.play(*[Write(label) for label in labels])
        self.wait(1)

""",
"complex": """
from manim import *

class ComplexFunctionVisual(ThreeDScene):
    def construct(self):
        # Define the complex function: f(z) = z^2
        def func(z):
            return z**2

        # Create a complex plane
        plane = ComplexPlane().add_coordinates()
        
        # Map the complex function onto the plane
        mapped_plane = plane.copy().apply_complex_function(func)

        # Set up the scene
        self.add(plane)
        self.play(Transform(plane, mapped_plane))
        self.wait(2)

""",
"planetary": """
from manim import *

class PlanetaryOrbitSystem(ThreeDScene):
    def construct(self):
        # Create the sun and planets
        sun = Sphere(radius=1, color=YELLOW).move_to(ORIGIN)
        planet = Sphere(radius=0.2, color=BLUE).move_to(RIGHT * 5)

        # Define the orbit path
        orbit = Circle(radius=5, color=WHITE).set_stroke(width=2)

        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(sun, planet, orbit)
        self.play(Rotate(planet, about_point=ORIGIN, angle=2*PI, run_time=10, rate_func=linear))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(10)

""",
"wormhole": """
from manim import *

class WormholeIllustration(ThreeDScene):
    def construct(self):
        # Define spheres representing entry and exit points
        sphere1 = Sphere(radius=1, color=BLUE).shift(LEFT * 3)
        sphere2 = Sphere(radius=1, color=RED).shift(RIGHT * 3)

        # Define the "throat" of the wormhole as a cylinder
        throat = Cylinder(radius=0.5, height=6, direction=RIGHT * 6).set_color(GREEN)

        # Set up the scene
        self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
        self.add(sphere1, sphere2, throat)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)

""",
"bouncing": """
from manim import *
import numpy as np

class BouncingBalls(Scene):
    def construct(self):
        box = Rectangle(height=6, width=6).set_color(WHITE)
        balls = VGroup(*[Circle(radius=0.2, color=random_bright_color()).move_to(
            np.array([np.random.uniform(-3, 3), np.random.uniform(-3, 3), 0]))
            for _ in range(5)])
        gravity = np.array([0, -0.1, 0])
        velocities = [np.random.uniform(-1, 1, size=3) for _ in balls]

        self.add(box, balls)
        for _ in range(200):  # 200 frames of animation
            self.wait(0.05)
            for ball, vel in zip(balls, velocities):
                new_point = ball.get_center() + vel
                if not (-3 <= new_point[0] <= 3 and -3 <= new_point[1] <= 3):
                    vel *= -1  # Reverse the velocity if it hits the walls
                vel += gravity  # Apply gravity to velocity
                ball.shift(vel)

""",

"moon": """
from manim import *

class EarthMoonOrbit(ThreeDScene):
    def construct(self):
        # Set up the scene with Earth and Moon
        earth = Sphere(radius=1, color=BLUE, resolution=(32, 32))
        moon = Sphere(radius=0.2, color=GRAY, resolution=(32, 32)).shift(RIGHT * 3)  # 3 units away from Earth

        # Add Earth and Moon to the scene
        self.add(earth, moon)

        # Set up the camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Animate the Moon orbiting around the Earth
        self.play(Rotate(moon, about_point=ORIGIN, angle=2*PI, run_time=10, rate_func=linear))

        # Keep the camera stationary and let the animation loop
        self.wait(2)

""",

"lissajous": """
from manim import *
import numpy as np

class LissajousAnimation(Scene):
    def construct(self):
        # Lissajous curve parameters that evolve over time
        a = 3
        b = 2
        delta = PI / 2

        # Create a Lissajous curve
        lissajous_curve = ParametricFunction(
            lambda t: np.array([
                np.sin(a * t + delta),
                np.sin(b * t),
                0
            ]),
            t_range=[0, 2*PI],
            color=RED
        )

        # Animating the evolution of the curve
        self.play(Create(lissajous_curve), run_time=2)
        self.wait(1)

        # Change parameters over time
        self.play(lissajous_curve.animate.set_function(
            lambda t: np.array([
                np.sin((a+1) * t + delta),
                np.sin((b+1) * t),
                0
            ])
        ), run_time=5)
        self.wait(2)

""",

"circle": """
from manim import *

class ExpandingCollapsingCircleGrid(Scene):
    def construct(self):
        # Create a grid of circles
        grid = VGroup(*[Circle(radius=0.2, color=WHITE).shift(x * RIGHT + y * UP)
                       for x in range(-4, 5, 2)
                       for y in range(-3, 4, 2)])

        # Animation
        self.play(LaggedStart(*[GrowFromCenter(circle) for circle in grid], lag_ratio=0.1),
                  run_time=2)
        self.wait(1)
        self.play(LaggedStart(*[ShrinkToCenter(circle) for circle in grid], lag_ratio=0.1),
                  run_time=2)
        self.wait(1)

""",
"pendulum": """
from manim import *

class CollidingPendulums(Scene):
    def construct(self):
        # Create two pendulums
        pendulum1 = Line(UP * 2, DOWN * 2).set_stroke(width=3).move_to(LEFT * 2)
        pendulum2 = Line(UP * 2, DOWN * 2).set_stroke(width=3).move_to(RIGHT * 2)
        ball1 = Circle(radius=0.2, color=BLUE).next_to(pendulum1, DOWN)
        ball2 = Circle(radius=0.2, color=RED).next_to(pendulum2, DOWN)

        # Grouping them
        group1 = VGroup(pendulum1, ball1)
        group2 = VGroup(pendulum2, ball2)

        # Animation
        self.play(FadeIn(group1), FadeIn(group2))
        self.play(Rotate(group1, angle=PI/4, about_point=UP*2 + LEFT*2),
                  Rotate(group2, angle=-PI/4, about_point=UP*2 + RIGHT*2),
                  run_time=2, rate_func=there_and_back, repeat=3)
        self.wait(1)

""",
"surface": """
from manim import *
import numpy as np

class SurfaceOfRevolution(ThreeDScene):
    def construct(self):
        # Define a parabola
        def curve(t):
            return np.array([t, t**2, 0])

        # Generate the surface of revolution
        surface = Surface(
            lambda u, v: curve(u) @ np.array([
                [np.cos(v), 0, np.sin(v)],
                [0, 1, 0],
                [-np.sin(v), 0, np.cos(v)]
            ]),
            u_range=[-2, 2],
            v_range=[0, 2 * PI],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(20, 20)
        )

        # Setup the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(surface)
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)

""",
"vector": """
from manim import *
import numpy as np

class VectorField3D(ThreeDScene):
    def construct(self):
        # Define a vector field
        field = ArrowVectorField(
            lambda pos: np.cross(pos, OUT + SMALL_BUFF * UP),
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1]
        )

        # Set up the camera
        self.set_camera_orientation(phi=45 * DEGREES, theta=135 * DEGREES)
        self.add(field)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)

""",
"cube": """
from manim import *

class CubeSphereRotation(ThreeDScene):
    def construct(self):
        # Create a cube and a sphere
        cube = Cube()
        sphere = Sphere()

        # Position the sphere to the right of the cube
        sphere.shift(RIGHT * 3)

        # Set initial colors
        cube.set_color(BLUE)
        sphere.set_color(RED)

        # Prepare the scene
        self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
        self.add(cube, sphere)
        self.wait(1)

        # Animate rotation around the y-axis
        self.play(Rotate(cube, angle=PI/2, axis=UP), Rotate(sphere, angle=PI/2, axis=UP), run_time=2)
        self.wait(1)

        # Further rotation around the x-axis
        self.play(Rotate(cube, angle=PI/2, axis=RIGHT), Rotate(sphere, angle=PI/2, axis=RIGHT), run_time=2)
        self.wait(1)

""",
"helix": """
from manim import *
import numpy as np

class Plot3DHelix(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 2, 1]
        )

        # Define the parametric function for a helix
        helix = ParametricFunction(
            lambda t: np.array([
                np.cos(t),
                np.sin(t),
                t / 2  # Control the vertical displacement
            ]),
            t_range=np.array([0, 10*PI, 0.1]),  # Several twists
            color=RED
        )

        # Draw everything
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)
        self.play(Create(helix))
        self.wait(2)

""",
"sine": """
from manim import *

class PlotSineWave(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={'color': BLUE}
        )

        # Create the sine wave graph
        sine_wave = axes.plot(lambda x: np.sin(x), color=GREEN)

        # Label for the sine wave
        label = axes.get_graph_label(sine_wave, label='y = \\sin(x)')

        # Draw axes and sine wave
        self.play(Create(axes), Create(sine_wave), Write(label))
        self.wait(1)

""",
"pentagon": """
from manim import *

class DrawPentagon(Scene):
    def construct(self):
        # Create a regular pentagon
        pentagon = RegularPolygon(5)
        # Set color and line width
        pentagon.set_fill(ORANGE, opacity=0.5)
        pentagon.set_stroke(color=WHITE, width=4)

        # Animate the creation of the pentagon
        self.play(Create(pentagon))
        self.wait(1)

""",
"timeline": """
from manim import *

class HistoricalTimeline(Scene):
    def construct(self):
        # Timeline setup
        timeline = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        start_label = Text("1900", font_size=24).next_to(timeline.get_start(), DOWN)
        end_label = Text("2000", font_size=24).next_to(timeline.get_end(), DOWN)

        # Events
        events = [
            ("WWI", -4),
            ("Great Depression", -2),
            ("WWII", 0),
            ("Moon Landing", 2),
            ("Fall of Berlin Wall", 4),
        ]

        # Create event markers and labels
        dots = VGroup()
        labels = VGroup()
        for event, pos in events:
            dot = Dot().move_to(timeline.point_from_proportion((pos + 5) / 10))
            label = Text(event, font_size=18).next_to(dot, UP)
            dots.add(dot)
            labels.add(label)

        # Animate
        self.play(Create(timeline), Write(start_label), Write(end_label))
        self.wait(1)
        for dot, label in zip(dots, labels):
            self.play(GrowFromCenter(dot), Write(label))
            self.wait(0.5)
        
        # Final wait
        self.wait(2)

""",
"pie": """
from manim import *

class PieChartExample(Scene):
    def construct(self):
        # Data for the pie chart
        data = [30, 15, 20, 35]  # Percentages of each sector
        colors = [TEAL, ORANGE, PURPLE_A, GOLD]  # Colors for each sector

        # Total of all segments
        total = sum(data)
        current_angle = 0  # Start angle for the first segment
        radius = 2  # Radius of the pie chart

        # Create a pie chart from the data
        pie_chart = VGroup()  # Initialize a group to store pie slices
        labels = VGroup()  # Group for labels

        for i, value in enumerate(data):
            # Calculate the angle covered by the segment
            angle = value / total * 360 * DEGREES

            # Create a sector (pie slice)
            sector = Sector(
                start_angle=current_angle,
                angle=angle,
                color=colors[i],
                fill_opacity=0.8,
                outer_radius=radius
            )

            # Calculate label position
            label_position = sector.get_center() + np.array([
                radius * 0.75 * np.cos(current_angle + angle / 2),
                radius * 0.75 * np.sin(current_angle + angle / 2),
                0
            ])

            # Create label for the sector
            label = MathTex(f"{value}%")
            label.move_to(label_position)

            # Add sector and label to their respective groups
            pie_chart.add(sector)
            labels.add(label)

            # Update the start angle for the next sector
            current_angle += angle

        # Center the pie chart
        pie_chart.move_to(ORIGIN)
        labels.move_to(ORIGIN)

        # Title for the pie chart
        title = Title("Pie Chart Example")

        # Animate everything
        self.play(
            FadeIn(title),
            Create(pie_chart),
            FadeIn(labels),
            run_time=4
        )
        self.wait(2)

""",
"bar": """
from manim import *

class BarChartExample(Scene):
    def construct(self):
        # Data for the bar chart
        data = [2, 5, 3, 6]  # Sample data values
        categories = ['A', 'B', 'C', 'D']  # Categories for the data

        # Create a bar chart
        bar_chart = BarChart(
            values=data,
            bar_names=categories,
            bar_colors=[BLUE, YELLOW, GREEN, RED],
            y_range=[0, 10, 1],  # Setting the range for the y-axis
            y_length=6,  # The vertical length of the bars
            x_length=6,  # The horizontal spacing of the bars
        )

        # Title for the bar chart
        title = Title('Bar Chart Example')

        # Animate the creation of the bar chart
        self.play(
            Write(title),
            Create(bar_chart),
            run_time=4
        )
        self.wait(2)

""",
"wave": """
from manim import *

class WaveInterference(Scene):
    def construct(self):
        # Wave sources
        source_a = Dot(LEFT * 2)
        source_b = Dot(RIGHT * 2)

        # Define wave parameters
        amplitude = 1
        frequency = 2
        wavelength = 2 * PI

        # Create waves for each source
        waves_a = FunctionGraph(lambda x: amplitude * np.sin(frequency * x), x_range=[-10, 0], color=BLUE)
        waves_b = FunctionGraph(lambda x: amplitude * np.sin(frequency * x + PI), x_range=[0, 10], color=RED)

        # Group the wave graphs
        waves = VGroup(waves_a, waves_b)

        # Move the waves to the sources
        waves_a.move_to(source_a.get_center())
        waves_b.move_to(source_b.get_center())

        # Group all elements and animate
        self.play(DrawBorderThenFill(source_a), DrawBorderThenFill(source_b), Create(waves), run_time=4)
        self.wait(2)

""",
"orbital": """
from manim import *

class OrbitalMechanics(Scene):
    def construct(self):
        # Define the colors and sizes for higher visibility
        sun_color = YELLOW
        planet_color = BLUE
        # Sun setup
        sun = Circle(radius=1, color=sun_color)  # Larger radius for the sun
        sun.set_fill(sun_color, opacity=1)
        sun.move_to(ORIGIN)
        # Planet setup with explicit visibility enhancements
        planet = Dot(radius=0.3, color=planet_color)  # Increased the radius of the planet
        planet.set_fill(planet_color, opacity=1)
        planet.move_to(5 * RIGHT)  # Increase the distance to make the orbit larger
        # Orbit path (ellipse to represent the orbital path)
        orbit_path = Ellipse(width=10, height=4, color=WHITE)  # Larger and wider orbit path
        # Animation for the planet orbiting the sun
        orbit_animation = Rotating(planet, about_point=ORIGIN, radians=2*PI, run_time=3, rate_func=smooth)
        # Drawing the sun, planet, and orbit path with a clear distinction
        self.play(
            DrawBorderThenFill(sun),
            Create(orbit_path),
            GrowFromCenter(planet),
            orbit_animation
        )
        self.wait(2)

""",
"x^2": """
from manim import *

class VisualizeDerivative(Scene):
    def construct(self):
        # Create axes and plots for the function and its derivative
        axes = Axes(x_range=[-3, 3, 1], y_range=[-5, 5, 1], axis_config={'color': BLUE})
        func = axes.plot(lambda x: x**2, color=RED)
        derivative = axes.plot(lambda x: 2*x, color=GREEN)
        graphs = VGroup(axes, func, derivative)
        # Labels for the functions
        func_label = MathTex('f(x) = x^2').next_to(func, UP)
        derivative_label = MathTex("f'(x) = 2x").next_to(derivative, UP+RIGHT)
        labels = VGroup(func_label, derivative_label)
        # Create and animate everything together
        self.play(Create(graphs), FadeIn(labels, shift=UP), run_time=2)
        self.wait(1)

""",
"pythagoras": """
from manim import *

class PythagorasTheorem(Scene):
    def construct(self):
        # Define the points of the right-angled triangle
        pointA = ORIGIN
        pointB = 4 * RIGHT
        pointC = 4 * RIGHT + 3 * UP
        # Create the triangle
        triangle = Polygon(pointA, pointB, pointC, color=WHITE)
        triangle.set_fill(BLUE, opacity=0.5)
        # Labels for the sides of the triangle
        a_label = MathTex("c", color=RED).next_to(triangle, LEFT, buff=0.1)
        b_label = MathTex("b", color=GREEN).next_to(triangle, DOWN, buff=0.1)
        c_label = MathTex("a", color=BLUE).next_to(triangle, RIGHT, buff=0.1)
        # Heading for context
        heading = Text("Pythagorean Theorem", font_size=36).to_edge(UP)
        # The theorem formula
        theorem_formula = MathTex("c^2 = a^2 + b^2", color=PURPLE).scale(1.5).next_to(heading, DOWN)
        # Grouping all elements for a single animation command
        all_elements = VGroup(triangle, a_label, b_label, c_label, heading, theorem_formula)
        # Animate all elements together using DrawBorderThenFill for a coherent drawing effect
        self.play(DrawBorderThenFill(all_elements), run_time=3)
        self.wait(2)

""",
"multiplication": """
from manim import *

class ComplexNumberMultiplication(Scene):
    def construct(self):
        # Setup complex plane
        plane = ComplexPlane().add_coordinates()
        # Multiplication of two complex numbers
        num1 = complex(1, 2)  # represented by 1 + 2i
        num2 = complex(2, 1)  # represented by 2 + 1i
        result = num1 * num2  # Result of the multiplication
        # Plot points for complex numbers and the result
        dot1 = Dot(plane.n2p(num1), color=YELLOW)
        dot2 = Dot(plane.n2p(num2), color=RED)
        result_dot = Dot(plane.n2p(result), color=GREEN)
        dots = VGroup(dot1, dot2, result_dot)
        # Labels for the points
        dot1_label = MathTex("1+2i").next_to(dot1, UP)
        dot2_label = MathTex("2+1i").next_to(dot2, UP)
        result_label = MathTex("5i").next_to(result_dot, UP)
        labels = VGroup(dot1_label, dot2_label, result_label)
        # Create and animate everything together
        self.play(Create(plane), FadeIn(dots), FadeIn(labels), run_time=2)
        self.wait(1)

""",
"tessellation": """
from manim import *

class HexagonTessellation(Scene):
    def construct(self):
        # Create a hexagon
        def hexagon():
            return RegularPolygon(6, radius=1, stroke_color=BLUE, fill_color=ORANGE, fill_opacity=0.6)
        # Arrange hexagons into a tessellation pattern
        tessellation = VGroup(*[
            hexagon().shift(i * np.sqrt(3) * RIGHT + j * np.sqrt(3) * UP * 0.5)
            for i in range(-5, 5) for j in range(-5, 5)
            if (i+j)%2 == 0
        ])
        # Add the tessellation to the scene and animate
        self.play(Create(tessellation))
        self.wait(1)

""",
"triangle": """
from manim import *

class SierpinskiTriangle(Scene):
    def construct(self):
        # Recursive function to create Sierpinski triangle
        def sierpinski(order, scale):
            if order == 0:
                return Triangle().scale(scale)
            else:
                triangle = sierpinski(order - 1, scale / 2)
                return VGroup(
                    triangle.copy().shift(LEFT*scale),
                    triangle.copy().shift(RIGHT*scale),
                    triangle.copy().shift(UP*scale)
                )
        # Create Sierpinski triangle of order 3
        sierpinski_triangle = sierpinski(3, 2)
        # Add the fractal to the scene and animate
        self.play(Create(sierpinski_triangle))
        self.wait(1)

""",
"spiral": """
from maclass ParametricSpiral(Scene):
    def construct(self):
        # Define a parametric curve for a spiral
        def spiral(t):
            return np.array([
                t * np.cos(t),
                t * np.sin(t),
                0
            ])
        # Create a curve based on the spiral function
        spiral_curve = ParametricFunction(
            spiral, t_range = np.array([0, 10, 0.1]),
            color = BLUE
        )
        # Add the curve to the scene and animate
        self.play(Create(spiral_curve))
        self.wait(1)

""",
"quadratic": """
from manim import *

class PlotQuadraticFunction(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 10, 1],
            axis_config={'color': BLUE}
        )
        # Create a quadratic function graph y = x^2
        graph = axes.plot(lambda x: x**2, color=RED)
        # Label for the graph
        graph_label = axes.get_graph_label(graph, label='y=x^2')
        # Create the axes and graph with an animated drawing
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)

""",
"linear": """
from manim import *

class PlotLinearFunction(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 5, 1],
            axis_config={'color': BLUE}
        )
        # Create a line based on the equation y = 2x + 1
        line = axes.plot(lambda x: 2*x + 1, color=GREEN)
        # Label for the line
        line_label = axes.get_graph_label(line, label='y=2x+1')
        # Draw the line with an animation
        self.play(Create(axes), Create(line), Write(line_label))
        self.wait(1)

""",
"spin": """
from manim import *

class RotateShape(Scene):
    def construct(self):
        # Create a pentagon
        pentagon = RegularPolygon(5)
        # Set color
        pentagon.set_fill(PURPLE, opacity=0.5)
        # Rotate the pentagon
        self.play(Rotate(pentagon, angle=2*PI))
        self.wait(1)

""",
"transform": """
from manim import *

class TransformShape(Scene):
    def construct(self):
        # Create a square and a circle
        square = Square()
        circle = Circle()

        # Position the square
        square.shift(LEFT)

        # Position the circle
        circle.shift(RIGHT)

        # Show square and transform it into circle
        self.play(Create(square))
        self.wait(0.5)
        self.play(Transform(square, circle))
        self.wait(1)

""",
"combine": """
from manim import *

class CombineShapes(Scene):
    def construct(self):
        # Create a circle, square, and triangle
        circle = Circle(radius=1, color=RED, fill_opacity=0.5)
        square = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        triangle = RegularPolygon(n=3, color=GREEN, fill_opacity=0.5)
        triangle.set_width(2)

        # Position the shapes to form a house shape
        circle.move_to(UP * 1)
        square.move_to(DOWN * 0.5)
        triangle.move_to(DOWN * 1.5)

        # Group the shapes
        house_shape = VGroup(circle, square, triangle)

        # Show creation of the combined shape
        self.play(Create(house_shape))
        self.wait(1)

""",
"equilateral": """
from manim import *

class DrawTriangle(Scene):
    def construct(self):
        # Create an equilateral triangle
        triangle = Polygon(np.array([0, 1, 0]), np.array([-1, -1, 0]), np.array([1, -1, 0]))

        # Set color and line width
        triangle.set_fill(YELLOW, opacity=0.5)
        triangle.set_stroke(color=WHITE, width=4)

        # Show creation of the triangle
        self.play(Create(triangle))
        self.wait(1)

""",
"square": """
from manim import *

class DrawSquare(Scene):
    def construct(self):
        # Create a square
        square = Square()
        # Set color and line width
        square.set_fill(BLUE, opacity=0.5)
        square.set_stroke(color=WHITE, width=4)

        # Show creation of the square
        self.play(Create(square))
        self.wait(1)

""",
"circle": """
from manim import *

class DrawCircle(Scene):
    def construct(self):
        # Create a circle
        circle = Circle()
        # Set color and line width
        circle.set_fill(PINK, opacity=0.5)
        circle.set_stroke(color=WHITE, width=4)

        # Show creation of the circle
        self.play(Create(circle))
        self.wait(1)

"""
        # Add more prompt-keyword to Manim-code mappings as needed
    }

    # Check if the prompt keyword exists in the examples dictionary
    if prompt.lower() in examples:
        return examples[prompt.lower()]
    else:
        return None  # Return None if prompt keyword not found
