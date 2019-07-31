
====================================
Welcome to qc-utils's documentation!
====================================

.. include:: ../README.rst
   :start-after: short-intro-begin
   :end-before: short-intro-end

Getting Started
================

``qc-utils`` is a Python-only package `hosted on PyPI <https://pypi.org/project/qc-utils/>`_. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: console

   $ pip install qc-utils

Usage
=======

The basic pattern is to create ``QCMetric`` objects, and then add related ones to a ``QCMetricRecord``. ``QCMetric`` objects can be created directly from dicts, or from files. Supported parsers are for now for samtools flagstats and for STAR log. You can also write your own: provide a function that takes a filepath as input and returns a dict.

Examples
---------

To create directly from dicts:
::

    from qc_utils import QCMetric, QCMetricRecord

    record = QCMetricRecord()
    obj1 = QCMetric('first_metric', {'metric1': 1, 'metric2': 2})
    record.add(obj1)


Table of Contents
==================

.. toctree::
   :maxdepth: 2

   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
