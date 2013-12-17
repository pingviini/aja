class aja {
  vcsrepo { "/home/vagrant/aja":
    ensure => present,
    provider => git,
    source => "https://github.com/pingviini/aja",
    user => "vagrant",
  }
  exec { "python /home/vagrant/aja/setup.py install":
    cwd => "/home/vagrant/aja",
    user => "root",
    path => ["/bin", "/usr/bin"],
    onlyif => [ "test -d /home/vagrant/aja" ]
  }

  file { "/home/vagrant/.aja":
    ensure => "directory",
    owner => "vagrant",
    group => "vagrant",
  }

  file { "/home/vagrant/.aja/config.cfg":
    ensure => "present",
    owner => "vagrant",
    group => "vagrant",
    require => File["/home/vagrant/.aja"],
    content => '[global]
  buildouts-folder = /var/buildout
  buildouts-config-folder = /home/vagrant/.aja/sites
  effective-user = vagrant
  buildout-user = vagrant

  [git]
  path = /usr/bin/git

  [hg]
  path = /usr/bin/hg'
  }
}