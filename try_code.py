# from manim import *

# class QuadraticEquationSolver(Scene):
#     def construct(self):
#         # Equation
#         equation = MathTex("ax^2 + bx + c = 0").scale(1.5)
#         self.play(Write(equation))
#         self.wait(1)
#         self.play(FadeOut(equation))

#         # Coefficients
#         a, b, c = 2, -5, 2
#         coefficients = MathTex(f"a = {a}, b = {b}, c = {c}").scale(1.2)
#         self.play(Write(coefficients))
#         self.wait(1)


#         # Quadratic Formula
#         formula = MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}").scale(1.2)
#         self.play(TransformMatchingTex(coefficients, formula))
#         self.wait(1)
#         self.play(FadeOut(formula))

#         # Substitution
#         substitution = MathTex(r"x = \frac{-(-5) \pm \sqrt{(-5)^2 - 4(2)(2)}}{2(2)}").scale(1.2)
#         self.play(Write(substitution))
#         self.wait(1)
#         self.play(FadeOut(substitution))

#         # Simplification
#         simplification1 = MathTex(r"x = \frac{5 \pm \sqrt{25 - 16}}{4}").scale(1.2)
#         self.play(TransformMatchingTex(substitution, simplification1))
#         self.wait(1)
#         self.play(FadeOut(simplification1))

#         simplification2 = MathTex(r"x = \frac{5 \pm \sqrt{9}}{4}").scale(1.2)
#         self.play(TransformMatchingTex(simplification1, simplification2))
#         self.wait(1)
#         self.play(FadeOut(simplification2))

#         # Solutions
#         solution1 = MathTex(r"x_1 = \frac{5 + 3}{4} = 2").scale(1.2)
#         solution2 = MathTex(r"x_2 = \frac{5 - 3}{4} = \frac{1}{2}").scale(1.2)
#         solutions = VGroup(solution1, solution2).arrange(DOWN)
#         self.play(Write(solutions))
#         self.wait(1)


#         # Graph
#         axes = Axes(x_range=[-1, 3, 1], y_range=[-1, 5, 1], axis_config={"include_numbers": True})
#         parabola = axes.plot(lambda x: 2*x**2 - 5*x + 2, color=YELLOW)
#         roots = [0.5, 2]
#         root_dots = VGroup(*[Dot(axes.c2p(root, 0), color=RED) for root in roots])
#         self.play(Create(axes), Create(parabola), Create(root_dots))
#         self.wait(2)


#         self.play(*[FadeOut(mob) for mob in self.mobjects])
from manim import *

class ProjectileMotion(Scene):
    def construct(self):
        # --- Scene Setup ---
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": True}
        )
        labels = axes.get_axis_labels(x_label="x (m)", y_label="y (m)")

        # --- Physics and Calculations ---
        g = 9.81  # Acceleration due to gravity (m/s^2)
        v0 = 10  # Initial velocity (m/s)
        theta = PI / 4  # Launch angle (radians)

        t = np.linspace(0, 2 * v0 * np.sin(theta) / g, 100) # Time vector

        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * g * t**2

        path = ParametricFunction(lambda t: axes.c2p(v0 * np.cos(theta) * t, v0 * np.sin(theta) * t - 0.5 * g * t**2), t_range=[0, 2 * v0 * np.sin(theta) / g])
        projectile = Dot(color=YELLOW)

        # --- Object and Path Animations ---
        self.play(Create(axes), Create(labels))
        self.play(Create(path))

        projectile.move_to(axes.c2p(0,0)) #Starting Position
        self.play(
            MoveAlongPath(projectile, path),
            run_time=2 # Adjust animation speed
        )

        # --- Dynamic Elements ---
        velocity_vector = Arrow(start=axes.c2p(0,0), end=axes.c2p(v0*np.cos(theta),v0*np.sin(theta)), color=RED, buff=0)
        self.play(Create(velocity_vector))

        # --- Concept-Specific Features ---
        max_height_point = axes.c2p(x[np.argmax(y)], np.max(y))
        max_height_label = Tex("Max Height").next_to(max_height_point, UP)
        self.play(
            Indicate(max_height_point),
            Create(max_height_label)
        )


        # ---Scene Transitions (Example)---
        self.wait(1)


        # ---Error Prevention - Example (check for valid attributes before use)---
        if hasattr(projectile, "move_to"):
          self.play(projectile.move_to(axes.c2p(x[-1],y[-1]))) # Move projectile to end position
        else:
          print("Error: projectile object does not have move_to method")


        self.wait(2)