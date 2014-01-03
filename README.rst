Aja
===

.. image:: https://secure.travis-ci.org/pingviini/aja.png
    :target: http://travis-ci.org/pingviini/aja

Aja is a tool for deploying buildouts to remote server.

Why another deploy tool - we already have hostout and hostout.pushdeploy?

With Aja I'm trying to streamline the deployment process with following ideas
in mind:

#. Adding new aja buildout configuration shouldn't need any other steps than
   adding the config to a specified location.
#. Deploy process should rsync only the packages which are used by buildout
   - even when using shared eggs-folder or develop-eggs.
#. People have different environments with different requirements - Aja should
   support plugins which extend its functionality.

Installation
------------

Install aja normally with pip. Aja installs following requirements:

* Fabric
* docopt
* zc.buildout
* path.py

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

Copy and modify the following content inside config.cfg you just created::

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
    target = ssh.example.org

    [develop]
    config = develop.cfg

    [vcs]
    type = hg
    uri = https://www.example.org/buildout

Usage (deployment not implemented yet)
--------------------------------------

::

    $ aja update bootstrap buildout deploy kirjasto

Plugins
-------

Currently there are three plugins available:

`ajaplugin_hg`_
    Adds Mercurial.
`ajaplugin_git`_
    Adds Git support.
`ajaplugin_plone`_
    Adds Plone deployment support.

Enjoy!


.. _ajaplugin_hg: https://github.com/pingviini/ajaplugin_hg
.. _ajaplugin_git: https://github.com/pingviini/ajaplugin_git
.. _ajaplugin_plone: https://github.com/pingviini/ajaplugin_plone
