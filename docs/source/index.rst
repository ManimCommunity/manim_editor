.. warning::

    This documentation is a work in progress, please tread carefully.

Manim Editor Overview
=====================

The ``Manim Editor`` is a tool for post-processing animations generated via ``Manim``.

    Animating technical concepts is traditionally pretty tedious since it can be difficult to make the animations precise enough to convey them accurately.
    ``Manim`` uses Python to generate animations programmatically, making it possible to specify exactly how each one should run.

    -- The `Manim Documentation <https://docs.manim.community/en/stable>`_

The ``Manim Editor`` offers two main functions:

* Reliable web presentations.
* Automated video editing (not yet implemented).

.. tip::

    If you want to test the presentation output of the ``Manim Editor`` without having to install anything, take a look at the `example <https://manimeditorproject.github.io/manim_editor/Tutorial/index.html>`_.

If you don't know how to use ``Manim``, `it's documentation <https://docs.manim.community/en/stable>`_ is where you should start.
Come back once you've familiarised yourself with the core concepts.

Main Idea
*********

The ``Manim Editor`` is using the `Manim Section API <https://docs.manim.community/en/stable/tutorials/a_deeper_look.html#sections>`_.
It allows the separation of a scene into multiple sections.
In addition to that it optionally stores names and types for each section.
``Manim`` only supports the type ``DefaultSesctionType.NORMAL`` out of the box.
The ``Manim`` Editor defines more types, which define how a section should be played in the presentation.
They are described `here <use/create_scene>`_.

Each section is equivalent to a slide from PowerPoint and can be shown individually.
Multiple sections (possibly from different ``Manim`` scenes) build one project that can be presented as a whole.
A Manim Editor project is a directory that will house everything needed to present a project.
More on that `here <use/create_project>`_.

.. note::

    The Section API is a new feature of ``Manim`` v0.12.0;
    thus you can't use any older versions than that.

.. Why the Manim Editor has Value
.. ******************************

.. ``Manim`` is one of the best ways of explaining complicated concepts with the precision of a programmatic approach.
.. This precision has value not just for videos with a voice over but also for presentations.
.. Everyone knows what a pain aligning graphics in PowerPoint is.
.. That's were the ``Manim Editor`` comes into play:
.. It allows the user to reliably present her pretty (and technically accurate) animations live in front of an audience.

.. "OK I get that, but why do I have to use the web to do that?", you ask?
.. How often do computers fail?
.. What if the laptop you were planning on using for your presentation runs out of battery and no one has a matching power adaptor?
.. What if it thinks performing an update right now is more important than your precious presentation?
.. Or what if it simply refuses to open your application of choice because it's suffering a sudden identity crisis?

.. In a situation like this the ``Manim Editor`` allows you to use any other non-dead internet-capable device.
.. After all the presenter is running on the web, the software required to give your presentation is already installed on most devices, a modern web browser.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   use
   internals
