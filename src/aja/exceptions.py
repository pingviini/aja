class NoExecutable(Exception):
    """No valid executable found."""


class NoBootstrapException(Exception):
    """Missing bootstrap.py."""


class NoBuildoutConfigException(Exception):
    """Missing buildout.cfg."""


class AjaConfigException(Exception):
    """Invalid configuration."""


class RegistrationException(Exception):
    """Registration failed."""
