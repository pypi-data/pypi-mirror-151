sysexits
========

.. image:: https://github.com/chris-mcdo/sysexits/workflows/tests/badge.svg
  :target: https://github.com/chris-mcdo/sysexits/actions?query=workflow%3Atests
  :alt: Unit Tests

.. image:: https://codecov.io/gh/chris-mcdo/sysexits/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/chris-mcdo/sysexits
  :alt: Unit Test Coverage

.. image:: https://img.shields.io/badge/license-MIT-purple
  :target: https://github.com/chris-mcdo/sysexits/blob/main/LICENSE
  :alt: MIT License


A simple python wrapper around the FreeBSD
`"preferable exit codes for programs" <https://www.freebsd.org/cgi/man.cgi?query=sysexits>`_.

It is useful for getting informative error messages from subprocesses which use
FreeBSD-recommended exit codes (linked above).

Usage
-----

Either select an exception manually using the ``EXCEPTIONS`` dictionary, or call
``raise_for_returncode`` with the completed process.

.. code-block:: python

    import subprocess
    import sysexits
    
    print(sysexits.EX_PROTOCOL)
    # 76

    process = subprocess.run("exit 76", shell=True)
    print(sysexits.EXCEPTIONS[process.returncode])
    # <class 'sysexits.ProtocolError'>

    sysexits.raise_for_returncode(process)
    # Traceback (most recent call last):
    # ...
    # sysexits.ProtocolError


License
-------

Copyright (c) 2022 Christopher McDonald

Distributed under the terms of the
`MIT <https://github.com/chris-mcdo/sysexits/blob/main/LICENSE>`_
license.
