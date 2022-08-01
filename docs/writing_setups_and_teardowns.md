# Writing Setups with BATSPP

You can write setups for assertions as standole commands `$ command`,

For example the first two commands are setup and the last one an assertion, note that setups commands do not have text after the command
``` bash
# Test setup and title
$ filepath=$(echo $TMP/testfile-"$$")
$ echo -n "this is a file content to run an example test" | sudo tee $filepath
$ cat $filepath
this is a file content to run an example test
```

You can write global setups for all tests writing setups commands without previus test

``` bash
# Setup
$ shopt -s expand_aliases
$ source ./bash_example.bash
```

If a previus test/assertion is founded before, the setup will be interpreted as local.

You can specify to switch test you want to append it adding `of` followed by the title of that test `# Setup of some test`
``` bash
# Test some important test
$ filepath=$(echo $TMP/testfile-"$$")
$ echo -n "this is a file content to run an example test" | sudo tee $filepath

...

# Setup of some important test
$ echo -n " using setup" >> $filepath
$ echo -n " and continue directives" >> $filepath
```

# Writing Teardowns with BATSPP

Can be added a global teardown for every tests with:
``` bash
# Teardown
echo "this will be runned when the test finish"
```
The generated Bats teardown will be:
``` Bash
# Teardown function
function run_teardown () {
	echo "this will be runned when the test finish"
}
```
