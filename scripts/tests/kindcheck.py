DISALLOWED_KINDS = set([
    'Pod',  # for a gitops flow we don't want to define pods
])

class KindCheckTests(object):
    """Tests for disallowing specific kinds of objects
    """

    def evaluate_manifest(self, fpath, path_namespace, key, obj):
        if key.kind in DISALLOWED_KINDS:
            raise Exception("Disallowed kind %s found in %s.%s" % (key.kind, path_namespace, key))
