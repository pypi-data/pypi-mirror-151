# AssertCount

A pytest plugin to count the actual number of asserts in a pytest run.

### Output

The output will be shown as the second last result in the pytest output, right above ````short test summary info````.<br>
Example:
```
...
===== assert statistics =====
total asserts : 1
passed asserts: 1 (100%)
failed asserts: 0 (0%)
== short test summary info ==
...
```

### Restrictions

This plugin to only able to count "non-trivial" asserts, so
````python
assert scoring("a", "b") == 10
````
would work for some given ````scoring```` function, but
````python
assert 2*3 == 10
````
would not be counted, as it's a pointless assert.

Furthermore, only asserts in the ````test_XYZ.py```` files will be counted.