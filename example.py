from manim import *


class Test(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle)
        self.wait()
        self.next_section()
        self.add(square)
        self.wait()
        self.next_section()
        self.remove(circle)
        self.wait()
        self.next_section()
        self.remove(square)
        self.wait()
