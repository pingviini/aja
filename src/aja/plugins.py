from pkg_resources import iter_entry_points


def get_plugins(group):
    plugins = {}
    for plugin in iter_entry_points(group=group, name=None):
        cls = plugin.load()
        plugins[plugin.name] = {'cls': cls,
                                'group': group.split('.')[-1],
                                'desc': cls.__doc__}
    return plugins
