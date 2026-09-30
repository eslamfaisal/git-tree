# Publishing a release

The installers users download are attached to a release of **this** repository. The release workflow here
builds and publishes them (below); the manual route at the end is the fallback. Either way, this
page is the checklist that keeps the website's download buttons and the README's links working.

## How users get the installer

| Where | Link | How it resolves |
|---|---|---|
| Website and README buttons | `https://gittree.app/api/download/macos` · `…/windows` · `…/linux` (the `.deb`) · `…/linux-appimage` | The site asks GitHub for this repository's published releases, takes the **highest stable version**, and redirects to that release's installer file — a direct download, not the release page. It reuses GitHub's answer for a few minutes, so a new release reaches the buttons within about 10. |
| If GitHub's API cannot be asked (rate limit, outage) | the same buttons | They redirect to GitHub's permanent link below instead, so a download still starts. |
| Permanent links, no website needed | `https://github.com/eslamfaisal/git-tree/releases/latest/download/Git-Tree-macOS.dmg` · `…/Git-Tree-Windows-setup.exe` · `…/Git-Tree-Linux.deb` · `…/Git-Tree-Linux.AppImage` | GitHub redirects `latest/download/<name>` to the file of that name on the **latest release**. The names never change, so these links never break. |

What the website picks (first match):

| Platform | Asset |
|---|---|
| macOS | a `.dmg` whose name contains `universal` (`Git-Tree_X.Y.Z_universal.dmg`), else any `.dmg` (`Git-Tree-macOS.dmg`) |
| Windows | `…_x64-setup.exe` (`Git-Tree_X.Y.Z_x64-setup.exe`), else any `…-setup.exe`, any `.exe`, then a `.msi` |
| Linux (`.deb`) | `…_amd64.deb` (`Git-Tree_X.Y.Z_amd64.deb`), else any `.deb` (`Git-Tree-Linux.deb`) |
| Linux (AppImage) | `…_amd64.AppImage` (`Git-Tree_X.Y.Z_amd64.AppImage`), else any `.AppImage` (`Git-Tree-Linux.AppImage`); a `.AppImage.sig` or `.AppImage.tar.gz` is never picked |

- **Drafts, pre-releases and tags that are not `vX.Y.Z` are never served.**
- With no release, or no matching asset, the buttons open the Releases page instead of failing.
- Every release must therefore carry the **six installer names** below — the three stable ones are what the
  permanent links need.

## Every release attaches

| File | What |
|---|---|
| `Git-Tree_X.Y.Z_universal.dmg` | the macOS installer (Apple silicon and Intel) |
| `Git-Tree_X.Y.Z_x64-setup.exe` | the Windows installer |
| `Git-Tree_X.Y.Z_amd64.deb` | the Debian / Ubuntu package (64-bit; Ubuntu 22.04 and later, Debian 12 and later) |
| `Git-Tree_X.Y.Z_amd64.AppImage` | the portable Linux app (same systems) |
| `Git-Tree-macOS.dmg` | the same `.dmg` under a name that never changes |
| `Git-Tree-Windows-setup.exe` | the same installer under a name that never changes |
| `Git-Tree-Linux.deb` | the same `.deb` under a name that never changes |
| `Git-Tree-Linux.AppImage` | the same AppImage under a name that never changes |
| `SHA256SUMS.txt` | SHA-256 of every file above |

Never attach source code or anything from the private repositories: GitHub's automatic *Source code* archives
contain only this public repository.

## Automatic: run the release workflow (free)

**Actions › release › Run workflow**, with the version tag (`v1.0.0`; the source's version must equal it).
The workflow checks out the maintainer's private source repository, builds the installers on
GitHub's macOS, Windows and Ubuntu runners (macOS and Windows are signed when the secrets below are set; the Linux
`.deb` and AppImage are not signed, `SHA256SUMS.txt` is how users verify them), checks their sizes, and once
**all three** exist creates the release
`vX.Y.Z` here with the files above, `SHA256SUMS.txt` and release notes. It lives in this public
repository on purpose: standard runners are free and unlimited for public repositories, so it costs
nothing on GitHub's free plan. Only people with write access here can start it. A tag with a suffix
(`v1.1.0-beta.1`) is published as a pre-release and never becomes *Latest*.

One-time setup, by the owner (Settings › Environments › New environment `release`, with required reviewers):

| Secret in the `release` environment | What |
|---|---|
| `SOURCE_REPO_TOKEN` | required: a fine-grained personal access token limited to the private source repository, permission *Contents: Read-only* |
| `APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`, `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH` | optional: Developer ID signing and notarization. Without them the `.dmg` is unsigned and the release notes say so |

The Linux leg needs no secret of its own.

Build logs of a public repository are public: a failing build can print file names and compiler
messages of the private source. Keep the environment's required reviewer on, and never pass the source
token to anything but the checkout steps.

## By hand (fallback)

1. Build and sign locally, or take `installers-*` from the workflow run's artifacts.
2. Name the files as in the table above. Tauri writes `Git Tree_X.Y.Z_universal.dmg`,
   `Git Tree_X.Y.Z_x64-setup.exe`, `Git Tree_X.Y.Z_amd64.deb` and `Git Tree_X.Y.Z_amd64.AppImage` (with a space);
   from the folder holding them:
   ```bash
   V=1.0.0
   cp "Git Tree_${V}_universal.dmg" "Git-Tree_${V}_universal.dmg"
   cp "Git Tree_${V}_universal.dmg" Git-Tree-macOS.dmg
   cp "Git Tree_${V}_x64-setup.exe" "Git-Tree_${V}_x64-setup.exe"
   cp "Git Tree_${V}_x64-setup.exe" Git-Tree-Windows-setup.exe
   cp "Git Tree_${V}_amd64.deb" "Git-Tree_${V}_amd64.deb"
   cp "Git Tree_${V}_amd64.deb" Git-Tree-Linux.deb
   cp "Git Tree_${V}_amd64.AppImage" "Git-Tree_${V}_amd64.AppImage"
   cp "Git Tree_${V}_amd64.AppImage" Git-Tree-Linux.AppImage
   chmod +x Git-Tree_"${V}"_amd64.AppImage Git-Tree-Linux.AppImage
   sha256sum Git-Tree_"${V}"_universal.dmg Git-Tree_"${V}"_x64-setup.exe Git-Tree_"${V}"_amd64.deb Git-Tree_"${V}"_amd64.AppImage \
     Git-Tree-macOS.dmg Git-Tree-Windows-setup.exe Git-Tree-Linux.deb Git-Tree-Linux.AppImage > SHA256SUMS.txt
   ```
3. Create the release: tag `vX.Y.Z` (SemVer), title `Git Tree vX.Y.Z`, release notes, and attach the nine files.
4. Leave **Set as a pre-release** unticked and **Set as the latest release** ticked for a stable version, then
   **Publish release**.

## After publishing

1. Open `https://github.com/eslamfaisal/git-tree/releases/latest/download/Git-Tree-macOS.dmg` and the Windows,
   Linux `.deb` and Linux AppImage links: each must start a download.
2. Within about 10 minutes, `https://gittree.app/api/download/macos`, `…/windows`, `…/linux` and
   `…/linux-appimage` must download the same files.
3. On an Ubuntu machine, `sudo apt install ./Git-Tree-Linux.deb` must succeed and **Git Tree** must open from the
   application menu.

## In-app updates

Git Tree updates itself from **this** repository's releases (ADR-0021 in the source repository). At launch,
unless the user turned **Automatically check for updates** off, it reads
`https://api.github.com/repos/eslamfaisal/git-tree/releases`, picks the newest newer release that has an
installer for the machine, and offers it in its update bar. On the user's click it downloads that installer,
checks its SHA-256, and installs it: the `.dmg` replaces the app bundle, the Windows installer runs passively and
relaunches the app, the `.deb` goes through the administrator prompt (`pkexec apt-get install`), and an AppImage
is replaced beside itself. When that is impossible it opens the installer for the user.

So every release must keep what the app reads, exactly as the tables above describe:

- the tag `vX.Y.Z` (`vX.Y.Z-beta.N` for a pre-release, which only users on the beta channel are offered);
  a draft, or a tag of any other shape, is never offered;
- the **versioned installer names** (`Git-Tree_X.Y.Z_universal.dmg`, `…_x64-setup.exe`, `…_amd64.deb`,
  `…_amd64.AppImage`); the stable-name copies are the fallback;
- **`SHA256SUMS.txt`** listing each installer. The app compares the download with that line and with the
  SHA-256 GitHub records for the uploaded file; a mismatch is deleted and never installed, and an installer
  that neither states is refused.

Once the owner generates the updater key pair (`P00-T28` in the source repository), each installer also gets a
minisign signature `<installer name>.sig` (for example `Git-Tree_1.2.0_amd64.deb.sig`), and from the first build
that embeds the public key the app refuses an installer without a valid one. There is no `latest.json`. The
website's download buttons never pick a `.sig`.
