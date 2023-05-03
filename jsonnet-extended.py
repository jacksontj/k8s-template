#!/usr/bin/env python

import sys
import argparse
import shlex
from subprocess import Popen, PIPE

import json
import _jsonnet
import yaml


def run_cmd(cmd):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception("cmd error: %s" % stderr)
    return stdout

parser = argparse.ArgumentParser(
    prog='jsonnet-extend',
    description='extend jsonnet with helm')

parser.add_argument('filename')           
parser.add_argument('-J', '--jpath')      
parser.add_argument('-y', '--yaml-stream', action='store_true')
parser.add_argument('--tla-code-file')
args = parser.parse_args()


# TODO: better?
# this inlines a method into jsonnet which will shell out to `helm template` with the same tla code file data??
def helm(chart, values):
    values = json.loads(values)
    
    app_values = ','.join([ str(k)+'='+json.dumps(v) for k, v in values.items() ])
    cmd = ["helm", "template", '--skip-tests', chart, "--set-json='"+app_values+"'" ]
    if 'version' in values:
        cmd.append('--version='+values['version'])
    # TODO: figure out some weird escaping...
    cmd = shlex.split(' '.join(cmd))
    stdout = run_cmd(cmd)

    out_objs = []
    objs = yaml.safe_load_all(stdout)
    for o in objs:
        # TODO: remove -- this is a hack around some weird helm-ness
        # right now if the chart is remote then helm prints out a pulled/digest block -- which is valid yaml but not valid manifests
        if sorted(o.keys()) == ['Digest', 'Pulled', ]:
            continue
        # TODO: better?
        # upstream `helm template` doesn't honor the `--namespace` flag (https://github.com/helm/helm/issues/3553)
        # and as such most helm charts don't handle it either. so for now we are cheating by adding this in here
        if 'namespace' in values:
            if 'metadata' in o and 'namespace' not in o['metadata']:
                o['metadata']['namespace'] = values['namespace']
        out_objs.append(o)
    
    
    return out_objs

native_callbacks = {
    'helm': (('chart', 'values'), helm),
}

tla_codes = {}
if args.tla_code_file:
    k, v = args.tla_code_file.split('=', 1)
    tla_codes = {k: open(v).read()}

ret = _jsonnet.evaluate_file(
    args.filename,
    jpathdir=args.jpath,
    
    tla_codes=tla_codes,
    native_callbacks=native_callbacks,
)

ret = json.loads(ret)

if args.yaml_stream:
    # replicate the same output stream
    for obj in ret:
        print('---\n'+json.dumps(obj, indent="   "), file=sys.stdout)
    print ('...', file=sys.stdout)
else:
    print ('done')
    print (ret)
    print ('done')
