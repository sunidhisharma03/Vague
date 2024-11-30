from manim import *

class QuadraticEquationSolver(Scene):
    def construct(self):
        # Equation (MathTex ensures it can be used in TransformMatchingTex)
        equation = MathTex("ax^2 + bx + c = 0").scale(1.5)
        self.play(Write(equation))
        self.wait(1)

        # Quadratic Formula
        formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
        ).scale(1.2).to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # Example Equation (Make sure this is MathTex as well)
        example = MathTex("2x^2 + 5x + 2 = 0").next_to(equation, DOWN, buff=1)
        self.play(Write(example))
        self.wait(1)

        # Extract coefficients as MathTex (not Integer or other types)
        a = MathTex("2").set_color(YELLOW).next_to(example, RIGHT, buff=0.5)
        b = MathTex("5").set_color(YELLOW).next_to(a, RIGHT, buff=0.5)
        c = MathTex("2").set_color(YELLOW).next_to(b, RIGHT, buff=0.5)
        coef_group = VGroup(a, b, c)

        # Transform matching text objects
        self.play(TransformMatchingTex(example[0:1], a),
                  TransformMatchingTex(example[3:4], b),
                  TransformMatchingTex(example[6:7], c))
        self.wait(1)
        self.play(FadeOut(example))
        
        # Substitute into the formula (using MathTex)
        substituted_formula = MathTex(
            "x = \\frac{-5 \\pm \\sqrt{5^2 - 4(2)(2)}}{2(2)}"
        ).scale(1.2).next_to(formula, DOWN, buff=1)

        self.play(TransformMatchingTex(formula, substituted_formula))
        self.wait(1)

        # Simplify steps (keep all as MathTex)
        step1 = MathTex("x = \\frac{-5 \\pm \\sqrt{25 - 16}}{4}").next_to(substituted_formula, DOWN, buff=1)
        step2 = MathTex("x = \\frac{-5 \\pm \\sqrt{9}}{4}").next_to(step1, DOWN, buff=1)
        step3 = MathTex("x = \\frac{-5 \\pm 3}{4}").next_to(step2, DOWN, buff=1)

        self.play(TransformMatchingTex(substituted_formula, step1))
        self.wait(1)
        self.play(TransformMatchingTex(step1, step2))
        self.wait(1)
        self.play(TransformMatchingTex(step2, step3))
        self.wait(1)

        # Solutions
        solution1 = MathTex("x_1 = \\frac{-5 + 3}{4} = \\frac{-2}{4} = -\\frac{1}{2}").next_to(step3, DOWN, buff=1)
        solution2 = MathTex("x_2 = \\frac{-5 - 3}{4} = \\frac{-8}{4} = -2").next_to(solution1, DOWN, buff=1)

        self.play(Write(solution1))
        self.wait(1)
        self.play(Write(solution2))
        self.wait(2)

        # Final Display 
        final_display = VGroup(equation, formula, solution1, solution2)
        self.play(final_display.arrange(DOWN, buff=1).scale(0.8).center())
        self.wait(3)
