.. _internals:

Internals
=========

Build from Source
*****************

* clone repo: ``git clone https://github.com/ManimEditorProject/manim_editor && cd manim_editor``
* install poetry dependencies: ``poetry install``
* enter poetry shell: ``poetry shell``
* install npm modules: ``npm ci``
* compile web files: ``npm run build_debug`` or ``npm run build_release``
* start editor in debug mode: ``manedit --debug``

Files to be Updated when Bumping Version
****************************************

* ``pyproject.toml``
* ``package.json``
* ``manim_editor/config.py``
* ``docs/source/conf.py``

A Brief History of the Manim Editor
***********************************

This project started in September 2021 as the `Manim Web Presenter <https://github.com/christopher-besch/manim_web_presenter>`__, which has been inspired by the `Manim Presentation Repo <https://github.com/galatolofederico/manim-presentation>`__.
Back then ``Manim`` didn't have any sections, therefore this functionality had to be implemented using wrappers around the ``Scene`` class and subclasses.
This was an ugly solution, which turned obsolete with the `implementation of the Section API <https://github.com/ManimCommunity/manim/pull/2152>`__.
Since more and more features were requested, it made sense to re-design the project from scratch and give it another name: the ``Manim Editor``.

These people directly participated in developing the ``Manim Editor`` (in order of first contribution):

* `Christopher Besch <https://github.com/christopher-besch>`__
* `Markus Jørstad Svendsen <https://github.com/MarcasRealAccount>`__
* `Jan-Hendrik Müller <https://github.com/kolibril13>`__
