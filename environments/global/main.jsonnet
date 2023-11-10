local envs = import 'environments.libsonnet';

local data = function(cluster) {
};

envs.allEnvs('global', data)
