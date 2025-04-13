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
