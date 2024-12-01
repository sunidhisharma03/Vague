from manim import *

class LorentzTransformation(Scene):
    def construct(self):
        equation = MathTex(
            "x' = \gamma(x - vt)"
        )
        self.play(Write(equation))
        self.wait(2)
        self.play(Write("v = 0.0"))
        self.wait(1)
        self.play(Write("v = 0.1"))
        self.wait(1)
        self.play(Write("v = 0.2"))
        self.wait(1)
        self.play(Write("v = 0.3"))
        self.wait(1)
        self.play(Write("v = 0.4"))
        self.wait(1)
        self.play(Write("v = 0.5"))
        self.wait(1)
        self.play(Write("v = 0.6"))
        self.wait(1)

        self.play(Write("v = 0.8"))
        self.wait(1)
        self.play(Write("v = 0.9"))