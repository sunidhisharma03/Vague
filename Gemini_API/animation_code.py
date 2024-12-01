from manim import *

class QuadraticEquationSolution(Scene):
    def construct(self):
        # Title
        title = Tex("Solving Quadratic Equations").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(1)

        # Equation
        equation = MathTex("ax^2 + bx + c = 0")
        self.play(Write(equation))
        self.wait(1)

        # Explanation of coefficients
        a_label = MathTex("a", color=YELLOW).next_to(equation[0][0], DOWN, buff=0.3) # Access parts correctly
        b_label = MathTex("b", color=YELLOW).next_to(equation[0][1], DOWN, buff=0.3)
        c_label = MathTex("c", color=YELLOW).next_to(equation[0][2], DOWN, buff=0.3)

        #Improved layout.  Added brackets to improve visual separation between terms.
        equation_bracketed = MathTex("(a)x^2", "+", "(b)x", "+", "(c) = 0")
        a_label = MathTex("a", color=YELLOW).next_to(equation_bracketed[0], DOWN, buff=0.3)
        b_label = MathTex("b", color=YELLOW).next_to(equation_bracketed[2], DOWN, buff=0.3)
        c_label = MathTex("c", color=YELLOW).next_to(equation_bracketed[4], DOWN, buff=0.3)


        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(2)

        #Further explanations can be added here (e.g., Quadratic Formula, examples)