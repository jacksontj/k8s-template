# tests

This directory contains all of the tests that will be run over the release directory.

## How a test works
A test is simply a python class with an `evaluate_manifest` method that is passed:

1. `file_path`: path to the manifest file being parsed
2. `path_namespace` the namespace for the manifest as determined by the location in the `releases/` directory
3. `key`: a namedtuple of (`kind` and `name`)
4. `obj`: the actual manifest object being tested


This method can do whatever testing it wants to -- and will pass assuming it returns. All the tests in the `manifest_plugins` dict in [plugins.py](plugins.py).
