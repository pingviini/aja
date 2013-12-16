from aja.rsync import Rsync


class Deploy(object):
    """Deploy buildout to target host."""

    def __init__(self, config, development=False):
        self.config = config
        self.development = development

    def deploy(self):
        rsync = Rsync(self.config, self.development)
        rsync.push()


