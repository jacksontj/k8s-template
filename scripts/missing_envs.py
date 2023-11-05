#!/usr/bin/env python3
'''missing_envs simply prints out the list of missing environments

'''

import json
import os.path

# To knoow what is missing, we need to know what we expect
# to do this we parse the environments.json to enumerate the
# clusters we expect
clusters = set()
with open('lib/imported/environments.json') as fh:
    environments = json.load(fh)

for env in environments:
    clusters.add(env['metadata']['labels']['cluster'])


# Now that we've found the expected clusters, we spin over our
# release manifest checking for (1) files that don't exist or
# (2) clusters that no longer exist
missing_envs = set()
with open('releases/manifest.json') as fh:
    data = json.load(fh)

# Check the manifest for missing files
for (output_file, env_file) in data.items():
    if not os.path.exists(env_file):
        missing_envs.add(env_file)
        continue
    # check if the cluster is missing
    cluster_name = output_file.split('/')[0]
    if cluster_name not in clusters:
        missing_envs.add(env_file)

for m in missing_envs:
    print (m)
