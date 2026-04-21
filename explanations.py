EXPLANATIONS = {
    "sampleRate": (
        """The default clock rate at which the PipeWire graph processes data measured in Hz (samples per second). The sample rate determines the real time duration of the quantums. For example a quantum of 128 at 44100Hz your audio latency is ~2.9ms, but if you have the same quantum at 48000Hz that gives you ~2.7ms. You may want to adjust your sample rate if you want to preserve similar latency durations.""",
        [
            "https://docs.pipewire.org/page_man_pipewire_conf_5.html",
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "bufferSize": (
        """Represents the active quantum size (not min or max from config) – the number of audio samples processed per processing cycle of the PipeWire graph. Decreasing this to a smaller number causes the driver to process audio more frequently, reducing the latency, with a tradeoff of higher CPU overhead. The driver quantum adopts the lowest quantum requested by any connected follower node (apps/devices such but not limited by, Spotify, microphone, etc.) or falls back to PipeWire default.""",
        [
            "https://docs.pipewire.org/page_man_pipewire_conf_5.html",
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "audioLatency": (
        """(Buffer Size / Sample Rate) * 1000 = audio latency in ms""",
        [],
    ),
    "busyRatio": (
        """The ratio of the processing time until completion of the graph and the quantum size (again for driver node). This ratio is a good indicator of the load of the driver node. Now let's call B(Busy)/Q = busyRatio. Using this, the headroom % is calculated by: (1.0 - busyRatio) * 100 = space for cpu to do work, which is the opposite of busyRatio. In practice, if your busyRatio was 0.3=30%, there is 70% headroom. Now if your busyRatio is 0.01=1%, you have 99% headroom, which indicates far comfort and less of a chance for xruns to occur than the prior example.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "waitRatio": (
        """The ratio of the time taken for processing the graph, and the quantum size (for the driver node). The ratio is a good indicator of the load of the graph.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "xrunCount": (
        """Xruns are indicators of when the graph did not complete a cycle. It can also be contributed from scheduling delays that cause the deadline to be missed. A possible reason xruns might occur is because of stress/load on the system because it needs to process audio in smaller chunks which arrive more frequently. Basically, the lower the latency, the more likely the system will fail to meet its processing deadline – resulting in more xruns, that can possibly leave clicks, pops, and crackles.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
            "https://manual.ardour.org/synchronization/latency-and-latency-compensation/",
        ],
    ),
    "cpuGovernor": (
        """Outputs the type of scaling cpu governor. Scaling governors are power schemes determined by the desired frequency of the CPU. The reason this is implemented is to let the operating system scale CPU frequency up or down in order to save power or improve performance, or do something different. Here are two examples of scaling governors, but there are more (to see, click the link below for documentation and more examples):
→ performance: runs the cpu at the maximum frequency
→ powersave: runs the cpu at the minimum frequency""",
        [
            "https://wiki.archlinux.org/title/CPU_frequency_scaling#Scaling_governors",
            "https://wiki.linuxaudio.org/wiki/system_configuration#do_i_really_need_a_real-time_kernel",
        ],
    ),
    "compositor": (
        """Software that provides applications with an off-screen buffer for each window, then composites these window buffers into an image representing the screen and writes the result into the display memory. For Desktop Environments (DE's) especially on less powerful machines it is recommended to use a lighter DE than Gnome, KDE or Unity. Possible alternatives include LXDE, XFCE or IceWM. Another option is to only use a lightweight Window Manager (WM) like Openbox or Fluxbox.""",
        [
            "https://en.wikipedia.org/wiki/Compositing_manager",
            "https://wiki.linuxaudio.org/wiki/system_configuration#do_i_really_need_a_real-time_kernel",
        ],
    ),
    "kernel": (
        """The core of the operating system that manages CPU scheduling, memory, and hardware interrupts. For real-time audio, the kernel determines how quickly your system can respond to audio events, which directly affects latency and xruns.

Modern kernels perform well for audio without modification, but for the lowest possible latencies, a real-time (PREEMPT_RT) or low-latency (PREEMPT) kernel is recommended. A standard kernel uses voluntary preemption and is the default on most distros — fine for general use. A low-latency kernel is compiled with CONFIG_PREEMPT, making it more willing to interrupt itself to run time-sensitive tasks. A dynamic kernel (PREEMPT_DYNAMIC, available on kernel 5.12+) lets you switch between preemption levels at boot via the preempt= flag, so a single kernel binary can act as standard, low-latency, or near-RT without recompiling.

Generic kernels can also be improved by enabling the threadirqs boot option, which allows IRQ handlers to run as threads that can be prioritized.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#the_kernel",
            "https://wiki.linuxfoundation.org/realtime/documentation/howto/applications/preemptrt_setup",
        ],
    ),
    "threadirqs": (
        """A kernel boot option that causes interrupt request (IRQ) handlers to run as schedulable threads rather than in a fixed, non-preemptible context. Normally, when hardware (like a sound card or USB device) signals the CPU, the kernel drops everything to handle it immediately, which can interfere with time-sensitive audio processing. With threadirqs enabled, these handlers become regular threads that can be assigned priorities, allowing audio-critical IRQs (like your sound card) to take precedence over less important ones. This brings much of the benefit of a real-time kernel to a standard or low-latency kernel, and is required for tools like rtirq to work on non-RT kernels.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#the_kernel",
            "https://www.kernel.org/doc/html/latest/core-api/genericirq.html",
        ],
    ),
    "mitigations": (
        """Kernel-level workarounds created to increase CPU Security, due to vulnerabilities. Those vulnerabilities, found by Spectre and Meltdown, let a malicious program read memory it should have access to (like passwords or encryption keys from other programs), by exploiting the speed and instructions of modern CPUs. As a result, the kernel inserts extra checks and disables some CPU optimization, causing performance loss. There is a way to turn this off, but be careful!""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#disabling_spectre_and_meltdown_mitigations",
            "https://meltdownattack.com/",
            "https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/index.html",
        ],
    ),
    "maxCstate": (
        """A kernel boot parameter that allows you to cap how deeply the CPU is allowed to sleep when it is idle. Modern CPUs save power by going into progressively deeper sleep states (called C-states) when they have nothing to do. For example, C0 is fully active, C1 is in light sleep that wakes up almost instantly, but something like C7, or C8, they power down large portions of the CPU to save more energy.

Deeper states take longer to wake up, sometimes even hundreds of microseconds. When an audio event fires while the CPU is in a deep C-state, the CPU has to "warm-up" before it can respond, which may cause xruns.

An example of implementation would be, processor.max_cstate=N, where N specifies the kernel to only use C-states from C0 to CN. Also, the max C-states is determined by the type of CPU too. Cool fun fact, that when a CPU is constrained from being put into an available idle state, the CPU will execute more or less useless instructions in a loop until it is assigned a new task to run lol. Overall, by setting a max to the C-state the cores can be at, eliminates the latency spikes at the cost of higher power and heat.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#quality_of_service_interface",
            "https://docs.kernel.org/admin-guide/pm/cpuidle.html",
        ],
    ),
    "clockSource": (
        """The hardware counter the Linux kernel reads to track time, for gettimeofday(), timers, timeouts, and latency measurements. The preferred source is the Time Stamp Counter (TSC), a register inside the CPU that's fast to read and high-resolution. If the kernel's watchdog marks TSC unreliable, it falls back to the High Precision Event Timer (HPET), which is slower and lower-resolution but more robust. Further fallbacks include ACPI_PM, PIT, and RTC. Not having TSC as the active clocksource can impact audio latency, since realtime audio threads read the clock constantly and pay the per-read cost on every wakeup.""",
        [
            "https://docs.kernel.org/timers/timekeeping.html",
            "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_for_real_time/8/html/optimizing_rhel_8_for_real_time_for_low_latency_operation/managing-system-clocks-to-satisfy-application-needs_optimizing-rhel8-for-real-time-for-low-latency-operation",
            "https://news.lavx.hu/article/hpet-vs-tsc-how-linux-s-clock-source-choice-can-slash-redis-performance",
        ],
    ),
}
