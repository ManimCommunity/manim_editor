.. _export_presentation:

Export Presenter
================

When you've created a project and you launch ``manedit``, you can select the project and edit it.
If everything is to your liking you can export the project as a presentation.
This adds a few files required to present the project to the project directory.
You can copy this directory to a flash drive or wherever you need it.

.. raw:: html

   <video muted autoplay loop width=854 height=480>
       <source src="../_static/export_presenter.mp4">
       Your browser doesn't support embedded videos.
   </video>

Now you don't need the ``Manim Editor`` to be installed anymore to be able to present the project.
You only need a local web server.
If you have Python installed, you're good to go.
Simply run this in the projects directory:

.. code-block:: bash

   python3 -m http.server

Instead of running a local web server you can host the project on an online web server (e.g. GitHub Pages).
That way you can access it from anywhere.
This is how the `example <https://manimcommunity.github.io/manim_editor/Tutorial/index.html>`__ has been created.

If you intend to use GitHub Pages, you have to create a GitHub repository first.
All the steps you need to follow are explained in `this official GitHub Pages tutorial <https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site>`__.
The tutorial diverges at one point:
You don't have to create any markdown or HTML files.
Instead, copy the contents of the project folder (after you've exported the presenter) into the root of the repo.
Which branch you want to populate is entirely up to you.
Any Python files used to create the presentation aren't needed.
In the GitHub Pages settings you have to select the branch you chose (in this case ``pages``) in the GitHub Pages settings.
In the end you should end up with settings that look similar to these:

.. image:: ../_static/github_pages.png
   :alt: GitHub Pages Settings

And the root directory directory of said branch should look like this:

.. code-block:: bash

   .
   ├── img
   │   ├── arrow_clockwise.svg
   │   ├── banner.png
   │   ├── favicon.png
   │   ├── hourglass_split.svg
   │   ├── play_btn.svg
   │   └── wind.svg
   ├── index.html
   ├── project.json
   ├── thumb_0000.jpg
   ├── thumb_0001.jpg
   ├── thumb_0002.jpg
   ├── thumb_0003.jpg
   ├── thumb_0004.jpg
   ├── thumb_0005.jpg
   ├── video_0000.mp4
   ├── video_0001.mp4
   ├── video_0002.mp4
   ├── video_0003.mp4
   ├── video_0004.mp4
   ├── video_0005.mp4
   └── webpack
       ├── 67475f65d9d8a1fe03a2.woff
       ├── base.css
       ├── base.js
       ├── base.js.LICENSE.txt
       ├── d0ec932c09e146590948.woff2
       ├── edit_project.js
       └── scene_selection.js

If you've done all that correctly, everyone with an internet connection can access your presentation under the URL listed in the settings.
Should you require multiple presentations, you can simply put them in individual subdirectories and append the subdirectory name to the url (like ``https://manimcommunity.github.io/manim_editor/Tutorial`` instead of ``https://manimcommunity.github.io/manim_editor``).

Supported Browsers
******************

These browsers are officially supported.
Others may work as well but haven't been tested yet.

* Firefox
* Chrome
* Edge

If you confirm another functioning browser, feel free to `open an issue <https://github.com/manimcommunity/manim_editor/issues>`__ and tell the devs.

Presenter Explanation
*********************

The presenter is separated in three parts: timeline, video player, controls and informative tables.

In the timeline you can find the name, type (which is also displayed in the tables beneath the controls) and the thumbnail of each slide.
You can click on an element and it will take you to that part in the presentation.
In addition to that it shows the amount of time spent playing each slide.
This value will only update once a different section is being shown or the section gets restarted.
That way you get accurate information on how much time you spent on each section.

Instead of using the keyboard, you can utilise the controls on the right.
They offer basic media functionality like play last section, play next section, pause, restart section and enter fullscreen.
Pressing the "last section" button (or using ArrowLeft on the keyboard) doesn't necessarily go back one section.
If the current section has already been playing for a while, the current section will be restarted instead.
You can always use the Control key (or Command on a Mac) to forcefully go to the next or last section.

If you are hosting the presenter on a remote webserver, you should consider using the "Cache Videos" button.
It requests all videos and thus offers the browser the opportunity of caching them, speeding up future requests.

.. note::

   The timeline shows slides while the controls jump from section to section.
   That way you can create a lot of individual sections that don't clutter the timeline.

The player settings offer some fine-grained options, most of which are for debugging purposes.
Only the loader switch is of any interest:
The presenter of the ``Manim Editor`` employs two redundant video loaders, the buffer and the fallback loader.
You should always use the buffer loader.
But if for any reason it doesn't work, you can use the fallback loader instead.

.. warning::

    Be aware that the fallback loader has a detrimental effect on loading times between sections.
    Only use it when there is no other way!
