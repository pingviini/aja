Aja
===

Aja is a tool for deploying buildouts to remote server.

Installation
------------

Install aja normally with pip. Aja installs following requirements:

* Fabric
* docopt
* zc.buildout
* reg

::

    $ pip install aja

Configure
---------

Create global configuration for aja. Aja will look up the configuration from
the following directories by default:

* /etc/aja/config.cfg
* /usr/local/etc/config.cfg
* $HOME/.aja/config.cfg

    $ mkdir -p ~/.aja/sites
    $ touch ~/.aja/config.cfg

Copy and modifu the following content inside config.cfg you just created::

    [global]
    buildouts-folder = /path/to/buildouts
    buildouts-config-folder = /path/to/buildouts/aja/configuration
    effective-user = username
    buildout-user = username

    [git]
    path = /path/to/git

    [hg]
    path = /path/to/hg


Add config for site under /path/to/buildouts/aja/configuration::

    [config]
    python-path = /path/to/python/for/bootstrapping
    vcs-path = https://www.example.org/buildout
    vcs-type = hg
    target = ssh.example.org

    [develop]
    config = develop.cfg

Usage (deployment not implemented yet)
--------------------------------------

::

    $ aja update bootstrap buildout deploy kirjasto

Enjoy!
