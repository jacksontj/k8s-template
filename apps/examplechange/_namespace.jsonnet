local helm = import 'lib/helm.libsonnet';
local namespace = import 'lib/namespace.libsonnet';
local patch = import 'lib/patch.libsonnet';

function(ctx) std.flattenArrays([
  namespace('examplechange'),
  patch.patchArray(
    // array input
    helm.template(
      'examplechange',  // namespace name
      'https://github.com/helm/examples/releases/download/hello-world-0.1.0/hello-world-0.1.0.tgz',
      '0.1.0',
      {
        service: {
          port: 8080,
        },
      }
    ),
    // Filter
    {
      kind: 'Deployment',
    },
    // patch
    {
      spec: { template: { metadata: { annotations: {
        a: 'a',
      } } } },
    }
  ),
])
