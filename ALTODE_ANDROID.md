# ALTODE for Android

ALTODE's Android app is built on the official Geode Android launcher. This keeps
Geode's existing Android integration, mod loader, mod format, dependency handling,
and mod catalogue instead of creating a second, incompatible mod system.

## Source layout

- The repository root is the native Geode/ALTODE loader source.
- `android-launcher/` is a pinned Git submodule containing the official Android launcher.
- `tools/prepare_altode_android.py` applies the ALTODE app identity to a local
  submodule checkout. The upstream launcher source itself is not rewritten in this repository.

The Android launcher currently pins the stable Geode runtime version in its Gradle
build. That is intentional for compatibility with the published Android runtime and
existing Geode mods. ALTODE's root `VERSION` (currently an alpha native source version)
is not automatically substituted for the published Android runtime.

## Clone and prepare

Clone with the launcher submodule:

```sh
git clone --recurse-submodules https://github.com/djdhsvsbdb-design/ALTODE.git
cd ALTODE
python3 tools/prepare_altode_android.py
```

If the repository was cloned without submodules:

```sh
git submodule update --init --recursive
python3 tools/prepare_altode_android.py
```

## Build

On a machine with the Android SDK, Android NDK, and a compatible JDK installed:

```sh
cd android-launcher
./gradlew assembleStandardRelease
```

On Windows use `gradlew.bat assembleStandardRelease`.

The APK is produced under the launcher's `app/build/outputs/apk/` directory.
The build has not yet been run in CI for ALTODE, so APK size, installation, and
device compatibility are not claimed as verified. The project target is to keep
the distributable APK below 50 MB; ABI-specific APKs should be measured separately
from any universal APK.

## Compatibility boundary

ALTODE changes the launcher identity while Geode remains the runtime and mod
platform. A mod must still declare compatibility with the installed Geode/runtime
version and Android ABI. This integration does not bundle Geometry Dash or distribute
the game's proprietary files; users must install their own legitimate copy.

## Next implementation work

1. Replace the upstream launcher artwork and Compose screens with ALTODE branding.
2. Keep Geode's install/update, mod index, dependency, log, and safe-mode services intact.
3. Add CI builds for `arm64-v8a` and `armeabi-v7a`, then measure release APK sizes.
4. Only move the Android runtime to ALTODE's native alpha after matching Android
   binaries and resources have been built and tested.
