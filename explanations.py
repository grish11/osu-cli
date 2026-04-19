EXPLANATIONS = {
    "bufferSize": (
        """represents the active quantum size (not min or max from config) – the number of audio samples processed per processing cycle of the PipeWire graph. Decreasing this to a smaller number causes the driver to process audio more frequently, reducing the latency, with a tradeoff of higher CPU overhead. The driver quantum adopts the lowest quantum requested by any connected follower node (apps/devices such but not limited by, Spotify, microphone, etc.) or falls back to PipeWire default.""",
        [
            "https://docs.pipewire.org/page_man_pipewire_conf_5.html",
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "sampleRate": (
        """the default clock rate at which the PipeWire graph processes data measured in Hz (samples per second). The sample rate determines the real time duration of the quantums. For example a quantum of 128 at 44100Hz your audio latency is ~2.9ms, but if you have the same quantum at 48000Hz that gives you ~2.7ms. You may want to adjust your sample rate if you want to preserve similar latency durations.""",
        [
            "https://docs.pipewire.org/page_man_pipewire_conf_5.html",
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "waitRatio": (
        """the ratio of the time taken for processing the graph, and the quantum size (for the driver node). The ratio is a good indicator of the load of the graph.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "busyRatio": (
        """B(Busy)/Q = busyRatio. This is a ratio of the processing time until completion of the graph and the quantum size (again for driver node). This ratio is a good indicator of the load of the driver node. 
In addition, the CPU Headroom is represented as: (1.0 - busyRatio) * 100 = space for cpu to do work, which is the opposite of busyRatio. For example if busyRatio was 0.3=30%, there is 70% headroom which indicates comfort and less of a chance for xruns to occur.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
        ],
    ),
    "xrunCount": (
        """Xruns are indicators of when the graph did not complete a cycle. It can also be contributed from scheduling delays that cause the deadline to be missed. A possible reason xrun's might occur is because of stress/load on the system because it needs to process audio in smaller chunks which arrive more frequently. Basically, the lower the latency, the more likely the system will fail to meet its processing deadline – resulting in more Xruns, that can possibly leave clicks, pops, and crackles.""",
        [
            "https://docs.pipewire.org/page_man_pw-top_1.html",
            "https://manual.ardour.org/synchronization/latency-and-latency-compensation/",
        ],
    ),
    "audioLatency": (
        """(bufferSize / sampleRate) * 1000 = audio latency in ms""",
        [],
    ),
    "cpuHeadroomPercent": (
        """(1.0 - busyRatio) * 100 = space for cpu to do work, which is the opposite of busyRatio. For example if busyRatio was 0.3=30%, there is 70% headroom which indicates comfort and less of a chance for xruns to occur.""",
        [],
    ),
    "cpuGovernor": (
        """outputs the type of scaling cpu governor. Scaling governors are power schemes determined by the desired frequency of the CPU. The reason this is implemented is to let the operating system scale CPU frequency up or down in order to save power or improve performance, or do something different. Here are two examples of scaling governors, but there are more (to see, click the link below for documentation and more examples):
→ performance: runs the cpu at the maximum frequency
→ powersave: runs the cpu at the minimum frequency""",
        [
            "https://wiki.archlinux.org/title/CPU_frequency_scaling#Scaling_governors",
            "https://wiki.linuxaudio.org/wiki/system_configuration#do_i_really_need_a_real-time_kernel",
        ],
    ),
    "compositor": (
        """software that provides applications with an off-screen buffer for each window, then composites these window buffers into an image representing the screen and writes the result into the display memory. For Desktop Environments (DE's) especially on less powerful machines it is recommended to use a lighter DE than Gnome, KDE or Unity. Possible alternatives include LXDE, XFCE or IceWM. Another option is to only use a lightweight Window Manager (WM) like Openbox or Fluxbox.""",
        [
            "https://en.wikipedia.org/wiki/Compositing_manager",
            "https://wiki.linuxaudio.org/wiki/system_configuration#do_i_really_need_a_real-time_kernel",
        ],
    ),
    "kernel": (
        """the core of the operating system that manages CPU scheduling, memory, and hardware interrupts. For real-time audio, the kernel determines how quickly your system can respond to audio events, which directly affects latency and xruns.

Modern kernels perform well for audio without modification, but for the lowest possible latencies, a real-time (PREEMPT_RT) or low-latency (PREEMPT) kernel is recommended. A standard kernel uses voluntary preemption and is the default on most distros — fine for general use. A low-latency kernel is compiled with CONFIG_PREEMPT, making it more willing to interrupt itself to run time-sensitive tasks. A dynamic kernel (PREEMPT_DYNAMIC, available on kernel 5.12+) lets you switch between preemption levels at boot via the preempt= flag, so a single kernel binary can act as standard, low-latency, or near-RT without recompiling.

Generic kernels can also be improved by enabling the threadirqs boot option, which allows IRQ handlers to run as threads that can be prioritized.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#the_kernel",
            "https://wiki.linuxfoundation.org/realtime/documentation/howto/applications/preemptrt_setup",
        ],
    ),
    "threadirqs": (
        """a kernel boot option that causes interrupt request (IRQ) handlers to run as schedulable threads rather than in a fixed, non-preemptible context. Normally, when hardware (like a sound card or USB device) signals the CPU, the kernel drops everything to handle it immediately, which can interfere with time-sensitive audio processing. With threadirqs enabled, these handlers become regular threads that can be assigned priorities, allowing audio-critical IRQs (like your sound card) to take precedence over less important ones. This brings much of the benefit of a real-time kernel to a standard or low-latency kernel, and is required for tools like rtirq to work on non-RT kernels.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#the_kernel",
            "https://www.kernel.org/doc/html/latest/core-api/genericirq.html",
        ],
    ),
    "mitigations": (
        """kernel-level workarounds created to increase CPU Security, due to vulnerabilities. Those vulnerabilities, found by Spectre and Meltdown, let a malicious program read memory it should have access to (like passwords or encryption keys from other programs), by exploiting the speed and instructions of modern CPUs. As a result, the kernel inserts extra checks and disables some CPU optimization, causing performance loss. There is a way to turn this off, but be careful!""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#disabling_spectre_and_meltdown_mitigations",
            "https://meltdownattack.com/",
            "https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/index.html",
        ],
    ),
    "maxCstate": (
        """a kernel boot parameter that allows you to cap how deeply the CPU is allowed to sleep when it is idle. Modern CPUs save power by going into progressively deeper sleep states (called C-states) when they have nothing to do. For example, C0 is fully active, C1 is in light sleep that wakes up almost instantly, but something like C7, or C8, they power down large portions of the CPU to save more energy.

Deeper states take longer to wake up, sometimes even hundreds of microseconds. When an audio event fires while the CPU is in a deep C-state, the CPU has to "warm-up" before it can respond, which may cause xruns.

An example of implementation would be, processor.max_cstate=N, where N specifies the kernel to only use C-states from C0 to CN. Also, the max C-states is determined by the type of CPU too. Cool fun fact, that when a CPU is constrained from being put into an available idle state, the CPU will execute more or less useless instructions in a loop until it is assigned a new task to run lol. Overall, by setting a max to the C-state the cores can be at, eliminates the latency spikes at the cost of higher power and heat.""",
        [
            "https://wiki.linuxaudio.org/wiki/system_configuration#quality_of_service_interface",
            "https://docs.kernel.org/admin-guide/pm/cpuidle.html",
        ],
    ),
}
