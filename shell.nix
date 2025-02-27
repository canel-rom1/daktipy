{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python3Packages.tkinter
    pkgs.python312Packages.virtualenv

    pkgs.espeak-ng
  ];

  shellHook = ''
    echo "✅ Environnement activé avec Tkinter"
  '';
}
