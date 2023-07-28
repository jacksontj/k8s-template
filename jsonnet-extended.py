#!/usr/bin/env python

import sys
import argparse
import shlex
from subprocess import Popen, PIPE

import jsonschema
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
def helm_template(namespace, chart, version, values=None, releasename=''):
    cmd = ["helm", "template", '--skip-tests']

    if releasename != '':
        cmd.append(releasename)

    cmd += [chart, '--version='+version, '--namespace='+namespace]

    # If values were passed in, we need to pass them down ourselves
    if values:
        values = json.loads(values)
        app_values = ','.join([ str(k)+'='+json.dumps(v) for k, v in values.items() ])
        cmd.append("--set-json='"+app_values+"'")

    # TODO: figure out some weird escaping...
    stdout = run_cmd(shlex.split(' '.join(cmd)))

    out_objs = []
    objs = yaml.safe_load_all(stdout)
    for o in objs:
        if not o:
            continue

        # TODO: remove -- this is a hack around some weird helm-ness
        # right now if the chart is remote then helm prints out a pulled/digest block -- which is valid yaml but not valid manifests
        if sorted(o.keys()) == ['Digest', 'Pulled', ]:
            continue
        # TODO: better?
        # *SOME* upstream `helm template` doesn't honor the `--namespace` flag (https://github.com/helm/helm/issues/3553)
        # and as such most helm charts don't handle it either. so for now we are cheating by adding this in here
        if 'metadata' in o:
            o['metadata']['namespace'] = namespace
        out_objs.append(o)

    return out_objs

def jsonschema_validate(obj, schema_obj):
    obj = json.loads(obj)
    schema_obj = json.loads(schema_obj)
    try:
        jsonschema.validate(obj, schema_obj, format_checker=jsonschema.FormatChecker())
        return {'valid': True, 'reason': ''}
    except jsonschema.ValidationError as e:
        return {'valid': False, 'reason': str(e)}

native_callbacks = {
    'helm.template': (('namespace', 'chart', 'version', 'values', 'releasename'), helm_template),
    'jsonschema.validate': (('obj', 'schema_obj'), jsonschema_validate),
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
