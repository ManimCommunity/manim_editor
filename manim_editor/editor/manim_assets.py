from manim import VGroup, SVGMobject

class IconNormal(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_normal = SVGMobject("play-btn.svg")
        self.add(icon_normal)

class IconSkip(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_skip = SVGMobject("wind.svg")
        self.add(icon_skip)

class IconLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_loop = SVGMobject("arrow-clockwise.svg")
        self.add(icon_loop)

class IconCompleteLoop(VGroup):
    def __init__(self):
        VGroup.__init__(self)
        icon_completeloop = SVGMobject("hourglass-split.svg")
        self.add(icon_completeloop)


