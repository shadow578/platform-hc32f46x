# How to upload to HC32F460

The HC32F460 platform supports uploading using a debug probe and [pyOCD](https://github.com/pyocd/pyOCD).

## Prerequisites

to debug the HC32F460, you will need the following:
- a HC32F460 based board
- a SWD debug probe (see [supported debug probes](./SUPPORTED_DEBUG_PROBES.md))
- a PlatformIO compatible IDE (e.g. VSCode)

## Preparing your Project

to prepare your project for uploading, you will need to add the `upload_tool` option to your environment:

```ini
[env:my_env]
# ...
upload_tool = cmsis-dap # or jlink
```
