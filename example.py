from manim import *

from manim_editor import (
    EditorBanner,
    IconCompleteLoop,
    IconLoop,
    IconNormal,
    IconSkip,
    PresentationSectionType,
)


class IconTest(Scene):
    def construct(self):
        self.add(VGroup(IconNormal(), IconSkip(), IconLoop(), IconCompleteLoop()).arrange(RIGHT))


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


def make_elements():  # only setting up the mobjects
    dots = VGroup(Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), z_index=0)
    dots.arrange(buff=0.7).scale(2).set_color(BLUE)
    dots[0].set_color(ORANGE)
    dots[-1].set_color(ORANGE)
    moving_dot = Dot(color=ORANGE, z_index=1).scale(2.5)
    moving_dot.move_to(dots[0])
    path = VGroup()
    path.add_updater(lambda x: x.become(Line(dots[0], moving_dot, stroke_width=10, z_index=1, color=ORANGE)))
    return dots, moving_dot, path


class MinimalPresentationExample(Scene):
    def construct(self):

        dots, moving_dot, path = make_elements()
        self.add(dots, moving_dot, path)

        self.next_section("A", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[1]), rate_func=linear)

        self.next_section("A.1", PresentationSectionType.SUB_NORMAL)
        self.play(moving_dot.animate.move_to(dots[2]), rate_func=linear)

        self.next_section("B", PresentationSectionType.SKIP)
        self.play(moving_dot.animate.move_to(dots[3]), rate_func=linear)

        self.next_section("C", PresentationSectionType.LOOP)
        self.play(moving_dot.animate.move_to(dots[4]), rate_func=linear)

        self.next_section("D", PresentationSectionType.COMPLETE_LOOP)
        self.play(moving_dot.animate.move_to(dots[5]), rate_func=linear)

        self.next_section("E", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[6]), rate_func=linear)


def setup_slider():
    dots = VGroup(Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), z_index=5)  # < z_index broken with updaters!

    dots.arrange(buff=0.5).scale(2).set_color(BLUE).shift(2.5 * DOWN)
    dots[0].set_color(ORANGE)
    dots[-1].set_color(ORANGE)
    l = Line(dots[0], dots[-1], stroke_width=10, stroke_opacity=0.5, z_index=0, color=WHITE)

    icons = VGroup(
        IconNormal(), IconNormal(), IconSkip(), IconNormal(), IconLoop(), IconNormal(), IconCompleteLoop(), IconNormal()
    ).scale(0.2)
    for val, icon in enumerate(icons):
        icon.move_to(VGroup(dots[val], dots[val + 1]).get_center()).shift(0.4 * DOWN)

    moving_dot = Dot(color=ORANGE, z_index=1).scale(2.5)
    path = VGroup(z_index=0)
    path.add_updater(lambda x: x.become(Line(dots[0], moving_dot, stroke_width=10, z_index=2, color=ORANGE)))
    slider_number = Integer(1).scale(2).to_corner(DR)

    moving_dot.move_to(dots[0])
    moving_dot.x0 = 0
    moving_dot.x1 = 0
    moving_dot.FRACTION = 0

    def my_updater(mobj, dt):
        dt = 1 / config.frame_rate
        mobj.set_x(mobj.x0 + mobj.FRACTION * (mobj.x1 - mobj.x0))
        mobj.FRACTION += dt / mobj.run_time

    moving_dot.add_updater(my_updater)
    return dots, icons, moving_dot, l, path, slider_number


class IconArray(VGroup):
    def __init__(self):
        def get_offset(text):
            y1 = text[0][0].get_y()  # fist letter
            y2 = text.get_y()  # whole word
            return y1 - y2

        super().__init__()
        fac = 0.25
        pos = VGroup(*[Dot() for i in range(0, 4)]).arrange(DOWN, buff=0.7)
        icon_normal = IconNormal().scale(fac).next_to(pos[0], LEFT)
        t1 = Text("Normal").next_to(icon_normal)
        t1.shift(DOWN * get_offset(t1))
        icon_normal.add(t1)

        icon_skip = IconSkip().scale(fac).next_to(pos[1], LEFT)
        t2 = Text("Skip").next_to(icon_skip)
        t2.shift(DOWN * get_offset(t2))
        icon_skip.add(t2)

        icon_loop = IconLoop().scale(fac).next_to(pos[2], LEFT)
        t3 = Text("Loop").next_to(icon_loop)
        t3.shift(DOWN * get_offset(t3))
        icon_loop.add(t3)

        icon_completeloop = IconCompleteLoop().scale(fac).next_to(pos[3], LEFT)
        t4 = Text("Complete Loop").next_to(icon_completeloop)
        t4.shift(DOWN * get_offset(t4))

        icon_completeloop.add(t4)
        self.add(icon_normal, icon_skip, icon_loop, icon_completeloop)
        self.move_to(ORIGIN)


class TitleLine(VGroup):
    def __init__(self):
        super().__init__()
        line = Line(LEFT, RIGHT)
        line.width = config["frame_width"] - 4
        line.to_edge(UP, buff=2)
        self.add(line)


class Tutorial(Scene):
    def construct(self):

        dots, icons, moving_dot, l, path, slider_number = setup_slider()
        self.add(icons, moving_dot, l, path, slider_number, dots)

        #################################################################

        self.next_section("A", PresentationSectionType.NORMAL, skip_animations=False)
        slider_number.set_value(1)
        moving_dot.x0 = dots[0].get_x()
        moving_dot.x1 = dots[1].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 8
        banner = EditorBanner().scale(1.2)
        self.play(FadeIn(banner, scale=1.5, shift=DOWN))
        self.play(banner.animate.shift(2.5 * UP))
        A1 = "Welcome! This presentation will guide you through the 4 provided section types."
        A1 = Text(A1).scale(0.5)
        A2 = IconArray().scale(0.7)
        A2.add(SurroundingRectangle(A2, stroke_color=BLUE, corner_radius=0.1, buff=0.2))
        VGroup(A1, A2).arrange(DOWN).next_to(banner, DOWN)
        self.play(Write(A1), run_time=2)
        self.play(FadeIn(A2))
        self.wait(3)
        self.remove(banner, A1, A2)

        #################################################################

        self.next_section("B", PresentationSectionType.NORMAL, skip_animations=False)
        slider_number.set_value(2)
        moving_dot.x0 = dots[1].get_x()
        moving_dot.x1 = dots[2].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 4

        line = TitleLine()
        t1 = Text("Introducing:")
        t2 = IconArray()[0]
        t2.add(SurroundingRectangle(t2, stroke_color=BLUE, corner_radius=0.1, buff=0.2))
        t12 = VGroup(t1, t2).arrange(RIGHT)
        t12.next_to(line, UP)

        t3 = (
            VGroup(
                Text('Press any of the usual "next slide"-keys'),
                Text("like RightArrow or PageUp"),
                Text("to go to the next section."),
                Text("You can also use the controls on the right."),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(line, DOWN, buff=0.7)
        )
        self.add(line, t12, t3)
        self.wait(4)
        self.remove(t12, t3)

        #################################################################

        self.next_section("C", PresentationSectionType.SKIP, skip_animations=False)
        slider_number.set_value(3)
        moving_dot.x0 = dots[2].get_x()
        moving_dot.x1 = dots[3].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 4

        # line = TitleLine()
        t1 = Text("Introducing:")
        t2 = IconArray()[1]
        t2.add(SurroundingRectangle(t2, stroke_color=BLUE, corner_radius=0.1, buff=0.2))
        t12 = VGroup(t1, t2).arrange(RIGHT)
        t12.next_to(line, UP)
        t3 = (
            VGroup(
                Text("When the video of the skip section has finished "),
                Text("it automatically continues with the next."),
                Text("No user input required."),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(line, DOWN, buff=0.7)
        )
        self.add(t12, t3)
        self.wait(2)
        wind = IconSkip().set_style(fill_opacity=0).shift(2 * LEFT).scale(1.9)
        wind.my_opactiy = 0
        wind.coming = True

        def wind_updater(mobj, dt):
            if wind.coming:
                if mobj.my_opactiy < 0.4:
                    mobj.my_opactiy += dt
            if not wind.coming:
                if mobj.my_opactiy > 0:
                    mobj.my_opactiy -= dt
            mobj.set_style(fill_opacity=mobj.my_opactiy)

        wind.add_updater(wind_updater)
        wind.add_updater(lambda x: x.shift(0.02 * RIGHT))
        self.add(wind)
        self.wait(2)

        #################################################################

        self.next_section("D", PresentationSectionType.NORMAL, skip_animations=False)
        slider_number.set_value(4)
        moving_dot.x0 = dots[3].get_x()
        moving_dot.x1 = dots[4].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 3

        self.wait(1)
        wind.coming = False
        self.wait(2)
        wind.clear_updaters()
        self.remove(wind)
        self.remove(t12, t3)

        #################################################################

        self.next_section("E", PresentationSectionType.LOOP, skip_animations=False)
        slider_number.set_value(5)
        moving_dot.x0 = dots[4].get_x()
        moving_dot.x1 = dots[5].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 3

        t1 = Text("Introducing:")
        t2 = IconArray()[2]
        t2.add(SurroundingRectangle(t2, stroke_color=BLUE, corner_radius=0.1, buff=0.2))
        t12 = VGroup(t1, t2).arrange(RIGHT)
        t12.next_to(line, UP)
        t3 = (
            VGroup(
                Text("Its looping!"),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(line, DOWN, buff=0.7)
        )
        self.add(t12, t3)

        iconloop = IconLoop().set_style(fill_opacity=0.8)
        iconloop.stroke_opacity = 0.8

        iconloop.add_updater(lambda x, dt: x.rotate(-dt / 3 * TAU, about_point=ORIGIN - 0.16 * UP))

        self.add(iconloop)
        self.wait(3)

        #################################################################

        self.next_section("F", PresentationSectionType.NORMAL, skip_animations=False)
        slider_number.set_value(6)
        moving_dot.x0 = dots[5].get_x()
        moving_dot.x1 = dots[6].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 6

        t3b = (
            VGroup(
                Text("There won't be any smooth transitions"),
                Text("when continuing to the next section though."),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(line, DOWN, buff=0.7)
        )
        t3.become(t3b)
        self.wait(0.5)
        iconloop.add_updater(lambda x, dt: x.set_opacity(x.stroke_opacity - dt))
        self.wait(2)

        t4 = (
            VGroup(
                Text("This is where Complete Loop Sections come in."),
            )
            .scale(0.7)
            .next_to(t3, DOWN, buff=0.7)
        )
        self.add(t4)
        self.wait(3.5)
        self.remove(t12, t3, t4)

        #################################################################

        self.next_section("G", PresentationSectionType.COMPLETE_LOOP, skip_animations=False)
        slider_number.set_value(7)
        moving_dot.x0 = dots[6].get_x()
        moving_dot.x1 = dots[7].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 3

        t1 = Text("Introducing:")
        t2 = IconArray()[3]
        t2.add(SurroundingRectangle(t2, stroke_color=BLUE, corner_radius=0.1, buff=0.2))
        t12 = VGroup(t1, t2).arrange(RIGHT)
        t12.next_to(line, UP)
        t3 = (
            VGroup(
                Text("When continuing to the next section,"),
                Text("all animations of this section finish first."),
                Text("Enjoy some smooth transitions!"),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(line, DOWN, buff=0.7)
        )
        self.add(t12, t3)

        iconcompleteloop = IconCompleteLoop().set_style(fill_opacity=0.8)
        iconcompleteloop.stroke_opacity = 0.8
        iconcompleteloop.add_updater(lambda x, dt: x.rotate(-dt / 3 * TAU))

        self.add(iconcompleteloop)
        self.wait(3)

        #################################################################

        self.next_section("H", PresentationSectionType.NORMAL, skip_animations=False)
        slider_number.set_value(8)
        moving_dot.x0 = dots[7].get_x()
        moving_dot.x1 = dots[8].get_x()
        moving_dot.FRACTION = 0
        moving_dot.run_time = 8

        iconcompleteloop.add_updater(lambda x, dt: x.set_opacity(x.stroke_opacity - dt))
        self.wait(2)
        iconcompleteloop.clear_updaters()
        self.play(Unwrite(VGroup(t3, t12, line)), run_time=1)
        self.play(Write(Text("THE END").scale(4)), run_time=2)
        self.wait(3)
