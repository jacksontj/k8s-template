from . import names, namespaces, kindcheck

manifest_plugins = {
    'names': names.NameTests,
    'namespaces': namespaces.NamespaceTests,
    'kindcheck': kindcheck.KindCheckTests,
}
