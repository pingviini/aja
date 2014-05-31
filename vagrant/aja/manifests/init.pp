class aja (
  $is_master = false,
  $master_private_key = '',
  $master_public_key = ''
){

  group { 'buildout':
    ensure => 'present'
  }

  user { 'buildout':
    ensure => 'present',
    home => '/home/buildout',
    managehome => true,
    shell => '/bin/bash',
    gid => 'buildout',
    require => Group['buildout']
  }

  file { '/home/buildout':
    ensure => 'directory',
    mode => 0744,
    owner => 'buildout',
    group => 'buildout',
    require => User['buildout']
  }

  file { '/home/buildout/.ssh':
    ensure => 'directory',
    mode => 0700,
    owner => 'buildout',
    group => 'buildout',
    require => User['buildout']
  }

  file { '/home/buildout/.buildout':
    ensure => 'directory',
    owner => 'buildout',
    group => 'buildout',
    require => User['buildout']
  }

  file { '/var/buildout':
    ensure => 'directory',
    owner => 'buildout',
    group => 'buildout',
    require => User['buildout']
  }

  file { '/var/buildout/eggs-directory':
    ensure => 'directory',
    owner => 'buildout',
    group => 'buildout',
    require => File['/var/buildout']
  }

  file { '/var/buildout/download-cache':
    ensure => 'directory',
    owner => 'buildout',
    group => 'buildout',
    require => File['/var/buildout']
  }

  file { '/var/buildout/extends-cache':
    ensure => 'directory',
    owner => 'buildout',
    group => 'buildout',
    require => File['/var/buildout']
  }

#  exec { 'chown -R buildout /var/buildout/eggs-directory':
#    require => File['/var/buildout/eggs-directory'],
#    path => ['/bin']
#  }
#
#  exec { 'chown -R buildout /var/buildout/download-cache':
#    require => File['/var/buildout/download-cache'],
#    path => ['/bin']
#  }
#
#  exec { 'chown -R buildout /var/buildout/extends-cache':
#    require => File['/var/buildout/extends-cache'],
#    path => ['/bin']
#  }

  file { '/home/buildout/.buildout/default.cfg':
    ensure => 'present',
    content => '[buildout]
eggs-directory = /var/buildout/eggs-directory
download-cache = /var/buildout/download-cache
extends-cache = /var/buildout/extends-cache',
    owner => 'buildout',
    group => 'buildout',
    require => [
      File['/var/buildout/eggs-directory'],
      File['/var/buildout/download-cache'],
      File['/var/buildout/extends-cache']
    ]
  }

  if $is_master {
    file { '/tmp/aja-requirements.txt':
      ensure => 'present',
      content => '
-e git+https://github.com/datakurre/aja.git@master#egg=aja',
      owner => 'root',
      group => 'root'
    }
    python::virtualenv { '/usr/local/aja':
      ensure => 'present',
      requirements => '/tmp/aja-requirements.txt',
      systempkgs => false,
      owner => 'root',
      group => 'root',
      require => File['/tmp/aja-requirements.txt']
    }
    file { '/usr/local/bin/aja':
      ensure => 'link',
      target => '/usr/local/aja/bin/fab',
      require => Python::Virtualenv['/usr/local/aja']
    }
    if $master_private_key {
      file { '/home/buildout/.ssh/id_rsa.pub':
        ensure => 'present',
        content => $master_public_key,
        mode => 0644,
        require => File['/home/buildout/.ssh'],
        owner => 'buildout',
        group => 'buildout'
      }
      file { '/home/buildout/.ssh/id_rsa':
        ensure => 'present',
        content => $master_private_key,
        mode => 0600,
        require => File['/home/buildout/.ssh'],
        owner => 'buildout',
        group => 'buildout'
      }
    }
  }
  else {
    if $master_public_key {
      file { '/home/buildout/.ssh/authorized_keys':
        ensure => 'present',
        mode => 0600,
        content => $master_public_key,
        owner => 'buildout',
        group => 'buildout',
        require => File['/home/buildout/.ssh']
      }
    }
  }
}
