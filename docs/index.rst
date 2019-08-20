
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

The basic pattern is to create ``QCMetric`` objects, and then add related ones to a ``QCMetricRecord``. ``QCMetric`` objects can be created from dicts. Supported parsers are for now for samtools flagstats and for STAR log. You can also write your own: provide a function that takes a path to a file as input and returns a dict.

Examples
---------

To create directly from dicts:
::

    from qc_utils import QCMetric, QCMetricRecord

    record = QCMetricRecord()
    qc_obj1 = QCMetric('first_metric', {'metric1': 1, 'metric2': 2})
    qc_obj1 = QCMetric('second_metric', {'metric1': 3, 'metric2': 4})
    record.add_all([qc_obj1, qcobj2])

To create from a STAR log file in ``/path/to/star_Log.out``:
::

    from qc_utils import QCMetric, QCMetricRecord
    from qc_utils.parsers import parse_starlog
    starlog = parse_starlog("/path/to/star_Log.out")
    record = QCMetricRecord()
    log_qc_obj = QCMetric("starlogQC", starlog)
    record.add(log_qc_obj)

To create from a samtools flagstats file in ``/path/to/flagstats.txt`` and write into a ``json``-object in ``/path/to/flagstats.json``:
::

    import json
    from qc_utils import QCMetric, QCMetricRecord
    from qc_utils.parsers import parse_flagstats
    flagstats = parse_flagstats("/path/to/flagstats.txt")
    flagstat_qc_obj = QCMetric("flagstat", flagstats)
    with open("/path/to/flagstats.json", "w") as fp:
        json.dump(flagstat_qc_obj.to_ordered_dict(), fp)

QCMetricRecord can also have a name, and can be written into ``json`` as follows:
::

    import json
    from qc_utils import QCMetric, QCMetricRecord
    from qc_utils.parsers import parse_flagstats, parse_starlog
    starlog = parse_starlog("/path/to/star_Log.out")
    flagstats = parse_flagstats("/path/to/flagstats.txt")
    log_qc_obj = QCMetric("starlogQC", starlog)
    flagstat_qc_obj = QCMetric("flagstat", flagstats)
    record = QCMetricRecord([log_qc_obj, flagstat_qc_obj], name="alignment_qc")
    with open("/path/to/alignment_qc.json", "w") as fp:
        json.dump(record.to_ordered_dict(), fp)

You can combine two QCMetricRecords as follows:
::

    from qc_utils import QCMetric, QCMetricRecord
    record1 = QCMetricRecord()
    record2 = QCMetricRecord()
    qc_obj1 = QCMetric('first_metric', {'metric1': 1, 'metric2': 2})
    qc_obj1 = QCMetric('second_metric', {'metric1': 3, 'metric2': 4})
    record1.add(qc_obj1)
    record2.add(qc_obj2)
    record1.add_all(record2)



Table of Contents
==================

.. toctree::
   :maxdepth: 2

   license
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
