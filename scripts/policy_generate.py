#!/usr/bin/env python3

import jinja2
import glob
import yaml

if __name__ == '__main__':
    # using the tanka name
    cluster_namespaces = []

    namespace_files = sorted(glob.glob("releases/*/*/Namespace*.yaml"))
    for namespace_file in namespace_files:
        with open(namespace_file) as fh:
            cluster_namespace = yaml.safe_load(fh)
            cluster_namespace['cluster'] = namespace_file.split('/')[1]
            cluster_namespace['owners'] = cluster_namespace['metadata']['labels']['owners'].split(',')
            cluster_namespaces.append(cluster_namespace)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = environment.get_template("scripts/policy.yml.tmpl")

    content = template.render(
        cluster_namespaces=cluster_namespaces,
    )

    #print (content)

    print (yaml.dump(yaml.safe_load(content)))
