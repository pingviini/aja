import os
import subprocess
import shlex
import logging

from aja.utils import memoize
from pprint import pprint
from zc.buildout.buildout import (
    Buildout,
)


class AjaBuildout(object):

    def __init__(self, config, name):
        self.config = config
        self.name = name

    def update_buildout(self):
        os.chdir("%s/%s" % (self.config.buildouts_folder,
                            self.name))
        cmd = "%s pull" % (self.hg)
        subprocess.check_call(shlex.split(cmd))
        cmd = "%s update -C" % (self.hg)
        subprocess.check_call(shlex.split(cmd))

    def bootstrap_buildout(self):
        os.chdir("%s/%s" % (self.config.buildouts_folder,
                            self.name))
        cmd = "%s bootstrap.py" % self.config.python
        subprocess.check_call(shlex.split(cmd))

    def run_buildout(self):
        os.chdir("%s/%s" % (self.config.buildouts_folder,
                            self.name))
        cmd = "bin/buildout -N"
        subprocess.check_call(shlex.split(cmd))

    @memoize
    @property
    def buildout_config(self):
        """Parse buildout config with zc.buildout ConfigParser."""
        logging.info("Loading buildout.cfg...")
        cfg = Buildout("%s/%s/buildout.cfg" % (self.config.buildouts_folder,
                                               self.name),
                       [('buildout', 'verbosity', '0')])
        return cfg

    @property
    def buildout_parts(self):
        try:
            return self.buildout_config['buildout']['parts'].split('\n')
        except KeyError:
            logging.error("Couldn't get the buildout parts.")
            raise

    @property
    def instances(self):
        instance_list = []
        for part in self.buildout_parts:
            if self.check_recipe('plone.recipe.zope2instance', part):
                instance_list.append(part)
            elif self.check_recipe('plone.recipe.zeoserver', part):
                instance_list.append(part)
        return instance_list

    def check_recipe(self, recipe, part):
        if recipe in self.buildout_config[part]['recipe']:
            return True
        return False

    def print_config(self):
        """Print buildout config."""
        pprint(self.buildout_config)

    def parse_instance(self, path):
        with open(path, 'r') as instance:
            data = instance.readlines()
            start = 0
            end = 0
            eggs_list = []
            for counter, line in enumerate(data):
                if not start:
                    if 'sys.path[0:0]' in line:
                        start = counter + 1
                if counter >= start and not end:
                    if ']' in line:
                        end = counter

            eggs_list = self.clean_eggs_list(data[start:end])
            return eggs_list

    def clean_eggs_list(self, eggs_list):
        tmp = []
        for line in eggs_list:
            line = line.lstrip().rstrip()
            line = line.replace('\'', '')
            line = line.replace(',', '')
            if line.endswith('site-packages'):
                continue
            tmp.append(line)
        return tmp

    @property
    def eggs(self):
        """Return list of paths to eggs."""
        eggs = set()
        for instance in self.instances:
            path = "%s/%s" % (self.buildout_config[instance]['bin-directory'],
                              instance)
            eggs.update(self.parse_instance(path))
        return eggs
