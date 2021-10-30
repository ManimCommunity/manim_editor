Installation
============

Just as Manim the Manim Editor is a `Python package on PyPi <https://pypi.org/project/manim-editor/>`_.
If you know what you're doing, simply install that package using pip.
But make sure that FFmpeg is accessible through the ``ffmpeg`` command.

First you have to `install Manim <https://docs.manim.community/en/stable/installation.html#local-installation>`_ and ensure that it is functioning on your system.

.. tip::

    On Windows it is recommended to use the manual installation as it simplifies the installation of the Manim Editor later on.

.. note::

    You don't necessarily need to have Manim installed for the Manim Editor to work.
    Though as you cannot do anything without a rendered Manim scene, it is highly recommended to `install Manim <https://docs.manim.community/en/stable/installation.html#local-installation>`_ prior to installing the Manim Editor.
    In addition to that FFmpeg is one of the requirements for the Manim Editor.
    It's installation is described in the installation instructions for Manim.

Once your Python environment is functioning and populated with Manim and its requirements you can run this command:

.. code-block::

    python -m pip install manim-editor

Now the Manim Editor is accessible through the terminal via ``manim_editor`` or ``manedit``.
If you've gotten stuck and don't know what to do, feel free to ask on the `Manim Discord Server <https://www.manim.community/discord/>`_ or open an `Issue on GitHub <https://github.com/ManimEditorProject/manim_editor/issues>`_.
(The latter is preferred.)
