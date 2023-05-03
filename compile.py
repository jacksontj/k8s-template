#!/usr/bin/python

import hashlib
import os.path
from os import walk
from subprocess import Popen, PIPE
import glob
import json
import yaml

import concurrent.futures
# TODO: add options for ProcessPoolExecutor() and/or setting workers
executor = concurrent.futures.ThreadPoolExecutor()

clusters = [x.split('./clusters/')[1].rsplit('.jsonnet')[0] for x in glob.glob("./clusters/*.jsonnet")]

def run_cmd(cmd):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception("run_cmd error: %s" % stderr)
    return stdout

# build a specific namespace and return the filepath written
def compile_cluster_namespace(cluster, cluster_output, namespace):
    # TODO: find namespace file better
    fpath = os.path.join('./apps', namespace, '_namespace.jsonnet')
    if not os.path.exists(fpath):
        raise Exception('Namespace file %s not found for cluster %s' % (fpath, cluster))
    cmd = ["./jsonnet-extended.py", fpath, "-J", ".", "-y", '--tla-code-file', 'ctx='+cluster_output]
    stdout = run_cmd(cmd)

    # as we explicitly require includes; we'll consider no results an error
    if not stdout.strip():
        raise Exception('Namespace %s returned nothing!' % namespace)

    output = fpath.replace("./apps", "./releases/"+cluster+"/release").replace(".jsonnet",".yaml")
    # ensure the output dir exists
    output_dir = os.path.dirname(output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output, 'wb') as fh:
        fh.write(stdout)
        return output

def compile_cluster(cluster):
    print ('compiling cluster', cluster)
    files = set()

    # check cluster file, we need the name there to exist and match the filename
    cluster_data_raw = run_cmd(['jsonnet', os.path.join('clusters', cluster+'.jsonnet'), '-J', '.'])
    cluster_data = json.loads(cluster_data_raw)
    if cluster_data['Name'] != cluster:
        raise Exception('cluster Name should match the filename')
    cluster_output = os.path.join('./releases/', cluster, 'cluster.json')
    # ensure the output dir exists
    cluster_output_dir = os.path.dirname(cluster_output)
    if not os.path.exists(cluster_output_dir):
        os.makedirs(cluster_output_dir)
    with open(cluster_output, 'wb') as fh:
        fh.write(cluster_data_raw)

    futures = []
    for namespace in cluster_data.get('Namespaces', []):
        futures.append(executor.submit(compile_cluster_namespace, cluster, cluster_output, namespace))

    for future in concurrent.futures.as_completed(futures):
        files.add(future.result())

    # spin over all release files and remove ones that are no longer generated
    for (dirpath, dirnames, filenames) in walk("./releases/"+cluster+"/release"):
        for filename in filenames:
            fpath = os.path.join(dirpath, filename)
            if fpath not in files:
                os.remove(fpath)
        # if we emptied a directory, remove it
        if not os.listdir(dirpath):
            os.rmdir(dirpath)


    # Create kustomization yaml
    kustomize_path = "./releases/"+cluster+"/release/kustomization.yaml"
    with open(kustomize_path, "w") as f:
        f.write(yaml.dump({
            'apiversion': 'kustomize.config.k8s.io/v1beta1',
            'kind': 'Kustomization',
            'resources': [os.path.relpath(f, os.path.dirname(kustomize_path)) for f in sorted(files)]}))

# TODO: parallelize
cluster_futures = []
for cluster in clusters:
    cluster_futures.append(executor.submit(compile_cluster, cluster))

for future in concurrent.futures.as_completed(cluster_futures):
    future.result()
