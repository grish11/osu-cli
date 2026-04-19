# osutop
A Textual-based TUI for inspecting audio, system, and osu!lazer latency settings on Linux.

## Requirements
- Python 3.10+
- PipeWire (`pw-top`)
- osu!lazer (optional — osu! screen reads its config files)

## Install
```
git clone https://github.com/grish11/osutop.git
cd osutop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```python main.py```
