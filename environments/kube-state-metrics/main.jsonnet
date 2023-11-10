local envs = import 'environments.libsonnet';
local tanka = import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet';
local helm = import 'helm.libsonnet';
local namespace = import 'namespace.libsonnet';

local data = function(cluster) {
  namespace: namespace('kube-state-metrics'),

  'kube-state-metrics': helm.template('kube-state-metrics',
                                      'helm-charts/kube-state-metrics',
                                      {
                                        namespace: 'kube-state-metrics',
                                        values: {
                                        },
                                      }),
};

envs.allEnvs('kube-state-metrics', data)
