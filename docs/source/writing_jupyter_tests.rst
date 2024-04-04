Writing Jupyter Tests
=====================

With Batspp, you can also write tests using Jupyter Notebooks.
This is useful to write regression tests and check that a command or group of commands
always produce the same output.

Setup the Jupyter Notebook
--------------------------

You must install `takluyver/bash_kernel <https://github.com/takluyver/bash_kernel>`_ to run Bash commands in the notebook cells
and then in the Jupyter notebook, you can change to the fresh installed kernel.

Your first jupyter test
-----------------------

Once the setup is done, you can creaet a new jupyter notebook file and write in a cell,
the command that you want to test, for example:

.. code-block:: bash

   In [1]: # Your Jupyter notebook cell code here
      ...: echo "Hello World"

   Out[1]: Hello World

Then you can run the regression test with:

.. code-block:: bash

    $ batspp <notebook_name>.ipynb

Writing setups in Jupyter Tests
-------------------------------

You can write setups for tests in Jupyter Notebooks cells too, for example you can write this:

.. code-block:: bash

   In [1]: shopt -s expand_aliases
      ...: function fibonacci () {
      ...:     result=""
      ...:     a=0
      ...:     b=1
      ...:     for (( i=0; i<=$1; i++ ))
      ...:     do
      ...:         result="$result$a "
      ...:         fn=$((a + b))
      ...:         a=$b
      ...:         b=$fn
      ...:     done
      ...:     echo $result
      ...: }
      ...: alias run-fibonacci='echo "The Fibonacci series is:"; fibonacci'

And if you want, in another cell you can put the assertion for this alias:

.. code-block:: bash

   In [2]: run-fibonacci 10

   Out[2]: The Fibonacci series is: 0 1 1 2 3 5 8 13 21 34 55 
