function(ctx) [
  {
    apiVersion: 'v1',
    kind: 'Service',
    metadata: {
      name: 'podinfo',
      namespace: 'podinfo',
    },
    spec: {
      type: 'ClusterIP',
      selector: {
        app: 'podinfo',
      },
      ports: [
        {
          name: 'http',
          port: 9898,
          protocol: 'TCP',
          targetPort: 'http',
        },
        {
          port: 9999,
          targetPort: 'grpc',
          protocol: 'TCP',
          name: 'grpc',
        },
      ],
    },
  },
]
