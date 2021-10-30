Internals
=========

Coming soon.

Build from Source
*****************

* clone repo: ``git clone https://github.com/ManimEditorProject/manim_editor && cd manim_editor``
* install poetry dependencies: ``poetry install``
* enter poetry shell: ``poetry shell``
* install npm modules: ``npm ci``
* compile web files: ``npm run build_debug` or `npm run build_release``
* start editor in debug mode: ``manedit --debug``


History
*******

This project started in September 2021 as the `Manim Web Presenter <https://github.com/christopher-besch/manim_web_presenter>`_, which has been inspired by the `Manim Presentation Repo <https://github.com/galatolofederico/manim-presentation>`_.
Back then Manim didn't have any sections, therefore this functionality had to be implemented using wrappers around the ``Scene`` class and subclasses.
This was an ugly solution, which turned obsolete with the `implementation of the Section API <https://github.com/ManimCommunity/manim/pull/2152>`_
Since more and more features were requested, it made sense to re-design the project from scratch and give it another name: the ``Manim Editor``.
