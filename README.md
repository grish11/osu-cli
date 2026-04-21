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
</div>

<details open>
<summary><b>Preview</b></summary>
<br />
<div align="center">
  <img src="https://github.com/grish11/osutop/blob/main/assets/osuTop.png" alt="osutop preview" width="800">
</div>
</details>

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
