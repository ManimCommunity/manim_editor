from manim import *
from manim_editor import PresentationSectionType, IconNormal, IconSkip, IconLoop, IconCompleteLoop


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

import manim
from .config import get_config
from manim_editor import PresentationSectionType

class IconNormal(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)
        icon_normal = manim.SVGMobject(str(get_config().STATIC_DIR / "img" / "play_btn.svg"))
        self.add(icon_normal)


class IconSkip(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)
        icon_skip = manim.SVGMobject(str(get_config().STATIC_DIR / "img" / "wind.svg"))
        self.add(icon_skip)


class IconLoop(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)
        icon_loop = manim.SVGMobject(str(get_config().STATIC_DIR / "img" / "arrow_clockwise.svg"))
        self.add(icon_loop)


class IconCompleteLoop(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)
        icon_completeloop = manim.SVGMobject(str(get_config().STATIC_DIR / "img" / "hourglass_split.svg"))
        self.add(icon_completeloop)


class EditorLogo(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        triangle = manim.Triangle(color=logo_red, fill_opacity=1, z_index=10).shift(1.2*manim.RIGHT)
        square = manim.Square(color=logo_blue, fill_opacity=1, z_index=20).shift(manim.UP)
        circle = manim.Circle(color=logo_green, fill_opacity=1, z_index=30).shift(manim.LEFT)
        logo = manim.VGroup(triangle, square, circle).scale(2.5)
        logo.move_to(manim.ORIGIN)
        self.add(logo)

        l1 = manim.Rectangle(height=1.7, width=0.6, stroke_width=0, fill_opacity=1, z_index=11)
        l2 = l1.copy()
        pause = manim.VGroup(l1, l2).arrange(manim.RIGHT)
        pause.move_to(triangle.get_center_of_mass())
        self.add(pause)

        play = manim.Triangle(color=manim.WHITE, fill_opacity=1, z_index=21).rotate(-90*manim.DEGREES).move_to(square.get_center()).scale(1.5).shift(0.2*manim.RIGHT)
        self.add(play)

        inner = 1.2
        outer = 1.75
        arc = manim.Sector(arc_center=circle.get_center(), inner_radius=inner, outer_radius=outer, start_angle=-manim.PI/2, angle=-1.5*manim.PI, color=manim.WHITE, stroke_width=0, z_index=31)
        tip = manim.mobject.geometry.ArrowTriangleFilledTip(z_index=31, color=manim.WHITE, start_angle=-manim.PI/2).scale(3.5)
        tip.next_to(arc.get_right(), manim.DOWN, buff=0).shift((outer-inner)/2*manim.LEFT+0.05*manim.UP)

        loop = manim.VGroup(arc, tip).rotate(-manim.PI/16)
        self.add(loop)


class EditorBanner(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)

        logo_all = EditorLogo().scale(0.5)

        logo_black = "#343434"
        M = manim.MathTex(r"\mathbb{M}").scale(7).set_color(logo_black)
        anim = manim.Tex(r"\textbf{anim}", tex_template=manim.TexFontTemplates.gnu_freeserif_freesans).scale(7).set_color(logo_black).scale(0.75748)

        E = manim.MathTex(r"\mathbb{E}").scale(7).set_color(logo_black)
        ditor = manim.Tex(r"\textbf{ditor}", tex_template=manim.TexFontTemplates.gnu_freeserif_freesans).scale(7).set_color(logo_black).scale(0.75748)
        x = manim.VGroup(M, anim).arrange(manim.RIGHT, buff=0.1)
        y = manim.VGroup(E, ditor).arrange(manim.RIGHT, buff=0.1)
        banner = manim.VGroup(x, y, logo_all).arrange(manim.RIGHT, buff=0.5)
        anim.align_to(M, manim.DOWN)
        ditor.align_to(M, manim.DOWN)
        self.add(manim.RoundedRectangle(fill_color="#ece6e2", height=banner.get_height()+1, width=banner.get_width()+1.5, fill_opacity=1, stroke_width=0, z_index=0))
        self.add(banner)
        self.scale(0.3)

from manim import Dot,VGroup,ORANGE,BLUE,Scene, Line, linear

def make_elements():  # only setting up the mobjects
    dots = VGroup(Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), z_index=0)
    dots.arrange(buff=0.7).scale(2).set_color(BLUE)
    dots[0].set_color(ORANGE)
    dots[-1].set_color(ORANGE)
    moving_dot = Dot(color=ORANGE, z_index=1).scale(2.5)
    moving_dot.move_to(dots[0])
    path = VGroup()
    path.add_updater(
        lambda x: x.become(
            Line(dots[0], moving_dot, stroke_width=10, z_index=1, color=ORANGE)
        )
    )
    return dots, moving_dot, path
class MinimalPresentationExample(Scene):
    def construct(self):

        dots, moving_dot, path = make_elements()
        self.add(dots, moving_dot, path)

        self.next_section("A", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[1]), rate_func=linear)

        self.next_section("B", PresentationSectionType.SKIP)
        self.play(moving_dot.animate.move_to(dots[2]), rate_func=linear)

        self.next_section("C", PresentationSectionType.LOOP)
        self.play(moving_dot.animate.move_to(dots[3]), rate_func=linear)

        self.next_section("D", PresentationSectionType.COMPLETE_LOOP)
        self.play(moving_dot.animate.move_to(dots[4]), rate_func=linear)

        self.next_section("E", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[5]), rate_func=linear)



class Tutorial(Scene):
    def construct(self):
        #########
        # title #
        #########
        self.next_section("title", PresentationSectionType.NORMAL)
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait()
        self.play(Unwrite(banner))

        title = Text("Manim Editor", font_size=60).shift(2*UP)
        title_ul = Underline(title)
        self.play(Write(title), run_time=0.5)
        text = VGroup(
            Text("Press any of the usual \"next\"-keys"),
            Text("like RightArrow or PageUp"),
            Text("to go to the next section."),
            Text("You can also use the > button above."),
        ).arrange(DOWN).shift(DOWN)
        self.play(Write(text), Write(title_ul), run_time=0.5)
        self.wait()

        ##################
        # normal section #
        ##################
        self.next_section("normal section", PresentationSectionType.NORMAL)
        self.remove(title, title_ul, text)

        dot = Dot([-4, -2, 0]).scale(3)
        text = VGroup(
            Text("There are four different types of sections."),
            MarkupText("This is the first type, a <b>normal section</b>."),
            Text("The animation plays and patiently waits"),
            Text("for the speaker to finally"),
            Text("get their point across."),
        ).arrange(DOWN).shift(UP)
        self.play(FadeIn(dot), Write(text), run_time=0.5)
        self.play(dot.animate.shift(8*RIGHT), run_time=2)
        self.wait()

        ################
        # back in time #
        ################
        self.next_section("back in time", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("You can go back in time as well. Try it!"),
            Text("Don't expect any smooth"),
            Text("transitions though."),
            Text("If you want to start from the beginning,"),
            Text("reload the page."),
        ).arrange(DOWN).shift(UP)
        self.play(Write(text), run_time=0.5)
        self.play(dot.animate.shift(4*LEFT))
        self.wait()

        ##############
        # fullscreen #
        ##############
        self.next_section("fullscreen", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("Your eyes hurt from the tiny video?"),
            Text("Stop whining!"),
            Text("Or press F to enter fullscreen."),
        ).arrange(DOWN)
        self.play(FadeOut(dot), Write(text), run_time=0.5)
        self.wait()

        ######################
        # loop section intro #
        ######################
        self.next_section("loop section intro", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("Let's do something different now."),
            Text("What follows is an animation from the"),
            Text("Manim CE Gallery"),
            Text("that I ruthlessly stole :)"),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        ################
        # loop section #
        ################
        self.next_section("loop section", PresentationSectionType.LOOP)
        self.remove(text)

        text = VGroup(
            Text("This is the second type,"),
            MarkupText("a <b>loop section</b>."),
        ).arrange(DOWN).shift(2*UP)
        self.play(Write(text), run_time=0.5)

        circle = Circle(arc_center=[0, -2, 0], radius=1, color=YELLOW)
        dot = Dot([0, -2, 0])
        self.add(dot)

        line = Line([3, -2, 0], [5, -2, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(dot.animate.shift(RIGHT))
        self.play(MoveAlongPath(dot, circle), run_time=2)

        ######################
        # skip section intro #
        ######################
        self.next_section("skip section intro", PresentationSectionType.NORMAL)
        self.remove(text, dot, line, circle)

        text = VGroup(
            Text("If you payed close attention,"),
            Text("you might have noticed that"),
            Text("the animation is...fucked."),
            Text("It just cuts at the end."),
            Text("Smooth transitions look different!"),
            Text("Let me show you how it's done."),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        ################
        # skip section #
        ################
        self.next_section("skip section", PresentationSectionType.SKIP)
        self.remove(text)

        text = VGroup(
            MarkupText("This is a <b>skip section</b>"),
            Text("It functions just like a normal section"),
            Text("with the difference that it immediately"),
            Text("continues with the next section"),
            Text("once it's finished."),
        ).arrange(DOWN).shift(1.5*UP)

        self.play(Write(text), run_time=0.5)

        dot.move_to([0, -2, 0])
        self.add(line)
        self.play(GrowFromCenter(circle))
        self.play(dot.animate.shift(RIGHT))

        self.next_section("loop section after skip section", PresentationSectionType.LOOP)
        self.play(MoveAlongPath(dot, circle), run_time=2)

        #########################
        # animation fucked again#
        #########################
        self.next_section("animation fucked again", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("Let's finish the animation. Here we"),
            Text("encounter another problem: The dot"),
            Text("teleports when progressing to the"),
            Text("next section. You didn't see it?"),
            Text("Go back in time and try again."),
        ).arrange(DOWN).shift(1.5*UP)

        self.play(Write(text), Rotating(dot, about_point=[2, -2, 0]), run_time=1.5)
        self.wait()

        ###############################
        # complete loop section intro #
        ###############################
        self.next_section("complete loop section intro", PresentationSectionType.NORMAL)
        self.remove(text, dot, circle, line)

        text = VGroup(
            Text("This is where"),
            MarkupText("<b>complete loop section</b> come in."),
            Text("They are just like loop sections."),
            Text("But when the speaker continues to"),
            Text("the next section, the complete loop"),
            Text("section finishes before continuing."),
            Text("Third time's the charm:"),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        #########################
        # complete loop section #
        #########################
        self.next_section("before complete loop section", PresentationSectionType.SKIP)
        self.remove(text)

        text = VGroup(
            Text("When you go to the next section,"),
            Text("the animation finishes first."),
            Text("Enjoy some smooth transitions"),
        ).arrange(DOWN).shift(2*UP)

        dot.move_to([0, -2, 0])
        self.add(line)
        self.play(Write(text), GrowFromCenter(circle), run_time=0.5)
        self.play(dot.animate.shift(RIGHT))

        self.next_section("complete loop section", PresentationSectionType.COMPLETE_LOOP)
        self.play(MoveAlongPath(dot, circle), run_time=2)

        self.next_section("after complete loop section", PresentationSectionType.NORMAL)
        self.play(Rotating(dot, about_point=[2, -2, 0]), run_time=1.5)
        self.wait()

        ############
        # timeline #
        ############
        self.next_section("timeline", PresentationSectionType.NORMAL)
        self.remove(text, dot, circle, line)

        text = VGroup(
            Text("On the left you can see the"),
            Text("timeline. If you're in fullscreen,"),
            Text("you have to exit it first."),
            Text("To do that you can use Escape or F."),
            Text("The timeline shows the names"),
            Text("and types of all section. When"),
            Text("you click on a section on the timeline,"),
            Text("that section plays immediately."),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        self.next_section("skip sections and the timeline", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("This shows another use case for"),
            Text("skip sections:"),
            Text("Splitting up bigger animations."),
            Text("With the timeline"),
            Text("you can skip to any part of it."),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        ##########
        # github #
        ##########
        self.next_section("active development", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("This project is still under"),
            Text("active development."),
            Text("If you encounter any problems"),
            Text("or have good ideas for new features,"),
            MarkupText("please open an <b>Issue on GitHub</b>."),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        self.next_section("docs", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("On GitHub you'll find a more in-depth"),
            Text("documentation. It explains some nerdy"),
            Text("details about how the videos are"),
            Text("being played, buffered and cached."),
            Text("It also shows how to use the"),
            Text("presentation API."),
            Text("If you have any questions,"),
            Text("this is where you should look first."),
        ).arrange(DOWN)
        self.play(Write(text), run_time=0.5)
        self.wait()

        ##########
        # ending #
        ##########
        self.next_section("ending", PresentationSectionType.NORMAL)
        self.remove(text)

        text = VGroup(
            Text("You can find the code here:"),
            Text("github.com/christopher-besch/"),
            Text("manim_web_presenter"),
            Text("And as always, thanks for watching!"),
        ).arrange(DOWN).shift(1*DOWN)
        end = Text("The End", font_size=60).shift(2*UP)
        end_ul = Underline(end)
        self.play(Write(text), run_time=0.5)
        self.wait()
        self.play(Write(end), run_time=0.5)
        self.play(Write(end_ul), run_time=0.5)
        self.wait()

        ############
        # fade out #
        ############
        self.next_section("heli flying into the sunset; fade out", PresentationSectionType.NORMAL)
        self.play(Unwrite(text), Unwrite(end), Unwrite(end_ul))
        self.wait(2)

        image = ImageMobject("img.jpg")
        image.height = 9
        self.play(FadeIn(image))
        self.wait(4)
        self.remove(image)
        self.wait()
