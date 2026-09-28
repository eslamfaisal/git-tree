# Publishing a release

The installers users download are attached to a release of **this** repository. The maintainer's build
pipeline does it on a version tag (below); the manual route at the end is the fallback. Either way, this
page is the checklist that keeps the website's download buttons and the README's links working.

## How users get the installer

| Where | Link | How it resolves |
|---|---|---|
| Website and README buttons | `https://gittree.app/api/download/macos` · `…/windows` | The site asks GitHub for this repository's published releases, takes the **highest stable version**, and redirects to that release's installer file — a direct download, not the release page. It reuses GitHub's answer for about 5 minutes. |
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

## Automatic: push the tag

In the source repository, `git tag vX.Y.Z && git push origin vX.Y.Z` (the version in the code must match; the
run refuses otherwise). Its release workflow builds and signs both installers, checks their sizes, and once
**both** exist creates this repository's release `vX.Y.Z` with the files above, `SHA256SUMS.txt` and release
notes. It needs the owner-side setup listed in that repository's `docs/05-release/OWNER_ACTIONS.md`
(GitHub Actions minutes, the `release` environment's signing secrets, and a token allowed to write to this
repository). A tag with a suffix (`v0.1.0-beta.1`) is published as a pre-release and never becomes *Latest*.

## By hand (fallback)

1. Build and sign locally, or take `installers-*` from the workflow run's artifacts.
2. Name the files as in the table above. Then:
   ```bash
   shasum -a 256 Git-Tree_*_universal.dmg Git-Tree_*_x64-setup.exe Git-Tree-macOS.dmg Git-Tree-Windows-setup.exe > SHA256SUMS.txt
   ```
3. Create the release: tag `vX.Y.Z` (SemVer), title `Git Tree vX.Y.Z`, release notes, and attach the five files.
4. Leave **Set as a pre-release** unticked and **Set as the latest release** ticked for a stable version, then
   **Publish release**.

## After publishing

1. Open `https://github.com/eslamfaisal/git-tree/releases/latest/download/Git-Tree-macOS.dmg` and the Windows
   link: each must start a download.
2. After ~5 minutes, `https://gittree.app/api/download/macos` and `…/windows` must download the same files.
3. Raise `latestVersion` for each platform in the account service's `app_configs` documents, **after** the
   downloads work (a forced update pointing at a missing installer locks users out).

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
