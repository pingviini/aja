# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile

from fabric import api
from fabric.api import task
from fabric.context_managers import (
    lcd,
    settings
)
from fabric.network import parse_host_string
from fabric.tasks import (
    Task,
    execute
)
from fabric.operations import (
    local,
    os
)
from aja.utils import (
    local_buildout_user,
    get_rsync,
    get_buildout_directory,
    get_buildout_config,
    get_buildout_extends,
    get_buildout_eggs
)


class AjaTask(Task):
    def __init__(self, func, *args, **kwargs):
        super(AjaTask, self).__init__(*args, **kwargs)
        self.func = func

    def run(self, *args, **kwargs):
        buildout_directory = get_buildout_directory(api.env.host)
        buildout = get_buildout_config(
            os.path.join(buildout_directory, 'buildout.cfg')
        )
        keys = api.env.keys()
        config = dict([
            (key.replace('-', '_'), value) for key, value
            in buildout.get('aja', {}).items() if key in keys
        ])
        if 'host_string' in config:
            config.update(parse_host_string(config.get('host_string')))
        config['buildout'] = buildout
        directory = buildout.get('buildout', {}).get('directory')
        with settings(**config):
            with lcd(directory):
                return self.func(*args, **kwargs)


@task()
def create(buildout_directory, buildout_extends):
    """Create buildout directory
    """
    ##
    # Resolve arguments
    aja_buildout_directory = get_buildout_directory(buildout_directory)
    aja_buildout_extends = get_buildout_extends(
        buildout_directory, buildout_extends
    )

    ##
    # Create buildout directory
    local_buildout_user(
        'mkdir -p {0:s}'.format(aja_buildout_directory)
    )

    # Create buildout.cfg
    aja_buildout_filename = os.path.join(
        aja_buildout_directory, 'buildout.cfg'
    )
    contents = """\
[buildout]
extends = {0:s}
""".format(aja_buildout_extends)

    # Write buildout.cfg
    with NamedTemporaryFile() as output:
        print("[localhost] create: {0:s}".format(output.name))
        output.write(contents)
        output.flush()
        local('chmod a+r {0:s}'.format(output.name))
        local_buildout_user('cp {0:s} {1:s}'.format(
            output.name, aja_buildout_filename)
        )


@task(task_class=AjaTask)
def bootstrap_download(*args):
    cmd = 'curl -O http://downloads.buildout.org/2/bootstrap.py'
    local_buildout_user(' '.join([cmd] + list(args)))
bootstrap_download.__doc__ = \
    """Download bootstrap.py
    """


@task(task_class=AjaTask)
def bootstrap(*args):
    if not os.path.isfile('bootstrap.py'):
        execute(bootstrap_download)
    cmd = '{0:s} bootstrap.py'.format(
        (api.env.buildout.get('aja') or {}).get('executable')
        or api.env.buildout.get('buildout').get('executable')
    )
    local_buildout_user(' '.join([cmd] + list(args)))
bootstrap.__doc__ = \
    """Execute bootstrap.py
    """


@task(task_class=AjaTask)
def buildout(*args):
    if not os.path.isfile('bin/buildout'):
        execute(bootstrap)
    cmd = 'bin/buildout'
    local_buildout_user(' '.join([cmd] + list(args)))
buildout.__doc__ = \
    """Execute bin/buildout
    """


@task(task_class=AjaTask)
def push():
    ##
    # Push bin
    with get_rsync(
        files=api.env.buildout['buildout'].get('bin-directory'),
        exclude=os.path.join(
            api.env.buildout['buildout'].get('bin-directory'), 'buildout')
    ) as cmd:
        local_buildout_user(cmd)
    ##
    # Push parts
    with get_rsync(
        files=api.env.buildout['buildout'].get('parts-directory')
    ) as cmd:
        local_buildout_user(cmd)
    ##
    # Push eggs
    with get_rsync(
        files=get_buildout_eggs(api.env.buildout)
    ) as cmd:
        local_buildout_user(cmd)
push.__doc__ = \
    """Push bin-, parts- and eggs-directories
    """
