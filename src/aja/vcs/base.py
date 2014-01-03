import abc


class VcsBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def pull(self, repository_uri):
        """Pull source code."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        """Update repository."""
        raise NotImplementedError

