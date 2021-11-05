import os
from manim import VGroup, SVGMobject
from .config import get_config


class IconNormal(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_normal = SVGMobject(os.path.join(get_config().STATIC_DIR, "img", "play_btn.svg"))
        self.add(icon_normal)


class IconSkip(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_skip = SVGMobject(os.path.join(get_config().STATIC_DIR, "img", "wind.svg"))
        self.add(icon_skip)


class IconLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_loop = SVGMobject(os.path.join(get_config().STATIC_DIR, "img", "arrow_clockwise.svg"))
        self.add(icon_loop)


class IconCompleteLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_completeloop = SVGMobject(os.path.join(get_config().STATIC_DIR, "img", "hourglass_split.svg"))
        self.add(icon_completeloop)
