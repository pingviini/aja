class aja {
  exec { "git clone https://github.com/pingviini/aja":
    user => "vagrant",
    path => [
      "/bin",
      "/usr/bin"
    ],
    require => [
      Package['git']
    ]
  }

  exec { "python /home/vagrant/aja/setup.py install":
    cwd => "/home/vagrant/aja",
    user => "root",
    require => Exec["git clone https://github.com/pingviini/aja"],
    path => ["/bin", "/usr/bin"]
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