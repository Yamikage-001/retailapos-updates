# RetailaPOS updates

This public repository hosts release installers and the update manifest used by
the RetailaPOS Android, Windows, and macOS apps. It does not contain application
source or signing keys.

`latest.json` is the current stable update. The app checks it on opening the POS
and from **Settings → Check for updates**. The app downloads the platform asset,
verifies its SHA-256 hash, and opens the system installer.

## Publishing

Build and sign each artifact first. Keep the Android keystore backed up; every
later APK must use the same key. Windows installers should be Authenticode signed,
and macOS disk images must contain a Developer ID signed, notarized app.

Use the `scripts/publish.py` helper from a machine with `gh` logged in as an
account allowed to publish here. It creates a GitHub release, computes hashes,
and updates `latest.json`. It accepts any subset of platforms; omitted platforms
are not offered that release.

```sh
python3 scripts/publish.py 1.0.1 2 \
  --android /path/to/RetailaPOS.apk \
  --windows /path/to/RetailaPOS_Setup.exe \
  --macos /path/to/RetailaPOS.dmg \
  --notes 'Stock and app update fixes'
```

The first app with this updater is version `1.0.1+2`. The previous Android APK
was signed with an Android debug key. It cannot be upgraded in place with the new
production key; devices on `1.0.0+1` require a one-time uninstall and reinstall
after the new release is published. Back up any unsynced offline sales first.
