# Writing Tests with BATSPP

The tests using Batspp are very similar to the shell terminal, an assertion can be written like this
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

If we save as `example.batspp` and then run `$ batspp ./example.batspp` we should see the result of the test
```
$ batspp /path/to/test.batspp
1..1
ok 1 test of line 3
```

When the assertion fails, you will see the actual and expected outputs:

```
$ batspp /path/to/test.batspp
1..1
not ok 1 test of line 3
# (in test file /tmp/main-8zolvc_v, line 21)
#   `[ "$actual" == "$expected" ]' failed
# ========== actual ==========
# 15
# ========= expected =========
# 23
# ============================
```

You can replace the assigned title `test of line [number]` with a better title using the test directive `# Test [some better title]`:

``` bash
#!/usr/bin/env batspp

# Test testing batspp titles
$ echo "here we will use a title for this test" | wc -c
39
```

Running it we will see:

```
$ batspp /path/to/test.batspp
1..1
ok 1 testing batspp titles
```

Tests directives also are used to group multiple assertions and setups commands, for example
``` bash
#!/usr/bin/env batspp

# Test multiple setup and assertions
$ filepath=$(echo $TMP/testfile-"$$")
$ echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
$ cat $filepath | wc -l
3
$ cat $filepath | wc -c
46
```
You can found more information about setups [here](./writing_setups.md)

If you want to continue a previus test, you can use the continuation directive `# Continue of [some test title]`
``` bash
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
```
```
1..1
ok 1 multiple setups and assertions
```
Continuation directives without specific title assigned, for example `# Continue` are assigned to the lastest founded test directive, if there are no previus test, throws exception
