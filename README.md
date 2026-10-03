# LeshMesh Homebrew tap

[AppLayout](https://github.com/LeshMesh/app-layout) — keyboard input sources per application.

Apple Silicon · macOS 26 or later · MIT.

## Install

```sh
brew install --cask leshmesh/tap/app-layout
```

Homebrew downloads the versioned GitHub release, verifies its SHA256, and installs AppLayout.app in Applications. No Xcode is required to install the prebuilt app.

**Current signing status:** ad-hoc signed, not Developer ID signed or notarized. Installation through Homebrew preserves macOS quarantine and Gatekeeper checks. macOS may prevent the first launch. This tap does not bypass those protections. Source-build instructions are in the [app repository](https://github.com/LeshMesh/app-layout#build-on-your-mac).

If you already installed the app manually, quit it and move only the old AppLayout.app out of Applications first. Keep the settings folder in Application Support so rules survive.

## Update

```sh
brew update
brew upgrade --cask leshmesh/tap/app-layout
```

Quit AppLayout before updating. Rules are stored separately and retained.

## Remove

Turn off Launch at login in AppLayout and quit before removal:

```sh
brew uninstall --cask leshmesh/tap/app-layout
```

Ordinary uninstall keeps rules and preferences. To explicitly remove those too:

```sh
brew uninstall --cask --zap leshmesh/tap/app-layout
```

## Validation

The macOS CI checks Ruby syntax/style and installs the actual GitHub release. It verifies architecture/version/signature integrity, upgrades from 1.0.0, checks that settings survive upgrade/uninstall/reinstall, and checks explicit zap cleanup. Signature integrity is not notarization or Gatekeeper approval. No protection is disabled and the CI does not launch the app.

## Maintaining releases

1. Publish a new AppLayout release after its native CI succeeds.
2. Update version and SHA256 in Casks/app-layout.rb from the published archive. Never replace an archive under an existing version.
3. Run `brew style --cask leshmesh/tap/app-layout` on a Mac and push the update.
4. Require the tap CI lifecycle checks to pass.

This is the author's tap, separate from the official homebrew/cask catalog. The app itself never checks for updates or contacts the network.

## По-русски

Установка: `brew install --cask leshmesh/tap/app-layout`.
Обновление: `brew update`, затем `brew upgrade --cask leshmesh/tap/app-layout`.

Нужны Apple Silicon и macOS 26+. Если приложение установлено вручную, заверши его и убери старый AppLayout.app из «Программ», сохранив папку настроек. Затем установи через brew.

Сборка пока без Developer ID и нотарификации; ограничения macOS при первом запуске сохраняются. Обычное удаление через brew оставляет правила. Для удаления вместе с настройками есть `--zap`. Перед удалением отключи автозапуск в приложении.

[MIT license](LICENSE).
