# BATSPP Basic Usage

Using Batspp is very easy, once [installed](./installation.md) you can run tests with `$ batspp ./path/to/test.batspp`.

## Saving generated tests files
You can use the `--save` argument to save the generated Bats file on a determined path.

`$ batspp --save ./result.bats ./path/to/test.batspp`

## Sourcing another files
You can source another files using the `--source` argument.

`$ batspp --source ./some/file/to/source.bash ./path/to/test.batspp`

This will append the next setup block to the generated Bats file.

``` bash
# Load sources
shopt -s expand_aliases
source ./some/file/to/source.bash
```

## Outputing result following the Standard IO Paradigm
You can output the resulting generated file and avoid executing it with the `--output` option.

## Skip running tests
You can skip running the tests with the `--skip_run` option.

## Debugging assertions
Verbose debug and hexdump can be printed when a test fail with the flag `--hexdump_debug` or `--verbose_debug`, this verbose debug can be modified manually in the generated Bats file (with `--save` argument) editing this line:
``` bash
VERBOSE_DEBUG="| python3 -m hexdump -"
```
You can set a custom debug with the argument `--debug "| commands"`.

## Setting temporal test directory
A default temporal directory for tests can be setted with the argument `--temp_dir`, without this argument, the default parent directory is /tmp.

## Copying a directory into the test directory
A directory can be copied into the test directory with `--copy_dir` argument.

## Setting executables visible to the tests file
With `--visible_paths "file.bash another.bash"`  argument you can add scripts visible to the PATH.

## Setting Bats options
You can add options to run Bats with `--run_opts "bats options"`, these will be added to the resulting generated test [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)).

## Omitting trace
Actual/expected trace can be omitted from test file with the `--omit_trace` option.

## Disable aliaces sourcing
Sourcing of aliases can be done with `--disable_aliases` option.
