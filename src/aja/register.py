import os

from ConfigParser import ConfigParser
from aja.exceptions import RegistrationException


class Register(object):

    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config
        self.path = self.validate_path()
        self.registrar = self.register()
        self.write_config()

    def register(self):
        """Register buildout."""

        config = ConfigParser()
        config.add_section('config')
        config.set('config', 'python-path', self.arguments['--python-path'])
        config.set('config', 'vcs-path', self.arguments['--vcs'])
        config.set('config', 'target', self.arguments['--production-host'])

        if '--development-host' in self.arguments.keys():
            config.add_section('develop')
            config.set('develop', 'target',
                       self.arguments['--development-host'])
        return config

    def validate_path(self):
        path = "%s/%s.cfg" % (self.config.buildouts_config_folder,
                              self.arguments['<name>'])
        if os.path.isfile(path):
            raise RegistrationException("Buildout registration exists already")
        else:
            return path

    def write_config(self):
        with open(self.path, 'w') as buildout_config:
            self.registrar.write(buildout_config)
