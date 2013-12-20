import abc


class DeployBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deploy(self):
        """Deploy buildout to target."""
        raise NotImplementedError
