class NoExecutable(Exception):
    """No valid executable found."""


class NoBootstrapException(Exception):
    """Missing bootstrap.py."""


class NoBuildoutConfigException(Exception):
    """Missing buildout.cfg."""


class AjaConfigError(Exception):
    """Invalid configuration."""
