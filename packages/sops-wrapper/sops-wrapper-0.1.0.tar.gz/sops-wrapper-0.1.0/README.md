# sops-wrapper

This is a simple wrapper around [sops](https://github.com/mozilla/sops), which
does use the `.sops.yaml` to determine the files which need to be encrypted or
decrypted.

## Usage

1. install via pip
2. run it with `sops-wrapper encrypt --dry-run` or `sops-wrapper decrypt
   --dry-run`, remove the `--dry-run` flag to make it actually happen.


.. _sops: https://github.com/mozilla/sops
