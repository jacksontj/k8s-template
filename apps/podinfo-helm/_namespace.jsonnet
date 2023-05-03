local helm = import 'lib/helm.libsonnet';
local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  helm.template(
    'podinfo-helm',
    'oci://ghcr.io/stefanprodan/charts/podinfo',
    '6.3.5',
    {
      logLevel: 'debug',
      podAnnotations: {
        environment: ctx.Environment,
      },
    }
  ),
])
