Creating the Manim Scene
========================

Once you have `installed the Manim Editor <installation>` you can start it by using `manedit`.

The first thing you have to take care of is your Manim scene.
What you have to take care of is the type of each section.
The Manim Editor defines four types, which can be imported using ``from manim_editor import PresentationSectionType``.

These types are explained in the `interactive tutorial <https://manimeditorproject.github.io/manim_editor/tutorial/>`_.

.. table:: Types defined by the Manim Editor

   :widths: auto
   =============  ==============================================================================
   Name           Function
   =============  ==============================================================================
   NORMAL         start, end, wait for continuation by user
   SKIP           start, end, immediately continue to next slide
   LOOP           start, end, restart, immediately continue to next slide when continued by user
   COMPLETE_LOOP  start, end, restart, when user continues finish animation first

With this information you can create a Manim scene with the correct types like this:

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
Otherwise the Manim Editor won't find anything to work with.

This creates a ``media`` directory in the current working directory (CWD).

Launching the Manim Editor
..........................

The Manim Editor searches the current working directory (CWD) for Manim scenes.
Therefore you should run the ``manedit`` command where your ``media`` folder has been created.

That that command launches a local web server on an open port.
It presents an address which you can open in your browser.
Here you can select any Manim Editor Projects you have created.
These projects house everything needed to present a project, including
