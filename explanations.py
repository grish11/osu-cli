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
        """the ratio of the processing time until completion of the graph and the quantum size (again for driver node). This ratio is a good indicator of the load of the driver node.""",
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
}
