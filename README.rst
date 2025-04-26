====================
sass-embedded-python
====================

Embedded Sass Host for Python.

.. important::

   This is laboratory stage project. It does not ensure to continue development for goal.

Overview
========

This is Python project to compile Sass/SCSS using `Dart Sass <https://sass-lang.com/dart-sass/>`
that is primary implementation of Sass using Dart runtime.

Simple usage
============

Install:

.. code:: console

   pip install sass-embedded

Source:

.. code:: css
   :name: style.scss

   @use "sass:list";
   @use "sass:color";

   $font-stack: Helvetica, Arial;
   $primary-color: #333;

   body {
     $font-stack: list.append($font-stack, sans-serif);
     font: $font-stack;
   }

   a {
     color: $primary-color;

     &:hover{
       color: color.scale($primary-color, $lightness: 20%);
     }
   }

   @debug $font-stack;

Run:

.. code:: python

   from pathlib import Path
   from sass_embedded import compile_file

   compile_file(Path("style.scss"))

Output:

.. code:: css
   :name: style.css

   body {
     font: Helvetica, Arial, sans-serif;
   }

   a {
     color: #333;
   }
   a:hover {
     color: rgb(91.8, 91.8, 91.8);
   }

Motivation
==========

I develop `sphinx-revealjs <https://pypi.org/project/sphinx-revealjs>`_
that is Python Project to generate HTML presentation from reStructuredText or Markdown.

Reveal.js uses Sass to create presentation themes, and this uses ``sass:color`` module since v5.2.0.
But ``sphinxcontrib-sass`` does not compile themes, because this module is not supported by LibSass.

To resolve it, I am developing optional extension optimized sphinx-revealjs.
Concurrently I will develop generic project for multiple usecases.

This is the side of "generic project".

Project goal
============

Final goal is to have features as same as other "Sass Embedded" libraries.

But I will split some steps for it.

First goal
----------

Works as compile Sass/SCSS with subprocess-based actions.

- Provide single entrypoint to compile sources using Dart Sass native executable.
- Generate Dart Sass bundled bdist files every platforms.

Second goal
-----------

Works as "Sass Embedded Host for Python".

- Support `The Embedded Sass Protocol <https://github.com/sass/sass/blob/main/spec/embedded-protocol.md>`_.

Third goal
----------

Works as alternative to ``libsass-python``.

- Support all api of ``libsass-python`` using Dart Sass native executable.

Support
=======

This project supports only Python 3.9+.

License
=======

I plan for Apache License 2.0.
