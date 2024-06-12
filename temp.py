
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
            MathTex('1\quad 1'),
            MathTex('1\quad 2\quad 1'),
            MathTex('1\quad 3\quad 3\quad 1')
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
