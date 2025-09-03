let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05") {
    config = {}; overlays = [];
  };
  nur = import (fetchTarball "https://github.com/nix-community/NUR/archive/main.tar.gz") {
    inherit pkgs;
  };
in

pkgs.mkShellNoCC {
  packages = [
    pkgs.python3
    pkgs.python3Packages.adjusttext
    pkgs.python3Packages.geopandas
    pkgs.python3Packages.matplotlib
    pkgs.python3Packages.osmnx
    pkgs.python3Packages.pandas
    pkgs.python3Packages.shapely
    nur.repos.sikmir.contextily
  ];
}
