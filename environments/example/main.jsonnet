local envs = import 'environments.libsonnet';
local tanka = import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet';
local helm = import 'helm.libsonnet';
local namespace = import 'namespace.libsonnet';

local data = function(cluster) {
  namespace: namespace('example'),

  example: helm.template('example',
                         'helm-charts/hello-world',
                         {
                           namespace: 'example',
                           values: {
                             service: {
                               port: 8080,
                             },
                           },
                         }),
};

envs.allEnvs('example', data)
