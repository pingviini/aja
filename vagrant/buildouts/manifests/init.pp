class buildouts {
  file { "/home/vagrant/.buildout":
    ensure => "directory",
    owner => "vagrant",
  }

  file { "/var/buildout":
    ensure => "directory",
    owner => "vagrant",
  }

  file { "/var/buildout/eggs-directory":
    ensure => "directory",
    owner => "vagrant",
    require => File["/var/buildout"]
  }

  exec { "chown -R vagrant /var/buildout/eggs-directory":
    require => File["/var/buildout/eggs-directory"],
    path => ["/bin"]
  }

  file { "/var/buildout/download-cache":
    ensure => "directory",
    owner => "vagrant",
    require => File["/var/buildout"]
  }

  exec { "chown -R vagrant /var/buildout/download-cache":
    require => File["/var/buildout/download-cache"],
    path => ["/bin"],
  }

  file { "/var/buildout/extends-cache":
    ensure => "directory",
    owner => "vagrant",
    require => File["/var/buildout"]
  }

  exec { "chown -R vagrant /var/buildout/extends-cache":
    require => File["/var/buildout/extends-cache"],
    path => ["/bin"]
  }

  file { "/home/vagrant/.buildout/default.cfg":
    ensure => "present",
    content => "[buildout]
  eggs-directory = /var/buildout/eggs-directory
  download-cache = /var/buildout/download-cache
  extends-cache = /var/buildout/extends-cache
  ",
    owner => "vagrant",
    group => "vagrant",
    require => [
      File["/var/buildout/eggs-directory"],
      File["/var/buildout/download-cache"],
      File["/var/buildout/extends-cache"]
    ]
  }
}