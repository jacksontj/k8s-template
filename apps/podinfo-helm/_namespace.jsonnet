local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  std.native('helm')('oci://ghcr.io/stefanprodan/charts/podinfo', std.manifestJsonEx({ namespace: 'podinfo-helm' }, ' ')),
])
