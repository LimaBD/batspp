# BATSPP Basic Usage

Using Batspp is very easy, once [installed](./installation.md) you can run tests with `$ batspp ./path/to/test.batspp`

## Saving generated tests files

You can use the `--save` argument to save the generated Bats file on a determined path

`$ batspp --save ./result.bats ./path/to/test.batspp`

## Sourcing another files

You can source another files using the `--source` argument

`$ batspp --source ./some/file/to/source.bash ./path/to/test.batspp`

This will append the next setup block to the generated Bats file

``` bash
# Load sources
shopt -s expand_aliases
source ./some/file/to/source.bash
```

## Outputing result following the Standard IO Paradigm

You can output the resulting generated file and avoid executing it with the `--output` flag
