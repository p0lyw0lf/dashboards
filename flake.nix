{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          venvDir = ".venv";
          packages =
            (with pkgs; [
              awscli2
              nodejs
              python312
            ])
            ++ (with pkgs.python312Packages; [
              pip
              venvShellHook
            ])
            ++ (with pkgs.nodePackages; [
              pnpm
            ]);
        };
      }
    );
}
