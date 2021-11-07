.. _create_project:

Create a New Project
====================

Once you have :ref:`installed the Manim Editor <installation>` you can start it by running `manedit`.

.. tip::

    If the `manedit` command fails, try running `python3 -m manim_editor` instead.

The ``Manim Editor`` searches the current working directory (CWD) for ``Manim`` scenes which have been rendered using the ``--save_sections`` flag.
Therefore you should run the ``manedit`` command where your ``media`` folder has been created.

That command launches a local web server on an open port.
It presents an address which you can open in your browser.
Here you can select any ``Manim Editor`` Projects you have already created.

When you create a new project, the editor asks you to select the scenes you want to be included in the new project.
The order of the scenes can be adjusted with the priority; the smaller the priority the earlier that scene gets played.

.. raw:: html

   <video muted autoplay loop width=854 height=480>
       <source src="../_static/create_project.mp4">
       Your browser doesn't support embedded videos.
   </video>
