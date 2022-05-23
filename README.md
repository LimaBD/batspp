# BATSPP

This process and run shell style tests using bats-core
``` bash
#!/usr/bin/env batspp

$ echo -e "hello\nworld"
hello
world

$ echo "this is a test" | wc -c
15
```

And Also, you can run embedded tests in bash comments, for example:
``` bash
#!/bin/bash

function fibonacci () {
    result=""

    a=0
    b=1
    for (( i=0; i<=$1; i++ ))
    do
        result="$result$a "
        fn=$((a + b))
        a=$b
        b=$fn
    done

    echo $result
}

# $ run-fibonacci 9
# The Fibonacci series is:
# 0 1 1 2 3 5 8 13 21 34
#
alias run-fibonacci='echo "The Fibonacci series is:"; fibonacci'
```
With: ```$ batspp /path/to/bash/file/with/embedded/tests```


## Table of contents
- [Installation](#installation)
- [Testing](#usage)
- [Contributing](#contributing)


## Installation
Batspp uses [bats-core](https://github.com/bats-core/bats-core.git) to run tests, you can install it with:
```
$ npm install -g bats
```
You can install Batspp:
- from pip
    ```
    $ pip install batspp
    ```
- from source
    ```
    $ git clone https://github.com/LimaBD/batspp
    $ cd ./batspp
    $ ./build.bash
    ```


## Testing
The syntax using for output assertions is the follow:
``` bash
$ [command]
[expected output]
```
for example:
``` bash
#!/usr/bin/env batspp

$ echo "this is a test" | wc -c
15
```
running it with `$ batspp /path/to/test.batspp`, if the tests pass you should see:
```
$ batspp /path/to/test.batspp
1..1
ok 1 test id998957
```
otherwise you will see the actual and expected outputs:
```
$ batspp /path/to/test.batspp
1..1
not ok 1 test id998957
# (in test file /tmp/main-8zolvc_v, line 21)
#   `[ "$actual" == "$expected" ]' failed
# ========== actual ==========
# 15
# ========= expected =========
# 23
# ============================
```
You can replace the assigned id to the test with a title
``` bash
#!/usr/bin/env batspp

# Test testing batspp titles
$ echo "here we will use a title for this test" | wc -c
39
```
running it we see "testing batspp titles" instead of an id+number:
```
$ batspp /path/to/test.batspp
1..1
ok 1 testing batspp titles
```

## Contributing
All contribution is welcome!
