# Publishing a release

The installers users download are attached to a release of **this** repository. The maintainer's build
release workflow here does it (below); the manual route at the end is the fallback. Either way, this
page is the checklist that keeps the website's download buttons and the README's links working.

## How users get the installer

| Where | Link | How it resolves |
|---|---|---|
| Website and README buttons | `https://gittree.app/api/download/macos` · `…/windows` | The site asks GitHub for this repository's published releases, takes the **highest stable version**, and redirects to that release's installer file — a direct download, not the release page. It reuses GitHub's answer for a few minutes, so a new release reaches the buttons within about 10. |
| If GitHub's API cannot be asked (rate limit, outage) | the same buttons | They redirect to GitHub's permanent link below instead, so a download still starts. |
| Permanent links, no website needed | `https://github.com/eslamfaisal/git-tree/releases/latest/download/Git-Tree-macOS.dmg` · `…/Git-Tree-Windows-setup.exe` | GitHub redirects `latest/download/<name>` to the file of that name on the **latest release**. The names never change, so these links never break. |

What the website picks (first match):

| Platform | Asset |
|---|---|
| macOS | a `.dmg` whose name contains `universal` (`Git-Tree_X.Y.Z_universal.dmg`), else any `.dmg` (`Git-Tree-macOS.dmg`) |
| Windows | `…_x64-setup.exe` (`Git-Tree_X.Y.Z_x64-setup.exe`), else any `…-setup.exe`, any `.exe`, then a `.msi` |

- **Drafts, pre-releases and tags that are not `vX.Y.Z` are never served.**
- With no release, or no matching asset, the buttons open the Releases page instead of failing.
- Every release must therefore carry the **four installer names** below — the two stable ones are what the
  permanent links need.

## Every release attaches

| File | What |
|---|---|
| `Git-Tree_X.Y.Z_universal.dmg` | the macOS installer (Apple silicon and Intel) |
| `Git-Tree_X.Y.Z_x64-setup.exe` | the Windows installer |
| `Git-Tree-macOS.dmg` | the same `.dmg` under a name that never changes |
| `Git-Tree-Windows-setup.exe` | the same installer under a name that never changes |
| `SHA256SUMS.txt` | SHA-256 of every file above |

Never attach source code or anything from the private repositories: GitHub's automatic *Source code* archives
contain only this public repository.

## Automatic: run the release workflow (free)

**Actions › release › Run workflow**, with the version tag (`v1.0.0`; the source's version must equal it).
The workflow checks out the maintainer's private source repository, builds and signs both installers on
GitHub's macOS and Windows runners, checks their sizes, and once **both** exist creates the release
`vX.Y.Z` here with the files above, `SHA256SUMS.txt` and release notes. It lives in this public
repository on purpose: standard runners are free and unlimited for public repositories, so it costs
nothing on GitHub's free plan. Only people with write access here can start it. A tag with a suffix
(`v1.1.0-beta.1`) is published as a pre-release and never becomes *Latest*.

One-time setup, by the owner (Settings › Environments › New environment `release`, with required reviewers):

| Secret in the `release` environment | What |
|---|---|
| `SOURCE_REPO_TOKEN` | required: a fine-grained personal access token limited to the private source repository, permission *Contents: Read-only* |
| `APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`, `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH` | optional: Developer ID signing and notarization. Without them the `.dmg` is unsigned and the release notes say so |

Build logs of a public repository are public: a failing build can print file names and compiler
messages of the private source. Keep the environment's required reviewer on, and never pass the source
token to anything but the checkout steps.

## By hand (fallback)

1. Build and sign locally, or take `installers-*` from the workflow run's artifacts.
2. Name the files as in the table above. Tauri writes `Git Tree_X.Y.Z_universal.dmg` and
   `Git Tree_X.Y.Z_x64-setup.exe` (with a space); from the folder holding them:
   ```bash
   V=1.0.0
   cp "Git Tree_${V}_universal.dmg" "Git-Tree_${V}_universal.dmg"
   cp "Git Tree_${V}_universal.dmg" Git-Tree-macOS.dmg
   cp "Git Tree_${V}_x64-setup.exe" "Git-Tree_${V}_x64-setup.exe"
   cp "Git Tree_${V}_x64-setup.exe" Git-Tree-Windows-setup.exe
   shasum -a 256 Git-Tree_"${V}"_universal.dmg Git-Tree_"${V}"_x64-setup.exe Git-Tree-macOS.dmg Git-Tree-Windows-setup.exe > SHA256SUMS.txt
   ```
3. Create the release: tag `vX.Y.Z` (SemVer), title `Git Tree vX.Y.Z`, release notes, and attach the five files.
4. Leave **Set as a pre-release** unticked and **Set as the latest release** ticked for a stable version, then
   **Publish release**.

## After publishing

1. Open `https://github.com/eslamfaisal/git-tree/releases/latest/download/Git-Tree-macOS.dmg` and the Windows
   link: each must start a download.
2. Within about 10 minutes, `https://gittree.app/api/download/macos` and `…/windows` must download the same files.

## In-app updates (once the updater is enabled)

The app checks for updates at fixed addresses in **this** repository, frozen from the first
updater-enabled build:

| Channel | Manifest the app reads |
|---|---|
| Stable | `https://github.com/eslamfaisal/git-tree/releases/latest/download/latest.json` |
| Beta | `https://github.com/eslamfaisal/git-tree/releases/download/beta/latest.json` |

So every updater-enabled release also attaches:

- the updater archives and their signatures that `tauri build` writes next to the installers
  (`Git.Tree_universal.app.tar.gz` + `.sig` for macOS, the NSIS updater bundle + `.sig` for Windows);
- a **`latest.json`** made with `tooling/render-update-manifest.py` (in the source repository) from
  those `.sig` files and **this release's own asset URLs**. The script refuses URLs of any other
  repository; never upload a `latest.json` that names the private repository.

A stable release puts `latest.json` on the release itself. A beta (`-beta.N`) updates the assets of
the moving pre-release tagged `beta` instead. Neither the `.tar.gz` archives nor `latest.json` are
ever picked by the website's download buttons.
