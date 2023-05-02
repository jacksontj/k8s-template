local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('podinfo'),
  (import 'deployment.jsonnet')(ctx),
  (import 'hpa.jsonnet')(ctx),
  (import 'service.jsonnet')(ctx),
])
