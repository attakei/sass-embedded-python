=================
Versioning policy
=================

.. note:: This is plan and current stage is **v0** that it is possibility to change.

Using "Semantic Versioning"
===========================

This project uses `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`_ to manage version.

Tracing release of Dart Sass
============================

This project depends on Dart Sass and current version of it is ``v1.86.3``.
Therefore, this project will trace release of it and will update new version synchronously.

Rules of synchronize are these:

* When Dart Sass release as new patch version, this will release as new patch version.
* When Dart Sass release as new minor version, this will release as new patch or minor version.

  * If this project already supports new features without current api,
    it regards as "patch version update".
  * If this project is required to fix sources for new features,
    it regards as "minor version update".
    This will release after fix for new features.

* When Dart Sass release as new major version, this will not apply it as soon.

When does this project release v1?
==================================

I will release as ``v1.0.0`` when it fully supports for Sass Embedded Protocol.
