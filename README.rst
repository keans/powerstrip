powerstrip
==========

The `powerstrip` module is a simple helper module to manage Python plugins.

Plugins can be developed in an independent plugin directory, then packed and
distributed as plugin packages. The packed plugins can then be installed to
an applications plugin folder and be discovered and used by the application.

Please notice that the module is still in beta phase so breaking changes
may appear. Do not use this in production environments!


Setup
-----

The easiest way to install the current version of `powerstrip` is by using
`pip`:

::

    # install the module
    pip install -U powerstrip

    # or install the module with mkdocs support
    pip install -U powerstrip[docs]


Documentation
-------------

Build the documentation as follows:

::

    cd docs
    mkdocs build


Development
-----------

::

    python -m venv env
    source env/bin/activate
    pip install -e .

    # testing
    cd test
    pytest


Links
-----

* Website: https://github.com/keans/powerstrip
