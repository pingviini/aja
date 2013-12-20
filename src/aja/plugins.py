from pkg_resources import iter_entry_points


def get_plugins():
    vcs_plugins = {}
    for object in iter_entry_points(group='aja.plugins.vcs', name=None):
        vcs_plugins[object.name] = object.load()
    return vcs_plugins
