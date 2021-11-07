.. _cli:

Command Line Interface
======================

Instead of using a web browser to create a project and export the presenter, you can use the CLI.

.. code-block:: bash

   manedit --quick_present_export path/to/example.json

This command creates a new project with the name ``example``, populates it with videos and thumbnails and exports the presenter.
That way you immediately have the final presenter, which you can load onto a webserver.

It loads all sections referenced in the JSON file provided.
These files get created by ``Manim`` when using the ``--save_sections`` flag.
If you need multiple scenes to become one project, you can use the ``--quick_present_export`` flag multiple times:

.. code-block:: bash

   manedit --quick_present_export path/to/a.json --quick_present_export path/to/b.json

.. note::

   You can also define the name of the to be created project with the ``--project_name`` flag.
