from pkg_resources import iter_entry_points


def get_plugins():
    vcs_plugins = {}
    for plugin in iter_entry_points(group='aja.plugins.vcs', name=None):
        cls = plugin.load()
        vcs_plugins[plugin.name] = {'cls': cls,
                                    'desc': cls.__doc__}
    return vcs_plugins
