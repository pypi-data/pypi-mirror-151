# DevDeck - macOS
![CI](https://github.com/marcus-crane/devdeck-macos/workflows/CI/badge.svg?branch=main)

> A drop-in replacement for operating system controls and decks implemented in [DevDeck](https://github.com/jamesridgway/devdeck).

DevDeck is a really neat tool but some of the default controls such as the volume controls assume you are running on a machine with [PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) ie; Linux.

This package is intended as a replacement for those controls but with support for macOS instead.

More specifically, it uses `osascript` to issue system commands under the hood.

By drop-in, you should only have to change the package name in the original DevDeck controls to achieve the same effect for macOS eg;

```diff
decks:
  - serial_number: "ABC123456789"
    name: 'devdeck.decks.single_page_deck_controller.SinglePageDeckController'
    settings:
      controls:
-       - name: 'devdeck.controls.volume_mute_control.VolumeMuteControl'
+       - name: 'devdeck_macos.controls.volume_mute_control.VolumeMuteControl'
```

## Installing
Simply install *DevDeck - macOS* into the same python environment that you have installed DevDeck.

```shell
$ pip install devdeck-macos
```

You can then update your DevDeck configuration to use decks and controls from this package.

## Configuration

At the moment, only `VolumeMuteControl` is implemented but I plan to port over more controls shortly.

Example configuration:

```yaml
decks:
  - serial_number: "ABC123456789"
    name: 'devdeck.decks.single_page_deck_controller.SinglePageDeckController'
    settings:
      controls:
        - name: 'devdeck_macos.controls.volume_mute_control.VolumeMuteControl'
          key: 0
```

**NOTE**: Unlike the original package, you do not have to specify the specific microphone as it will default to the currently selected default in System Preferences.

If there is a need for it, I can see whether osascript supports muting a specific input device.