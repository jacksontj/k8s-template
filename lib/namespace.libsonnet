local serviceCatalog = import 'imported/service_catalog.json';

function(name, labels={}, serviceName=null) [
  local key = if serviceName != null then serviceName else name;
  assert key in serviceCatalog : 'key %s must be in catalog' % key;
  local catalogEntry = std.get(serviceCatalog, key, {});

  {
    kind: 'Namespace',
    apiVersion: 'v1',
    metadata: {
      name: name,
      labels: {
        name: name,
      } + labels + {
        owners: std.join(',', serviceCatalog[key].owners),
        // TODO: also define oncall
      },
    },
  },

  // TODO: handle bindings for users
  /*
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
          name: 'ORGNAME:k8s-users',
        },
      ],
    },
    */
]
