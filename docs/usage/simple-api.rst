==========
Simple API
==========

This is simple usage guide.
When you want to learn more information,
please see :py:mod:`module document <sass_embedded>`.

Compile single file
===================

This is example to compile files on these directory.

.. code-block:: text

   (Current directory)
   + sass/
   | + style.scss
   + css/

.. code-block:: scss
   :caption: style.scss

   $font-stack: Helvetica, sans-serif;
   $primary-color: #333;

   body {
     font: 100% $font-stack;
     color: $primary-color;
   }

To compile ``sass/style.scss`` into ``css/style.css``:

.. code-block:: python

   from pathlib import Path
   from sass_embedded import compile_file

   compile_file(
       Path("sass/style.scss"),
       Path("css/style.css"),
   )

When ``compile_file`` runs with default arguments, it create two files:

* ``css/style.css``: Compiled stylesheet file.
* ``css/style.css.map``: Source map file.

Compile file with external modules
==================================

This supports to compile file with loading external modules.

.. code-block:: text

   + reveal.js/ .. clone from https://github.com/hakimel/reveal.js
   + (Current directory)
     + sass/
     | + theme.scss
     + css/

.. code-block:: scss
   :caption: theme.scss

   @use 'template/mixins';
   @use 'template/setting';

   // Write font, color and more variables.

   @use 'template/theme';

To compile ``sass/theme.scss`` into ``css/theme.css``:

.. code-block:: python

   from pathlib import Path
   from sass_embedded import compile_file

   compile_file(
       Path("sass/theme.scss"),
       Path("css/theme.css"),
       load_paths=[
           Path("../reveal.js/css/theme"),
       ],
   )

When ``compile_file`` runs with refer Reveal.js assets passed by ``load_paths``.

Compile files on directory
==========================

If you need to compile multiple files on a directory,
you can use ``compile_directory``.

.. code-block:: text
   :caption: Example of files.

   + (Current directory)
     + sass/
     | + _base.scss
     | + form.scss
     | + index.scss
     + css/

Using ``compile_directory`` create multiple stylesheet from all target files on passed directory.

.. code-block:: python

   from pathlib import Path
   from sass_embedded import compile_directory

   compile_file(
       Path("sass"),
       Path("css"),
   )

After run ``compile_directory``,
there are four files on ``css`` folder.

* ``form.css``
* ``form.css.map``
* ``index.css``
* ``index.css.map``

It does not generate file from ``_base.scss``.
