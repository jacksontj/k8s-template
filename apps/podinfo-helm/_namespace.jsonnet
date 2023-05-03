local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  std.native('helm')('oci://ghcr.io/stefanprodan/charts/podinfo', std.manifestJsonEx({ version: '6.3.5', namespace: 'podinfo-helm' }, ' ')),
])
