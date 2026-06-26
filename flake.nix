{
  description = "do52 / do52pro ZMK firmware build environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          # Toolchain + build tools. `uv` manages the Python env / `west`
          # (see scripts/zmk.py); we don't pin Python packages in Nix.
          packages = [
            pkgs.cmake
            pkgs.ninja
            pkgs.dtc
            pkgs.gcc-arm-embedded
            pkgs.uv
            pkgs.python3
          ];

          shellHook = ''
            echo "do52 ZMK devShell — run: ./scripts/zmk.py setup (once), then build/flash"
          '';
        };
      });
}
