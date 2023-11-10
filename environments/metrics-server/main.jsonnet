local envs = import 'environments.libsonnet';
local tanka = import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet';
local helm = import 'helm.libsonnet';
local namespace = import 'namespace.libsonnet';

local data = function(cluster) {
  namespace: namespace('metrics-server'),

  'metrics-server': helm.template('metrics-server',
                                  'helm-charts/metrics-server',
                                  {
                                    namespace: 'metrics-server',
                                    values: {
                                    },
                                  }),
};

envs.allEnvs('metrics-server', data)
