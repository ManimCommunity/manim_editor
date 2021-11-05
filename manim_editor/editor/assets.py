import pathlib
import os
from manim import VGroup, SVGMobject

BASE_DIR = pathlib.Path(__file__).parent.absolute()


class IconNormal(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        print(os.path.join(BASE_DIR, "..", "app", "static", "img", "play_btn.svg"))
        icon_normal = SVGMobject(os.path.join(BASE_DIR, "..", "app", "static", "img", "play_btn.svg"))
        self.add(icon_normal)


class IconSkip(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_skip = SVGMobject(os.path.join(BASE_DIR, "..", "app", "static", "img", "wind.svg"))
        self.add(icon_skip)


class IconLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_loop = SVGMobject(os.path.join(BASE_DIR, "..", "app", "static", "img", "arrow_clockwise.svg"))
        self.add(icon_loop)


class IconCompleteLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_completeloop = SVGMobject(os.path.join(BASE_DIR, "..", "app", "static", "img", "hourglass_split.svg"))
        self.add(icon_completeloop)
