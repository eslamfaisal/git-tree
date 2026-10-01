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

## Release asset contract (binding)

One table, read the same way by the website's download buttons, the in-app updater and the release gate
(`tooling/release-gate.py` in the source repository). `V` is the tag without its `v` (`v1.2.0` → `1.2.0`,
`v1.3.0-beta.1` → `1.3.0-beta.1`). A download or an update takes the **versioned** name, else the **stable** name,
compared exactly (case and all). **No other file is ever picked**: never an installer for another architecture
(`…_aarch64.dmg`, `…_x64.dmg`, `…_arm64-setup.exe`, `…_arm64.deb`, `…_aarch64.AppImage`), never a `.msi`, and never a
`.sig`, `.zsync` or `.tar.gz` beside an installer. When a release has neither name for a platform, that platform is
explicitly *unavailable* for it: the website sends the visitor to the releases list, the app says there is no
installer for this computer yet.

| Platform (install format) | Versioned name | Stable name |
|---|---|---|
| macOS, Apple silicon **and** Intel (one universal `.dmg`) | `Git-Tree_V_universal.dmg` | `Git-Tree-macOS.dmg` |
| Windows x64 (NSIS installer) | `Git-Tree_V_x64-setup.exe` | `Git-Tree-Windows-setup.exe` |
| Linux x86_64 / amd64 (Debian package) | `Git-Tree_V_amd64.deb` | `Git-Tree-Linux.deb` |
| Linux x86_64 / amd64 (AppImage) | `Git-Tree_V_amd64.AppImage` | `Git-Tree-Linux.AppImage` |

Beside each installer: `<installer name>.sig` (its minisign signature, once the updater key exists, below) and one
`SHA256SUMS.txt` listing every file. The stable-name copy has exactly the bytes of the versioned file.

- **Drafts, pre-releases and tags that are not `vX.Y.Z` are never served by the website**, even when no stable
  release exists. Pre-releases (`vX.Y.Z-pre`, or GitHub's *pre-release* flag) reach only app users who chose the
  beta channel.
- The highest version wins, not the most recently created release: a hotfix of an older line published later
  never takes the downloads or the update back.
- The website and the app read **every page** of the release list, so the newest stable release is found behind
  any number of pre-releases.

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
3. Create the release: tag `vX.Y.Z` (SemVer), title `Git Tree vX.Y.Z`, release notes, and attach the nine files,
   plus every `<installer>.sig` once the updater key exists (below). `tooling/publish-release.sh` in the source
   repository stages, signs, checks (the release gate) and publishes in one go; prefer it to these steps.
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

## Updater signatures — a release gate

The app checks each download against `SHA256SUMS.txt` and the digest GitHub records. Both come from this
repository, so they catch a corrupt, truncated or swapped download, not a compromised release. A minisign signature
made with the owner's offline key covers that:

1. **Once, the owner** generates the key pair (`pnpm tauri signer generate -w ~/.tauri/git-tree-updater.key`,
   `P00-T28` in the source repository), keeps the private key offline and backed up, puts its public key (the
   `.pub` file's base64, as printed) into `UPDATER_PUBLIC_KEY` in the source
   (`crates/ogt-infrastructure/src/updater/mod.rs`), and adds the private key and its password as the
   `TAURI_SIGNING_PRIVATE_KEY` and `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` secrets of the `release` environment here
   (and of the source repository's, if its own workflow publishes). The private key never enters any repository.
2. **Every release:** the workflow's first job refuses a **stable** tag unless the source embeds the key and the
   secret is set (a pre-release may go unsigned, with a warning, until then; once a key is embedded every release
   must be signed). The publish job signs every installer (`<installer>.sig`), verifies each signature with the
   app's own verifier and embedded key, writes `SHA256SUMS.txt`, and checks the folder against the contract above
   before anything is published. A build that embeds the key refuses an installer without a valid signature.

There is no `latest.json`. The website's download buttons never pick a `.sig`.

## If an update is interrupted

- **macOS:** the new app is copied next to the running one, then the two are exchanged in one step
  (`renamex_np(RENAME_SWAP)` on APFS, which `/Applications` is on every supported macOS). At no moment is there no
  app: an interruption (the app killed, the Mac shut down) leaves the old or the new app in place, and the next
  launch removes the leftover hidden `.Git Tree.app.update-<pid>` folder. On a volume that cannot exchange (HFS+,
  some network or external drives) the app falls back to two renames, putting the old app back if the second
  fails; only a power cut between those two renames leaves no app in place, and reinstalling from
  `https://gittree.app/en/download` restores it (settings and repositories are not inside the app).
- **Windows:** the NSIS installer replaces the files itself; an interrupted install is re-run from the downloaded
  installer or the website.
- **Linux `.deb`:** `apt` installs it as one package transaction; `sudo dpkg --configure -a` finishes an
  interrupted one.
- **Linux AppImage:** the new file is written beside the old one and renamed over it in one step.

## Per-platform release procedure

1. Publish the release here (workflow or by hand) with the installers of the contract above, checksums and, once
   the key exists, signatures. Check *After publishing*.
2. Only then raise the account service's release gate for each platform you shipped, one Firestore document per
   platform: `app_configs/macos`, `app_configs/windows` and `app_configs/linux` (the backend repository's
   `docs/SETUP.md`, "Releasing a version"). `app_configs/default` is the development fallback that Linux reads only
   while `app_configs/linux` does not exist; keep it equal to `linux` until then. Never point a gate at a version
   whose installer is not published for that platform.
