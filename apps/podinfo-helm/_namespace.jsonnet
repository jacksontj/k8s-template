local helm = import 'lib/helm.libsonnet';
local namespace = import 'lib/namespace.libsonnet';

local patch = import 'lib/patch.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  patch.patchArray(
    helm.template('podinfo-helm', 'oci://ghcr.io/stefanprodan/charts/podinfo', '6.3.5', {
      logLevel: 'debug',
      podAnnotations: {
        environment: ctx.Environment,
      },
    }),
    {
      metadata: {
        namespace: 'podinfo-helm',
      },
    },
    {
      metadata: {
        labels: {
          foo: 'bar',
        },
      },
    },
  ),
])
