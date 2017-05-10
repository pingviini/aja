{ pkgs ? import <nixpkgs> {}
, pythonPackages ? pkgs.python27Packages
}:

let self = rec {
  buildout = pythonPackages.zc_buildout_nix.overrideDerivation (args: {
    postInstall = "";
    propagatedNativeBuildInputs = [
      pythonPackages.paramiko
    ];
  });
};
in pkgs.stdenv.mkDerivation rec {
  name = "env";
  env = pkgs.buildEnv { name = name; paths = buildInputs; };
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup; ln -s $env $out
  '';
  buildInputs = with self; [
    buildout
    (pkgs.pythonFull.buildEnv.override {
      extraLibs = buildout.propagatedNativeBuildInputs;
    })
  ];
  shellHook = ''
    export BUILDOUT_ARGS="\
        versions:setuptools= \
        versions:zc.buildout="
  '';
}
