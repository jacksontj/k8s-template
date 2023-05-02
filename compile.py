#!/usr/bin/python

import hashlib
import os.path
from os import walk
from subprocess import Popen, PIPE
import glob
import json
import yaml


clusters = [x.split('./clusters/')[1].rsplit('.jsonnet')[0] for x in glob.glob("./clusters/*.jsonnet")]

def run_jsonnet(cmd):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception("jsonnet error: %s" % stderr)
    return stdout

def compile_cluster(cluster):
    print ('compiling cluster', cluster)
    files = set()

    # check cluster file, we need the name there to exist and match the filename
    cluster_data_raw = run_jsonnet(['jsonnet', os.path.join('clusters', cluster+'.jsonnet'), '-J', '.'])
    cluster_data = json.loads(cluster_data_raw)
    if cluster_data['Name'] != cluster:
        raise Exception('cluster Name should match the filename')
    output = os.path.join('./releases/', cluster, 'cluster.json')
    # ensure the output dir exists
    output_dir = os.path.dirname(output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output, 'wb') as fh:
        fh.write(cluster_data_raw)

    for namespace in cluster_data.get('Namespaces', []):
        # TODO: find namespace file better
        fpath = os.path.join('./apps', namespace, '_namespace.jsonnet')
        if not os.path.exists(fpath):
            continue
        cmd = ["jsonnet", fpath, "-J", ".", "-y", '--tla-code-file', 'ctx='+output]
        stdout = run_jsonnet(cmd)
        # if there was no output, we'll skip this (as its not wanted in this cluster)
        if not stdout.strip():
            continue

        output = fpath.replace("./apps", "./releases/"+cluster+"/release").replace(".jsonnet",".yaml")
        # ensure the output dir exists
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output, 'wb') as fh:
            fh.write(stdout)
            files.add(output)

    # spin over all release files and remove ones that are no longer generated
    for (dirpath, dirnames, filenames) in walk("./releases/"+cluster+"/release"):
        for filename in filenames:
            fpath = os.path.join(dirpath, filename)
            if fpath not in files:
                os.remove(fpath)
        # if we emptied a directory, remove it
        if not os.listdir(dirpath):
            os.rmdir(dirpath)


    # TODO: move to method to duplicate?
    kustomization = {
        'apiVersion': 'kustomize.config.k8s.io/v1beta1',
        'kind': 'Kustomization',
        'resources': [],
    }
    
    output = "./releases/"+cluster+"/release/kustomization.yaml"
    for fpath in files:
        kustomization['resources'].append(os.path.relpath(fpath, os.path.dirname(output)))
    
    sorted(kustomization['resources'])

    with open(output, "w") as f:
        f.write(yaml.dump(kustomization))

# TODO: parallelize
for cluster in clusters:
    compile_cluster(cluster)
