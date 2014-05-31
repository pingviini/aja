# -*- coding: utf-8 -*-
from contextlib import contextmanager
import os.path
from tempfile import NamedTemporaryFile
from urlparse import (
    urlparse,
    urljoin
)

from fabric import api
from fabric.operations import local
from zc.buildout.buildout import Buildout


_memo = {}


def memoize(function):
    def wrapper(*args):
        if args in _memo:
            return _memo[args]
        else:
            rv = function(*args)
            _memo[args] = rv
            return rv
    return wrapper


@memoize
def get_buildout_config(buildout_filename):
    """Parse buildout config with zc.buildout ConfigParser
    """
    print("[localhost] get_buildout_config: {0:s}".format(buildout_filename))
    buildout = Buildout(buildout_filename, [('buildout', 'verbosity', '-100')])
    while True:
        try:
            len(buildout.items())
            break
        except OSError:
            pass
    return buildout


def get_buildout_parts(buildout, query=None):
    """Return buildout parts matching the given query
    """
    parts = names = (buildout['buildout'].get('parts') or '').split('\n')
    for name in names:
        part = buildout.get(name) or {}
        for key, value in (query or {}).items():
            if value not in (part.get(key) or ''):
                parts.remove(name)
                break
    return parts


def get_buildout_eggs(buildout, query=None):
    """Return buildout eggs matching the parts for the given query
    """
    eggs = set()
    for name in get_buildout_parts(buildout, query=query):
        if name == 'buildout':
            continue  # skip eggs from the buildout script itself
        path = os.path.join(buildout['buildout'].get('bin-directory'), name)
        if os.path.isfile(path):
            eggs.update(parse_eggs_list(path))
    return list(eggs)


def parse_eggs_list(path):
    """Parse eggs list from the script at the given path
    """
    with open(path, 'r') as script:
        data = script.readlines()
        start = 0
        end = 0
        for counter, line in enumerate(data):
            if not start:
                if 'sys.path[0:0]' in line:
                    start = counter + 1
            if counter >= start and not end:
                if ']' in line:
                    end = counter
        script_eggs = tidy_eggs_list(data[start:end])
    return script_eggs


def tidy_eggs_list(eggs_list):
    """Tidy the given eggs list
    """
    tmp = []
    for line in eggs_list:
        line = line.lstrip().rstrip()
        line = line.replace('\'', '')
        line = line.replace(',', '')
        if line.endswith('site-packages'):
            continue
        tmp.append(line)
    return tmp


@contextmanager
def get_rsync(files, source='/', target='/', exclude=None, arguments=None):
    with NamedTemporaryFile() as files_file:
        with NamedTemporaryFile() as exclude_file:
            cmd = ['rsync']

            # fix or set default files
            if isinstance(files, str) or isinstance(files, unicode):
                files = [files]
            elif files is None:
                files = []

            # fix or set default exclude
            if isinstance(exclude, str) or isinstance(exclude, unicode):
                exclude = [exclude]
            elif exclude is None:
                exclude = []

            # set common prefix to avoid rsync with root ('/') if possible
            prefix = os.path.commonprefix(files + exclude)
            try:
                target_host, target_path = target.split(':')
            except ValueError:
                target_host = None
                target_path = target
            if prefix.startswith(source) and prefix.startswith(target_path):
                source = prefix
                if target_host:
                    target = ':'.join([target_host, prefix])
                else:
                    target = prefix
            else:
                prefix = ''

            # build files-from
            for line in (files or []):
                files_file.write(line[len(prefix):] + '\n')
                files_file.flush()
            if files:
                local('chmod a+r {0:s}'.format(files_file.name))
                cmd.append('--files-from={0:s}'.format(files_file.name))

            # build exclude-from
            for line in (exclude or []):
                exclude_file.write(line[len(prefix):] + '\n')
                exclude_file.flush()
            if exclude:
                local('chmod a+r {0:s}'.format(exclude_file.name))
                cmd.append('--exclude-from={0:s}'.format(exclude_file.name))

            # -p preserve permissions
            # -t preserve modification times
            # -h output numbers in a human-readable format
            # -l copy symlinks as symlinks
            # -r recurse into directories
            # -z compress file data during the transfer
            cmd.append('-pthlrz')

            if arguments:
                cmd.append(arguments)

            cmd.append(source)
            cmd.append(target)

            yield ' '.join(cmd)


def local_buildout_user(cmd, *args, **kwargs):
    aja_buildout_user = api.env.get('aja_buildout_user') or None
    if api.env.aja_buildout_user:
        local_sudo = 'sudo -u {0:s} '.format(aja_buildout_user)
    else:
        local_sudo = ''
    local(local_sudo + cmd, *args, **kwargs)


def get_buildout_directory(buildout_directory):
    aja_buildout_root = api.env.get('aja_buildout_root') or ''
    if not urlparse(buildout_directory).path.startswith('/'):
        return os.path.join(aja_buildout_root,
                            buildout_directory)
    else:
        return buildout_directory


def get_buildout_extends(buildout_directory, buildout_extends):
    aja_buildout_prefix = api.env.get('aja_buildout_prefix') or ''
    if not urlparse(buildout_extends).path.startswith('/'):
        return urljoin(urljoin(aja_buildout_prefix, buildout_directory) + '/',
                       buildout_extends)
    else:
        return buildout_extends
