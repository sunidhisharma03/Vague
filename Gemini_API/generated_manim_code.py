import math
from manim import *
import numpy as np

class IntegrateXsquared(Scene):
    def construct(self):
        # Constants
        a = 2
        b = 7
        num_rects = 30  # Increased for smoother animation

        # Axes
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 200, 50],
            axis_config={"include_numbers": True},
            x_length=6, # Adjusted x_length for better spacing
            y_length=4 # Adjusted y_length for better spacing

        ).to_edge(LEFT, buff=1)
        labels = axes.get_axis_labels(x_label="x", y_label="$x^2$").set_color(WHITE)

        # Function
        graph = axes.plot(lambda x: x**2, x_range=[a, b], color=BLUE)

        # Integral Notation
        integral_text = MathTex(r"\int_2^7 x^2 \, dx").to_edge(UP, buff=1).set_color(WHITE)

        # Calculation
        result = (b**3)/3 - (a**3)/3
        result_text = MathTex(f"= {result:.2f}").next_to(integral_text, RIGHT, buff=1).to_edge(UP).set_color(WHITE)


        # Shaded Area (using a more efficient method)
        riemann_rects = self.create_riemann_rects(axes, a, b, num_rects)
        shaded_area = self.create_shaded_area(riemann_rects)

        # Animations
        self.play(Create(axes), Create(labels), Write(integral_text), run_time=2)
        self.wait(1)
        self.play(Create(graph), run_time=2)
        self.wait(1)
        self.play(Create(riemann_rects), run_time=5) # Increased runtime
        self.wait(1)
        self.play(Transform(riemann_rects, shaded_area), run_time=4) # Smoother transition, increased runtime
        self.wait(1)
        self.play(Write(result_text), run_time=2)
        self.wait(10) # Extended wait time


    def create_riemann_rects(self, axes, a, b, num_rects):
        dx = (b - a) / num_rects
        rects = VGroup()
        for i in range(num_rects):
            x = a + i * dx
            rect_height = axes.c2p(x, x**2)[1] - axes.c2p(x,0)[1]
            rect = Rectangle(
                width=dx,
                height=rect_height,
                fill_opacity=0.7,
                fill_color=YELLOW,
            ).move_to(axes.c2p(x + dx/2,0))
            rect.shift(UP*rect_height/2)
            rects.add(rect)
        return rects

    def create_shaded_area(self, rects):
        shaded_area = VMobject()
        for rect in rects:
            shaded_area.add_points_as_corners(rect.get_points())
        shaded_area.set_fill(YELLOW, 0.7)
        return shaded_area
