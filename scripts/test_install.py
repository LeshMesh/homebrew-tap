#!/usr/bin/env python3
"""Destructive lifecycle checks, restricted to a disposable GitHub macOS runner."""
import json
import os
from pathlib import Path
import plistlib
import re
import subprocess
import sys

if sys.platform != "darwin" or os.environ.get("GITHUB_ACTIONS") != "true":
    raise SystemExit("Run only on a disposable GitHub macOS runner.")
token = "leshmesh/tap/app-layout"
app = Path("/Applications/AppLayout.app")
settings_dir = Path.home() / "Library/Application Support/AppLayout"
if app.exists() or settings_dir.exists():
    raise SystemExit("Expected a clean runner; refusing to touch existing app or settings.")

def brew(*args):
    subprocess.run(["brew", *args], check=True)

def verify(version):
    with (app / "Contents/Info.plist").open("rb") as stream:
        info = plistlib.load(stream)
    assert info["CFBundleShortVersionString"] == version, info
    assert info["LSMinimumSystemVersion"] == "26.0"
    assert info["CFBundleIdentifier"] == "dev.leshmesh.AppLayout"
    executable = app / "Contents/MacOS/AppLayout"
    arch = subprocess.check_output(["lipo", "-archs", str(executable)], text=True).strip()
    assert arch == "arm64", arch
    subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)
    print(f"Verified installed AppLayout {version}: arm64, macOS 26, signature integrity.", flush=True)

tap = Path(subprocess.check_output(["brew", "--repository", "leshmesh/tap"], text=True).strip())
definition = tap / "Casks/app-layout.rb"
current = definition.read_text()
version = re.search(r'^\s*version "([^"]+)"', current, re.M).group(1)
# The first published release is a real upgrade fixture, not a rebuilt substitute.
baseline = re.sub(r'(^\s*version ")[^"]+', r'\g<1>1.0.0', current, count=1, flags=re.M)
baseline = re.sub(r'(^\s*sha256 ")[^"]+',
                  r'\g<1>578636790f58f053ab5528bdfb82653628fb4a49569244a7389e2f79f143d051',
                  baseline, count=1, flags=re.M)
try:
    definition.write_text(baseline)
    brew("install", "--cask", token)
    verify("1.0.0")

    settings_dir.mkdir(parents=True)
    settings = settings_dir / "settings.json"
    data = json.dumps({
        "schemaVersion": 1, "language": "ru", "isPaused": True,
        "hasCompletedWelcome": True, "hasInitializedLoginItem": True,
        "rules": [{"bundleIdentifier": "com.google.Chrome",
                   "displayName": "Chrome", "inputSourceID": "com.apple.keylayout.Russian"}],
    }).encode()
    settings.write_bytes(data)

    definition.write_text(current)
    brew("upgrade", "--cask", token)
    verify(version)
    assert settings.read_bytes() == data, "Upgrade modified user settings"

    brew("uninstall", "--cask", token)
    assert not app.exists()
    assert settings.read_bytes() == data, "Ordinary uninstall removed user settings"

    brew("install", "--cask", token)
    verify(version)
    assert settings.read_bytes() == data
    brew("uninstall", "--cask", "--zap", token)
    assert not app.exists()
    assert not settings_dir.exists(), "Explicit zap did not clean up settings"
    print("Install, upgrade from 1.0.0, reinstall, uninstall and explicit zap passed.", flush=True)
    print("This test does not launch the quarantined app or claim Gatekeeper approval.", flush=True)
finally:
    definition.write_text(current)
