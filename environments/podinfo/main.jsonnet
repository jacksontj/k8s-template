local envs = import 'environments.libsonnet';
local tanka = import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet';
local helm = import 'helm.libsonnet';
local namespace = import 'namespace.libsonnet';

local data = function(cluster) {
  namespace: namespace('podinfo'),

  podinfo: helm.template('podinfo',
                         'helm-charts/podinfo',
                         {
                           namespace: 'podinfo',
                           skipTests: true,
                           values: {
                             logLevel: 'debug',
                           },
                         }),
};

envs.allEnvs('podinfo', data)
