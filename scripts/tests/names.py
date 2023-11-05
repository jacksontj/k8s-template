import collections


GLOBAL_KINDS = (
    "ClusterRoleBinding",
    "ClusterRole",
    # TODO: do better handling/parsing for these, for now just treating as a global (meaning it needs to be in kube-system)
    "CustomResourceDefinition",
    "PodSecurityPolicy",
    "StorageClass",
)


class NameTests(object):
    """Tests for conflicting names in the respective spaces (global or namespace)
    """

    def __init__(self):
        self.global_map = collections.defaultdict(set)
        self.namespace_map = collections.defaultdict(set)

    def evaluate_manifest(self, fpath, path_namespace, key, obj):
        if key.kind in GLOBAL_KINDS:
            # TODO: enable this check, for now we'll allow them to be in any folder but longer-term
            # we should require them to be somewhere
            if False and path_namespace != "kube-system":
                raise Exception(
                    "global objects can only be defined in the kube-system namespace: %s.%s" % (path_namespace, key)
                )
            if key in self.global_map[key.kind]:
                raise Exception("conflicting global object %s name %s" % (kind, key))
            else:
                self.global_map[key.kind].add(key)
        else:
            namespace = obj["metadata"].get("namespace", "default")
            if key.kind == "Namespace":
                if key.name != path_namespace:
                    raise Exception(
                        "namespace %s must match directory name expected=%s actual=%s"
                        % (fpath, path_namespace, namespace)
                    )
            else:
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
