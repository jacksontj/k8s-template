{
  // patchArray will apply `patch` to all items in `array` that are a superset of `filter`
  patchArray(array, filter, patch):: [
    // Return boolean if `filter` is a subset of `obj`
    local ifMapSubset(filter, obj) = std.all([
      local filterVal = std.get(filter, fieldName);
      local objVal = std.get(obj, fieldName);

      // If the type is an object; we need to recurse
      if std.type(filterVal) == 'object' then
        ifMapSubset(filterVal, objVal)
      // Otherwise; we just chekc the value
      else
        filterVal == objVal
      for fieldName in std.objectFields(filter)
    ]);

    // For each item in the array; check for the filter match -- if it exists merge
    if ifMapSubset(filter, obj) then
      std.mergePatch(obj, patch)
    else
      obj
    for obj in array
  ],
}
