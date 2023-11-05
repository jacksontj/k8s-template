#!/usr/bin/env python3

'''policy_generate.py generates a .policy.yml (policy-bot config) for the repository.

At a high-level the policy is as follows:
    - Regular operations: owner approval is required to make changes to "their namespace"
    - Owner operational override: a namespace owner is allowed to FORCE_COMMIT a change (bypass review). This should be reviewed post-fact
    - Admin operational override: a cluster admin is allowed to FORCE_COMMIT a change (bypass review). This should be reviewed post-fact
'''

import collections
import os.path
import glob
import yaml

def combine_policies(policies, op):
    return {
        op: policies,
    }

def if_clause_for_filepaths(filepaths):
    return {
        'changed_files': {
            'paths': sorted(filepaths),
        },
    }

def approvers_for_namespace(filepath):
    '''Return a unique key of the owners, and an object containing ownership
    '''
    with open(filepath) as fh:
        for obj in yaml.safe_load_all(fh):
            if obj['kind'] == 'Namespace':
                owners = sorted(obj['metadata']['labels'].get('owners', '').split(','))
                return {'users': owners}

    raise Exception()

def get_rule(name, if_clause=None, approvers=None, options=None, methods=None):
    ret = {
        'name': name,
        'requires': {
            'count': 1,
        },
        'options': {
            'allow_author': False,
            'invalidate_on_push': True,
            'methods': methods if methods else {
                'github_review': True,
            },
        },
    }
    if options:
        ret['options'].update(options)

    if if_clause:
        ret['if'] = if_clause

    if approvers:
        ret['requires'].update(approvers)

    return ret


if __name__ == '__main__':
    # map of namespace (release filepath) -> ownership {users:[], groups: []}
    # map of ownerkey -> {approvers: {users: []}, filepaths: []}
    OwnerEntry = collections.namedtuple('OwnerEntry', ['approvers', 'filepaths'])
    ownership_dict = {}

    # Spin over "release directory" to determine who owns what files
    namespace_files = glob.glob("releases/*/*/Namespace*.yaml")
    for namespace_file in namespace_files:
        output_parts = namespace_file.split('/')
        key = output_parts[1]+'/'+output_parts[2]
        approvers = approvers_for_namespace(namespace_file)
        if key not in ownership_dict:
            ownership_dict[key] = OwnerEntry(approvers, [])
        ownership_dict[key].filepaths.append('^'+os.path.dirname(namespace_file)+'.*$')

    # all of the per-namespace policies
    namespace_policies = {
        'owner_regular': [],    # list of names
        'owner_override': [],   # list of names
    }

    # list of rules; the names here must match all of the ones in namespace_policies
    approval_rules = []

    # for each ownership group; generate the owner based rules (as they are file specific)
    for key, owner_entry in ownership_dict.items():
        # regular entry
        name = "owner_regular-"+key
        namespace_policies['owner_regular'].append(name)
        approval_rules.append(get_rule(name,
                                    if_clause=if_clause_for_filepaths(owner_entry.filepaths),
                                    approvers=owner_entry.approvers))

        # override entry
        name = "owner_override-"+key
        namespace_policies['owner_override'].append(name)
        approval_rules.append(get_rule(name,
                                    if_clause=if_clause_for_filepaths(owner_entry.filepaths),
                                    options={'allow_author': True},
                                    methods={'comments': ['FORCE_COMMIT']},
                                    approvers=owner_entry.approvers))

    # combine into POLICY_BASE
    POLICY_BASE = {
        'policy': {
            'approval':[
                {'or': [
                    {'and': namespace_policies['owner_regular']},
                    {'and': namespace_policies['owner_override']},
                    'admin_override',
                ]},
            ],
        },
        # TODO: move to separate config, base, or inline-yaml?
        'approval_rules': approval_rules + [
            {
                'name': 'admin_override',
                'if': {
                    'changed_files': {
                        'paths': ["^.*$"],
                    },
                },
                'requires': {
                    'count': 1,
                    'users': ["jacksontj"],
                },
                'options': {
                    'allow_author': True,
                    'invalidate_on_push': True,
                    'methods': {
                        'comments': ['FORCE_COMMIT'],
                    },
                },
            },
        ],
    }


    print (yaml.dump(POLICY_BASE))
