.. _create_scene:

Creating the Manim Scene
========================

Basics
******

The first thing you have to take care of is your ``Manim`` scene.
You have to be aware of the different types each section can have.
These types are defined by the ``Manim Editor`` and can be imported using ``from manim_editor import PresentationSectionType``.

Four types (and four secondary types) are provided:

.. table:: Types defined by the ``Manim Editor``
   :widths: auto

   =====================  ================================================================================
   Name                   Function
   =====================  ================================================================================
   ``NORMAL``             start, end, wait for continuation by user
   ``SKIP``               start, end, immediately continue to next section
   ``LOOP``               start, end, restart, immediately continue to next section when continued by user
   ``COMPLETE_LOOP``      start, end, restart, when user continues finish animation first
   ``SUB_NORMAL``         same as ``NORMAL`` but as sub section
   ``SUB_SKIP``           same as ``SKIP`` but as sub section
   ``SUB_LOOP``           same as ``LOOP`` but as sub section
   ``SUB_COMPLETE_LOOP``  same as ``COMPLETE_LOOP`` but as sub section
   =====================  ================================================================================

They are also explained in the `interactive tutorial <https://manimcommunity.github.io/manim_editor/Tutorial/index.html>`__.
Sub sections are sections that don't get listed in the timeline.
They belong to the slide of the last full section.
If you don't need sub sections you can simply ignore this feature.
When there are no sub sections, sections and slides are synonymous.

With this information you can create a ``Manim`` scene with the correct types like this:

.. code-block:: python

   from manim import *
   from manim_editor import PresentationSectionType

   class Test(Scene):
       def construct(self):
           self.next_section(type=PresentationSectionType.NORMAL)
           # play some animations...
           self.next_section("Names are still supported.", type=PresentationSectionType.SKIP)
           # play more animations...

When you have defined your scene, you have to render it like this:

.. code-block:: bash

   manim --save_sections example.py

It is essential that you use the ``--save_sections`` flag.
Otherwise the ``Manim Editor`` won't find anything to work with.

This creates a ``media`` directory in the current working directory (CWD).

You can create as many scenes as your heart desires, they should only be created in the ``media`` directory.
That way they can be used together for the same project.
Once you're happy with your scene, you can :ref:`create the Manim Editor project <create_project>`.

Minimal Example
***************

You can run the following minimal example, to get your first presentation.
It results in `this presentation <https://manimcommunity.github.io/manim_editor/MinimalPresentationExample/index.html>`__.

.. code-block:: python

   from manim import *
   from manim_editor import PresentationSectionType

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
