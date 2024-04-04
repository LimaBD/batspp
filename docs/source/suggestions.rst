Suggestions
===========

Avoid flaky tests
-----------------

Avoid flaky tests (tests that sometimes pass and sometimes fail) for example when using dates or random numbers, you can avoid this by replacing the random number with a fixed number or using a regex to match the output.

Bad:

.. code-block:: bash

    # The date will change every day, making tests flaky
    date

.. code-block:: bash

    sáb 14 oct 2023 11:26:38 -03

Good:

.. code-block:: bash

    date | sed 's/\w\+ [0-9]\+ \w\+ [0-9]\+ [0-9]\+:[0-9]\+:[0-9]\+ -[0-9]\+/thu 00 oct 0000 00:00:00 -00/'

.. code-block:: bash

    thu 00 oct 0000 00:00:00 -00

Avoid long outputs
------------------

This could cause some problems with Jupyter Notebook tests, depending on the settings,
this will truncate very long outputs, the tests will keep working but you only will see part of the output,

Bad:

.. code-block:: bash

    function nstrings () {
    for ((i = 1; i <= $1; i++)); do
        echo -en "$2"
    done
    }
    nstrings 50 "this is a long output\n"

This will output:

.. code-block:: bash
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    ...
    this is a long output
    this is a long output
    this is a long output
    this is a long output
    Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

Good:

.. code-block:: bash

    nstrings 50 "this is a long output\n" | wc -l

this outputs:

.. code-block:: bash
    50
