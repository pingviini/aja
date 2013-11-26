import os
import sys
import glob
import logging

from ConfigParser import (
    ConfigParser,
    NoOptionError,
    NoSectionError,
)


DEFAULT_PATHS = [
    '/etc/aja/config.cfg',
    '/usr/local/etc/aja/config.cfg',
    os.path.expanduser('~/.aja/config.cfg'),
]


class Config(object):

    def __init__(self, name=None):
        self.parser = ConfigParser()
        self.parser.read(DEFAULT_PATHS)
        if name:
            self.buildout_parser = ConfigParser()
            self.buildout_parser.read("%s/%s.cfg" % (
                self.buildouts_config_folder, name))
        else:
            self.buildout_parser = None

    def get_global_option(self, option, section='global'):
        try:
            return self.parser.get(section, option)
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
            raise  # let it flow down through the code

    def get_buildout_option(self, option, section='config'):
        try:
            return self.buildout_parser.get(section, option)
        except (NoOptionError, NoSectionError) as e:
            logging.error(str(e))
            raise  # let it flow down through the code

    @property
    def buildouts_folder(self):
        """Return path to folder which contains buildouts."""
        return self.get_global_option('buildouts-folder')

    @property
    def buildouts_config_folder(self):
        """
        Return path to folder which contains buildouts config files for
        aja.
        """
        path = self.get_global_option('buildouts-config-folder')
        if os.path.isdir(path):
            return path
        else:
            raise AjaConfigError("Invalid buildouts-config-folder. Please "
                                 "check your settings.")

    @property
    def effective_user(self):
        """
        Return effective user. If not configured, return current logged in user.
        """
        return self.get_user('effective-user')

    @property
    def buildout_user(self):
        """
        Return effective user. If not configured, return current logged in user.
        """
        return self.get_user('buildout-user')

    def get_user(self, user):
        try:
            return self.get_buildout_option(user)
        except (NoOptionError, NoSectionError):
            return self.get_global_option(user)
        except AttributeError:
            pass  # return logged in user

        return os.getlogin()

    @property
    def target(self):
        """Return deployment target hostname."""
        return self.get_buildout_option('host')

    def get_all_config_files(self):
        """Print names of available buildout config files."""
        for files in self.buildout_config_files:
            print(files)

    @property
    def buildout_config_files(self):
        """Return names of available buildout config files."""
        return glob.glob("%s/*.cfg" % self.buildouts_config_folder)

    @property
    def python(self):
        """Return path to python interpreter."""
        try:
            return self.get_buildout_option('python-path')
        except NoOptionError:
            # Ok, no python path. Maybe there is virtualenv name.
            try:
                virtualenv_name = self.get_buildout_option('virtualenv')
                return self.get_global_option(option=virtualenv_name,
                                              section='python')
            except NoOptionError:
                # Okay, so we have no python-path nor virtualenv name specified
                # in aja buildout config. Maybe we have python-path in
                # global config?
                try:
                    return self.get_global_option(option='python-path')
                except NoOptionError:
                    # Nope, no no no.
                    logging.error("You have not specified python-path or "
                                  "virtualenv in your config (%s). Please "
                                  "add one to continue.")
                    sys.exit()
        except NoSectionError as e:
            logging.error(str(e))

    @property
    def vcs_type(self):
        """Return vcs type."""
        return self.get_buildout_option('vcs-type')

    @property
    def vcs_path(self):
        """Return path to the actual buildout."""
        return self.get_buildout_option('vcs-path')

    @property
    def hg_path(self):
        """Return path to hg."""
        return self.get_global_option(option='path', section='hg')

    @property
    def deployment_target(self):
        """Deployment path."""
        return self.get_buildout_option('target')
