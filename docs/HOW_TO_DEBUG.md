# How to use the PlatformIO Debugger

using the PlatformIO debugger is a great way to debug your code. It allows you to set breakpoints, step through your code, and inspect variables. This document will show you how to setup your Project for use with the PlatformIO debugger and the HC32F460.

> [!WARNING]
> please note that debugging support is a fairly experimental feature for the HC32F460 platform. 
> while most things should work okay, there may be some issues.


## Limitations

please note that the HC32F460 platform is currently somewhat limited in terms of debugging support.

things that work / don't work:

| Status          | Feature                        | Notes                                                                  |
| --------------- | ------------------------------ | ---------------------------------------------------------------------- |
| :yellow_circle: | Breakpoints                    | can only use software breakpoints, so max. 6 breakpoints are available |
| :green_circle:  | Step Over / Into / Out         |
| :green_circle:  | Variable inspection            | variable inspection tends to be kind of slow                           |
| :yellow_circle: | Watchpoints                    | only 4 watchpoints are available                                       |
| :green_circle:  | Call stack inspection          |                                                                        |
| :yellow_circle: | Peripheral register inspection | some registers of the Cortex-M4 core seem to be missing                |
| :green_circle:  | CPU register inspection        |
| :green_circle:  | Memory inspection              |
| :green_circle:  | Disassembly view               | if you're into that kind of thing                                      |

> :green_circle: = works
> :yellow_circle: = works, but with limitations (see notes)
> :red_circle: = not working


## Prerequisites

to debug the HC32F460, you will need the following:
- a HC32F460 based board
- a SWD debug probe (see [supported debug probes](./SUPPORTED_DEBUG_PROBES.md))
- a PlatformIO compatible IDE (e.g. VSCode)


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


## Debugging your Code

to debug your code, please refer to the [official PlatformIO documentation](https://docs.platformio.org/en/latest/plus/debugging.html) on how to use the debugger.

