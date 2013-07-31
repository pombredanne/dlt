dlt - Debian License Tools
==========================

A set of tools for parse and write the debian license (DEP5 compliant) quickly
and without pain.

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
