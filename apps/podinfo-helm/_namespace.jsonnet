local helm = import 'lib/helm.libsonnet';
local jsonschema = import 'lib/jsonschema.libsonnet';
local namespace = import 'lib/namespace.libsonnet';


local schema = {
  type: 'object',
  properties: {
    logLevel: { type: 'string' },
  },
};

function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  helm.template(
    'podinfo-helm',
    'oci://ghcr.io/stefanprodan/charts/podinfo',
    '6.3.5',
    jsonschema.validate({
      logLevel: 3,  //'debug',
      podAnnotations: {
        environment: ctx.Environment,
      },
    }, schema),
  ),
])
