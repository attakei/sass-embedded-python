Version 0.1.5
=============

:Release date: 2026-07-05 (Asia/Tokyo)
:Dart Sass version: 1.99.0

Breaking changes
----------------

Features
--------

Fixes
-----

Others
------

ver 0.1.4
=========

:Release date: 2026-06-23 (Asia/Tokyo)
:Dart Sass version: 1.99.0

Fixes
-----

* Resolve aarch64 as arm64 when detecting host architecture. [ `#40`_ by `@Crozzers`_, closes `#39`_ ]

Others
------

* Update bundle Dart Sass.
* Raise minimum protobuf to 6.33.0 (security).
* Fix typos in docstrings of compile functions. [ `#37`_ by `@cclauss`_ ]

.. _#37: https://github.com/attakei/sass-embedded-python/pull/37
.. _#39: https://github.com/attakei/sass-embedded-python/issues/39
.. _#40: https://github.com/attakei/sass-embedded-python/pull/40
.. _@Crozzers: https://github.com/Crozzers
.. _@cclauss: https://github.com/cclauss

ver 0.1.3
=========

:Release date: 2025-09-28 (Asia/Tokyo)
:Dart Sass version: 1.91.2

This does not have source changes.

Others
------

* Update bundle Dart Sass.

ver 0.1.2
=========

:Release date: 2025-06-26 (Asia/Tokyo)
:Dart Sass version: 1.89.2

This does not have source changes.

Others
------

* Update bundle Dart Sass.

ver 0.1.1
=========

:Release date: 2025-06-21 (Asia/Tokyo)
:Dart Sass version: 1.87.0

This does not have source changes.

Others
------

* Add links on PyPI page.

ver 0.1.0
=========

:Release date: 2025-04-26 (Asia/Tokyo)
:Dart Sass version: 1.87.0

First release.

Features
--------

* Define 2 mode.

  * Mode as wrapper of CLI to compile sources from string, file or directory.
  * Mode as client of The Embedded Sass Protocol (low-level).
