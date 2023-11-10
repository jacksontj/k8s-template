#!/usr/bin/env python3

import jinja2
import glob

import os.path
import json
import yaml

class ClusterNamespace(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __getitem__(self, key):
        return ClusterNamespaceKind(self.dirname, key)

class ClusterNamespaceKind(object):
    def __init__(self, dirname, kind):
        self.dirname = dirname
        self.kind = kind
    def __getitem__(self, name):
        fpath = os.path.join(self.dirname, self.kind+'-'+name+'.yaml')
        with open(fpath) as fh:
            o = yaml.safe_load(fh)
            return o

if __name__ == '__main__':
    with open('lib/imported/environments.json') as fh:
        environments = json.load(fh)

    for env in environments:
        env['obj'] = ClusterNamespace(os.path.join('releases', env['metadata']['labels']['cluster'], env['spec']['namespace']))

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = environment.get_template("scripts/policy.yml.tmpl")

    content = template.render(
        environments=environments,
    )

    # TODO: flag??
    if False:
        print (content)
    else:
        # reload and dump to clean up whitespace etc.
        print (yaml.dump(yaml.safe_load(content)))
