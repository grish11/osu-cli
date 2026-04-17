# osu-cli

A CLI latency checker for osu!lazer on Linux. ** STATIC
Reads your system and osu! settings to surface latency issues in one place.

## Dependencies

- osu!lazer (not stable), and requires you to run in background for input
on audio latency, and rtkit
- Python 3
- pipewire + pw-top
- Linux (Fedora first, Ubuntu/Debian and Arch/NixOS coming soon)

## Install

```bash
git clone https://github.com/grish11/osu-cli
cd osu-cli
bash install.sh
```

## Usage

```bash
latency-check
```
