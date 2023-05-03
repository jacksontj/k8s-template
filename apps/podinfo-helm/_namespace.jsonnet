local helmutil = import 'lib/helm-util.libsonnet';
local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  helmutil.toArray(std.mergePatch(
    helmutil.toMap(std.native('helm')('oci://ghcr.io/stefanprodan/charts/podinfo', std.manifestJsonEx({ namespace: 'podinfo-helm' }, ' '))),
    helmutil.objectPatch('podinfo-helm', 'Deployment', 'release-name-podinfo', {
      metadata: {
        labels: {
          foo: 'bar',
        },
      },
    })
  )),
])
