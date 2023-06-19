{
  template(namespace, chart, version, values=null, releasename=''):: std.native('helm.template')(namespace, chart, version, if values == null then null else std.manifestJsonEx(values, ' '), releasename),
}
