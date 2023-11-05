local raw_clusters = std.parseYaml(importstr 'imported/clusters.yaml');
local switch = import 'switch.libsonnet';

{
  local this = self,
  clusters: {
    [kv.key]: { apiserver: 'noop' } + kv.value
    for kv in std.objectKeysValues(raw_clusters)
  },

  // Filter the clusters we have by a given environment (account)
  forEnv(env):: {
    [if kv.value.account == env then kv.key else null]: kv.value
    for kv in std.objectKeysValues(this.clusters)
  },
}
