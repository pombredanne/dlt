dlt - Debian License Tools
==========================

This tool is no longer maintained. See https://github.com/nexB/debian-inspector 
for an alternative.

A tool set for parse and write the debian license (DEP5 compliant) quickly and
without pain.

.. image:: https://travis-ci.org/agustinhenze/dlt.png
    :target: https://travis-ci.org/agustinhenze/dlt

Get it
------

::

    git clone https://github.com/agustinhenze/dlt.git
    cd dlt

Install it
----------

::

    virtualenv testing_dlt
    source testing_dlt/bin/activate
    python setup.py install

Use it
------

To use the check tool::

    dlt project/debian/copyright
