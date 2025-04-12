============
Installation
============

Install from PyPI
=================

This is published on PyPI.
You can install it easily by your using package manager.

.. code-block:: console
   :caption: Example with pip

   pip install sass-embedded

Wheel bundles Dart Sass executable
----------------------------------

Some bdist have already Dart Sass executable for platform.
When you install it, you can use this without additional operations.

You can list of registered bdist on `"Download files" page of PyPI <https://pypi.org/project/sass-embedded/#files>`_.

Any target wheel and sdist does not bundle it
---------------------------------------------

When pip runs installation this,
it installs ``none-any`` bdist or sdist if platform does not match registered bdist.

These distributions don't have Dart Sass executable at default.
You must install it manually by calling sass-embedded module.

See :ref:`install-dart-sass`.

Install from source code
========================

.. code-block:: console
   :caption: Example with pip

   pip install https://github.com/attakei/sass-embedded-python/archive/refs/heads/main.zip

It also don't have Dart Sass executable at default.
You must install it manually by calling sass-embedded module.

See :ref:`install-dart-sass`.

.. _install-dart-sass:

Install Dart Sass executable
============================

``sass-embedded`` provides runner to install Dart Sass executable into package space.

Run these command when you need to install it.

.. code-block:: console
   :caption: Install Dart Sass executable

   python -m sass_embedded.dart_sass
