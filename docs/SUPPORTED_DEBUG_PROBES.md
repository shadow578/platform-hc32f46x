# Supported Debug Probes

The HC32F460 Platform currently supports the following debug probes:

- [Raspberry Pi Debug Probe (CMSIS-DAP v2)](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html)
- (generic) CMSIS-DAP (untested)
- J-Link (untested)

it may be possible to add support for other debug probes as long as they are supported by [pyOCD](https://github.com/pyocd/pyOCD).

> [!TIP]
> when using the [Raspberry Pi Debug Probe (CMSIS-DAP v2)](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html),
> use `cmsis-dap`


> [!TIP]
> A Raspberry Pi Pico (or clone) with [raspberrypi/debugprobe](https://github.com/raspberrypi/debugprobe) can be used 
> as a inexpensive (< $5) SWD Probe.
