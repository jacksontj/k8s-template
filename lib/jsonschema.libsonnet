{
  validate(obj, schema_obj):: [
    local valid = std.native('jsonschema.validate')(std.manifestJsonEx(obj, ' '), std.manifestJsonEx(schema_obj, ' '));
    assert valid.valid : valid.reason;
    obj,
  ][0],
}
