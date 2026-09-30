{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    xonsh
    matplotlib
    numpy
    pandas
  ]);
in

pkgs.mkShell {
  packages = with pkgs; [
    pypy3
    pythonEnv
    unzip
    curl
    sqlite
    texliveBasic
  ];
}
