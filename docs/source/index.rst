.. warning::

    This documentation is a work in progress, please tread carefully.

.. _index:

Manim Editor Overview
=====================

The ``Manim Editor`` is a tool for post-processing animations generated via ``Manim``.

    Animating technical concepts is traditionally pretty tedious since it can be difficult to make the animations precise enough to convey them accurately.
    ``Manim`` uses Python to generate animations programmatically, making it possible to specify exactly how each one should run.

    -- The `Manim Documentation <https://docs.manim.community/en/stable>`__

The ``Manim Editor`` offers two main functions:

* Reliable web presentations.
* Automated video editing (not yet implemented).

.. tip::

    If you want to test the presentation output of the ``Manim Editor`` without having to install anything, take a look at the `example <https://manimeditorproject.github.io/manim_editor/Tutorial/index.html>`__.

If you don't know how to use ``Manim``, `it's documentation <https://docs.manim.community/en/stable>`__ is where you should start.
Come back once you've familiarised yourself with the core concepts.

Main Idea
*********

The ``Manim Editor`` is using the `Manim Section API <https://docs.manim.community/en/stable/tutorials/a_deeper_look.html#sections>`__.
It allows the separation of a scene into multiple sections.
In addition to that it optionally stores names and types for each section.
``Manim`` only supports the type ``DefaultSesctionType.NORMAL`` out of the box.
The ``Manim`` Editor defines more types, which define how a section should be played in the presentation.
They are described :ref:`here <create_scene>`.

Each section is equivalent to a slide from PowerPoint and can be shown individually.
Multiple sections (possibly from different ``Manim`` scenes) build one project that can be presented as a whole.
A Manim Editor project is a directory that will house everything needed to present a project.
More on that :ref:`here <create_project>`.

.. note::

    The Section API is a new feature of ``Manim`` v0.12.0;
    thus you can't use any older versions than that.

.. toctree::
   :maxdepth: 3
   :caption: Table of Contents:

   installation
   use
   internals
