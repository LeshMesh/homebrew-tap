cask "app-layout" do
  version "1.1.0"
  sha256 "e7bf067d04bb5a298d5f86220af35edcf0a5636697ee77d8153eae77d401f1b6"

  url "https://github.com/LeshMesh/app-layout/releases/download/v#{version}/AppLayout-#{version}-arm64.zip"
  name "AppLayout"
  desc "Switch keyboard input sources when activating applications"
  homepage "https://github.com/LeshMesh/app-layout"

  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "AppLayout.app"

  uninstall quit: "dev.leshmesh.AppLayout"

  zap trash: "~/Library/Application Support/AppLayout"

  caveats <<~EOS
    This release is ad-hoc signed, not Developer ID signed or notarized.
    Homebrew preserves macOS Gatekeeper checks when the app is opened.

    Before uninstalling, turn off Launch at login in AppLayout and quit it.
    Regular uninstall keeps your rules; --zap also deletes your settings.
  EOS
end
