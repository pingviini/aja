class { "epel": }

class bootstrap {
  package {[
    "autoconf",
    "automake",
    "asciidoc",
    "binutils",
    "bison",
    "byacc",
    "bzip2-devel",
    "cscope",
    "ctags",
    "cvs",
    "db4-devel",
    "diffstat",
    "doxygen",
    "elfutils",
    "elinks",
    "expat-devel",
    "flex",
    "freetype-devel",
    "gcc",
    "gcc-c++",
    "gcc-gfortran",
    "gdbm-devel",
    "gettext",
    "git",
    "htop",
    "indent",
    "intltool",
    "iptraf",
    "kernel-devel",
    "libcurl-devel",
    "libjpeg-turbo-devel",
    "libpng-devel",
    "libtool",
    "libxslt-devel",
    "lynx",
    "make",
    "openldap-clients",
    "openldap-devel",
    "openssl-devel",
    "patch",
    "patchutils",
    "pkgconfig",
    "python",
    "python-devel",
    "python-virtualenv",
    "python-pip",
    "rcs",
    "readline-devel",
    "subversion",
    "swig",
    "systemtap",
    "unzip",
    "vim-enhanced",
    "wget",
    "zip",
    "zlib-devel"]:
  ensure => "installed",
  require => Class["epel"],
  }

  package { ["mercurial_keyring", "mercurial"]:
    provider => "pip",
    ensure   => "installed"
  }
}


class { "bootstrap": }
class { "aja":
  is_master => true,
  master_private_key => $master_private_key,
  master_public_key => $master_public_key
}

file { "/etc/hosts":
  ensure => "present",
  content => "127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.50.11 production
192.168.50.12 development
"
}

