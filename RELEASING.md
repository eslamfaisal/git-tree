# Publishing a release

Releases are built, signed and uploaded **by hand** by the maintainer. This page is the checklist that keeps the
website's download buttons working.

## How the website finds the installer

The download buttons on [gittree.app](https://gittree.app) (and in this README) link to
`https://gittree.app/api/download/macos` and `…/windows`. Each click asks GitHub for this repository's **latest
release** and redirects to the matching asset:

| Platform | Asset picked (first match) |
|---|---|
| macOS | a `.dmg` whose name contains `universal`, else any `.dmg` |
| Windows | a `…-setup.exe`, else any `.exe`, else a `.msi` |

- **Drafts and pre-releases are never served.** Only the release GitHub marks **Latest** counts.
- A new release reaches the buttons within about **5 minutes** (the website reuses GitHub's answer that long).
- With no release, or no matching asset, the buttons open the Releases page instead of failing.

## Checklist

1. Build and sign locally: the macOS universal `.dmg` (Developer ID signed, notarized and stapled) and the Windows
   `…_x64-setup.exe`. Keep Tauri's default names, e.g. `Git.Tree_1.2.0_universal.dmg` and
   `Git.Tree_1.2.0_x64-setup.exe` (GitHub turns the space in `Git Tree` into a dot).
2. Write the checksums:
   ```bash
   shasum -a 256 Git.Tree_*_universal.dmg Git.Tree_*_x64-setup.exe > SHA256SUMS.txt
   ```
3. Create the release on GitHub: tag `vX.Y.Z` (SemVer; a `-beta.N` suffix makes it a pre-release), title
   `Git Tree vX.Y.Z`, release notes, and attach the `.dmg`, the `.exe` and `SHA256SUMS.txt`.
4. Leave **Set as a pre-release** unticked and **Set as the latest release** ticked for a stable version, then
   **Publish release**.
5. After ~5 minutes, check that <https://gittree.app/api/download/macos> and
   <https://gittree.app/api/download/windows> download the new files.

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

Never attach source code or anything from the private repositories to a release: GitHub's automatic *Source code*
archives contain only this public repository.
