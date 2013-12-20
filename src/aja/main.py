"""Aja

Usage:
    aja list
    aja list-plugins
    aja show-config <name>
    aja register <name> [--config-repo=<config>
                         --python-path=<python>
                         --vcs=<vcs>
                         --production-host=<phost>
                         --development-host=<dhost>]
    aja [(-c <config_path>)] info [<name>...]
    aja [(-c <config_path>)]  [clone update bootstrap buildout -N deploy -d] <name>...

Options:
    -c <config_path>, --config-path=<config_path>  Config path.
    -h --help   Show this screen.
    --version   Show version.
    -v          Verbose output.
    -d          Deploy to development server.


"""

import os

from docopt import docopt
from pprint import pprint
from path import path

from .buildout import AjaBuildout
from .config import Config
from .exceptions import (
    RegistrationException
)
from .rsync import Rsync
from .register import Register
from .plugins import get_plugins


class Aja(object):

    def __init__(self, arguments):
        self.arguments = arguments
        self.names = self.arguments['<name>']
        self.vcs_plugins = get_plugins('aja.plugins.vcs')
        self.deploy_plugins = get_plugins('aja.plugins.deploy')
        self.config_path = self.arguments['--config-path']
        self.configs = {name: Config(name, config_path=self.config_path) for
                        name in self.names}
        self.actions = {
            'clone': self.clone_buildout,
            'list': self.list_buildouts,
            'info': self.show_info,
            'update': self.update_buildout,
            'bootstrap': self.bootstrap_buildout,
            'buildout': self.run_buildout,
            'register': self.register,
            'deploy': self.deploy,
            'show-config': self.show_config,
            'list-plugins': self.list_plugins,
            }


    def __call__(self):
        actions = [action for key, action in self.actions.items()
                   if self.arguments[key]]
        for action in actions:
            action()

    def show_config(self):
        for name in self.names:
            buildout = AjaBuildout(self.configs[name], self.arguments)
            pprint(buildout.buildout_config)
            pprint(buildout.eggs)

    def show_info(self):
        for name in self.names:
            config = "Buildout {name} config.".format(name=name)
            print(config)
            print("%s" % "*" * len(config))

            print("Configured vcs path: {}".format(self.config.vcs_path))
            print("Configured python path: {}".format(self.config.python))
            print("Configured deployment target: {}".format(
                  self.config.deployment_target))

    def list_buildouts(self):
        for dir in path(self.config.buildouts_folder):
            print("* {0}".format(dir))

    def clone_buildout(self):
        for name in self.names:
            buildout = AjaBuildout(self.configs[name], self.arguments)
            buildout.clone_buildout()

    def update_buildout(self):
        for name in self.names:
            buildout = AjaBuildout(self.configs[name], self.arguments)
            buildout.update_buildout()

    def bootstrap_buildout(self):
        """Run bootstrap.py on buildout folder."""
        for name in self.names:
            buildout = AjaBuildout(self.configs[name], self.arguments)
            buildout.bootstrap_buildout()

    def run_buildout(self):
        for name in self.names:
            buildout = AjaBuildout(self.configs[name], self.arguments)
            buildout.run_buildout()

    def deploy(self):
        for name in self.names:
            config = self.configs[name]
            dep = self.deploy_plugins[self.configs[name].buildout_type]['cls'](
                config, self.arguments)
            dep.deploy()
            dep.deploy_eggs()

    def stage(self):
        for name in self.names:
            print("Staging {}...".format(name))

    def register(self):
        try:
            register = Register(self.arguments, self.config)
            register
        except RegistrationException as e:
            print(e)

    def list_plugins(self):
        """Print installed aja plugins with their documentation."""
        if self.vcs_plugins:
            print("VCS plugins:")
        for plugin in self.vcs_plugins:
            print " * {name} [{group}] - {docstring}".format(
                name=plugin,
                group=self.vcs_plugins[plugin]['group'],
                docstring=self.vcs_plugins[plugin]['desc']
            )

        if self.deploy_plugins:
            print("\nDeploy plugins::")
        for plugin in self.deploy_plugins:
            print " * {name} [{group}] - {docstring}".format(
                name=plugin,
                group=self.deploy_plugins[plugin]['group'],
                docstring=self.deploy_plugins[plugin]['desc']
            )


def main():
    arguments = docopt(__doc__, version='Aja 0.1dev')
    app = Aja(arguments)
    app()


if __name__ == "__main__":
    main()
