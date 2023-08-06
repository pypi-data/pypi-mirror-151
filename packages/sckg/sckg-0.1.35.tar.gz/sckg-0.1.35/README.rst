====
sckg
====


.. image:: https://img.shields.io/pypi/v/sckg.svg
        :target: https://pypi.python.org/pypi/sckg

.. image:: https://img.shields.io/travis/FudanSELab/sckg.svg
        :target: https://travis-ci.com/FudanSELab/sckg

.. image:: https://readthedocs.org/projects/sckg/badge/?version=latest
        :target: https://sckg.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A Software Concept Knowledge Graph


* Free software: MIT license
* Documentation: https://sckg.readthedocs.io.

Prerequisites
--------------


1. Spacy 3.0 以及对应的模型。

    其中模型有两种选择，
    - 一种是更加大而慢的，en_core_web_trf
    ```
    pip install -U pip setuptools wheel
    pip install -U spacy-nightly --pre
    python -m spacy download en_core_web_trf
    ```
    - 一种是小而快的，en_core_web_sm，目前我们先用小而快的
    ```
    pip install -U pip setuptools wheel
    pip install -U spacy
    python -m spacy download en_core_web_sm
    ```

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

