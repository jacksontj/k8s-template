// TODO: change this to take an object
// Generate a key for an object
local key(namespace, kind, name) = '%(namespace)s.%(kind)s.%(name)s' % { namespace: namespace, kind: kind, name: name };

{
  // TODO: something to maintain order? (maybe have a map somewhere of the mapping) -- this causes some re-ordering
  //		Something like getKey(kind, name, namespace='')	-- with some mapping of what is global and what isn't; then combine into string key
  // This converts an array to a dict of
  //	namespace (or global) -> kind -> name
  toMap:: function(array) {
    [key(if std.objectHas(x.metadata, 'namespace') then x.metadata.namespace else 'global', x.kind, x.metadata.name)]: x
    for x in array
  },

  // This re-expands the array back to the list format it came from
  toArray:: function(obj) [
    obj[k]
    for k in std.objectFields(obj)
  ],

  objectPatch:: function(namespace, kind, name, patch) {
    [key(namespace, kind, name)]+: patch,
  },
}
