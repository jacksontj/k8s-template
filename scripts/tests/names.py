import collections

# To generate the list:
# kubectl api-resources --verbs=patch -o wide --namespaced=false | cut -c 48- | awk '{print $3, $1}'
TMP = '''
Namespace v1
Node v1
PersistentVolume v1
MutatingWebhookConfiguration admissionregistration.k8s.io/v1
ValidatingWebhookConfiguration admissionregistration.k8s.io/v1
CustomResourceDefinition apiextensions.k8s.io/v1
APIService apiregistration.k8s.io/v1
ClusterIssuer cert-manager.io/v1
CertificateSigningRequest certificates.k8s.io/v1
FlowSchema flowcontrol.apiserver.k8s.io/v1beta3
PriorityLevelConfiguration flowcontrol.apiserver.k8s.io/v1beta3
IngressClass networking.k8s.io/v1
RuntimeClass node.k8s.io/v1
ClusterRoleBinding rbac.authorization.k8s.io/v1
ClusterRole rbac.authorization.k8s.io/v1
PriorityClass scheduling.k8s.io/v1
CSIDriver storage.k8s.io/v1
CSINode storage.k8s.io/v1
StorageClass storage.k8s.io/v1
VolumeAttachment storage.k8s.io/v1
[jacksontj@localhost k8s-template]$'''.strip().splitlines()

GLOBAL_RESOURCES = []
for row in TMP:
    parts = row.split()
    GLOBAL_RESOURCES.append((parts[0], parts[1]))


class NameTests(object):
    """Tests for conflicting names in the respective spaces (global or namespace)
    """

    def __init__(self):
        self.global_map = collections.defaultdict(set)
        self.namespace_map = collections.defaultdict(set)

    def evaluate_manifest(self, fpath, path_namespace, key, obj):
        # special case the `Namespace` kind
        if key.kind == "Namespace":
            if key.name != path_namespace:
                raise Exception(
                    "namespace %s must match directory name expected=%s actual=%s"
                    % (fpath, path_namespace, namespace)
                )

        resource_key = (key.kind, key.apiVersion)
        if resource_key in GLOBAL_RESOURCES:
            if key in self.global_map[key.kind]:
                raise Exception("conflicting global object %s name %s" % (kind, key))
            else:
                self.global_map[key.kind].add(key)
        else:
            namespace = obj["metadata"].get("namespace", "default")
            if namespace != path_namespace:
                raise Exception(
                    "namespace for %s %s must match directory name expected=%s actual=%s"
                    % (
                        fpath,
                        key,
                        path_namespace,
                        namespace,
                    )
                )

            if key in self.namespace_map[namespace]:
                raise Exception(
                    "conflicting object name %s in namespace %s" % (key, namespace)
                )
            else:
                self.namespace_map[namespace].add(key)
