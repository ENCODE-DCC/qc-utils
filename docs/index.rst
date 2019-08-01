
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
    qc_obj = QCMetric('first_metric', {'metric1': 1, 'metric2': 2})
    record.add(qc_obj)

To create from a STAR log file in ``/path/to/star_Log.out``:
::

    from qc_utils import QCMetric, QCMetricRecord
    from qc_utils.parsers import parse_starlog
    record = QCMetricRecord()
    log_qc_obj = QCMetric("starlogQC", "/path/to/star_Log.out", parser=parse_starlog)
    record.add(log_qc_obj)

To create from a samtools flagstats file in ``/path/to/flagstats.txt`` and write into a ``json``-object in ``/path/to/flagstats.json``:
::

    import json
    from qc_utils import QCMetric, QCMetricRecord
    from qc_utils.parsers import parse_flagstats

    record = QCMetricRecord()
    flagstat_qc_obj = QCMetric("flagstat", "/path/to/flagstats.txt", parser=parse_flagstats)
    record.add(flagstat_qc_obj)
    with open("/path/to/flagstats.json", "w") as fp:
        json.dump(record.to_ordered_dict(), fp)



Table of Contents
==================

.. toctree::
   :maxdepth: 2

   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
