from textual import work
from textual.app import ComposeResult
from textual.widgets import Header, Footer, DataTable
from textual.screen import Screen
import os
import shutil
import subprocess

from screens.variableDetail import VariableDetailScreen


# Functions -------------------------------------------
def getCpuGovernor() -> str:
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "—"


def getCompositor() -> str:
    compositor = (
        os.environ.get("XDG_CURRENT_DESKTOP")
        or os.environ.get("DESKTOP_SESSION")
        or "unknown"
    )
    if os.environ.get("WAYLAND_DISPLAY"):
        displayServer = "Wayland"
    elif os.environ.get("DISPLAY"):
        displayServer = "Xorg"
    else:
        displayServer = "unknown"
    return f"{compositor} ({displayServer})"


def getKernelInfo() -> str:
    if not shutil.which("uname"):
        return "—"
    try:
        kernelVersion = subprocess.run(
            ["uname", "-r"], capture_output=True, text=True, timeout=3
        ).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"

    kernelType = "standard"
    if "rt" in kernelVersion:
        kernelType = "realtime"
    elif "cachyos" in kernelVersion:
        kernelType = "cachyos"
    return f"{kernelType} ({kernelVersion})"


def getKernelParams() -> dict[str, str]:
    """Returns threadirqs, preempt, mitigations, maxCstate, clocksource."""
    result = {
        "threadirqs":   "—",
        "preempt":      "—",
        "mitigations":  "—",
        "maxCstate":    "—",
        "clocksource":  "—",
    }
    try:
        with open("/proc/cmdline", "r") as f:
            bootParams = f.read().strip()
    except FileNotFoundError:
        return result

    params = {}
    for item in bootParams.split():
        if "=" in item:
            key, value = item.split("=", 1)
            params[key] = value
        else:
            params[item] = True

    result["threadirqs"] = "enabled" if params.get("threadirqs") else "not set"

    preempt = params.get("preempt")
    result["preempt"] = preempt if preempt else "not set"

    mitigations = params.get("mitigations")
    if mitigations == "off":
        result["mitigations"] = "off"
    elif mitigations is None:
        result["mitigations"] = "default (on)"
    else:
        result["mitigations"] = str(mitigations)

    maxCstate = params.get("processor.max_cstate")
    result["maxCstate"] = maxCstate if maxCstate else "not set"

    try:
        with open(
            "/sys/devices/system/clocksource/clocksource0/current_clocksource", "r"
        ) as f:
            result["clocksource"] = f.read().strip()
    except FileNotFoundError:
        pass

    return result


def getRtkitStatus() -> str:
    if not shutil.which("systemctl"):
        return "systemctl not found"
    try:
        active = subprocess.run(
            ["systemctl", "is-active", "rtkit-daemon"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"
    if active != "active":
        return "not running"

    if not shutil.which("pgrep"):
        return "pgrep not found"
    try:
        pid = subprocess.run(
            ["pgrep", "-x", "pipewire"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"
    if not pid:
        return "PipeWire not running"

    try:
        schedulingInfo = subprocess.run(
            ["ps", "-T", "-p", pid, "-o", "cls,rtprio"],
            capture_output=True, text=True, timeout=3,
        ).stdout
    except subprocess.TimeoutExpired:
        return "—"

    for line in schedulingInfo.splitlines():
        if "FF" in line or "RR" in line:
            return "active — PipeWire has realtime priority"

    return "running but PipeWire not realtime"


def getUsbAutosuspend() -> str:
    try:
        with open("/sys/module/usbcore/parameters/autosuspend", "r") as f:
            timeout = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return "—"
    if timeout == -1:
        return "disabled"
    if timeout == 0:
        return "immediate"
    return f"{timeout}s"


def getSystemInfoStatic() -> dict[str, str]:
    """Info that doesn't change at runtime — fetched once."""
    kernelParams = getKernelParams()
    return {
        "cpuGovernor":  getCpuGovernor(),
        "compositor":   getCompositor(),
        "kernel":       getKernelInfo(),
        "threadirqs":   kernelParams["threadirqs"],
        "preempt":      kernelParams["preempt"],
        "mitigations":  kernelParams["mitigations"],
        "maxCstate":    kernelParams["maxCstate"],
        "clocksource":  kernelParams["clocksource"],
    }


def getSystemInfoActive() -> dict[str, str]:
    """Info that can change at runtime — refreshed periodically."""
    return {
        "rtkit":          getRtkitStatus(),
        "usbAutosuspend": getUsbAutosuspend(),
    }


# Screens ---------------------------------------------
STATIC_ROWS = [
    ("cpuGovernor",  "CPU governor"),
    ("compositor",   "Compositor"),
    ("kernel",       "Kernel"),
    ("threadirqs",   "threadirqs"),
    ("preempt",      "preempt"),
    ("mitigations",  "mitigations"),
    ("maxCstate",    "processor.max_cstate"),
    ("clocksource",  "active clocksource"),
]

ACTIVE_ROWS = [
    ("rtkit",          "rtkit"),
    ("usbAutosuspend", "USB autosuspend"),
]

ALL_ROWS = STATIC_ROWS + ACTIVE_ROWS

class SystemLatencyScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_column("variable", key="variable")
        table.add_column("value", key="value")

        # seed static rows once
        staticData = getSystemInfoStatic()
        for key, label in STATIC_ROWS:
            table.add_row(label, staticData[key], key=key)

        # seed active rows with initial values
        activeData = getSystemInfoActive()
        for key, label in ACTIVE_ROWS:
            table.add_row(label, activeData[key], key=key)

        # refresh only the active rows
        self.set_interval(5.0, self.refreshActiveValues)

    @work(exclusive=True, thread=True)
    def refreshActiveValues(self) -> None:
        data = getSystemInfoActive()
        table = self.query_one(DataTable)
        for key, _ in ACTIVE_ROWS:
            self.app.call_from_thread(
                table.update_cell, key, "value", data[key]
            )

    def on_data_table_row_selected(
        self, event: DataTable.RowSelected
    ) -> None:
        key = event.row_key.value
        table = self.query_one(DataTable)
        currentValue = table.get_cell(event.row_key, "value")
        displayLabel = dict(ALL_ROWS)[key]
        self.app.push_screen(
            VariableDetailScreen(key, displayLabel, currentValue)
        )
