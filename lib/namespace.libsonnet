local serviceRegistry = import 'imported/service_registry.json';

function(name, labels={}, enablePathProtector=false) [

  assert name in serviceRegistry : 'namespace must be in service registry';
  local registryLabels = {
    owners: std.join(',', serviceRegistry[name].owners),
  };

  {
    kind: 'Namespace',
    apiVersion: 'v1',
    metadata: {
      name: name,
      labels: {
        name: name,
        [if enablePathProtector then 'path-protector']: 'enabled',
      } + labels + registryLabels,
    },
  },

  // We want to give everyone in kube-users (for now) admin access in all but the kube-system namespaces
  {
    apiVersion: 'rbac.authorization.k8s.io/v1',
    kind: 'RoleBinding',
    metadata: {
      labels: {
        'addonmanager.kubernetes.io/mode': 'EnsureExists',
        'kubernetes.io/cluster-service': 'true',
      },
      name: 'k8s-users',
      namespace: name,
    },
    roleRef: {
      apiGroup: 'rbac.authorization.k8s.io',
      kind: 'ClusterRole',
      name: if name == 'kube-system' then 'view' else 'admin',
    },
    subjects: [
      {
        apiGroup: 'rbac.authorization.k8s.io',
        kind: 'Group',
        name: 'automatedoperations:k8s-users',
      },
    ],
  },
]
