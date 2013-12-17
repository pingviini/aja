class aja ($is_master = false, $master_private_key = "",
           $master_public_key = ""){

  user { "aja":
    ensure => "present",
    home => "/home/aja",
    managehome => true,
    shell => "/bin/bash",
  }

  file { "/home/aja":
    ensure => "directory",
    mode => 0744,
    owner => "aja",
    group => "aja",
    require => User["aja"],
  }

  file { "/home/aja/.ssh":
    ensure => "directory",
    mode => 0700,
    owner => "aja",
    group => "aja",
    require => User["aja"],
  }

  file { "/home/aja/.buildout":
    ensure => "directory",
    owner => "aja",
    require => User["aja"],
  }

  file { "/var/buildout":
    ensure => "directory",
    owner => "aja",
    require => User["aja"],
  }

  file { "/var/buildout/eggs-directory":
    ensure => "directory",
    owner => "aja",
    require => File["/var/buildout"],
  }

  exec { "chown -R aja /var/buildout/eggs-directory":
    require => File["/var/buildout/eggs-directory"],
    path => ["/bin"]
  }

  file { "/var/buildout/download-cache":
    ensure => "directory",
    owner => "aja",
    require => File["/var/buildout"],
  }

  exec { "chown -R aja /var/buildout/download-cache":
    require => File["/var/buildout/download-cache"],
    path => ["/bin"],
  }

  file { "/var/buildout/extends-cache":
    ensure => "directory",
    owner => "aja",
    require => File["/var/buildout"],
  }

  exec { "chown -R aja /var/buildout/extends-cache":
    require => File["/var/buildout/extends-cache"],
    path => ["/bin"]
  }

  file { "/home/aja/.buildout/default.cfg":
    ensure => "present",
    content => "[buildout]
eggs-directory = /var/buildout/eggs-directory
download-cache = /var/buildout/download-cache
extends-cache = /var/buildout/extends-cache",
    owner => "aja",
    group => "aja",
    require => [
    File["/var/buildout/eggs-directory"],
    File["/var/buildout/download-cache"],
    File["/var/buildout/extends-cache"]
    ]
  }

  if $is_master {
    vcsrepo { "/home/aja/aja":
      ensure => present,
      provider => git,
      source => "https://github.com/pingviini/aja",
      user => "aja",
      require => User["aja"],
    }

    exec { "python /home/aja/aja/setup.py install":
      cwd => "/home/aja/aja",
      user => "root",
      path => ["/bin", "/usr/bin"],
      require => Vcsrepo["/home/aja/aja"]
    }

    file { "/home/aja/.aja":
      ensure => "directory",
      owner => "aja",
      group => "aja",
      require => User["aja"],
    }

    file { "/home/aja/.aja/sites":
      ensure => "directory",
      owner => "aja",
      group => "aja",
      require => File["/home/aja/.aja"]
    }

    file { "/home/aja/.aja/config.cfg":
      ensure => "present",
      owner => "aja",
      group => "aja",
      require => File["/home/aja/.aja"],
      content => '[global]
buildouts-folder = /var/buildout
buildouts-config-folder = /home/aja/.aja/sites
effective-user = aja
buildout-user = aja

[git]
path = /usr/bin/git

[hg]
path = /usr/bin/hg'}

    if $master_private_key {
      file { "/home/aja/.ssh/id_rsa.pub":
        ensure => "present",
        content => $master_public_key,
        mode => 0644,
        require => File["/home/aja/.ssh"],
        owner => "aja",
        group => "aja",
      }
      file { "/home/aja/.ssh/id_rsa":
        ensure => "present",
        content => $master_private_key,
        mode => 0600,
        require => File["/home/aja/.ssh"],
        owner => "aja",
        group => "aja",
      }
    }
  }
  else {
    if $master_public_key {
      file { "/home/aja/.ssh/authorized_keys":
        ensure => "present",
        mode => 0600,
        content => $master_public_key,
        owner => "aja",
        group => "aja",
        require => File["/home/aja/.ssh"]
      }
    }
  }
}