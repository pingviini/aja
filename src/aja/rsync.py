import logging
import tempfile


class Rsync(object):

    def __init__(self, eggs_directory, path=None, files=None, excludes=None,
                 target=None, arguments=None, effective_user=None):
        if files:
            self.file = tempfile.NamedTemporaryFile()
            for line in files:
                self.file.write(line + "\n")
            self.file.seek(0)

        self.from_path = path and path + '/' or '--files-from={} /'.format(
            self.file.name)

        self.to_path = path and path or '/'  # eggs_directory
        self.arguments = arguments
        self.target = target
        self.effective_user = effective_user

        if excludes:
            self.excludes = self.generate_excludes(excludes)
        else:
            self.excludes = ()

    def generate_excludes(self, exclude):
        exclusions = tuple([str(s).replace('"', '\\\\"') for s in exclude])
        tmp = ' --exclude "%s"' * len(exclusions)
        return tmp % exclude

    def generate_excludes(self, exclude):
        exclusions = tuple([str(s).replace('"', '\\\\"') for s in exclude])
        tmp = ' --exclude "%s"' * len(exclusions)
        return tmp % exclude

    def push(self):
        """Push from here to remote."""

        cmd = 'rsync {exclude} -pthlrz {from_path} {user}@{host}:{to}'.format(
            exclude=self.excludes,
            from_path=self.from_path,
            user=self.effective_user,
            host=self.target,
            to=self.to_path)
        print("Running rsync:\n $ {cmd}".format(cmd=cmd))

        # subprocess.check_call(shlex.split(cmd))

    def pull(self):
        """Pull from remote to here."""
        cmd = 'rsync {exclude} -pthlrz {user}@{host}:{from_path} {to_path}'.format(
            exclude=self.exclusions,
            from_path=self.from_path,
            user=self.config.effective_user,
            host=self.target,
            to_path=self.to_path)
        logging.info("Running rsync: {cmd}".format(cmd=cmd))

        # subprocess.check_call(shlex.split(cmd))
