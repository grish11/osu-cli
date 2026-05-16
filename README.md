<div id="top"></div>
<br />
<div align="center">
  <h1 align="center">osutop</h1>
  <p align="center">
    A Textual-based TUI for inspecting audio, system, and osu!lazer latency settings on Linux.
    <br />
    <br />
    <a href="https://github.com/grish11/osutop/issues">Report Bug</a>
    ·
    <a href="https://github.com/grish11/osutop/issues">Request Feature</a>
  </p>
  <p align="center">
    <b> <i> Rankings, definitions, and recommendations based on osu!lazer optimization experience and community input. Results may vary by system configuration. </i> </b>
  </p>
</div>
<br />
<div align="center">
  <video src="https://github.com/user-attachments/assets/cc35bfb3-84d3-411c-ae12-275f736a21cb" controls autoplay loop muted width="700">
  </video>
</div>

## Distros Tested

| Distro | Status |
|--------|--------|
| Fedora 43 | ✅ |

> If you dont see your distro, that doesnt mean this tool wont work. This just means it has not been tested and verified it is fully functional.
> If you plan to test it if works, open an issue and I'll respond.
> This tool relies on standard Linux filesystem paths (e.g. /sys/, /proc/), so it will not work on NixOS or Windows.



## Requirements
- Python 3.10+
- PipeWire (`pw-top`)
- osu!lazer (optional — the osu! screen reads its config files)

## Install
```bash
git clone https://github.com/grish11/osutop.git
cd osutop
```
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python main.py
```
