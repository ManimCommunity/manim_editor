import manim

from .config import get_config

__all__ = ["IconNormal", "IconSkip", "IconLoop", "IconCompleteLoop", "EditorLogo", "EditorBanner"]


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
        triangle = manim.Triangle(color=logo_red, fill_opacity=1, z_index=10).shift(1.2 * manim.RIGHT)
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

        play = (
            manim.Triangle(color=manim.WHITE, fill_opacity=1, z_index=21)
            .rotate(-90 * manim.DEGREES)
            .move_to(square.get_center())
            .scale(1.5)
            .shift(0.2 * manim.RIGHT)
        )
        self.add(play)

        inner = 1.2
        outer = 1.75
        arc = manim.Sector(
            arc_center=circle.get_center(),
            inner_radius=inner,
            outer_radius=outer,
            start_angle=-manim.PI / 2,
            angle=-1.5 * manim.PI,
            color=manim.WHITE,
            stroke_width=0,
            z_index=31,
        )
        tip = manim.mobject.geometry.ArrowTriangleFilledTip(z_index=31, color=manim.WHITE, start_angle=-manim.PI / 2).scale(3.5)
        tip.next_to(arc.get_right(), manim.DOWN, buff=0).shift((outer - inner) / 2 * manim.LEFT + 0.05 * manim.UP)

        loop = manim.VGroup(arc, tip).rotate(-manim.PI / 16)
        self.add(loop)


class EditorBanner(manim.VGroup):
    def __init__(self):
        manim.VGroup.__init__(self)

        logo_all = EditorLogo().scale(0.5)

        logo_black = "#343434"
        M = manim.MathTex(r"\mathbb{M}").scale(7).set_color(logo_black)
        anim = (
            manim.Tex(r"\textbf{anim}", tex_template=manim.TexFontTemplates.gnu_freeserif_freesans)
            .scale(7)
            .set_color(logo_black)
            .scale(0.75748)
        )

        E = manim.MathTex(r"\mathbb{E}").scale(7).set_color(logo_black)
        ditor = (
            manim.Tex(r"\textbf{ditor}", tex_template=manim.TexFontTemplates.gnu_freeserif_freesans)
            .scale(7)
            .set_color(logo_black)
            .scale(0.75748)
        )
        x = manim.VGroup(M, anim).arrange(manim.RIGHT, buff=0.1)
        y = manim.VGroup(E, ditor).arrange(manim.RIGHT, buff=0.1)
        banner = manim.VGroup(x, y, logo_all).arrange(manim.RIGHT, buff=0.5)
        anim.align_to(M, manim.DOWN)
        ditor.align_to(M, manim.DOWN)
        self.add(
            manim.RoundedRectangle(
                fill_color="#ece6e2",
                height=banner.get_height() + 1,
                width=banner.get_width() + 1.5,
                fill_opacity=1,
                stroke_width=0,
                z_index=0,
            )
        )
        self.add(banner)
        self.scale(0.3)
