# How to use the PlatformIO Debugger

using the PlatformIO debugger is a great way to debug your code. It allows you to set breakpoints, step through your code, and inspect variables. This document will show you how to setup your Project for use with the PlatformIO debugger and the HC32F460.

> [!WARNING]
> please note that debugging support is a fairly experimental feature for the HC32F460 platform. 
> while most things should work okay, there may be some issues.


## Limitations

please note that the HC32F460 platform is currently somewhat limited in terms of debugging support.
while you're able to use most of the features of the debugger, you cannot modify the contents of flash memory.
since PlatformIO normally attempts to upload the firmware to the target device before debugging, this means that you will have to disable the upload process in order to use the debugger effectively.

things that work / don't work:

| Status          | Feature                        | Notes                                                                  |
| --------------- | ------------------------------ | ---------------------------------------------------------------------- |
| :yellow_circle: | Breakpoints                    | can only use software breakpoints, so max. 6 breakpoints are available |
| :green_circle:  | Step Over / Into / Out         |
| :green_circle:  | Variable inspection            | variable inspection tends to be kind of slow                           |
| :yellow_circle: | Watchpoints                    | only 4 watchpoints are available                                       |
| :green_circle:  | Call stack inspection          |                                                                        |
| :yellow_circle: | Peripheral register inspection | some registers of the Cortex-M4 core are unavailable                   |
| :green_circle:  | CPU register inspection        |
| :green_circle:  | Memory inspection              |
| :green_circle:  | Disassembly view               | if you're into that kind of thing                                      |
| :red_circle:    | Flash memory modification      | missing flash driver                                                   |

> :green_circle: = works
> :yellow_circle: = works, but with limitations (see notes)
> :red_circle: = not working


## Prerequisites

to debug the HC32F460, you will need the following:
- a HC32F460 based board
- a SWD debug probe (see below)
- a PlatformIO compatible IDE (e.g. VSCode)


### Supported Debug Probes

the HC32F460 platform supports the following debug probes:
- [Raspberry Pi Debug Probe (CMSIS-DAP v2)](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html)
- (generic) CMSIS-DAP (untested)
- J-Link (untested)

it may be possible to add support for other debug probes as long as they are supported by OpenOCD.


## Preparing your Project

to prepare your project for debugging, you will need to make a few changes to your `platformio.ini` file.

### 1. Enable Debugging

either set the `build_type` to `debug` __or__ add `-g3` to the `board_build.flags.common` option:

```ini
[env:my_env]
# ...
build_type = debug
# ... OR ...
board_build.flags.common = -g3
```

### 2. Select the Debug Probe

add the `debug_tool` option to your environment and set it to the debug probe you're using:

```ini
[env:my_env]
# ...
debug_tool = cmsis-dap # or jlink
```

> [!TIP]
> use `cmsis-dap` for the Raspberry Pi Debug Probe


### 3. Disable Firmware Upload

since HC32F460 does not support firmware upload via the debugger, you will need to disable the `debug_load` functionality of PlatformIO:

```ini
[env:my_env]
# ...
# disable firmware upload before debugging
# see https://community.platformio.org/t/attach-debugger-to-running-program-without-reset/18285/2
debug_load_cmds = 
debug_load_mode = manual
```


## Debugging your Code

to debug your code, please refer to the [official PlatformIO documentation](https://docs.platformio.org/en/latest/plus/debugging.html) on how to use the debugger.

please note the following:

1. you can only debug your code if it was not modified (or rebuild) since the last upload
  - if you see compilation output in the debug console, something went wrong and you may have to re-flash your firmware
2. you must start the debugger manually after uploading your firmware
  - PlatformIO should have configured launch configurations for you. Select "PIO Debug (without uploading)" from the debug configuration dropdown and start the debugger
3. the CPU may be reset when you start debugging


> [!TIP]
> if you notice breakpoints not working, the firmware running on the target may not match your local build.
> try re-flashing the firmware and starting the debugger again.

