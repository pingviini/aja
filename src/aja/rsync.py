import os
import logging


class Rsync(object):

    def __init__(self, config, arguments, exclude=()):
        self.config = config
        self.arguments = arguments
        if exclude:
            self.exclusions = self.generate_excludes(exclude)
        else:
            self.exclusions = ()

    def __call__(self):
        self.change_workingdir()

    def generate_excludes(self, exclude):
        exclusions = tuple([str(s).replace('"', '\\\\"') for s in exclude])
        tmp = ' --exclude "%s"' * len(exclusions)
        return tmp % self.exclusions

    def change_workingdir(self):
        logging.debug("Changing working dir to {working_dir}".format(
            working_dir=self.config.working_dir))
        os.chdir(self.config.working_dir)

    @property
    def target(self):
        """Return rsync target."""
        if '-d' in self.arguments:
            return self.config.development_target
        return self.config.deployment_target

    def push(self, path):
        """Push from here to remote."""

        cmd = 'rsync {exclude} -pthlrz {from_path} {user}@{host}:{to}'.format(
            exclude=self.exclusions,
            from_path=path,
            user=self.config.effective_user,
            host=self.target,
            to=path)
        logging.info("Running rsync: {cmd}".format(cmd=cmd))

        # subprocess.check_call(shlex.split(cmd))

    def pull(self):
        """Pull from remote to here."""
        cmd = 'rsync {exclude} -pthlrz {user}@{host}:{from_path} {to}'.format(
            exclude=self.exclusions,
            from_path=self.path,
            user=self.config.effective_user,
            host=self.target,
            to_path=self.path)
        logging.info("Running rsync: {cmd}".format(cmd=cmd))

        # subprocess.check_call(shlex.split(cmd))
