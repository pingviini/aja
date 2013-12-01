"""Aja

Usage:
    aja register [<name> --config-repo=<config> --python-path=<python>
                  --vcs=<vcs> --production-host=<phost>
                  --development-host=<dhost>]
    aja info [<name>]
    aja list
    aja [clone update bootstrap buildout deploy ] <name>
    aja show-config <name>

Options:
    -h --help   Show this screen.
    --version   Show version.
    -v          Verbose output.


"""

import os
import shlex
import subprocess

from aja.buildout import AjaBuildout
from aja.config import Config
from aja.exceptions import (
    NoExecutable,
    RegistrationException
)
from aja.register import Register
from docopt import docopt
from pprint import pprint


class Aja(object):

    def __init__(self, arguments):
        self.arguments = arguments
        self.config = Config(self.arguments['<name>'])
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
        }

    def __call__(self):
        actions = [action for key, action in self.actions.items()
                   if self.arguments[key]]
        for action in actions:
            action()

    @property
    def hg(self):
        hg = self.config.hg_path
        if hg:
            return hg
        else:
            raise NoExecutable("Couldn't find hg from PATH.")

    def show_config(self):
        name = self.arguments["<name>"]
        buildout = AjaBuildout(self.config, name)
        pprint(buildout.buildout_config)
        pprint(buildout.eggs)

    def show_info(self):
        name = self.arguments["<name>"]
        if name:
            config = "Buildout (%s) config." % name
            print(config)
            print("%s" % "*" * len(config))

            print("Configured vcs path: %s" % self.config.vcs_path)
            print("Configured python path: %s" % self.config.python)
            print("Configured deployment target: %s" %
                  self.config.deployment_target)

    def list_buildouts(self):
        for dir in os.listdir(self.config.buildouts_folder):
            print("* {0}".format(dir))

    def clone_buildout(self):
        os.chdir(self.config.buildouts_folder)
        cmd = "%s clone %s" % (self.hg, self.config.vcs_path)
        subprocess.check_call(shlex.split(cmd))

    def update_buildout(self):
        os.chdir("%s/%s" % (self.config.buildouts_folder,
                            self.arguments['<name>']))
        cmd = "%s pull" % (self.hg)
        subprocess.check_call(shlex.split(cmd))
        cmd = "%s update -C" % (self.hg)
        subprocess.check_call(shlex.split(cmd))

    def bootstrap_buildout(self):
        """Run bootstrap.py on buildout folder."""
        buildout = AjaBuildout(self.config, self.arguments['<name>'])
        buildout.run_bootstrap()

    def run_buildout(self):
        buildout = AjaBuildout(self.config, self.arguments['<name>'])
        buildout.run_buildout()

    def deploy(self):
        print("Deploy...")
        pass

    def register(self):
        try:
            register = Register(self.arguments, self.config)
            register
        except RegistrationException as e:
            print(e)


def main():
    arguments = docopt(__doc__, version='Aja 0.1dev')
    app = Aja(arguments)
    app()


if __name__ == "__main__":
    main()
