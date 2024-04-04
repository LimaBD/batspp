Welcome to Batspp's documentation!
==================================

Shell style tests using `bats-core framework <https://github.com/bats-core/bats-core>`_.

Bats is a great `TAP <https://testanything.org/>`_-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

The goal of Batspp is to allow writing shell style tests with a simple and less idiosyncratic syntax.

.. code-block:: bash

    #!/usr/bin/env batspp

    # Test example with multiple assertions
    $ filepath=$(echo $TMP/testfile-"$$")
    $ echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
    $ cat $filepath | wc -l
    3
    $ cat $filepath | wc -c
    46

Batspp grew out of work for `Thomas O'Hara <https://github.com/tomasohara>`_ on `shell-scripts <https://github.com/tomasohara/shell-scripts>`_ and `mezcla <https://github.com/tomasohara/mezcla>`_.

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   writing_tests
   writing_jupyter_tests
   suggestions
   batspp_internals
   common_errors
   contributing

License
-------

Batspp is released under an GNU Lesser General Public License Version 3, see `LICENSE.TXT <https://github.com/LimaBD/batspp/blob/main/LICENSE.txt>`_ for details.
