#!/usr/bin/python

''' This file contains all the tests we want to do post-jsonnet templating

The checks we currently have:
	- no namespace contains conflicting resource names
	-
'''

from os import walk
from subprocess import Popen, PIPE
import os.path
import glob
import yaml
import collections
import tests.plugins

def strip_right(text, suffix):
    if not text.endswith(suffix):
        return text
    # else
    return text[:len(text)-len(suffix)]

def strip_left(text, prefix):
    if not text.startswith(prefix):
        return text
    # else
    return text[len(prefix):]

KEY = collections.namedtuple("Key", ["kind", "name"])

kustomizations = [x for x in glob.glob("./releases/*/release/kustomization.yaml")]

for kustomization in kustomizations:
    cluster_tests = {}
    for k, v in tests.plugins.manifest_plugins.items():
        cluster_tests[k] = v()
    namespace_map = collections.defaultdict(set)
    global_map = collections.defaultdict(set)
    with open(kustomization, 'r') as fh:
        kustomization_data = yaml.safe_load(fh)
    for resource in kustomization_data['resources']:
        # path to the file on disk
        filepath = os.path.join(os.path.dirname(kustomization), resource)
        path_namespace = os.path.dirname(resource)

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
