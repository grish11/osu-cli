from textual import work
from textual.app import ComposeResult
from textual.widgets import Header, Footer, DataTable
from textual.screen import Screen
from screens.variableDetail import VariableDetailScreen

import os
import shutil
import subprocess


_kernelVersionCache: str | None = None
_kernelBuildInfoCache: str | None = None


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


def getKernelVersion() -> str:
    global _kernelVersionCache

    if _kernelVersionCache is not None:
        return _kernelVersionCache

    if not shutil.which("uname"):
        _kernelVersionCache = ""
        return ""
    try:
        _kernelVersionCache = subprocess.run(["uname", "-r"], capture_output=True, text=True, timeout=3).stdout.strip()
    except subprocess.TimeoutExpired:
        _kernelVersionCache = ""
    return _kernelVersionCache


def getKernelBuildInfo() -> str:
    global _kernelBuildInfoCache

    if _kernelBuildInfoCache is not None:
        return _kernelBuildInfoCache

    if not shutil.which("uname"):
        _kernelBuildInfoCache = ""
        return ""
    try:
        _kernelBuildInfoCache = subprocess.run(["uname", "-v"], capture_output=True, text=True, timeout=3).stdout.strip()
    except subprocess.TimeoutExpired:
        _kernelBuildInfoCache = ""
    return _kernelBuildInfoCache


def isRtKernel() -> bool:
    return "PREEMPT_RT" in getKernelBuildInfo()


def getKernelInfo() -> str:
    kernelVersion = getKernelVersion()
    if not kernelVersion:
        return "—"

    buildInfo = getKernelBuildInfo()
    if "PREEMPT_RT" in buildInfo:
        kernelType = "realtime"
    elif "PREEMPT_DYNAMIC" in buildInfo:
        kernelType = "dynamic"
    elif "PREEMPT " in buildInfo:
        kernelType = "low-latency"
    elif "cachyos" in kernelVersion.lower():
        kernelType = "cachyos"
    else:
        kernelType = "standard"
    return f"{kernelType} ({kernelVersion})"


def getKernelParams() -> dict[str, str]:
    """Returns threadirqs, mitigations, maxCstate, clockSource."""
    result = {
        "threadirqs":   "—",
        "mitigations":  "—",
        "maxCstate":    "—",
        "clockSource":  "—",
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

    if isRtKernel():
        result["threadirqs"] = "built-in (RT kernel)"
    else:
        result["threadirqs"] = "enabled" if params.get("threadirqs") else "not set"

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
            "/sys/devices/system/clocksource/clocksource0/current_clocksource", "r") as f:
            result["clockSource"] = f.read().strip()
    except FileNotFoundError:
        pass

    return result


def getRtkitStatus() -> str:
    if not shutil.which("systemctl"):
        return "systemctl not found"
    try:
        active = subprocess.run(["systemctl", "is-active", "rtkit-daemon"], capture_output=True, text=True, timeout=3).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"
    if active != "active":
        return "not running"

    if not shutil.which("pgrep"):
        return "pgrep not found"
    try:
        pid = subprocess.run(["pgrep", "-x", "pipewire"], capture_output=True, text=True, timeout=3).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"
    if not pid:
        return "PipeWire not running"

    try:
        schedulingInfo = subprocess.run(["ps", "-T", "-p", pid, "-o", "cls,rtprio"], capture_output=True, text=True, timeout=3).stdout
    except subprocess.TimeoutExpired:
        return "—"

    for line in schedulingInfo.splitlines():
        if "FF" in line or "RR" in line:
            return "active, PipeWire has realtime priority"

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


def getSoundCardIrqPriority() -> str:
    if not shutil.which("ps"):
        return "—"
    try:
        psOutput = subprocess.run(["ps", "-eo", "comm,cls,rtprio"], capture_output=True, text=True, timeout=3).stdout
    except subprocess.TimeoutExpired:
        return "—"

    # Look for a sound-related IRQ thread
    for line in psOutput.splitlines():
        if "irq/" in line and "snd" in line.lower():
            parts = line.split()
            if len(parts) >= 3:
                rtprio = parts[-1]
                if rtprio in ("-", "0"):
                    return "default (not prioritized)"
                return f"{rtprio} (prioritized)"

    # No sound IRQ thread found — likely means IRQs aren't threaded.
    return "n/a (IRQ not threaded)"


def getRtirqStatus() -> str:
    rtirqInstalled = (
        os.path.isfile("/etc/rtirq.conf")
        or os.path.isfile("/etc/default/rtirq")
    )
    if not rtirqInstalled:
        return "not installed"

    if not shutil.which("systemctl"):
        return "installed (can't check service)"
    try:
        active = subprocess.run(["systemctl", "is-active", "rtirq"], capture_output=True, text=True, timeout=3).stdout.strip()
    except subprocess.TimeoutExpired:
        return "—"

    if active == "active":
        return "active"
    return "installed but inactive"


def getUserLimits() -> dict[str, str]:
    result = {"rtprio": "—", "memlock": "—"}
    try:
        with open("/proc/self/limits", "r") as f:
            limitsText = f.read()
    except FileNotFoundError:
        return result

    for line in limitsText.splitlines():
        if line.startswith("Max realtime priority"):
            softLimit = line[26:47].strip()
            result["rtprio"] = softLimit if softLimit else "—"
        elif line.startswith("Max locked memory"):
            softLimit = line[26:47].strip()
            if softLimit == "unlimited":
                result["memlock"] = "unlimited"
            else:
                try:
                    mb = int(softLimit) // (1024 * 1024)
                    result["memlock"] = f"{mb} MB"
                except ValueError:
                    result["memlock"] = softLimit if softLimit else "—"
    return result


# ---------------------------------------------------------------------------------------------------
def getSystemInfo() -> dict[str, str]:
    """Reads every system-latency-relevant variable in one shot."""
    kernelParams = getKernelParams()
    limits = getUserLimits()
    return {
        "kernel":         getKernelInfo(),
        "cpuGovernor":    getCpuGovernor(),
        "rtkit":          getRtkitStatus(),
        "rtprio":         limits["rtprio"],
        "memlock":        limits["memlock"],
        "maxCstate":      kernelParams["maxCstate"],
        "threadirqs":     kernelParams["threadirqs"],
        "mitigations":    kernelParams["mitigations"],
        "clockSource":    kernelParams["clockSource"],
        "usbAutosuspend": getUsbAutosuspend(),
        "soundIrqPrio":   getSoundCardIrqPriority(),
        "rtirq":          getRtirqStatus(),
        "compositor":     getCompositor(),
    }


# Screens ---------------------------------------------
ROWS = [
    ("kernel",         "Kernel"),
    ("cpuGovernor",    "CPU governor"),
    ("rtkit",          "Rtkit"),
    ("rtprio",         "Rtprio Limit"),
    ("maxCstate",      "processor.max_cstate"),
    ("memlock",        "Memlock Limit"),
    ("threadirqs",     "Threadirqs"),
    ("mitigations",    "Mitigations"),
    ("clockSource",    "Active Clocksource"),
    ("usbAutosuspend", "USB autosuspend"),
    ("soundIrqPrio",   "Sound Card IRQ priority"),
    ("rtirq",          "Rtirq"),
    ("compositor",     "Compositor"),
]


class SystemLatencyScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_column("variable", key="variable")
        table.add_column("value  ** Ordered by impact on osu!lazer latency (high to low). Press 'r' to refresh.", key="value")

        data = getSystemInfo()
        for key, label in ROWS:
            table.add_row(label, data[key], key=key)

    @work(exclusive=True, thread=True)
    def action_refresh(self) -> None:
        data = getSystemInfo()
        table = self.query_one(DataTable)
        for key, _ in ROWS:
            self.app.call_from_thread(table.update_cell, key, "value", data[key])

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = event.row_key.value
        table = self.query_one(DataTable)
        currentValue = table.get_cell(event.row_key, "value")
        displayLabel = dict(ROWS)[key]
        self.app.push_screen(VariableDetailScreen(key, displayLabel, currentValue, source="system"))
