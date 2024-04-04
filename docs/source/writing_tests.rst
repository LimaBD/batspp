Writing Tests
=============

Batspp is a testing framework that allows users to write tests in a format resembling shell commands.
Tests consist of commands followed by expected outputs, facilitating easy verification.


.. code-block:: bash

    $ [command]
    [expected output]

Your first Batspp test
----------------------

To write your first Batspp test, create a new file ``example.batspp`` with the following content:

.. code-block:: bash

    $ echo "this is a test" | wc -c
    15

Running ``$ batspp ./example.batspp`` you should see the result of the test:

.. code-block:: bash

    $ batspp /path/to/test.batspp
    1..1
    ok 1 test of line 1

When the assertion fails, you will see something like this:

.. code-block:: bash

    $ batspp /path/to/test.batspp
    1..1
    not ok 1 test of line 1
    # (in test file /tmp/main-8zolvc_v, line 21)
    #   '[ "$actual" == "$expected" ]' failed
    # ========== actual ==========
    # 15
    # ========= expected =========
    # 23
    # ============================

Naming your tests
-----------------

You can replace the assigned title ``test of line [number]`` with a better title using the test directive ``# Test [some better title]``:

.. code-block:: bash

    # Test testing batspp titles
    $ echo "here we will use a title for this test" | wc -c
    39

Running it you will see:

.. code-block:: bash

    $ batspp /path/to/test.batspp
    1..1
    ok 1 testing batspp titles

Grouping commands into a single test
------------------------------------

Tests directives also are used to group multiple assertions and setups commands, for example:

.. code-block:: bash

    # Test multiple setup and assertions
    $ filepath=$(echo $TMP/testfile-"$$")
    $ echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
    $ cat $filepath | wc -l
    3
    $ cat $filepath | wc -c
    46

Splitting tests into multiple parts
-----------------------------------

If you want to split a test into multiple parts, you can first write the test directive and then use the continuation directive ``# Continue of [some test title]``:

.. code-block:: bash

    # Test multiple setups and assertions
    $ filepath=$(echo $TMP/testfile-"$$")
    $ echo -n "this is a file content to run an example test" | sudo tee $filepath
    $ cat $filepath
    this is a file content to run an example test

    ...

    # Continue of multiple setups and assertions
    $ echo -n " using setup" >> $filepath
    $ echo -n " and continue directives" >> $filepath
    $ cat $filepath
    this is a file content to run an example test using setup and continue directives

.. code-block:: bash

    1..1
    ok 1 multiple setups and assertions

Continuation directives without a specific title assigned, for example ``# Continue``, are assigned to the last found test directive. If there are no previous tests, it throws an exception.

Arrow assertions
----------------

Also, you can write assertions with arrows; ``=>`` (assert equals) and ``=/>`` (assert not equals):

.. code-block:: bash

    # This test should work fine:
    fibonacci 9 => 0 1 1 2 3 5 8 13 21 34

    # This is a negative test:
    fibonacci 3 =/> 8 2 45 34 3 5

Writing setups
--------------

You can write setups for assertions as standalone commands ``$ command``,

For example, the first two commands are setup and the last one an assertion, note that setup commands do not have text after the command:

.. code-block:: bash

    # Test setup and title
    $ filepath=$(echo $TMP/testfile-"$$")
    $ echo -n "this is a file content to run an example test" | sudo tee $filepath
    $ cat $filepath
    this is a file content to run an example test

You can specify a test target of the setup with `` of `` followed by the title of that test ``# Setup of [some test]``:

.. code-block:: bash

    # Test some important test
    $ filepath=$(echo $TMP/testfile-"$$")
    $ echo -n "this is a file content to run an example test" | sudo tee $filepath

    ...

    # Setup of some important test
    $ echo -n " using setup" >> $filepath
    $ echo -n " and continue directives" >> $filepath

Writing global setups
---------------------

You can write global setups for all tests writing setups commands without previous test:

.. code-block:: bash

    # Setup
    $ shopt -s expand_aliases
    $ source ./bash_example.bash

If a previous test/assertion is found before, the setup will be interpreted as local.

Also you can use the ``Global Setup`` directive to specify that the setup is global for all tests:

.. code-block:: bash

    # Global Setup
    $ alias count-words='wc -w'

Writing teardowns
-----------------

The equivalent directive of setups but for teardowns is ``# Teardown``:

.. code-block:: bash

    # Teardown
    echo "this will be run when the test finishes"

Writing global teardowns
------------------------

As with setups, you can write global teardowns for all tests writing teardowns commands without previous test:

.. code-block:: bash

    # Global Teardown
    echo "this will be run when the test finishes"

Coverage Reports
----------------

Section work in progress...

Mote test examples!
-------------------

On `examples <https://github.com/LimaBD/batspp/tree/main/docs/examples>`_, you can find several Batspp full examples and their related generated Bats files.
