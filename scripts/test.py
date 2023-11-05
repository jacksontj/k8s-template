#!/usr/bin/env python3

''' This file contains all the tests we want to do post-jsonnet templating

The checks we currently have:
	- no namespace contains conflicting resource names
	-
'''

RELEASE_DIR = './releases'

from os import walk
import os.path
import yaml
import collections
import tests.plugins

KEY = collections.namedtuple("Key", ["kind", "name"])

# for each release dir (cluster) we want to run the tests
for item in os.listdir(RELEASE_DIR):
    path = os.path.join(RELEASE_DIR, item)
    if not os.path.isdir(path):
        continue
    cluster_tests = {}
    for k, v in tests.plugins.manifest_plugins.items():
        cluster_tests[k] = v()
    namespace_map = collections.defaultdict(set)
    global_map = collections.defaultdict(set)

    # For each yaml file in the directory
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            if not filename.endswith('.yaml'):
                continue
            filepath = os.path.join(dirpath, filename)
            # parse our the "namespace" as defined by the filepath
            path_namespace = dirpath.removeprefix(path+'/')

            # check for conflicting namespaces
            with open(filepath) as fh:
                for obj in yaml.safe_load_all(fh):
                    key = KEY(obj["kind"], obj["metadata"]["name"])
                    for k, v in cluster_tests.items():
                        v.evaluate_manifest(
                            filepath,
                            path_namespace,
                            key,
                            obj,
                        )
