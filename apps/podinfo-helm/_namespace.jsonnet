local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo-helm'),
  std.native('helm')('podinfo-helm', 'oci://ghcr.io/stefanprodan/charts/podinfo', '6.3.5', std.manifestJsonEx({}, ' ')),
])
