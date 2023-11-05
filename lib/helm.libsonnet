local tanka = (import 'github.com/grafana/jsonnet-libs/tanka-util/main.libsonnet') + { helm+: {
  defaultLabels:: { 'app.kubernetes.io/managed-by': 'Helm' },
} };

// This is a helper method to not require the caller to figure out the correct relative path
tanka.helm.new(std.extVar('rootDir') + '/')
