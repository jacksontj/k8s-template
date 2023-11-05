import json

class NamespaceTests(object):
    """Check for specific attributes on a namespace
    """
    def __init__(self):
        with open('lib/imported/service_catalog.json') as fh:
            self.catalog = json.load(fh)

        self.owners = set()

        for val in self.catalog.values():
            self.owners.add(','.join(val['owners']))

    def evaluate_manifest(self, fpath, path_namespace, key, obj):
        if key.kind != "Namespace":
            return

        # ensure that all namespaces have the following 2 labels that match our catalog
        assert obj['metadata']['labels']['owners'] in self.owners
