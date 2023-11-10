local clusters = import 'clusters.libsonnet';
local tanka = import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet';
local serviceCatalog = import 'imported/service_catalog.json';

// Method to convert an array of clusters -> environments
local envsForClusters(clusters, fname, f, serviceName=null) = {
  local key = if serviceName != null then serviceName else fname,
  assert key in serviceCatalog : 'serviceName %s must be in catalog' % serviceName,
  local catalogEntry = std.get(serviceCatalog, key, {}),
  envs: {
    [kv.key]: tanka.environment.new(
                name=fname + '/' + kv.value.key,
                namespace=fname,
                apiserver=kv.value.apiserver,
              )
              + tanka.environment.withLabels(
                {
                  cluster: kv.value.key,
                  region: kv.value.region,
                } + std.get(kv.value, 'labels', {}) + {
                  owners: std.join(',', catalogEntry.owners),
                },
              )
              + tanka.environment.withData(f(kv.value))

    for kv in std.objectKeysValues(clusters)
  },
};

// These are all convenience methods for creating environments based on varying conditions
{
  // all clusters defined in this repository
  allEnvs(fname, f):: envsForClusters(clusters.clusters, fname, f),
}
