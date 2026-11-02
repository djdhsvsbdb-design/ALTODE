#!/usr/bin/env python3
"""Apply ALTODE branding to a checked-out Geode Android launcher submodule.

This intentionally changes only the Android application ID and visible product
names. The Geode runtime version, package namespace, mod services, and native
loader integration remain upstream-compatible.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "android-launcher"

def replace_once(path: Path, old: str, new: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Required launcher file is missing: {path}")
    text = path.read_text(encoding="utf-8")
    if new in text and old not in text:
        return  # already prepared
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected exactly one occurrence of {old!r} in {path}, found {count}. "
            "The upstream launcher may have changed; review the file before patching."
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

def main() -> int:
    if not (LAUNCHER / ".git").exists():
        print(
            "Android launcher submodule is missing. Run: "
            "git submodule update --init --recursive",
            file=sys.stderr,
        )
        return 2

    gradle = LAUNCHER / "app" / "build.gradle.kts"
    strings = LAUNCHER / "app" / "src" / "main" / "res" / "values" / "strings.xml"

    replace_once(gradle, 'applicationId = "com.geode.launcher"',
                 'applicationId = "com.altode.launcher"')
    replace_once(strings,
                 '<string name="app_name" translatable="false">Geode</string>',
                 '<string name="app_name" translatable="false">ALTODE</string>')
    replace_once(strings,
                 '<string name="launcher_title">Geode</string>',
                 '<string name="launcher_title">ALTODE</string>')
    replace_once(strings,
                 '<string name="launcher_update_name">Geode Launcher v%1$s</string>',
                 '<string name="launcher_update_name">ALTODE Launcher v%1$s</string>')

    print("ALTODE Android branding applied.")
    print("Geode runtime version and mod-loader implementation were left unchanged.")
    print("Build with: cd android-launcher && ./gradlew assembleStandardRelease")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
