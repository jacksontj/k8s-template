#!/usr/bin/env python3

import jinja2
import glob

import os.path
import json
import yaml

if __name__ == '__main__':
    with open('lib/imported/environments.json') as fh:
        environments = json.load(fh)

    for env in environments:
        namespace_file = os.path.join('releases', env['metadata']['labels']['cluster'], env['spec']['namespace'], 'Namespace-'+env['spec']['namespace']+'.yaml')
        with open(namespace_file) as fh:
            cluster_namespace = yaml.safe_load(fh)
            cluster_namespace['owners'] = cluster_namespace['metadata']['labels']['owners'].split(',')
            env['namespace'] = cluster_namespace

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = environment.get_template("scripts/policy.yml.tmpl")

    content = template.render(
        environments=environments,
    )

    print (yaml.dump(yaml.safe_load(content)))
