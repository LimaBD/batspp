![https://github.com/LimaBD/batspp/releases/latest](https://img.shields.io/github/v/release/limabd/batspp)
[![License: LGPLv3](https://img.shields.io/badge/License-LGPLv3-orange)](https://github.com/LimaBD/batspp/blob/main/LICENSE.txt)
[![Python: >=3.8](https://img.shields.io/badge/Python-%3E%3D3.8-yellow)](https://www.python.org/)
![tests](https://github.com/LimaBD/batspp/actions/workflows/tests.yml/badge.svg)


# BATSPP

Shell style tests using [bats-core framework](https://github.com/bats-core/bats-core)

Bats is a great [TAP](https://testanything.org/)-compliant testing framework for Bash. It provides a simple way to verify that the UNIX programs you write behave as expected.

The goal of Batspp to allow writing shell style tests with an simple and a less idiosyncratic syntax.

``` bash
#!/usr/bin/env batspp

# Test example with multiple assertions
$ filepath=$(echo $TMP/testfile-"$$")
$ echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
$ cat $filepath | wc -l
3
$ cat $filepath | wc -c
46
```

Batspp grew out of work for [Thomas O'Hara](https://github.com/tomasohara) on [shell-scripts](https://github.com/tomasohara/shell-scripts) and [mezcla](https://github.com/tomasohara/mezcla).

## License
Batspp is released under an GNU Lesser General Public License Version 3, see [LICENSE.TXT](./LICENSE.txt) for details.
