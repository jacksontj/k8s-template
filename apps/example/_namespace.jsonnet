local helm = import 'lib/helm.libsonnet';
local namespace = import 'lib/namespace.libsonnet';


function(ctx) std.flattenArrays([
  namespace('example'),
  helm.template(
    'example',  // namespace name
    'https://github.com/helm/examples/releases/download/hello-world-0.1.0/hello-world-0.1.0.tgz',
    '0.1.0',
    {
      service: {
        port: 8080,
      },
    }
  ),
])
