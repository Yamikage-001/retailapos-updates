# RetailaPOS updates

This public repository hosts release installers and the update manifest used by
the RetailaPOS Android, Windows, and macOS apps. It does not contain application
source or signing keys.

`latest.json` is the current stable update. The app checks it on opening the POS
and from **Settings → Check for updates**. The app downloads the platform asset,
verifies its SHA-256 hash, and opens the system installer.

## Publishing

Releases are built here by the **Build and publish RetailaPOS update** workflow
(Actions → Run workflow). It checks out the app code from
`Altris-Product-Systems/Apex-Mobile` (nothing is copied into this repository),
builds and signs the installers, creates the GitHub release and advances
`latest.json`.

1. In Apex-Mobile, bump `version:` in `pubspec.yaml` (e.g. `1.0.4+4`) and push.
2. Here, run the workflow with that `version`, `build`, release notes and
   `platforms` (`android`; add `windows,macos` once their certificates are set).

Secrets on this repository: `SOURCE_REPO_TOKEN` (read access to Apex-Mobile),
`ANDROID_KEYSTORE_BASE64`, `ANDROID_KEY_PASSWORD`; for Windows
`WINDOWS_SIGN_CERT_BASE64`, `WINDOWS_SIGN_CERT_PASSWORD`; for macOS
`APPLE_CERTIFICATE_BASE64`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_DEVELOPER_ID`,
`APPLE_ID`, `APPLE_APP_PASSWORD`, `APPLE_TEAM_ID`.

`scripts/publish.py` can still publish already-built installers by hand.

The first app with this updater is version `1.0.1+2`. The previous Android APK
was signed with an Android debug key. It cannot be upgraded in place with the new
production key; devices on `1.0.0+1` require a one-time uninstall and reinstall
after the new release is published. Back up any unsynced offline sales first.
