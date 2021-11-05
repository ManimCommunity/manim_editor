from manim import *
from manim.mobject.geometry import ArrowTriangleFilledTip

from manim_editor import PresentationSectionType, IconNormal, IconSkip, IconLoop, IconCompleteLoop


class IconTest(Scene):
    def construct(self):
        self.add(VGroup(IconNormal(), IconSkip(), IconLoop(), IconCompleteLoop()).arrange(RIGHT))


class ManimEditorSquareLogo(ZoomedScene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        triangle = Triangle(color=logo_red, fill_opacity=1, z_index=10).shift(1.2*RIGHT)
        square = Square(color=logo_blue, fill_opacity=1, z_index=20).shift(UP)
        circle = Circle(color=logo_green, fill_opacity=1, z_index=30).shift(LEFT)
        logo = VGroup(triangle, square, circle).scale(2.5)
        logo.move_to(ORIGIN)
        self.add(logo)

        l1 = Rectangle(height=1.7, width=0.6, stroke_width=0, fill_opacity=1, z_index=11)
        l2 = l1.copy()
        pause = VGroup(l1, l2).arrange(RIGHT)
        pause.move_to(triangle.get_center_of_mass())
        self.add(pause)

        play = Triangle(color=WHITE, fill_opacity=1, z_index=21).rotate(-90*DEGREES).move_to(square.get_center()).scale(1.5).shift(0.2*RIGHT)
        self.add(play)

        arc = Arc(arc_center=circle.get_center(), radius=1.3, start_angle=-PI/16-PI/2, angle=-1.5*PI, color=WHITE, stroke_width=35, z_index=31)
        tip = ArrowTriangleFilledTip(z_index=31, color=WHITE, start_angle=-PI/16-PI/2).scale(3)
        tip.next_to(arc.get_end(), DOWN, buff=-0.1)

        loop = VGroup(arc, tip)
        self.add(loop)
        self.camera.frame.scale(0.8)  # needs ZoomedScene


class ManimEditorFullLogo(ZoomedScene):
    def construct(self):
        self.camera.background_color = BLACK
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        triangle = Triangle(color=logo_red, fill_opacity=1, z_index=10).shift(1.2*RIGHT)
        square = Square(color=logo_blue, fill_opacity=1, z_index=20).shift(UP)
        circle = Circle(color=logo_green, fill_opacity=1, z_index=30).shift(LEFT)
        logo = VGroup(triangle, square, circle).scale(2.5)
        logo.move_to(ORIGIN)
        self.add(logo)

        l1 = Rectangle(height=1.7, width=0.6, stroke_width=0, fill_opacity=1, z_index=11)
        l2 = l1.copy()
        pause = VGroup(l1, l2).arrange(RIGHT)
        pause.move_to(triangle.get_center_of_mass())
        self.add(pause)

        play = Triangle(color=WHITE, fill_opacity=1, z_index=21).rotate(-90*DEGREES).move_to(square.get_center()).scale(1.5).shift(0.2*RIGHT)
        self.add(play)

        arc = Arc(arc_center=circle.get_center(), radius=1.3, start_angle=-PI/16-PI/2, angle=-1.5*PI, color=WHITE, stroke_width=35, z_index=31)
        tip = ArrowTriangleFilledTip(z_index=31, color=WHITE, start_angle=-PI/16-PI/2).scale(3)
        tip.next_to(arc.get_end(), DOWN, buff=-0.1)

        loop = VGroup(arc, tip)
        self.add(loop)
        logo_all = VGroup(logo, play, pause, loop).scale(0.5)
        self.camera.frame.scale(1.8)  # needs ZoomedScene

        logo_black = "#343434"
        M = MathTex(r"\mathbb{M}").scale(7).set_color(logo_black)
        anim = Tex(r"\textbf{anim}", tex_template=TexFontTemplates.gnu_freeserif_freesans).scale(7).set_color(logo_black).scale(0.75748)

        E = MathTex(r"\mathbb{E}").scale(7).set_color(logo_black)
        ditor = Tex(r"\textbf{ditor}", tex_template=TexFontTemplates.gnu_freeserif_freesans).scale(7).set_color(logo_black).scale(0.75748)
        x = VGroup(M, anim).arrange(RIGHT, buff=0.1)
        y = VGroup(E, ditor).arrange(RIGHT, buff=0.1)
        VGroup(x, y, logo_all).arrange(RIGHT, buff=0.5)
        anim.align_to(M, DOWN)
        ditor.align_to(M, DOWN)
        self.add(x, y)


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
