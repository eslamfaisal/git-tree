# Linux build for the v1.0.1 release (local build)

The Debian/Ubuntu package for Git Tree 1.0.1, built and tested on Ubuntu 24.04 (x86_64) so it can be attached to the GitHub release by hand
(see [`RELEASING.md`](../RELEASING.md), "By hand"). It is **unsigned**; `SHA256SUMS.txt` lists its checksum.

| File | Use |
|---|---|
| `Git-Tree_1.0.1_amd64.deb` | attach to the release under this name |
| `Git-Tree-Linux.deb` | the same file under the stable name the website's download link uses (`releases/latest/download/Git-Tree-Linux.deb`) |
| `SHA256SUMS.txt` | attach as well, or merge these lines into the release's `SHA256SUMS.txt` |

Install on Ubuntu 24.04 or Debian 12: `sudo apt install ./Git-Tree-Linux.deb`. Ubuntu 22.04 and Linux Mint 21 need a newer Git first
(`sudo add-apt-repository ppa:git-core/ppa && sudo apt update && sudo apt install git`).

This package was built on Ubuntu 24.04, not on the `ubuntu-22.04` runner the release workflow uses, so it is not the official build and has not
been run on 22.04. Once the workflow has published a release, delete this folder.
