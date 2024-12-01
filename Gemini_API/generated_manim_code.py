import math
from manim import *
import numpy as np

class FourierTransform(Scene):
    def construct(self):
        # Configuration
        axes_config = {"x_range": (-5, 5, 1), "y_range": (-2, 2, 0.5), "axis_config": {"include_tip": True}}
        func_color = BLUE
        circle_color = YELLOW
        fourier_color = GREEN

        # 1. Introduce the function
        func = lambda x: np.sin(x) + 0.5 * np.sin(3 * x)
        func_graph = self.get_function_graph(func, axes_config, func_color)
        func_label = MathTex(r"f(x) = \sin(x) + 0.5\sin(3x)").next_to(func_graph, UP, buff=0.5)

        self.play(Create(func_graph), Write(func_label), run_time=2)
        self.wait(1)

        # 2. Introduce Fourier Series Concept
        fourier_text = Tex("Fourier Series Representation").to_edge(UP)
        self.play(Write(fourier_text), run_time=1)
        self.wait(1)

        # 3. Animate the circles and their summation
        circles = VGroup()
        sum_graph = self.get_function_graph(lambda x: 0, axes_config, func_color)
        fourier_terms = VGroup()
        circles_group = VGroup()

        n_terms = 10 # Increased number of terms for a better visual and longer runtime.
        circles_start_pos = 3*LEFT
        fourier_terms_start_pos = 2*RIGHT

        for i in range(1, 2*n_terms, 2):
            amp = 1 / i
            freq = i
            circle = self.create_rotating_circle(amp, freq, circle_color)
            circles.add(circle)
            fourier_term = MathTex(f"+ {amp:.2f}\sin({freq}x)").set_color(fourier_color)
            fourier_terms.add(fourier_term)

        circles.arrange(RIGHT, buff=0.7).move_to(circles_start_pos) #Adjusted buffer for better spacing
        fourier_terms.arrange(DOWN, buff=0.5).move_to(fourier_terms_start_pos)


        self.play(Create(circles[0]), Create(fourier_terms[0]), run_time=2)
        self.add(sum_graph)

        for i in range(1, len(circles)):
            new_sum_func = lambda x: sum([amp * np.sin(freq * x) for amp, freq in self.get_fourier_coeffs(i + 1)])
            self.play(
                Create(circles[i]),
                Create(fourier_terms[i]),
                UpdateFromAlphaFunc(sum_graph, lambda mob, alpha: self.update_sum_graph(mob, new_sum_func, alpha)),
                run_time=1
            )
            self.wait(0.5)


        self.wait(3)
        self.play(FadeOut(fourier_text), FadeOut(circles), FadeOut(fourier_terms), run_time=2)

        # 4. Conclude
        conclusion_text = Tex("The Fourier Transform decomposes a function into its frequency components").to_edge(DOWN).scale(0.8) #Scaled for better fit.
        self.play(Write(conclusion_text), run_time=2)
        self.wait(3)


    def get_function_graph(self, func, axes_config, color):
        axes = Axes(**axes_config)
        graph = axes.plot(func, color=color)
        return VGroup(axes, graph)

    def create_rotating_circle(self, amplitude, frequency, color):
        circle = Circle(radius=amplitude, color=color)
        circle.add_updater(lambda c, dt: c.rotate(frequency * dt, about_point=ORIGIN))
        return circle

    def get_fourier_coeffs(self, n_terms):
        coeffs = []
        for i in range(1, 2 * n_terms, 2):
            amp = 1 / i
            freq = i
            coeffs.append((amp, freq))
        return coeffs

    def update_sum_graph(self, graph, func, alpha):
        axes = graph[0]
        new_graph = axes.plot(func, color=graph[1].get_color())
        graph[1].become(new_graph)
        return graph
